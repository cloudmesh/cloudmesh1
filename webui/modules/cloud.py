from flask import Blueprint
from flask import render_template, request, redirect, g
from cloudmesh.config.cm_config import cm_config
from cloudmesh.cm_mesh import cloudmesh
from cloudmesh.util.util import table_printer
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.user.cm_user import cm_user
from datetime import datetime
import time
from cloudmesh.util.util import cond_decorator
import cloudmesh
from flask.ext.login import login_required
import webbrowser

from cloudmesh.util.logger import LOGGER
from pprint import pprint

log = LOGGER(__file__)


cloud_module = Blueprint('cloud_module', __name__)

config = cm_config()
#prefix = config.prefix
#index = config.index

clouds = cm_mongo()
clouds.activate()

# DEFINING A STATE FOR THE CHECKMARKS IN THE TABLE

"""
for name in clouds.active():

        config.data['cloudmesh']['clouds']

for name in clouds.active():
    try:
        a = config.data['cloudmesh']['clouds'][name]['default']['filter']['state']
        print "- filter exist for cloud", name
    except:
        config.create_filter(name, clouds.states(name))
        config.write()
"""

def getCurrentUserinfo():
    userinfo = cm_user().info(g.user.id)
    return userinfo

# ============================================================
# ROUTE: REFRESH
# ============================================================


@cloud_module.route('/cm/refresh/')
@cloud_module.route('/cm/refresh/<cloud>/')
@cloud_module.route('/cm/refresh/<cloud>/<service_type>')
@login_required
def refresh(cloud=None, server=None, service_type=None):
    print "-> refresh", cloud, service_type
    userinfo = getCurrentUserinfo()
    # print "REQ", redirect(request.args.get('next') or '/').__dict__
    cloud_names = None
    # cloud field could be empty thus in that position it could be the types
    if cloud is None or cloud in ['servers', 'flavors', 'images', 'users']:
        #cloud_names = config.active()
        cloud_names = userinfo["defaults"]["activeclouds"]
    else:
        cloud_names = [cloud]

    if service_type is None:
        clouds.refresh(names=cloud_names, types=['servers', 'images', 'flavors'])
    else:
        clouds.refresh(names=cloud_names, types=[service_type])
        return redirect('/mesh/{0}'.format(service_type))
    # clouds.refresh()
    # clouds.all_filter()
    return redirect('/mesh/servers')



# ============================================================
# ROUTE: DELETE
# ============================================================


@cloud_module.route('/cm/delete/<cloud>/<server>/')
@login_required
def delete_vm(cloud=None, server=None):
    log.info ("-> delete {0} {1}".format(cloud, server))
    # if (cloud == 'india'):
    #  r = cm("--set", "quiet", "delete:1", _tty_in=True)
    clouds.vm_delete(cloud, server)
    time.sleep(5)
    clouds.release_unused_public_ips(cloud)
    clouds.refresh(names=[cloud], types=["servers"])
    return redirect('/mesh/servers')

# ============================================================
# ROUTE: DELETE GROUP
# ============================================================


@cloud_module.route('/cm/delete/<cloud>/')
@login_required
def delete_vms(cloud=None):
# donot do refresh before delete, this will cause all the vms to get deleted
    f_cloud = clouds.clouds[cloud]
    for id, server in f_cloud['servers'].iteritems():
        log.info("-> delete {0} {1}".format(cloud, id))
        clouds.delete(cloud, id)
    time.sleep(7)
    f_cloud['servers'] = {}
    return redirect('/mesh/servers')


# ============================================================
# ROUTE: ASSIGN PUBLIC IP
# ============================================================


@cloud_module.route('/cm/assignpubip/<cloud>/<server>/')
@login_required
def assign_public_ip(cloud=None, server=None):
    mycloud = config.cloud(cloud)
    if not mycloud.has_key('cm_automatic_ip') or mycloud['cm_automatic_ip'] is False:
        clouds.assign_public_ip(cloud, server)
        clouds.refresh(names=[cloud], types=["servers"])
        return redirect('/mesh/servers')
    # else:
    #    return "Manual public ip assignment is not allowed for {0} cloud".format(cloud)

# ============================================================
# ROUTE: START
# ============================================================

#
# WHY NOT USE cm_keys as suggested?
#


@cloud_module.route('/cm/start/<cloud>/')
@login_required
def start_vm(cloud=None, server=None):
    log.info("-> start {0}".format(cloud))
    # if (cloud == 'india'):
    #  r = cm("--set", "quiet", "start:1", _tty_in=True)
    key = None
    vm_image = None
    vm_flavor = None
    vm_flavor_id = None
    
    if 'keys' in config['cloudmesh']:
        key = config.get('cloudmesh.keys.default')
    userinfo = getCurrentUserinfo()
    
    #print userinfo
    if "key" in userinfo["defaults"]:
        key = userinfo["defaults"]["key"]
    elif len(userinfo["keys"]["keylist"].keys()) > 0:
        key = userinfo["keys"]["keylist"].keys()[0]
    #
    # before the info could be maintained in mongo, using the config file
    #vm_flavor = config.cloud(cloud)["default"]["flavor"]
    #vm_image = config.cloud(cloud)["default"]["image"]
    #vm_flavor_id = clouds.flavor_name_to_id(cloud, vm_flavor)
    
    # getting defulat flavor and image for the specified cloud out of mongo
    if "flavors" in userinfo["defaults"]:
        if cloud in userinfo["defaults"]["flavors"]:
            vm_flavor_id = userinfo["defaults"]["flavors"][cloud]
            flavors = clouds.flavors([cloud])[cloud]
            vm_flavor = flavors[vm_flavor_id]["name"]
    if "images" in userinfo["defaults"]:
        if cloud in userinfo["defaults"]["images"]:
            vm_image = userinfo["defaults"]["images"][cloud]
    if not vm_flavor_id:
        flavors = clouds.flavors([cloud])[cloud]
        #pprint(flavors)
        vm_flavor_id = flavors.keys()[0]
        vm_flavor = flavors[vm_flavor_id]["name"]
    if not vm_image:
        images = clouds.images([cloud])[cloud]
        #pprint(images)
        vm_image = images.keys()[0]

    # in case of error, setting default flavor id
    #if vm_flavor_id < 0:
    #    vm_flavor_id = 1
    prefix = userinfo["defaults"]["prefix"]
    index = userinfo["defaults"]["index"]
    log.info("STARTING {0} {1}".format(prefix, index))
    log.info("FLAVOR {0} {1}".format(vm_flavor, vm_flavor_id))
    metadata = {'cm_owner': prefix}
    # username = config.get('cloudmesh.hpc.username')
    username = userinfo["cm_user_id"]
    try:
        keynamenew = "%s_%s" % (username, key.replace('.', '_').replace('@', '_'))
    except AttributeError:
        keynamenew = "cloudmesh"  # Default key name if it is missing
    result = clouds.vm_create(
        cloud,
        prefix,
        index,
        vm_flavor_id,
        vm_image,
        keynamenew,
        meta=metadata)
    log.info ("{0}".format(result))
    # clouds.vm_set_meta(cloud, result['id'], {'cm_owner': config.prefix})
    # config.incr()
    userstore = cm_user()
    userstore.set_default_attribute(username, "index", int(index)+1)
    # config.write()

    #
    # BUG NOT SURE IF WE NEED THE SLEEP
    #

    time.sleep(5)

    clouds.refresh(names=[cloud], types=["servers"])
    return redirect('/mesh/servers')

# ============================================================
# ROUTE: VM Login
# ============================================================


@cloud_module.route('/cm/login/<cloud>/<server>/')
@login_required
def vm_login(cloud=None, server=None):
    message = ''
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    server = clouds.servers()[cloud][server]

    #
    # BUG MESSAGE IS NOT PROPAGATED
    #

    if len(server['addresses'][server['addresses'].keys()[0]]) < 2:
        message = 'Cannot Login Now, Public IP not assigned'
        log.info ("{0}".format(message))

    else:
        message = 'Logged in Successfully'
        ip = server['addresses'][server['addresses'].keys()[0]][1]['addr']
        #
        # BUG: login must be based on os
        # TODO: loginbug
        #
        link = 'ubuntu@' + ip
        webbrowser.open("ssh://" + link)

    return redirect('/mesh/servers')
# ============================================================
# ROUTE: VM INFO
# ============================================================

@cloud_module.route('/cm/info/<cloud>/<server>/')
@login_required
def vm_info(cloud=None, server=None):

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # print clouds.servers()[cloud]

    # a trick to deal with diffe1rent type of server_id
    # (string in FG; or int in e.g. hp_cloud)
    try:
        if "%s" % int(server) == server:
            server = int(server)
    except:
        pass
    clouds.servers()[cloud][server]['cm_vm_id'] = server
    clouds.servers()[cloud][server]['cm_cloudname'] = cloud

    return render_template('mesh/cloud/vm_info.html',
                           updated=time_now,
                           keys="",
                           server=clouds.servers()[cloud][server],
                           id=server,
                           cloudname=cloud,
                           table_printer=table_printer)


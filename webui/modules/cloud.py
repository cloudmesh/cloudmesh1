from flask import Blueprint
from flask import render_template, request, redirect
from cloudmesh.config.cm_config import cm_config
from cloudmesh.cm_mesh import cloudmesh
from cloudmesh.util.util import table_printer
from cloudmesh.cm_mongo import cm_mongo
from datetime import datetime
import time
from cloudmesh.util.util import cond_decorator
import cloudmesh
from flask.ext.login import login_required

from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

try:
    from sh import xterm
except:
    print "xterm not suppported"

    # TODO: THERE SHOULD BE A VARIABLE SET HERE SO THAT THE ARROW
    # START UP BUTTON CAN RETURN MEANINGFULL MESSAGE IF NOT SUPPORTED


cloud_module = Blueprint('cloud_module', __name__)

config = cm_config()
prefix = config.prefix
index = config.index

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

# ============================================================
# ROUTE: SAVE
# ============================================================


@cloud_module.route('/save/')
@cond_decorator(cloudmesh.with_login, login_required)
def save():
    print "Saving the cloud status"
    # clouds.save()
    return redirect('/mesh/servers')

# ============================================================
# ROUTE: LOAD
# ============================================================


@cloud_module.route('/load/')
@cond_decorator(cloudmesh.with_login, login_required)
def load():
    print "Loading the cloud status"
    # clouds.load()
    return redirect('/mesh/servers')

# ============================================================
# ROUTE: REFRESH
# ============================================================


@cloud_module.route('/cm/refresh/')
@cloud_module.route('/cm/refresh/<cloud>/')
@cloud_module.route('/cm/refresh/<cloud>/<service_type>')
@cond_decorator(cloudmesh.with_login, login_required)
def refresh(cloud=None, server=None, service_type=None):
    print "-> refresh", cloud, server

    print "REQ", redirect(request.args.get('next') or '/').__dict__

    if cloud in ['servers', 'flavors', 'images', 'users']:
        service_type = cloud
        cloud_names = config.active()
    else:
        cloud_names = [cloud]

    if cloud is None:
        clouds.refresh(types=['servers', 'images', 'flavors'])
    elif service_type is None:
        clouds.refresh(names=cloud_names, types=['servers', 'images', 'flavors'])
    else:
        clouds.refresh(names=cloud_names, types=[service_type])
        return redirect('/mesh/{0}'.format(service_type))
    # clouds.refresh()
    # clouds.all_filter()
    return redirect('/mesh/servers')

# ============================================================
# ROUTE: Filter
# ============================================================


@cloud_module.route('/cm/filter/<cloud>/', methods=['GET', 'POST'])
@cond_decorator(cloudmesh.with_login, login_required)
def filter(cloud=None):
    # print "-> filter", cloud

    #
    # BUG: when cloud is none
    #
    name = cloud
    if request.method == 'POST':
        query_states = []
        state_table = {}
        for state in clouds.states(name):
            state_name = "%s:%s" % (name, state)
            state_table[state] = state_name in request.form
            if state_table[state]:
                query_states.append(state)
        config.set_filter(name, state_table, 'state')

        clouds.state_filter(name, query_states)

    return redirect('/mesh/servers')


# ============================================================
# ROUTE: KILL
# ============================================================
@cloud_module.route('/cm/kill/')
@cond_decorator(cloudmesh.with_login, login_required)
def kill_vms():
    print "-> kill all"
    r = cm("--set", "quiet", "kill", _tty_in=True)
    return redirect('/mesh/servers')

# ============================================================
# ROUTE: DELETE
# ============================================================


@cloud_module.route('/cm/delete/<cloud>/<server>/')
@cond_decorator(cloudmesh.with_login, login_required)
def delete_vm(cloud=None, server=None):
    print "-> delete", cloud, server
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
@cond_decorator(cloudmesh.with_login, login_required)
def delete_vms(cloud=None):
# donot do refresh before delete, this will cause all the vms to get deleted
    f_cloud = clouds.clouds[cloud]
    for id, server in f_cloud['servers'].iteritems():
        print "-> delete", cloud, id
        clouds.delete(cloud, id)
    time.sleep(7)
    f_cloud['servers'] = {}
    return redirect('/mesh/servers')


# ============================================================
# ROUTE: ASSIGN PUBLIC IP
# ============================================================


@cloud_module.route('/cm/assignpubip/<cloud>/<server>/')
@cond_decorator(cloudmesh.with_login, login_required)
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
@cond_decorator(cloudmesh.with_login, login_required)
def start_vm(cloud=None, server=None):
    print "*********** STARTVM", cloud
    print "-> start", cloud
    # if (cloud == 'india'):
    #  r = cm("--set", "quiet", "start:1", _tty_in=True)
    key = None

    if 'keys' in config['cloudmesh']:
        key = config.get('cloudmesh.keys.default')

    # THIS IS A BUG
    # vm_flavor = clouds.default(cloud)['flavor']
    # vm_image = clouds.default(cloud)['image']
    #
    # before the info could be maintained in mongo, using the config file
    vm_flavor = config.cloud(cloud)["default"]["flavor"]
    vm_image = config.cloud(cloud)["default"]["image"]
    vm_flavor_id = clouds.flavor_name_to_id(cloud, vm_flavor)
    # in case of error, setting default flavor id
    if vm_flavor_id < 0:
        vm_flavor_id = 1
    print "STARTING", config.prefix, config.index
    print "FLAVOR", vm_flavor, vm_flavor_id
    metadata = {'cm_owner': config.prefix}
    username = config.get('cloudmesh.hpc.username')
    keynamenew = "%s_%s" % (username, key.replace('.','_').replace('@', '_'))
    result = clouds.vm_create(
        cloud, 
        config.prefix, 
        config.index, 
        vm_flavor_id, 
        vm_image, 
        keynamenew, 
        meta=metadata)
    print "P"*20
    print result
    # print "PPPPPPPPPPPP", result
    # clouds.vm_set_meta(cloud, result['id'], {'cm_owner': config.prefix})
    config.incr()
    config.write()
    time.sleep(5)
    clouds.refresh(names=[cloud], types=["servers"])
    return redirect('/mesh/servers')

# ============================================================
# ROUTE: VM Login
# ============================================================


@cloud_module.route('/cm/login/<cloud>/<server>/')
@cond_decorator(cloudmesh.with_login, login_required)
def vm_login(cloud=None, server=None):
    message = ''
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    server = clouds.servers()[cloud][server]

    if len(server['addresses'][server['addresses'].keys()[0]]) < 2:
        mesage = 'Cannot Login Now, Public IP not assigned'
        print message

    else:
        message = 'Logged in Successfully'
        ip = server['addresses'][server['addresses'].keys()[0]][1]['addr']
        # THIS IS A BUG AND MUST BE SET PER VM, E.G. sometimesvm type probably
        # decides that?
        print "ssh", 'ubuntu@' + ip
        xterm('-e', 'ssh', 'ubuntu@' + ip, _bg=True)

    return redirect('/mesh/servers')
# ============================================================
# ROUTE: VM INFO
# ============================================================


@cloud_module.route('/cm/info/<cloud>/<server>/')
@cond_decorator(cloudmesh.with_login, login_required)
def vm_info(cloud=None, server=None):

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    #print clouds.servers()[cloud]
    
    # a trick to deal with different type of server_id
    # (string in FG; or int in e.g. hp_cloud)
    try:
        if "%s" % int(server) == server:
            server = int(server)
    except:
        pass    
    clouds.servers()[cloud][server]['cm_vm_id'] = server
    clouds.servers()[cloud][server]['cm_cloudname'] = cloud
    
    return render_template('vm_info.html',
                           updated=time_now,
                           keys="",
                           server=clouds.servers()[cloud][server],
                           id=server,
                           cloudname=cloud,
                           table_printer=table_printer)

# ============================================================
# ROUTE: FLAVOR
# ============================================================

# @cloud_module.route('/flavors/<cloud>/' )


@cloud_module.route('/flavors/', methods=['GET', 'POST'])
@cond_decorator(cloudmesh.with_login, login_required)
def display_flavors(cloud=None):

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if request.method == 'POST':
        for cloud in config.active():
            config['cloudmesh']['clouds'][cloud]['default'][
                'flavor'] = request.form[cloud]
            config.write()

    return render_template(
        'flavor.html',
        updated=time_now,
        cloudmesh=clouds,
        clouds=clouds.clouds,
        config=config)


# ============================================================
# ROUTE: IMAGES
# ============================================================
# @cloud_module.route('/images/<cloud>/')
@cond_decorator(cloudmesh.with_login, login_required)
@cloud_module.route('/images/', methods=['GET', 'POST'])
def display_images():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if request.method == 'POST':
        for cloud in config.active():
            config['cloudmesh']['clouds'][cloud][
                'default']['image'] = request.form[cloud]
            config.write()

    return render_template(
        'images.html',
        updated=time_now,
        clouds=clouds.clouds,
        cloudmesh=clouds,
        config=config)

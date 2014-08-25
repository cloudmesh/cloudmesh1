from flask import Blueprint
from flask import render_template, request, redirect, g, jsonify, session
from cloudmesh.config.cm_config import cm_config
#  from cloudmesh.cm_mesh import cloudmesh
from cloudmesh_common.tables import table_printer
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.user.cm_user import cm_user
from datetime import datetime
import time
from cloudmesh_common.util import cond_decorator
import cloudmesh
from flask.ext.login import login_required
import webbrowser
from cloudmesh_common.util import address_string
from cloudmesh_common.logger import LOGGER
from pprint import pprint
from compiler.ast import Return

log = LOGGER(__file__)


cloud_module = Blueprint('cloud_module', __name__)

# config = cm_config()
# prefix = config.prefix
# index = config.index

# clouds = cm_mongo()
# clouds.activate()

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

    clouds = cm_mongo()
    cm_user_id = g.user.id
    clouds.activate(cm_user_id=cm_user_id)

    log.info("-> refresh {0} {1}".format(cloud, service_type))
    userinfo = getCurrentUserinfo()
    # print "REQ", redirect(request.args.get('next') or '/').__dict__
    cloud_names = None
    # cloud field could be empty thus in that position it could be the types
    if cloud is None or cloud in ['servers', 'flavors', 'images', 'users']:
        # cloud_names = config.active()
        cloud_names = userinfo["defaults"]["activeclouds"]
    else:
        cloud_names = [cloud]

    if service_type is None:
        # if both cloud and service_type are none, it's coming from the
        # refresh button from home page. So return to home
        if cloud is None:
            return redirect('/')
        else:
            clouds.refresh(cm_user_id=cm_user_id,
                           names=cloud_names,
                           types=['servers', 'images', 'flavors'])
            return redirect('/mesh/{0}'.format(cloud))
    else:
        clouds.refresh(cm_user_id=cm_user_id,
                       names=cloud_names,
                       types=[service_type])
        return redirect('/mesh/{0}'.format(service_type))

# ============================================================
# ROUTE: REFRESH by Celery task queue
# ============================================================

@cloud_module.route('/cm/refresh/q/')
@cloud_module.route('/cm/refresh/q/<cloud>/')
@cloud_module.route('/cm/refresh/q/<cloud>/<service_type>')
@login_required
def refresh_by_queue(cloud=None, service_type=None):
    """ Similar to refresh but using Celery task queue"""

    log.info("-> refresh by queue {0} {1}".format(cloud, service_type))
    cloud_names = None
    cm_user_id = g.user.id
    clouds = cm_mongo()

    if cloud is None or cloud in ['servers', 'flavors', 'images', 'users']:
        userinfo = getCurrentUserinfo()
        cloud_names = userinfo["defaults"]["activeclouds"]
    else:
        cloud_names = [cloud]

    for cloud_entry in  cloud_names:
        cm_type = clouds.get_cloud_info(cm_user_id, cloud_entry)['cm_type']
        # Celery task queue
        package = "cloudmesh.iaas.%s.queue" % cm_type
        name = "tasks"
        imported = getattr(__import__(package, fromlist=[name]), name)
        queue_name = "%s-%s" % (cm_type, service_type)
        imported.refresh.apply_async((cm_user_id, cloud_names,
                                  [service_type]), queue=queue_name)
 
    if service_type is None and cloud is None:
        return redirect('/')
    else:
        return redirect('/mesh/{0}'.format(service_type))

# ============================================================
# ROUTE: DELETE
# ============================================================


@cloud_module.route('/cm/delete/<cloud>/<server>/')
@login_required
def delete_vm(cloud=None, server=None):
    log.info ("-> delete {0} {1}".format(cloud, server))

    clouds = cm_mongo()
    clouds.activate(cm_user_id=g.user.id)

    # if (cloud == 'india'):
    #  r = cm("--set", "quiet", "delete:1", _tty_in=True)
    clouds.vm_delete(cloud, server, g.user.id)
    time.sleep(5)
    clouds.release_unused_public_ips(cloud, g.user.id)
    clouds.refresh(names=[cloud], types=["servers"], cm_user_id=g.user.id)
    return redirect('/mesh/servers')

# ============================================================
# ROUTE: DELETE Multiple VM CONFIRMATION AND DELETION
# ============================================================
@cloud_module.route('/cm/delete_vm_confirm', methods=('GET', 'POST'))
@login_required
def delete_vm_confirm():




    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # filter()
    config = cm_config()
    c = cm_mongo()
    c.activate(cm_user_id=g.user.id)


    userdata = g.user
    username = userdata.id
    user_obj = cm_user()
    user = user_obj.info(username)

    clouds = c.servers(cm_user_id=username)
    images = c.images(cm_user_id=username)
    flavors = c.flavors(cm_user_id=username)

    os_attributes = ['name',
                     'status',
                     'addresses',
                     'flavor',
                     'id',
                     'image',
                     'user_id',
                     'metadata',
                     'key_name',
                     'created']
    cloud_filters = None
    filtered_clouds = clouds
    cloud = request.form["cloud"]   
    select = request.form.getlist("selection_"+cloud);
    if select != None and cloud != None:
        session["delete_selection"] = (cloud, select)
    if "delete_selection" in session:
        print "writing selection to session"
        # print filtered_clouds
        selected_cloud_data = {}
        selected_cloud_data[cloud] = get_selected_clouds(filtered_clouds[session["delete_selection"][0]], session["delete_selection"][1])
        return render_template('mesh/cloud/delete_vms.html',
                               address_string=address_string,
                               attributes=os_attributes,
                               updated=time_now,
                               clouds=selected_cloud_data,
                               config=config,
                               user=user,
                               images=images,
                               flavors=flavors,
                               filters=cloud_filters)

    else:
        return render_template('error.html',
                               type="Deleting VMs",
                               error="No VMs to delete. ")


@cloud_module.route('/cm/delete_request_submit/<option>', methods=('GET', 'POST'))
@login_required
def delete_vm_submit(option):
    config = cm_config()
    c = cm_mongo()
    c.activate(cm_user_id=g.user.id)

    select = session.pop("delete_selection", None)

    clouds = c.servers(g.user.id)

    if option == "true":
        cloud = select[0]
        servers = select[1]  # [cloud]
        for server in servers:
            delete_vm(cloud=cloud, server=server)

        return render_template('success.html',
                               type="Deleting VMs",
                               error="Deleting the VMs completed. {0}".format(servers))
    else:
        return render_template('error.html',
                               type="Deleting VMs",
                               error="Deleting the VMs aborted. ")



def get_selected_clouds(cloud, select_ids):
    selected_clouds = {}
    for id in select_ids:
        if id in cloud:
            selected_clouds[id] = cloud[id]
    # print selected_clouds
    return selected_clouds

# ============================================================
# ROUTE: DELETE GROUP
# ============================================================


@cloud_module.route('/cm/delete/<cloud>/')
@login_required
def delete_vms(cloud=None):


    clouds = cm_mongo()
    clouds.activate(cm_user_id=g.user.id)

    # donot do refresh before delete, this will cause all the vms to get deleted
    f_cloud = clouds.clouds[g.user.id][cloud]
    for id, server in f_cloud['servers'].iteritems():
        log.info("-> delete {0} {1}".format(cloud, id))
        clouds.vm_delete(cloud, id, g.user.id)
    time.sleep(7)
    f_cloud['servers'] = {}
    return redirect('/mesh/servers')


# ============================================================
# ROUTE: ASSIGN PUBLIC IP
# ============================================================


@cloud_module.route('/cm/assignpubip/<cloud>/<server>/')
@login_required
def assign_public_ip(cloud=None, server=None):

    config = cm_config()
    clouds = cm_mongo()
    clouds.activate(cm_user_id=g.user.id)

    mycloud = config.cloud(cloud)
    if not mycloud.has_key('cm_automatic_ip') or mycloud['cm_automatic_ip'] is False:
        clouds.assign_public_ip(cloud, server, g.user.id)
        clouds.refresh(names=[cloud], types=["servers"], cm_user_id=g.user.id)
        return redirect('/mesh/servers')
    # else:
    #    return "Manual public ip assignment is not allowed for {0} cloud".format(cloud)

def _keyname_sanitation(username, keyname):
    keynamenew = "%s_%s" % (username, keyname.replace('.', '_').replace('@', '_'))
    return keynamenew

@cloud_module.route('/cm/keypairs/<cloud>/', methods=['GET', 'POST'])
@login_required
def manage_keypairs(cloud=None):

    clouds = cm_mongo()
    clouds.activate(cm_user_id=g.user.id)

    userinfo = getCurrentUserinfo()
    username = userinfo["cm_user_id"]
    keys = userinfo["keys"]["keylist"]

    # currently we do the registration only for openstack
    # not yet sure if other clouds support this
    # or if we have implemented them if they also support
    if cloud in clouds.clouds[g.user.id] and clouds.clouds[g.user.id][cloud]['cm_type'] in ['openstack', 'ec2', 'aws']:
        cloudmanager = clouds.clouds[g.user.id][cloud]['manager']
        if request.method == 'POST':
            action = request.form['action']
            keyname = request.form["keyname"]
            # remove beginning 'key ' part
            keycontent = keys[keyname]
            if keycontent.startswith('key '):
                keycontent = keycontent[4:]
            # print keycontent
            keynamenew = _keyname_sanitation(username, keyname)
            if action == 'register':
                log.debug("trying to register a key")
                r = cloudmanager.keypair_add(keynamenew, keycontent)
                # pprint(r)
            else:
                log.debug("trying to deregister a key")
                r = cloudmanager.keypair_remove(keynamenew)
            return jsonify(**r)
        else:
            registered = {}
            keysRegistered = cloudmanager.keypair_list()
            keynamesRegistered = []
            if "keypairs" in keysRegistered:
                keypairsRegistered = keysRegistered["keypairs"]
                for akeypair in keypairsRegistered:
                    keyname = akeypair['keypair']['name']
                    keynamesRegistered.append(keyname)
            # pprint(keynamesRegistered)
            for keyname in keys.keys():
                keynamenew = _keyname_sanitation(username, keyname)
                # print keynamenew
                if keynamenew in keynamesRegistered:
                    registered[keyname] = True
                else:
                    registered[keyname] = False
            return render_template('mesh/cloud/keypairs.html',
                                   keys=keys,
                                   registered=registered,
                                   cloudname=cloud)
    else:
        return render_template('error.html',
                               error="Setting keypairs for this cloud is not yet enabled")
        # return redirect('/mesh/servers')

def check_register_key(cloud, keyname, keycontent):
    clouds = cm_mongo()
    clouds.activate(cm_user_id=g.user.id, names=[cloud])
    cloudmanager = clouds.clouds[g.user.id][cloud]['manager']
    
    keynamenew = _keyname_sanitation(g.user.id, keyname)
    keysRegistered = cloudmanager.keypair_list()
    registered = False
    # Openstack & Eucalyptus
    if 'keypairs' in keysRegistered:
        keypairsRegistered = keysRegistered["keypairs"]
        for akeypair in keypairsRegistered:
            if keynamenew == akeypair['keypair']['name']:
                registered = True
                break
    else:
        if keynamenew in keysRegistered:
            registered = True
    
    if not registered:
        cloudmanager.keypair_add(keynamenew, keycontent)
        log.info("Automatically registered the default key <%s> for user <%s>" % (keyname, g.user.id))

# ============================================================
# ROUTE: START
# ============================================================

# @cloud_module.route('/cm/start/<cloud>/<count>')

@cloud_module.route('/cm/start/<cloud>/')
@login_required
def start_vm(cloud=None, server=None):
    log.info("-> start {0}".format(cloud))

    config = cm_config()
    clouds = cm_mongo()
    clouds.activate(cm_user_id=g.user.id, names=[cloud])

    key = None
    vm_image = None
    vm_flavor = None
    vm_flavor_id = None

    userinfo = getCurrentUserinfo()

    # print userinfo

    error = ''

    try:
        vm_flavor_id = userinfo["defaults"]["flavors"][cloud]
    except:
        error = error + "Please specify a default flavor."

    if vm_flavor_id in [None, 'none']:
        error = error + "Please specify a default flavor."

    try:
        vm_image = userinfo["defaults"]["images"][cloud]
    except:
        error = error + "Please specify a default image."

    if vm_image in [None, 'none']:
        error = error + "Please specify a default image."

    username = userinfo["cm_user_id"]
    
    if "key" in userinfo["defaults"]:
        key = userinfo["defaults"]["key"]
    elif len(userinfo["keys"]["keylist"].keys()) > 0:
        key = userinfo["keys"]["keylist"].keys()[0]
        
    if key:
        keycontent = userinfo["keys"]["keylist"][key]
        if keycontent.startswith('key '):
            keycontent = keycontent[4:]
        check_register_key(cloud, key, keycontent)
        keynamenew = _keyname_sanitation(username, key)
    else:
        error = error + "No sshkey found. Please <a href='https://portal.futuregrid.org/my/ssh-keys'>Upload one</a>"
    
    if error != '':
        return render_template('error.html', error=error)

    metadata = {'cm_owner': username}
    prefix = userinfo["defaults"]["prefix"]
    index = userinfo["defaults"]["index"]
    
    log.info("STARTING {0} {1}".format(prefix, index))
    # log.info("FLAVOR {0} {1}".format(vm_flavor, vm_flavor_id))
    log.debug("Starting vm using image->%s, flavor->%s, key->%s" % (vm_image, vm_flavor_id, keynamenew))
    result = clouds.vm_create(
        cloud,
        prefix,
        index,
        vm_flavor_id,
        vm_image,
        keynamenew,
        meta=metadata,
        cm_user_id=g.user.id)
    try:
        tmp = dict(result)
        tmp['server']['adminPass'] = "*******"
    except:
        pass

    log.info ("{0}".format(result))
    # clouds.vm_set_meta(cloud, result['id'], {'cm_owner': config.prefix})
    # config.incr()
    userstore = cm_user()
    userstore.set_default_attribute(username, "index", int(index) + 1)
    # config.write()

    #
    # BUG NOT SURE IF WE NEED THE SLEEP
    #

    time.sleep(5)

    clouds.refresh(names=[cloud], types=["servers"], cm_user_id=g.user.id)
    return redirect('/mesh/servers')

@cloud_module.route('/cm/start/queue/<cloud>/')
@login_required
def start_vm_with_queue(cloud=None, server=None):
    ''' 
    
    same as start_vm function but runs with
    celery task queue
    
    *vm_create_queue* function launches vm instances through
    a celery queue

    '''
    log.info("-> start {0}".format(cloud))

    config = cm_config()
    clouds = cm_mongo()
    clouds.activate(cm_user_id=g.user.id)

    key = None
    vm_image = None
    vm_flavor_id = None

    userinfo = getCurrentUserinfo()

    # print userinfo

    error = ''

    try:
        vm_flavor_id = userinfo["defaults"]["flavors"][cloud]
    except:
        error = error + "Please specify a default flavor."

    if vm_flavor_id in [None, 'none']:
        error = error + "Please specify a default flavor."

    try:
        vm_image = userinfo["defaults"]["images"][cloud]
    except:
        error = error + "Please specify a default image."

    if vm_image in [None, 'none']:
        error = error + "Please specify a default image."

    username = userinfo["cm_user_id"]
    
    if "key" in userinfo["defaults"]:
        key = userinfo["defaults"]["key"]
    elif len(userinfo["keys"]["keylist"].keys()) > 0:
        key = userinfo["keys"]["keylist"].keys()[0]
        
    if key:
        keycontent = userinfo["keys"]["keylist"][key]
        if keycontent.startswith('key '):
            keycontent = keycontent[4:]
        check_register_key(cloud, key, keycontent)
        keynamenew = _keyname_sanitation(username, key)
    else:
        error = error + "No sshkey found. Please <a href='https://portal.futuregrid.org/my/ssh-keys'>Upload one</a>"
    
    if error != '':
        return render_template('error.html', error=error)

    metadata = {'cm_owner': username}
    prefix = userinfo["defaults"]["prefix"]
    index = userinfo["defaults"]["index"]
    
    log.info("STARTING {0} {1}".format(prefix, index))
    # log.info("FLAVOR {0}".format(vm_flavor_id))
    log.debug("Starting vm using image->%s, flavor->%s, key->%s" % (vm_image, vm_flavor_id, keynamenew))
    result = clouds.vm_create_queue(
        cloud,
        prefix,
        index,
        vm_flavor_id,
        vm_image,
        keynamenew,
        metadata,
        g.user.id)
    log.info ("{0}".format(result))
    # clouds.vm_set_meta(cloud, result['id'], {'cm_owner': config.prefix})
    # config.incr()
    userstore = cm_user()
    userstore.set_default_attribute(username, "index", int(index) + 1)
    # config.write()

    clouds.refresh(names=[cloud], types=["servers"], cm_user_id=g.user.id)
    return redirect('/mesh/servers')


# ============================================================
# ROUTE: VM Login
# ============================================================


@cloud_module.route('/cm/login/<cloud>/<server>/')
@login_required
def vm_login(cloud=None, server=None):

    clouds = cm_mongo()
    clouds.activate(cm_user_id=g.user.id)

    message = ''
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    server = clouds.servers(cm_user_id=g.user.id)[cloud][server]

    #
    # BUG MESSAGE IS NOT PROPAGATED
    #
    if cloud == "aws":
        userid = "ubuntu" # temporary
        public_dns = server['extra']['dns_name']
        message = "ssh -i [your private key file] %s@%s" % (userid, public_dns)
        return render_template('success.html', error=message)
    elif cloud == "azure":
        userid = "root"
        public_dns = server["vip"] #["addresses"]["private"][0]["addr"] # temporary
        message = "ssh -i [your private key file] %s@%s" % (userid, public_dns)
        return render_template('success.html', error=message)

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

        c = cm_mongo()
        images = c.images([cloud], g.user.id)[cloud]

        image = server['image']['id']

        imagename = images[image]['name']
        print imagename

        if "ubuntu" in imagename:
            loginname = "ubuntu"
        elif "centos" in imagename:
            loginname = "root"
        elif "debian" in imagename:
            loginname = "root"
        else:
            userdata = g.user
            loginname = userdata.id

        link = 'ubuntu@' + ip
        webbrowser.open("ssh://" + link)

    return redirect('/mesh/servers')
# ============================================================
# ROUTE: VM INFO
# ============================================================

@cloud_module.route('/cm/info/<cloud>/<server>/')
@login_required
def vm_info(cloud=None, server=None):

    print "TYTYTYT"
    clouds = cm_mongo()
    print "TYTYTYT"
    clouds.activate(cm_user_id=g.user.id)
    print "TYTYTYT"

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # print clouds.servers()[cloud]

    # a trick to deal with diffe1rent type of server_id
    # (string in FG; or int in e.g. hp_cloud)
    '''
    try:
        if "%s" % int(server) == server:
            server = int(server)
    except:
        pass
    '''

    # clouds.servers()[cloud][server]['cm_vm_id'] = server
    # clouds.servers()[cloud][server]['cm_cloudname'] = cloud

    return render_template('mesh/cloud/vm_info.html',
                           updated=time_now,
                           keys="",
                           server=clouds.servers(cm_user_id=g.user.id)[cloud][server],
                           id=server,
                           cloudname=cloud,
                           table_printer=table_printer)


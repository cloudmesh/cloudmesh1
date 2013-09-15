from flask import Blueprint
from flask import render_template, request, redirect
from cloudmesh.config.cm_config import cm_config
from cloudmesh.cm_mesh import cloudmesh
from cloudmesh.util.util import table_printer
from datetime import datetime
import time

try:
    from sh import xterm
except:
    print "xterm not suppported"

    # TODO: THERE SHOULD BE A VARIABLE SET HERE SO THAT THE ARROW
    # START UP BUTTON CAN RETURN MEANINGFULL MESSAGE IF NOT SUPPORTED


cloud_module = Blueprint('cloud_module', __name__)

config = cm_config()
configuration = config.get()
prefix = config.prefix
index = config.index

clouds = cloudmesh()
# refresh, misses the search for display

clouds.refresh()
clouds.refresh_user_id()

# clouds.load()
# clouds.refresh("openstack")
# clouds.clouds

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

print config

clouds.all_filter()

# ============================================================
# ROUTE: SAVE
# ============================================================


@cloud_module .route('/save/')
def save():
    print "Saving the cloud status"
    clouds.save()
    return table()

# ============================================================
# ROUTE: LOAD
# ============================================================


@cloud_module .route('/load/')
def load():
    print "Loading the cloud status"
    clouds.load()
    return table()

# ============================================================
# ROUTE: TABLE
# ============================================================


@cloud_module .route('/table/')
def table():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    filter()
    return render_template('table.html',
                           updated=time_now,
                           keys="",  # ",".join(clouds.get_keys()),
                           cloudmesh=clouds,
                           clouds=clouds.clouds,
                           config=config)

# ============================================================
# ROUTE: REFRESH
# ============================================================


@cloud_module .route('/cm/refresh/')
@cloud_module .route('/cm/refresh/<cloud>/')
def refresh(cloud=None, server=None):
    # print "-> refresh", cloud, server
    clouds.refresh()
    clouds.all_filter()
    return table()

# ============================================================
# ROUTE: Filter
# ============================================================


@cloud_module .route('/cm/filter/<cloud>/', methods=['GET', 'POST'])
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

    return redirect("/table/")


# ============================================================
# ROUTE: KILL
# ============================================================
@cloud_module .route('/cm/kill/')
def kill_vms():
    print "-> kill all"
    r = cm("--set", "quiet", "kill", _tty_in=True)
    return table()

# ============================================================
# ROUTE: DELETE
# ============================================================


@cloud_module .route('/cm/delete/<cloud>/<server>/')
def delete_vm(cloud=None, server=None):
    print "-> delete", cloud, server
    # if (cloud == 'india'):
    #  r = cm("--set", "quiet", "delete:1", _tty_in=True)
    clouds.delete(cloud, server)
    time.sleep(5)
    #    clouds.refresh()
    return redirect("/table/")
#    return table()

# ============================================================
# ROUTE: DELETE GROUP
# ============================================================


@cloud_module .route('/cm/delete/<cloud>/')
def delete_vms(cloud=None):
# donot do refresh before delete, this will cause all the vms to get deleted
    f_cloud = clouds.clouds[cloud]
    for id, server in f_cloud['servers'].iteritems():
        print "-> delete", cloud, id
        clouds.delete(cloud, id)
    time.sleep(7)
    f_cloud['servers'] = {}
    return redirect("/table/")


# ============================================================
# ROUTE: ASSIGN PUBLIC IP
# ============================================================


@cloud_module .route('/cm/assignpubip/<cloud>/<server>/')
def assign_public_ip(cloud=None, server=None):
    try:
        if configuration['clouds'][cloud]['cm_automatic_ip'] is False:
            clouds.assign_public_ip(cloud, server)
            clouds.refresh(names=[cloud])
            return redirect("/table/")
        else:
            return "Manual public ip assignment is not allowed for {0} cloud".format(cloud)
    except Exception, e:
        return str(e) + "Manual public ip assignment is not allowed for {0} cloud".format(cloud)

# ============================================================
# ROUTE: START
# ============================================================

#
# WHY NOT USE cm_keys as suggested?
#


@cloud_module .route('/cm/start/<cloud>/')
def start_vm(cloud=None, server=None):
    print "*********** STARTVM", cloud
    print "-> start", cloud
    # if (cloud == 'india'):
    #  r = cm("--set", "quiet", "start:1", _tty_in=True)
    key = None

    # if configuration.has_key('keys'):
    if 'keys' in configuration:
        key = configuration['keys']['default']

    # THIS IS A BUG
    vm_flavor = clouds.default(cloud)['flavor']
    vm_image = clouds.default(cloud)['image']

    print "STARTING", config.prefix, config.index
    result = clouds.create(
        cloud, config.prefix, config.index, vm_image, vm_flavor, key)
    # print "PPPPPPPPPPPP", result
    clouds.vm_set_meta(cloud, result['id'], {'cm_owner': config.prefix})
    config.incr()
    config.write()

    return table()


# ============================================================
# ROUTE: VM Login
# ============================================================


@cloud_module .route('/cm/login/<cloud>/<server>/')
def vm_login(cloud=None, server=None):
    message = ''
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    server = clouds.clouds[cloud]['servers'][server]

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

    return redirect("/table/")
# ============================================================
# ROUTE: VM INFO
# ============================================================


@cloud_module .route('/cm/info/<cloud>/<server>/')
def vm_info(cloud=None, server=None):

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    clouds.clouds[cloud]['servers'][server]['cm_vm_id'] = server
    clouds.clouds[cloud]['servers'][server]['cm_cloudname'] = cloud

    return render_template('vm_info.html',
                           updated=time_now,
                           keys="",
                           server=clouds.clouds[cloud]['servers'][server],
                           id=server,
                           cloudname=cloud,
                           table_printer=table_printer)

# ============================================================
# ROUTE: FLAVOR
# ============================================================

# @cloud_module .route('/flavors/<cloud>/' )


@cloud_module .route('/flavors/', methods=['GET', 'POST'])
def display_flavors(cloud=None):

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if request.method == 'POST':
        for cloud in config.active():
            configuration['clouds'][cloud]['default'][
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
# @cloud_module .route('/images/<cloud>/')
@cloud_module .route('/images/', methods=['GET', 'POST'])
def display_images():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if request.method == 'POST':
        for cloud in config.active():
            configuration['clouds'][cloud][
                'default']['image'] = request.form[cloud]
            config.write()

    return render_template(
        'images.html',
        updated=time_now,
        clouds=clouds.clouds,
        cloudmesh=clouds,
        config=config)

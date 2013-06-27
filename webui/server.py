from flask_flatpages import FlatPages
debug = False


from os.path import isfile, join
with_cloudmesh = False
import sys
sys.path.insert(0, '.')
sys.path.insert(0, '..')

from ConfigParser import SafeConfigParser
from cloudmesh.provisioner.provisioner import *

server_config = SafeConfigParser(
    {'name': 'flasktest'})  # Default database name
server_config.read("server.config")

from cloudmesh.inventory.resources import FabricImage
from cloudmesh.util.util import table_printer

import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

if with_cloudmesh:
    from cloudmesh.config.cm_keys import cm_keys
    from cloudmesh.config.cm_projects import cm_projects
    from cloudmesh.config.cm_config import cm_config
    from cloudmesh.cloudmesh import cloudmesh

import os
import time
from flask import Flask, render_template, request, redirect
from flask.ext.autoindex import AutoIndex
from modules.flatpages import flatpages_module
from modules.keys import keys_module
from modules.inventory import inventory_module
from modules.view_git import git_module
from modules.profile import profile_module
from modules.menu import menu_module
# from menu.server_keys import menu_module

import base64
import struct
import hashlib

from datetime import datetime
import yaml

try:
    from sh import xterm
except:
    print "xterm not suppported"

    # TODO: THERE SHOULD BE A VARIABLE SET HERE SO THAT THE ARROW
    # START UP BUTTON CAN RETURN MEANINGFULL MESSAGE IF NOT SUPPORTED


# ============================================================
# allowing the yaml file to be written back upon change
# ============================================================
with_write = True

# ============================================================
# setting up reading path for the use of yaml
# ============================================================

default_path = '.futuregrid/cloudmesh.yaml'
home = os.environ['HOME']
filename = "%s/%s" % (home, default_path)

# ============================================================
# global vars
# ============================================================

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

import pkg_resources
version = pkg_resources.get_distribution("cloudmesh").version

# ============================================================
# INVENTORY
# ============================================================

from cloudmesh.inventory.resources import Inventory
from cloudmesh.inventory.resources import FabricService
from cloudmesh.inventory.resources import FabricServer

inventory_db = server_config.get("mongo", "dbname")
if server_config.has_option("mongo", "host"):
    inventory = Inventory(inventory_db,
                          server_config.get("mongo", "host"),
                          server_config.getint("mongo", "port"),
                          server_config.get("mongo", "user"),
                          server_config.get("mongo", "pass"))
else:
    inventory = Inventory(inventory_db)
inventory.clean()

inventory.create_cluster(
    "bravo", "101.102.203.[11-26]", "b{0:03d}", 1, "b001", "b")
#inventory.create_cluster(
#    "delta", "102.202.204.[1-16]", "d-{0:03d}", 1, "d-001", "d")
# inventory.create_cluster("gamma", "302.202.204.[1-16]", "g-{0:03d}", 1,
# "g-001", "g")
# inventory.create_cluster("india", "402.202.204.[1-128]", "i-{0:03d}", 1, "i-001", "i")
# inventory.create_cluster("sierra", "502.202.204.[1-128]", "s-{0:03d}", 1, "s-001", "s")

centos = FabricImage(
    name="centos6",
    osimage='/path/to/centos0602v1-2013-06-11.squashfs',
    os='centos6',
    extension='squashfs',
    partition_scheme='mbr',
    method='put',
    kernel='vmlinuz-2.6.32-279.19.1.el6.x86_64',
    ramdisk='initramfs-2.6.32-279.19.1.el6.x86_64.img',
    grub='grub',
    rootpass='reset'
).save()

redhat = FabricImage(
    name="ubuntu",
    osimage='/BTsync/ubuntu1304/ubuntu1304v1-2013-06-11.squashfs',
    os='ubuntu',
    extension='squashfs',
    partition_scheme='mbr',
    method='btsync',
    kernel='vmlinuz-2.6.32-279.19.1.el6.x86_64',
    ramdisk='initramfs-2.6.32-279.19.1.el6.x86_64.img',
    grub='grub2',
    rootpass='reset'
).save()


    # print inventory.pprint()
# ============================================================
# CLOUDMESH
# ============================================================

if with_cloudmesh:

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
# PROVISINOR
# ============================================================
provisionerImpl = ProvisionerSimulator
provisioner = provisionerImpl()

# pp.pprint (pages.__dict__['app'].__dict__)

# ============================================================
# STARTING THE FLASK APP
# ============================================================

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True
pages = FlatPages(app)
app.register_blueprint(keys_module, url_prefix='', )
app.register_blueprint(inventory_module, url_prefix='', )
app.register_blueprint(git_module, url_prefix='', )
app.register_blueprint(profile_module, url_prefix='', )
app.register_blueprint(menu_module, url_prefix='', )
app.register_blueprint(flatpages_module, url_prefix='', )



#@app.context_processor
#def inject_pages():
#    return dict(pages=pages)


# app.register_blueprint(menu_module, url_prefix='/', )

if debug:
    AutoIndex(app, browse_root=os.path.curdir)

# ============================================================
# VESRION
# ============================================================

@app.context_processor
def inject_version():
    return dict(version=version)


# ============================================================
# ROUTE: sitemap
# ============================================================

"""
@app.route("/site-map/")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        print"PPP>",  rule, rule.methods, rule.defaults, rule.endpoint, rule.arguments
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        try:
            if "GET" in rule.methods and len(rule.defaults) >= len(rule.arguments):
                url = url_for(rule.endpoint)
                links.append((url, rule.endpoint))
                print "Rule added", url, links[url]
        except:
            print "Rule not activated"
    # links is now a list of url, endpoint tuples
"""


# ============================================================
# ROUTE: /
# ============================================================
@app.route('/')
def index():
    return render_template('index.html')


# ============================================================
# ROUTE: REFRESH
# ============================================================
@app.route('/cm/refresh/')
@app.route('/cm/refresh/<cloud>/')
def refresh(cloud=None, server=None):
    # print "-> refresh", cloud, server
    clouds.refresh()
    clouds.all_filter()
    return table()

# ============================================================
# ROUTE: Filter
# ============================================================


@app.route('/cm/filter/<cloud>/', methods=['GET', 'POST'])
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
@app.route('/cm/kill/')
def kill_vms():
    print "-> kill all"
    r = cm("--set", "quiet", "kill", _tty_in=True)
    return table()

# ============================================================
# ROUTE: DELETE
# ============================================================


@app.route('/cm/delete/<cloud>/<server>/')
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


@app.route('/cm/delete/<cloud>/')
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


@app.route('/cm/assignpubip/<cloud>/<server>/')
def assign_public_ip(cloud=None, server=None):
    try:
        if configuration['clouds'][cloud]['cm_automatic_ip'] is False:
            clouds.assign_public_ip(cloud, server)
            clouds.refresh(names=[cloud])
            return redirect("/table/")
        else:
            return "Manual public ip assignment is not allowed for %s cloud" % cloud
    except Exception, e:
        return str(e) + "Manual public ip assignment is not allowed for %s cloud" % cloud

# ============================================================
# ROUTE: START
# ============================================================

#
# WHY NOT USE cm_keys as suggested?
#


@app.route('/cm/start/<cloud>/')
def start_vm(cloud=None, server=None):
    print "*********** STARTVM", cloud
    print "-> start", cloud
    # if (cloud == 'india'):
    #  r = cm("--set", "quiet", "start:1", _tty_in=True)
    key = None

    if keys in configuration:
        key = configuration['keys']['default']

    # THIS IS A BUG
    vm_flavor = clouds.default(cloud)['flavor']
    vm_image = clouds.default(cloud)['image']

    print "STARTING", config.prefix, config.index
    result = clouds.create(
        cloud, config.prefix, config.index, vm_image, vm_flavor, key)
    # print ">>>>>>>>>>>>>>", result
    clouds.vm_set_meta(cloud, result['id'], {'cm_owner': config.prefix})
    config.incr()
    config.write()

    return table()

'''
#gregors test
@app.route('/cm/metric/<startdate>/<enddate>/<host>')
def list_metric(cloud=None, server=None):
    print "-> generate metric", startdate, endadte
    #r = fg-metric(startdate, enddate, host, _tty_in=True)
    return render_template('metric1.html',
                           startdate=startdate,
                           endate=enddate)
    #return table()
'''

# ============================================================
# ROUTE: SAVE
# ============================================================


@app.route('/save/')
def save():
    print "Saving the cloud status"
    clouds.save()
    return table()

# ============================================================
# ROUTE: LOAD
# ============================================================


@app.route('/load/')
def load():
    print "Loading the cloud status"
    clouds.load()
    return table()

# ============================================================
# ROUTE: TABLE
# ============================================================


@app.route('/table/')
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
# ROUTE: VM Login
# ============================================================


@app.route('/cm/login/<cloud>/<server>/')
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


@app.route('/cm/info/<cloud>/<server>/')
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

#@app.route('/flavors/<cloud>/' )


@app.route('/flavors/', methods=['GET', 'POST'])
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
#@app.route('/images/<cloud>/')
@app.route('/images/', methods=['GET', 'POST'])
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


# ============================================================
# ROUTE: INVENTORY TABLE
# ============================================================
@app.route('/inventory/')
def display_inventory():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template('inventory.html',
                           updated=time_now,
                           inventory=inventory)


@app.route('/inventory/images/')
def display_inventory_images():
    return render_template('images.html',
                           inventory=inventory)


@app.route('/inventory/cluster/<cluster>/')
def display_cluster(cluster):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template('inventory_cluster.html',
                           updated=time_now,
                           cluster=inventory.find("cluster", cluster))


@app.route('/inventory/cluster/table/<cluster>/')
def display_cluster_table(cluster):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    parameters = {
        "rows": 10,
        "columns": 100,
    }
    return render_template('inventory_cluster_table.html',
                           updated=time_now,
                           parameters=parameters,
                           cluster=inventory.find("cluster", cluster))


@app.route('/inventory/images/<name>/')
def display_image(name):
    image = inventory.get('image', name)[0]
    return render_template('info_image.html',
                           table_printer=table_printer,
                           image=image.data,
                           name=name,
                           inventory=inventory)

# ============================================================
# ROUTE: INVENTORY ACTIONS
# ============================================================


@app.route('/inventory/info/server/<server>/')
def server_info(server):

    server = inventory.find("server", name)
    return render_template('info_server.html',
                           server=server,
                           inventory=inventory)


@app.route('/inventory/set/service/', methods=['POST'])
def set_service():
    server = request.form['server']
    service = request.form['service']

    inventory.set_service('%s-%s' % (server, service), server, service)
    provisioner.provision([server], service)
    return display_inventory()


@app.route('/inventory/set/attribute/', methods=['POST'])
def set_attribute():
    kind = request.form['kind']
    name = request.form['name']
    attribute = request.form['attribute']
    value = request.form['value']

    s = inventory.get(kind, name)
    s[attribute] = value
    s.save()
    return display_inventory()


@app.route('/inventory/get/<kind>/<name>/<attribute>')
def get_attribute():
    s = inventory.get(kind, name)
    return s[attribute]



# ============================================================
# ROUTE: METRIC
# ============================================================
#@app.route('/metric/<s_date>/<e_date>/<user>/<cloud>/<host>/<period>/<metric>')


@app.route('/metric/main', methods=['POST', 'GET'])
def metric():
    args = {"s_date": request.args.get('s_date', ''),
            "e_date": request.args.get('e_date', ''),
            "user": request.args.get('user', ''),
            "cloud": request.args.get('cloud', ''),
            "host": request.args.get('host', ''),
            "period": request.args.get('period', ''),
            "metric": request.args.get('metric', '')}

    return render_template('metric.html',
                           clouds=clouds.get(),
                           metrics=clouds.get_metrics(args))

# ============================================================
# ROUTE: PAGES
# ============================================================


@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

if __name__ == "__main__":
    app.run()

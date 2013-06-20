import sys
from ConfigParser import SafeConfigParser
from provisiner import *
server_config = SafeConfigParser({'name': 'flasktest'}) #Default database name
server_config.read("server.config")

sys.path.insert(0, './')
sys.path.insert(0, '../')

import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

from cloudmesh.cm_keys import cm_keys
from cloudmesh.cm_projects import cm_projects
from cloudmesh.cm_config import cm_config
from cloudmesh.cloudmesh import cloudmesh

import os
import time
from flask import Flask, render_template, request,redirect
from flask_flatpages import FlatPages
import base64,struct,hashlib

from datetime import datetime
import yaml

######################################################################
# allowing the yaml file to be written back upon change
######################################################################

with_write = True

######################################################################
# setting up reading path for the use of yaml
######################################################################

default_path = '.futuregrid/cloudmesh.yaml'
home = os.environ['HOME']
filename = "%s/%s" % (home, default_path)

######################################################################
# global vars
######################################################################

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

"""
import pkg_resources
version = pkg_resources.get_distribution("flask_cm").version
"""
version = "0.1"

######################################################################
# INVENTORY
######################################################################

from Inventory import Inventory
from Inventory import FabricService
from Inventory import FabricServer

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

# Simulate the Bravo cluster
bravo = inventory.ip_dict ("172.29.202.[11-26]", "b{0:03d}", 1)
for name in bravo:
    ip = bravo[name]
    log.info("create {0} {1}".format(name, ip))
    inventory.create("server", "dynamic", name)
    inventory.add_service('{0}-hpc'.format(name), name, 'hpc')
    server = inventory.find("server", name)
    server.ip_address = ip
    #server['ip_address'] = ip
    server.save()

inventory.create("cluster", "dynamic", "bravo")
bravo_cluster = inventory.find("cluster", "bravo")
bravo_cluster.management_node = inventory.find("server", "b001")
bravo_cluster.compute_nodes = filter(lambda s: s.name != "b001", inventory.servers())
bravo_cluster.service_choices = ('hpc', 'openstack', 'eucalyptus')
bravo_cluster.save()

#print inventory.pprint()

######################################################################
# PROVISINOR
######################################################################
provisionerImpl = ProvisionerSimulator

provisioner = provisionerImpl()


######################################################################
# STARTING THE FLASK APP
######################################################################

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)

######################################################################
# ACTIVATE STRUCTURE
######################################################################


def make_active(name):
    active = {'home': "",
              'inventory': "",
              'contact': "",
              'profile': ""}
    
    active[name] = 'active'
    return active

######################################################################
# ROUTE: /
######################################################################


@app.route('/')
def index():
    active = make_active('home')
    return render_template('index.html',
                           pages=pages,
                           active=active,
                           version=version)

######################################################################
# ROUTE: SAVE
######################################################################


@app.route('/inventory/save/')
def save():
    print "Saving the inventory"
    return display_inventory()

######################################################################
# ROUTE: LOAD
######################################################################


@app.route('/inventory/load/')
def load():
    print "Loading the inventory"
    return display_inventory()

######################################################################
# ROUTE: INVENTORY TABLE
######################################################################


@app.route('/inventory/')
def display_inventory():
    active = make_active('inventory')
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template('inventory.html',
                           updated=time_now,
                           pages=pages,
                           active=active,
                           version=version,
                           inventory=inventory)

@app.route('/inventory/cluster/<cluster>/')
def display_cluster(cluster):
    active = make_active('inventory')
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template('inventory_cluster.html',
                           updated=time_now,
                           pages=pages,
                           active=active,
                           version=version,
                           cluster=inventory.find("cluster", cluster))


######################################################################
# ROUTE: INVENTORY ACTIONS
######################################################################

@app.route('/inventory/info/server/<server>/')
def server_info(server):
    active = make_active('')
    
    server = inventory.find("server", name)
    return render_template('info_server.html',
                           server=server,
                           pages=pages,
                           active=active,
                           version=version,
                           inventory=inventory)

@app.route('/inventory/set/service/<server>/<service>')
def set_service(server, service):
    active = make_active('inventory')
    inventory.set_service('%s-%s' % (server, service), server, service)
    provisioner.provision([server], service)    
    return display_inventory()

@app.route('/inventory/set/<kind>/<name>/<attribute>/<value>')
def set_attribute():
    active = make_active('inventory')
    s = inventory.get (kind, name)
    s[attribute] = value
    s.save()
    return display_inventory()

@app.route('/inventory/get/<kind>/<name>/<attribute>')
def get_attribute():
    active = make_active('inventory')
    s = inventory.get (kind, name)
    return s[attribute]

##############################
# Helpers
##############################
    
def table_printer(the_dict):
    return_str = ''
    if isinstance(the_dict, dict):
        for name,value in the_dict.iteritems() :
            return_str =return_str +'<tr><td>'+name.title() +'</td><td>'+str(table_printer(value))+'</td></tr>'
        return_str = '<table>' + return_str + '</table>'
        return return_str
    elif type(the_dict) is list: 
        for element in the_dict:
            for name,value in element.iteritems() :
                return_str =return_str +'<tr><td>'+name.title()+'</td><td>'+str(table_printer(value))+'</td></tr>'
        return_str = '<table>' + return_str + '</table>'
        return return_str
    else:
        return the_dict





######################################################################
# ROUTE: PAGES
######################################################################


@app.route('/<path:path>/')
def page(path):
    active = make_active(str(path))
    page = pages.get_or_404(path)
    return render_template('page.html',
                           page=page,
                           pages=pages,
                           active=active,
                           version=version)


    
if __name__ == "__main__":
    app.run()

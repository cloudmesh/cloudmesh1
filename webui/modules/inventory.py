from flask import Blueprint
from flask import render_template, request
from datetime import datetime

from flask.ext.login import login_required

inventory_module = Blueprint('inventory_module', __name__)

from cloudmesh.inventory.inventory import Inventory as oldInventory
from cloudmesh.inventory import Inventory

from cloudmesh.util.util import table_printer
from cloudmesh.util.util import cond_decorator
import cloudmesh

inventory = oldInventory("nosetest")


n_inventory = Inventory()
n_inventory.clear()
n_inventory.generate()



@inventory_module.route('/inventory/')
@cond_decorator(cloudmesh.with_login, login_required)
def display_inventory():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    #inventory.refresh()

    clusters = ["bravo", "india", "delta", "echo", "sierra"]
    
    return render_template('mesh_inventory.html',
                           updated=time_now,
                           clusters=clusters)

"""
@inventory_module.route('/old/inventory/summary/')
def old_display_summary():
    parameters = {'columns': 12}
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template('inventory_summary_table.html',
                           inventory=inventory,
                           parameters=parameters,
                           updated=time_now)
"""

@inventory_module.route('/inventory/summary/')
@cond_decorator(cloudmesh.with_login, login_required)
def old_display_summary():
    
    #clusters = ["bravo", "india", "delta", "echo", "sierra"]
    clusters = ["bravo", "india", "delta", "echo"]
    
    inv = {}
    
    for cluster in clusters:
        inv[cluster] = n_inventory.hostlist(cluster)
    
    parameters = {'columns': 12}
    
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    return render_template('mesh_inventory_summary_table.html',
                           inventory=inv,
                           clusters=clusters,
                           parameters=parameters,
                           updated=time_now)

# ============================================================
# ROUTE: INVENTORY TABLE
# ============================================================

"""
@inventory_module.route('/inventory/')
def display_old_inventory():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    inventory.refresh()
    return render_template('inventory.html',
                           updated=time_now,
                           inventory=inventory)
"""


@inventory_module.route('/inventory/cluster/<cluster>/<name>')
@cond_decorator(cloudmesh.with_login, login_required)
def display_named_resource(cluster, name):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    #inventory.refresh()
    
    clusters = n_inventory.hostlist(cluster)
    server = n_inventory.host(name,auth=False)
    
    return render_template('mesh_inventory_cluster_server.html',
                           updated=time_now,
                           server=server,
                           printer=table_printer,
                           cluster=cluster)

"""
@inventory_module.route('/inventory/cluster/<cluster>/<name>')
def display_named_resource(cluster, name):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    inventory.refresh()
    return render_template('inventory_cluster_server.html',
                           updated=time_now,
                           server=inventory.get("server", name),
                           cluster=inventory.get("cluster", cluster),
                           inventory=inventory)


@inventory_module.route('/inventory/cluster/<cluster>/')
def display_cluster(cluster):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    inventory.refresh()
    return render_template('inventory_cluster.html',
                           updated=time_now,
                           cluster=inventory.get("cluster", cluster))

"""

@inventory_module.route('/inventory/cluster/<cluster>/')
@cond_decorator(cloudmesh.with_login, login_required)
def display_cluster(cluster):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    #inventory.refresh()
    
    servers = n_inventory.hostlist(cluster)
    
    return render_template('mesh_inventory_cluster.html',
                           updated=time_now,
                           servers=servers,
                           cluster=cluster,
                           services=['openstack', 'eucalyptus', 'hpc'])

"""
@inventory_module.route('/inventory/cluster/table/<cluster>/')
def display_cluster_table(cluster):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    inventory.refresh()

    cluster_obj = inventory.get("cluster", cluster)
    n = len(cluster_obj['servers'])
    parameters = {
        "columns": 10,
        "n": n
    }

    return render_template('inventory_cluster_table.html',
                           updated=time_now,
                           parameters=parameters,
                           cluster=inventory.get("cluster", cluster))
"""

@inventory_module.route('/inventory/cluster/table/<cluster>/')
@cond_decorator(cloudmesh.with_login, login_required)
def display_cluster_table(cluster):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    #inventory.refresh()

    servers = n_inventory.hostlist(cluster)


    cluster_obj = inventory.get("cluster", cluster)
    n = len(servers)
    parameters = {
        "columns": 10,
        "n": n
    }

    return render_template('mesh_inventory_cluster_table.html',
                           updated=time_now,
                           parameters=parameters,
                           servers= servers,
                           cluster=cluster)
                           
#                           cluster=inventory.get("cluster", cluster))


@inventory_module.route('/inventory/images/')
@cond_decorator(cloudmesh.with_login, login_required)
def display_inventory_images():
    images = inventory.get("images")
    inventory.refresh()
    return render_template('inventory_images.html',
                           images=images,
                           inventory=inventory)


@inventory_module.route('/inventory/image/<name>/')
@cond_decorator(cloudmesh.with_login, login_required)
def display_inventory_image(name):
    print "PRINT IMAGE", name
    inventory.refresh()
    if name is not None:
        image = inventory.get('images', name)
    return render_template('inventory_image.html',
                           image=image)


# ============================================================
# ROUTE: INVENTORY ACTIONS
# ============================================================


@inventory_module.route('/inventory/info/server/<server>/')
@cond_decorator(cloudmesh.with_login, login_required)
def server_info(server):

    server = inventory.find("server", server)
    return render_template('info_server.html',
                           server=server,
                           inventory=inventory)


@inventory_module.route('/inventory/set/service/', methods=['POST'])
@cond_decorator(cloudmesh.with_login, login_required)
def set_service():
    server_name = request.form['server']
    service_name = request.form['provisioned']

    server = inventory.get("server", server_name)
    server.provisioned = service_name
    server.save(cascade=True)
    # provisioner.provision([server], service)
    return display_inventory()


@inventory_module.route('/inventory/set/attribute/', methods=['POST'])
@cond_decorator(cloudmesh.with_login, login_required)
def set_attribute():
    kind = request.form['kind']
    name = request.form['name']
    attribute = request.form['attribute']
    value = request.form['value']

    s = inventory.get(kind, name)
    s[attribute] = value
    s.save()
    return display_inventory()


@inventory_module.route('/inventory/get/<kind>/<name>/<attribute>')
@cond_decorator(cloudmesh.with_login, login_required)
def get_attribute(kind, name, attribute):
    s = inventory.get(kind, name)
    return s[attribute]


@inventory_module.route('/inventory/save/')
@cond_decorator(cloudmesh.with_login, login_required)
def inventory_save():
    print "Not IMPLEMENTED YET"
    print "Saving the inventory"
    return display_inventory()


@inventory_module.route('/inventory/load/')
@cond_decorator(cloudmesh.with_login, login_required)
def inventory_load():
    print "Not IMPLEMENTED YET"
    return display_inventory()

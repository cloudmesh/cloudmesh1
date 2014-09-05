from flask import Blueprint
from flask import render_template, request
from datetime import datetime

from flask.ext.login import login_required

inventory_module = Blueprint('inventory_module', __name__)


from cloudmesh.inventory import Inventory

from cloudmesh_common.tables import table_printer
from cloudmesh_common.util import cond_decorator
from cloudmesh.config.cm_config import cm_config_server

from flask.ext.principal import Permission, RoleNeed


from cloudmesh_common.logger import LOGGER
from pprint import pprint

log = LOGGER(__file__)


admin_permission = Permission(RoleNeed('admin'))


import hostlist

inventory = Inventory()
# inventory.clear()
# inventory.generate()


@inventory_module.route('/inventory/')
@login_required
@admin_permission.require(http_exception=403)
def display_inventory():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # inventory.refresh()

    clusters = ["bravo", "india", "delta", "echo", "sierra"]

    return render_template('mesh/inventory/mesh_inventory.html',
                           updated=time_now,
                           clusters=clusters)


@inventory_module.route('/inventory/summary/')
@login_required
@admin_permission.require(http_exception=403)
def old_display_summary():

    # clusters = ["bravo", "india", "delta", "echo", "sierra"]
    clusters = ["bravo", "india", "delta", "echo"]

    inv = {}

    for cluster in clusters:
        inv[cluster] = inventory.hostlist(cluster)

    parameters = {'columns': 12}

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return render_template('mesh/inventory/mesh_inventory_summary_table.html',
                           inventory=inv,
                           clusters=clusters,
                           parameters=parameters,
                           updated=time_now)

# ============================================================
# ROUTE: INVENTORY TABLE
# ============================================================


@inventory_module.route('/inventory/cluster/<cluster>/<name>')
@login_required
@admin_permission.require(http_exception=403)
def display_named_resource(cluster, name):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # inventory.refresh()
    clusters = inventory.hostlist(cluster)
    server = inventory.host(name, auth=False)

    return render_template('mesh/inventory/mesh_inventory_cluster_server.html',
                           updated=time_now,
                           server=server,
                           printer=table_printer,
                           cluster=cluster)


@inventory_module.route('/inventory/cluster/<cluster>/')
@login_required
@admin_permission.require(http_exception=403)
def display_cluster(cluster):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # inventory.refresh()
    servers = inventory.hostlist(cluster)

    return render_template('mesh/inventory/mesh_inventory_cluster.html',
                           updated=time_now,
                           servers=servers,
                           cluster=cluster,
                           services=['openstack', 'eucalyptus', 'hpc'])


@inventory_module.route('/inventory/cluster-user')
@login_required
@admin_permission.require(http_exception=403)
def display_cluster_for_user():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # inventory.refresh()
    user = "gvonlasz"
    try:
        host_lists = get_user_host_list(user)
    except:
        return render_template('error.html', error="Could not load the user details")
    cluster_data = get_servers_for_clusters(host_lists)
    # servers = inventory.hostlist(cluster)
    return render_template('mesh/inventory/mesh_inventory_cluster_limited.html',
                           updated=time_now,
                           cluster_data=cluster_data,
                           services=['openstack', 'eucalyptus', 'hpc'])


@inventory_module.route('/inventory/cluster-proj')
@login_required
@admin_permission.require(http_exception=403)
def display_cluster_for_proj():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # inventory.refresh()
    proj = "fg82fsdfsd"
    try:
        host_lists = get_proj_host_list(proj)
    except:
        return render_template('error.html', error="Could not load the project details")
    cluster_data = get_servers_for_clusters(host_lists)

    # servers = inventory.hostlist(cluster)
    return render_template('mesh/inventory/mesh_inventory_cluster_limited.html',
                           updated=time_now,
                           cluster_data=cluster_data,
                           services=['openstack', 'eucalyptus', 'hpc'])


def get_user_host_list(user):
    config = cm_config_server()
    host_lists = config.get("provisioner.policy.users." + user)
    return host_lists


def get_proj_host_list(proj):
    config = cm_config_server()
    host_lists = config.get("provisioner.policy.projects." + proj)
    return host_lists


def get_servers_for_clusters(host_lists):
    log.info("get server fo closyer")
    cluster_dict = {"i": "india", "s": "sierra", "b": "bravo",
                    "e": "echo", "d": "delta"}  # move to config at some point
    return_dict = {}

    for h in host_lists:
        allowed_servers = hostlist.expand_hostlist(h)
        index = h.find("[")
        key = h[0:index]
        cluster = cluster_dict[key]
        cluster_servers = inventory.hostlist(cluster)
        l = list(set(cluster_servers) & set(allowed_servers))
        if cluster in return_dict:
            return_dict[cluster].extend(l)
        return_dict[cluster] = l
    return return_dict


@inventory_module.route('/inventory/cluster/table/<cluster>/')
@login_required
@admin_permission.require(http_exception=403)
def display_cluster_table(cluster):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # inventory.refresh()

    servers = inventory.hostlist(cluster)

    cluster_obj = inventory.get("cluster", 'cm_id', cluster)
    n = len(servers)
    parameters = {
        "columns": 10,
        "n": n
    }

    return render_template('mesh/inventory/mesh_inventory_cluster_table.html',
                           updated=time_now,
                           parameters=parameters,
                           servers=servers,
                           cluster=cluster)

#                           cluster=inventory.get("cluster", cluster))


# ============================================================
# ROUTE: INVENTORY ACTIONS
# ============================================================


@inventory_module.route('/inventory/info/server/<server>/')
@login_required
@admin_permission.require(http_exception=403)
def server_info(server):

    server = inventory.find("server", server)
    return render_template('info_server.html',
                           server=server,
                           inventory=inventory)


@inventory_module.route('/inventory/set/service/', methods=['POST'])
@login_required
@admin_permission.require(http_exception=403)
def set_service():
    server_name = request.form['server']
    service_name = request.form['provisioned']

    server = inventory.get("server", server_name)
    server.provisioned = service_name
    server.save(cascade=True)
    # provisioner.provision([server], service)
    return display_inventory()


@inventory_module.route('/inventory/set/attribute/', methods=['POST'])
@login_required
@admin_permission.require(http_exception=403)
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
@login_required
@admin_permission.require(http_exception=403)
def get_attribute(kind, name, attribute):
    s = inventory.get(kind, name)
    return s[attribute]

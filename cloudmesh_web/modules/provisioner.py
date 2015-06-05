from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.inventory import Inventory
# from cloudmesh.old_inventory.inventory import Inventory as oldInventory, \
#    PROVISIONING_CHOICES
from cloudmesh.provisioner.provisioner import *
from cloudmesh.provisioner.queue.celery import celery_provisiner_queue
from cloudmesh.provisioner.queue.tasks import provision
from cloudmesh_base.logger import LOGGER
from cloudmesh_common.util import cond_decorator
from cloudmesh_base.util import path_expand
from datetime import datetime
from flask import Blueprint, render_template, redirect, flash
from flask.ext.login import login_required
from flask.ext.principal import Permission, RoleNeed
from flask.ext.wtf import Form
from hostlist import expand_hostlist
from pprint import pprint
from wtforms import TextField, SelectField, TextAreaField
import cloudmesh


log = LOGGER(__file__)

admin_permission = Permission(RoleNeed('admin'))

provisioner_module = Blueprint('provisioner_module', __name__)


#inventory = oldInventory("nosetest")
n_inventory = Inventory()

# ============================================================
# PROVISINOR
# ============================================================
provisionerImpl = ProvisionerSimulator
provisioner = provisionerImpl()


@provisioner_module.route('/provision/policy')
@login_required
@admin_permission.require(http_exception=403)
def display_provisioner_policy():

    policy = cm_config_server().get("cloudmesh.server.provisioner.policy")

    return render_template('mesh/provision/provision_policy.html',
                           policy=policy)


@provisioner_module.route('/provision/summary/')
@login_required
@admin_permission.require(http_exception=403)
def display_provisioner_summary():

    queue = celery_provisiner_queue.control.inspect()

    """
    for j in range(10):
    print chr(27) + "[2J"
    inventory.print_cluster("bravo")
    for host in hosts:
        print host, t[host].status
    pprint (i.active())
    pprint (i.scheduled())
    pprint (i.reserved())
    time.sleep(1)
    """
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template('mesh/provision/provision_summary_table.html',
                           provisioner=provisioner,
                           queue=queue,
                           updated=time_now)


@provisioner_module.route('/provision/tasks/<cluster>/<spec>/<service>')
@login_required
@admin_permission.require(http_exception=403)
def display_provision_host_summary(cluster, spec, service):

    time.sleep(1)
    hosts = expand_hostlist(spec)
    queue = celery_provisiner_queue.control.inspect()

    active = queue.active()
    scheduled = queue.scheduled()
    reserved = queue.reserved()

    # total = len(active) + len(scheduled) + len(reserved)

    table = {}
    for host in hosts:
        table[host] = {"provision": service,
                       "start": "None",
                       "worker": "",
                       "task": "provision",
                       "status": "completed"
                       }

    for worker in active:
        for task in active[worker]:
            (host, service) = list(eval(task["args"]))
            table[host]['worker'] = worker
            table[host]['status'] = 'active'
            table[host]['task'] = host
            table[host]['start'] = task['time_start']

    for worker in scheduled:
        for task in scheduled[worker]:
            (host, service) = list(eval(task["args"]))
            table[host]['worker'] = worker
            table[host]['status'] = 'scheduled'
            table[host]['task'] = host
            table[host]['start'] = task['time_start']

    for worker in reserved:
        for task in reserved[worker]:
            (host, service) = list(eval(task["args"]))
            table[host]['worker'] = worker
            table[host]['status'] = 'reserved'
            table[host]['task'] = host
            table[host]['start'] = task['time_start']

    pprint(table)
    """
    for j in range(10):
    print chr(27) + "[2J"
    inventory.print_cluster("bravo")
    for host in hosts:
        print host, t[host].status
    pprint (i.active())
    pprint (i.scheduled())
    pprint (i.reserved())
    time.sleep(1)
    """
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template('mesh/provision/provision_host_table.html',
                           provisioner=provisioner,
                           queue=queue,
                           table=table,
                           hosts=hosts,
                           cluster=cluster,
                           service=service,
                           updated=time_now)


class ProvisionForm(Form):

    # clusters = [cluster.name for cluster in inventory.get("cluster")]

    clusters = cm_config_server().get("cloudmesh.server.provisioner.clusters")

    choices = zip(clusters, clusters)
    cluster = SelectField("Cluster", choices=choices)
    nodespec = TextField("Nodes")
    # provision_choices = zip(PROVISIONING_CHOICES, PROVISIONING_CHOICES)
    # service = SelectField("Service", choices=provision_choices)

    def validate(self):
        #cluster = inventory.get("cluster", self.cluster.data)
        posibilities = expand_hostlist(cluster.definition)
        choice = expand_hostlist(self.nodespec.data)
        if choice == []:
            ok = False
        else:
            ok = set(choice).issubset(posibilities)
        print "Validate", ok, choice
        return ok


@provisioner_module.route("/provision/", methods=("GET", "POST"))
@login_required
@admin_permission.require(http_exception=403)
def display_provision_form():

    clusters = cm_config_server().get("cloudmesh.server.provisioner.clusters")

    # clusters = ['india','bravo']

    # servers = n_inventory.hostlist(cluster)
    # server = n_inventory.host(name,auth=False)

    form = ProvisionForm(csrf=False)

    if form.validate_on_submit():
        flash("Success")
        print "FORM"
        pprint(form.__dict__)
        print "CLUSTER", form.cluster.data
        print "Service", form.service.data
        hosts = expand_hostlist(form.nodespec.data)
        print "Nodespec", hosts

        for host in hosts:
            print "PROVISION HOST", host
            provision.delay(host, form.service.data)

        return redirect("provision/tasks/{0}/{1}/{2}"
                        .format(form.cluster.data,
                                form.nodespec.data,
                                form.service.data))
        # return redirect("/provision/summary/")

    else:
        flash("Wrong submission")
    # inventory.refresh()
    return render_template("mesh/provision/provision.html", clusters=clusters, form=form)

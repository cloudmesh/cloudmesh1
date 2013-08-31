from sh import blockdiag
from flask import Blueprint
from flask import render_template, redirect, flash
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import TextField, SelectField, TextAreaField
from cloudmesh.inventory.inventory import Inventory
from hostlist import expand_hostlist
from cloudmesh.provisioner.provisioner import *
from cloudmesh.inventory.inventory import PROVISIONING_CHOICES
from cloudmesh.provisioner.queue.celery import celery
from cloudmesh.provisioner.queue.tasks import provision
from cloudmesh.config.cm_config import cm_config_server
from pprint import pprint
from cloudmesh.util.util import path_expand

from cloudmesh.inventory.ninventory import ninventory

provisioner_module = Blueprint('provisioner_module', __name__)


inventory = Inventory("nosetest")
n_inventory = ninventory()

# ============================================================
# PROVISINOR
# ============================================================
provisionerImpl = ProvisionerSimulator
provisioner = provisionerImpl()



@provisioner_module.route('/provision/policy')
def display_provisioner_policy():
    
    policy = cm_config_server().get("provisioner.policy")
    
    return render_template('provision_policy.html',
                           policy=policy)



@provisioner_module.route('/provision/summary/')
def display_provisioner_summary():

    queue = celery.control.inspect()

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
    return render_template('provision_summary_table.html',
                           provisioner=provisioner,
                           queue=queue,
                           updated=time_now)


@provisioner_module.route('/provision/tasks/<cluster>/<spec>/<service>')
def display_provision_host_summary(cluster, spec, service):

    time.sleep(1)
    hosts = expand_hostlist(spec)
    queue = celery.control.inspect()

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
    return render_template('provision_host_table.html',
                           provisioner=provisioner,
                           queue=queue,
                           table=table,
                           hosts=hosts,
                           cluster=cluster,
                           service=service,
                           updated=time_now)


class ProvisionForm(Form):

    #clusters = [cluster.name for cluster in inventory.get("cluster")]
    
    clusters = cm_config_server().get("provisioner.clusters")
    
    choices = zip(clusters, clusters)
    cluster = SelectField("Cluster", choices=choices)
    nodespec = TextField("Nodes")
    provision_choices = zip(PROVISIONING_CHOICES, PROVISIONING_CHOICES)
    service = SelectField("Service", choices=provision_choices)



    def validate(self):
        cluster = inventory.get("cluster", self.cluster.data)
        posibilities = expand_hostlist(cluster.definition)
        choice = expand_hostlist(self.nodespec.data)
        if choice == []:
            ok = False
        else:
            ok = set(choice).issubset(posibilities)
        print "Validate", ok, choice
        return ok


@provisioner_module.route("/provision/", methods=("GET", "POST"))
def display_provision_form():

    clusters = cm_config_server().get("provisioner.clusters")
    
    #clusters = ['india','bravo','sierra']
    
    #servers = n_inventory.hostlist(cluster)
    #server = n_inventory.host(name,auth=False)


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
    inventory.refresh()
    return render_template("provision.html", clusters=clusters, form=form)

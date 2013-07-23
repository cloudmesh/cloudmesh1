from flask import Blueprint
from flask import Flask, render_template, request, redirect, flash, url_for
from cloudmesh.config.cm_keys import cm_keys
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import TextField, SelectField
from cloudmesh.inventory.inventory import FabricImage, FabricServer, \
    FabricService, Inventory
from hostlist import expand_hostlist
    
provisioner_module = Blueprint('provisioner_module', __name__)


inventory = Inventory("nosetest")

@provisioner_module.route('/provision/summary/')
def display_summary():
    parameters = { 'columns': 12}
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template('provisioner_summary_table.html',
                           provisioner=provisioner,
                           parameters=parameters,
                           updated=time_now)

class ProvisionForm(Form):

    clusters = [cluster.name for cluster in inventory.get("cluster")]
    choices = zip (clusters, clusters)
    cluster = SelectField("Cluster", choices=choices)
    nodespec = TextField("Nodes")

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
def provision():

    form = ProvisionForm(csrf=False)

    if form.validate_on_submit():
        flash("Success")
        return render_template("provision.html", form=form, inventory=inventory)    
    else:
        flash("Wrong submission")
    inventory.refresh()
    return render_template("provision.html", form=form, inventory=inventory)    
    
        

from flask import Blueprint
from flask import Flask, render_template, request, redirect
from cloudmesh.config.cm_keys import cm_keys
from datetime import datetime

inventory_module = Blueprint('inventory_module', __name__)


#
# ROUTE: SAVE
#

@inventory_module.route('/inventory/save/')
def inventory_save():
    print "Saving the inventory"
    return display_inventory()

#
# ROUTE: LOAD
#


@inventory_module.route('/inventory/load/')
def inventory_load():
    print "Loading the inventory"
    return display_inventory()

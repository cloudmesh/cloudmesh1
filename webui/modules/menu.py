from flask import Blueprint
from flask import g
import flask
from os import listdir
from os.path import isfile, join
from cloudmesh.util.logger import LOGGER

log = LOGGER("module/menu")

menu_module = Blueprint('menu_module', __name__)

app_sidebar = [
    ["Home", "/"],
    ["Inventory", "/inventory/"],
    ["Profile", "/profile/"],
    ["- Keys", "/keys/"],
    ["Inventory Images", "/inventory/images/"],
    ["VMs", "/table/"],
    ["Images", "/images/"],
    ["Metric", "/metric/main/"],
    ["Projects", "/projects/"],
    ["Flavors", "/flavors/"],
]

sidebar_pages = []
for page in app_sidebar:
    sidebar_pages.append({'name': page[0], 'url': page[1]})

# registering sidebar into the global g
flask.Flask.app_ctx_globals_class.sidebar_pages = sidebar_pages

log.info("{0}".format(str(flask.Flask.app_ctx_globals_class.sidebar_pages)))


#
# ACTIVATE STRUCTURE
#

#@menu_module.context_processor
# def inject_sidebar():

#    print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"

    #    return dict(sidebar_pages=g.sidebar_pages)

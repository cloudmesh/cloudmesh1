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
    ["  - Summary", "/inventory/summary"],
    ["  - Images", "/inventory/images"],
    ["Provisioner", "/provision/summary/"],
    ["  - form", "/provision/"],
    ["  - workflow", "/provision/workflow"],
    ["Profile", "/profile/"],
    ["  - Keys", "/keys/"],
    ["VMs", "/table/"],
    ["  - Images", "/images/"],
    ["Metric", "/metric/main/"],
    ["Projects", "/projects/"],
    ["Flavors", "/flavors/"],
    ["QStat", "/pbs/india.futuregrid.org"],
    ["    - India", "/pbs/india.futuregrid.org"],
    ["    - Sierra", "/pbs/sierra.futuregrid.org"],
    ["    - Alamo", "/pbs/alamo.futuregrid.org"],
    ["    - Hotel", "/pbs/hotel.futuregrid.org"],
                
]

def add_menu(label, link):
    app_sidebar.append([label,link])

app_topbar = [
    ["Home", "/"],
    ["Profile", "/profile/"],
    ["About", "/about/"],
    ["Contact", "/contact/"],
]

app_externalbar = [
    ["FutureGrid", "https://portal.futuregrid.org"],
    ["Cloudmesh", "https://github.com/cloudmesh/cloudmesh"],
    ["Blog", "http://cloudmesh.blogspot.com"],
]


sidebar_pages = []
for page in app_sidebar:
    sidebar_pages.append({'name': page[0], 'url': page[1]})

# registering sidebar into the global g
flask.Flask.app_ctx_globals_class.sidebar_pages = sidebar_pages

#log.info("{0}".format(str(flask.Flask.app_ctx_globals_class.sidebar_pages)))

topbar_pages = []
for page in app_topbar:
    topbar_pages.append({'name': page[0], 'url': page[1]})

# registering topbar into the global g
flask.Flask.app_ctx_globals_class.topbar_pages = topbar_pages


#log.info("{0}".format(str(flask.Flask.app_ctx_globals_class.topbar_pages)))

externalbar_pages = []
for page in app_externalbar  :
    externalbar_pages.append({'name': page[0], 'url': page[1]})

# registering externalbar   into the global g
flask.Flask.app_ctx_globals_class.externalbar_pages = externalbar_pages


#log.info("{0}".format(str(flask.Flask.app_ctx_globals_class.externalbar_pages)))


#
# ACTIVATE STRUCTURE
#

#@menu_module.context_processor
# def inject_sidebar():

#    print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"

    #    return dict(sidebar_pages=g.sidebar_pages)

from flask import Blueprint
import flask
from cloudmesh.util.logger import LOGGER

log = LOGGER("module/menu")

menu_module = Blueprint('menu_module', __name__)


super_sidebar_pages = [
    ["Cloudmesh",
        [
            ["Home", "/"],
            ["Profile", "/profile/"],
            ["Keys", "/keys/"],
        ],
    ],
    ["Inventory",
        [
            ["Overview", "/inventory/"],
            ["Table", "/inventory/summary"],
            ["Images", "/inventory/images"]
        ],
    ],
    ["Provision",
        [
            ["Overview", "/provision/summary/"],
            ["Form", "/provision/"],
            ["Workflow", "/provision/workflow"],
        ],
    ],
    ["Clouds",
        [
            ["Refresh", "/cm/refresh"],
            ["VMs", "/mesh/servers"],
            ["Images", "/mesh/images"],
            ["Flavors", "/mesh/flavors/"],
            ["Users", "/mesh/users/"],
        ],
    ],
    ["HPC",
        [
            ["Queues", "/mesh/qstat"],
            ["Users", "/users/ldap"],
            ["Admin", "/hpc"]            
        ]
    ],
    
]


flask.Flask.app_ctx_globals_class.super_sidebar_pages = super_sidebar_pages

app_topbar = [
    ["Home", "/"],
    ["Profile", "/profile/"],
    ["About", "/about/"],
    ["Contact", "/contact/"],
]

app_externalbar = [
    ["FutureGrid", "https://portal.futuregrid.org"],
    ["-- Manual", "http://manual.futuregrid.org"],
    ["Cloudmesh", "https://github.com/cloudmesh/cloudmesh"],
    ["Blog", "http://cloudmesh.blogspot.com"],
]


topbar_pages = []
for page in app_topbar:
    topbar_pages.append({'name': page[0], 'url': page[1]})

# registering topbar into the global g
flask.Flask.app_ctx_globals_class.topbar_pages = topbar_pages


# log.info("{0}".format(str(flask.Flask.app_ctx_globals_class.topbar_pages)))

externalbar_pages = []
for page in app_externalbar:
    externalbar_pages.append({'name': page[0], 'url': page[1]})

# registering externalbar   into the global g
flask.Flask.app_ctx_globals_class.externalbar_pages = externalbar_pages


# log.info("{0}".format(str(flask.Flask.app_ctx_globals_class.externalbar_pages)))


#
# ACTIVATE STRUCTURE
#

#@menu_module.context_processor
# def inject_sidebar():

#    print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"

    #    return dict(sidebar_pages=g.sidebar_pages)

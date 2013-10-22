from flask import Blueprint
import flask
from cloudmesh.util.logger import LOGGER
from cloudmesh.util.util import banner
from pprint import pprint
import cloudmesh
log = LOGGER(__file__)

menu_module = Blueprint('menu_module', __name__)

super_duper_sidebar_pages = [
    ["Cloudmesh", None, None, ['all'],
        [
            ["Home", "/", None],
            ["Status", "/status", None],
            ["Profile", "/profile/", None],
        ],
    ],
    ["Clouds", "cm/refresh", "365_restart", ['all'],
        [
            ["Refresh", "/cm/refresh", None],
            ["VMs", "/mesh/servers", None],
            ["Images", "/mesh/images", None],
            ["Flavors", "/mesh/flavors/", None],
        ],
    ],
    ["HPC Queues", None, None, ['all'],
        [
            ["Jobs", "/mesh/qstat", None],
            ["Queueu Info", "/mesh/qinfo", None],
            ["Rack Diagram", "/inventory/rack", None],
        ]
    ],

    ["Admin", None, None, ['admin'],
        [
            ["Admin", "/admin", None],
            ["Users - LDAP", "/users/ldap", None],
            ["Users - Cloud", "/mesh/users/", None],
            ["Register - Cloud", "/mesh/register/clouds", None],
        ]
    ],
    ["Admin - Inventory", None, None, ['admin'],
        [
            ["Overview", "/inventory/", None],
            ["Table", "/inventory/summary", None],
            ["Images", "/inventory/images", None],
        ],
    ],
    ["Admin - Provision", None, None, ['admin', 'rain'],
        [
            ["Policy", "/provision/policy", None],
            ["Overview", "/provision/summary/", None],
            ["Form", "/provision/", None],
        ],
    ],
    ["Admin - Launcher", None, None, ['admin', 'rain'],
        [
            ["Launcher", "/cm/launch", None],
            ["Register", "/cm/register", None],
        ]
    ],
]


super_sidebar_pages = [
    ["Cloudmesh",
        [
            ["Home", "/"],
            ["Status", "/status"],
            ["Profile", "/profile/"],
        ],
    ],
    ["Clouds",
        [
            ["Refresh", "/cm/refresh"],
            ["VMs", "/mesh/servers"],
            ["Images", "/mesh/images"],
            ["Flavors", "/mesh/flavors/"],
        ],
    ],
    ["HPC Queues",
        [
            ["Jobs", "/mesh/qstat"],
            ["Queueu Info", "/mesh/qinfo"],
            ["Rack Diagram", "/inventory/rack"],
        ]
    ],

    ["Admin",
        [
            ["Admin", "/admin"],
            ["Users - LDAP", "/users/ldap"],
            ["Users - Cloud", "/mesh/users/"],
            ["Register - Cloud", "/mesh/register/clouds"],
        ]
    ],
    ["Admin - Inventory",
        [
            ["Overview", "/inventory/"],
            ["Table", "/inventory/summary"],
            ["Images", "/inventory/images"],
        ],
    ],
    ["Admin - Provision",
        [
            ["Policy", "/provision/policy"],
            ["Overview", "/provision/summary/"],
            ["Form", "/provision/"],
        ],
    ],
    ["Admin - Launcher",
        [
            ["Launcher", "/cm/launch"],
            ["Register", "/cm/register"]
        ]
    ],
]

flask.Flask.app_ctx_globals_class.super_sidebar_pages = super_sidebar_pages
flask.Flask.app_ctx_globals_class.super_duper_sidebar_pages = super_duper_sidebar_pages

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

# @menu_module.context_processor
# def inject_sidebar():

#    print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"

    #    return dict(sidebar_pages=g.sidebar_pages)

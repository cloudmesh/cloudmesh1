from flask import Blueprint
import flask
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.util import banner
from pprint import pprint
import cloudmesh
log = LOGGER(__file__)

menu_module = Blueprint('menu_module', __name__)

super_duper_sidebar_pages = [
    ["Cloudmesh", None, None, ['all'],
        [
            ['Home', "/", None],
            ["Status", "/status", None],
            ["Profile", "/profile/", None],
        ],
    ],
    ["Clouds", "/cm/refresh", "365_restart", ['all'],
        [
            ["VMs", "/mesh/servers", None],
            ["Images", "/mesh/images", None],
            ["Flavors", "/mesh/flavors/", None],
            ["Register", "/mesh/register/clouds", None],
        ],
    ],
    ["HPC Queues", "/mesh/refresh/qstat", "365_restart", ['all'],
        [
            ["Jobs", "/mesh/qstat", None],
            ["Queues Info", "/mesh/qinfo", None],
            ["Rack Diagram", "/inventory/rack", None],
        ]
    ],
    ["Baremetal", None, None, ['all'],
        [
            ["Request", "/baremetal/user/request", None],
            ["Provision", "/baremetal/user/provision", None],
        ],
    ],
    ["Admin", None, None, ['admin'],
        [
            ["Admin", "/admin", None],
            ["Users - LDAP", "/users/ldap", None],
            ["Users - Cloud", "/mesh/users/", None],
        ]
    ],
    ["Admin - Inventory", None, None, ['admin'],
        [
            ["Overview", "/inventory/", None],
            ["Table", "/inventory/summary", None],
        ],
    ],
    ["Admin - Provision", None, None, ['admin', 'rain'],
        [
            ["Policy", "/provision/policy", None],
            ["Overview", "/provision/summary/", None],
            ["Form", "/provision/", None],
            ["Users", "/provision/baremetal/users", None],
            ["Computers", "/provision/baremetal/computers", None],
        ],
    ],
    ["Admin - Cobbler", None, None, ['admin', 'rain'],
        [
            ["Distro", "/cobbler/distros", None],
            ["Profile", "/cobbler/profiles", None],
            ["System", "/cobbler/systems", None],
            ["Kickstart", "/cobbler/kickstarts", None],
        ],
    ],
    ["Admin - Launcher", None, None, ['admin', 'rain'],
        [
            ["Launcher", "/cm/launch", None],
            ["Register", "/cm/register", None],
        ]
    ],
]

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
    ["Cloudmesh", "http://cloudmesh.futuregrid.org"],
    ["-- Source", "https://github.com/cloudmesh/cloudmesh"],
    ["-- Bugs", "/bugs"],
    ["-- Git", "/git"],
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

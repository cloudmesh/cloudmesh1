from cloudmesh.config.cm_config import cm_config, cm_config_server
from flask import Blueprint, g, render_template, request, redirect, url_for
from flask.ext.login import login_required  # @UnresolvedImport
from flask.ext.wtf import Form  # @UnresolvedImport
from pprint import pprint
from sh import pwd  # @UnresolvedImport
from wtforms import SelectField
from flask.ext.principal import Permission, RoleNeed
import time
import json
import sys
import requests
from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)


cobbler_module = Blueprint('cobbler_module', __name__)

admin_permission = Permission(RoleNeed('admin'))

#
# ROUTE: cobbler
#
@cobbler_module.route('/cobbler/distros', methods=['GET'])
@login_required
def display_distros():
    result = request_rest_api("get", "/cm/v1/cobbler/distros/*")
    field_filter = [
                     ("name", "Name", "text", True),
                     ("arch", "Architecture", "text", True),
                     ("breed", "Breed", "text", True),
                     ("comment", "Comment", "text", False),
                     ("initrd", "Initrd", "text", True),
                     ("kernel", "Kernel", "text", True),
                     ("os_version", "OS Version", "text", True),
                     ("owners", "Owners", "list", True),
                    ]
    return render_template("mesh/cobbler/cobbler_distro.html", result=result, filter=field_filter)

@cobbler_module.route('/cobbler/profiles', methods=['GET'])
@login_required
def display_profiles():
    result = request_rest_api("get", "/cm/v1/cobbler/profiles/*")
    distros = request_rest_api("get", "/cm/v1/cobbler/distros")
    kickstarts = request_rest_api("get", "/cm/v1/cobbler/kickstarts")
    field_filter = [
                     ("name", "Name", "text", True),
                     ("distro", "Distribution", "select", False),
                     ("kickstart", "Kickstart", "select", False),
                     ("comment", "Comment", "text", False),
                     ("owners", "Owners", "list", True),
                    ]
    return render_template("mesh/cobbler/cobbler_profile.html", result=result, filter=field_filter, distros=distros, kickstarts=kickstarts)

def get_server_url():
    # ONLY for test
    # MUST changed to read info from yml file before commit
    return "http://gravel01.futuregrid.org:5000"

def request_rest_api(method, url, data=None):
    """
      method = [get, post, put, delete]
    """
    headers = {"content-type": "application/json", "accept": "application/json", }
    req_api = getattr(requests, method)
    req_url = get_server_url() + url
    if method == "get":
        r = req_api(req_url)
    else:
        if data:
            data["user_token"] = ""
        else:
            data = {"user_token": ""}
        r = req_api(req_url, data=json.dumps(data), headers=headers)
    return r.json()["cmrest"]["data"]

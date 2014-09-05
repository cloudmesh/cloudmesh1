from cloudmesh.config.cm_config import cm_config_server
from flask import Blueprint, render_template, get_template_attribute, request, Response
from flask.ext.login import login_required  # @UnresolvedImport
from cloudmesh.provisioner.baremetal_db import BaremetalDB
from flask.ext.principal import Permission, RoleNeed
import json
import requests
from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)


cobbler_module = Blueprint('cobbler_module', __name__)

admin_permission = Permission(RoleNeed('admin'))

cobbler_default_data = {
    "distros": {},
    "profiles": {},
    "systems": {},
    "kickstarts": {},
}

cobbler_default_data["distros"] = {
    "flag_collection": False,
    "get": "/cm/v1/cobbler/distros/*",
    "field_filter": {
        "normal": [
            ("name", "Name", "text", True),
            ("arch", "Architecture", "text", True),
            ("breed", "Breed", "text", True),
            # ("comment", "Comment", "text", False),
            ("initrd", "Initrd", "text", True),
            ("kernel", "Kernel", "text", True),
            ("os_version", "OS Version", "text", True),
            # ("owners", "Owners", "list", True),
        ],
        "add": [
            ("name", "Name", "text", False),
            ("url", "URL", "text", False),
        ],
    },
    "select_data": {
    },
    "process_vars": {
        "update": [],
        "add": ["name", "url", ],
    },
    "button": {
        "normal": [
            ("reset", 1),
            ("delete", 2),
        ],
        "add": [
            ("add", 3),
        ],
    },
}

cobbler_default_data["profiles"] = {
    "flag_collection": False,
    "get": "/cm/v1/cobbler/profiles/*",
    "field_filter": {
        "normal": [
            ("name", "Name", "text", True),
            ("distro", "Distribution", "select", False),
            ("kickstart", "Kickstart", "select", False),
            # ("comment", "Comment", "text", False),
            # ("owners", "Owners", "list", True),
        ],
        "add": [
            ("name", "Name", "text", False),
            ("distro", "Distribution", "select", False),
            ("kickstart", "Kickstart", "select", False),
        ],
    },
    "select_data": {
        "kickstart": "/cm/v1/cobbler/kickstarts",
        "distro": "/cm/v1/cobbler/distros",
    },
    "process_vars": {
        "update": ["kickstart", ],
        "add": ["name", "distro", "kickstart", ],
    },
    "button": {
        "normal": [
            ("reset", 1),
            ("update", 1),
            ("delete", 1),
        ],
        "add": [
            ("add", 3),
        ],
    },
}

cobbler_default_data["systems"] = {
    "flag_collection": True,
    "get": "/cm/v1/cobbler/systems/*",
    "field_filter": {
        "normal": [
            ("name", "Name", "text", True),
            ("profile", "Profile", "select", False),
            ("power_address", "Power Address", "text", False),
            ("power_type", "Power Type", "text", False),
            ("power_user", "Power User", "text", False),
            ("power_pass", "Power Password", "text", False),
            ("power_id", "Power ID", "text", False),
            # ("comment", "Comment", "text", False),
            # ("owners", "Owners", "list", True),
        ],
        "collection": {
            "normal": [("interfaces", "Interface")],
            "add": [("interfaces", "Interface")],
        },
        "interfaces": [
            ("name", "Name", "text", False),
            ("ip_address", "IP Address", "text", False),
            ("netmask", "Subnet Mask", "text", False),
            ("if_gateway", "Interface Gateway", "text", False),
            ("mac_address", "MAC Address", "text", False),
            ("management", "Management", "boolean", False),
        ],
        "add": [
            ("name", "Name", "text", False),
            ("profile", "Profile", "select", False),
            ("power_address", "Power Address", "text", False),
            ("power_type", "Power Type", "text", False),
            ("power_user", "Power User", "text", False),
            ("power_pass", "Power Password", "text", False),
            ("power_id", "Power ID", "text", False),
        ],
    },
    "select_data": {
        "profile": "/cm/v1/cobbler/profiles",
    },
    "process_vars": {
        "update": ["profile", "power_address", "power_type", "power_user", "power_pass", "power_id", ],
        "add": ["name", "profile", "power_address", "power_type", "power_user", "power_pass", "power_id", ],
    },
    "button": {
        "normal": [
            ("reset", 1),
            ("update", 1),
            ("delete", 1),
        ],
        "add": [
            ("add", 3),
        ],
    },
}

cobbler_default_data["kickstarts"] = {
    "flag_collection": False,
    "get": "/cm/v1/cobbler/kickstarts/*",
    "field_filter": {
        "normal": [
            ("contents", "Content", "textarea", False),
        ],
        "add": [
            ("name", "Name", "text", False),
            ("contents", "Content", "textarea", False),
        ],
    },
    "select_data": {
    },
    "process_vars": {
        "update": ["contents"],
        "add": ["name", "contents", ],
    },
    "button": {
        "normal": [
            ("reset", 1),
            ("update", 1),
            ("delete", 1),
        ],
        "add": [
            ("add", 3),
        ],
    },
}


@cobbler_module.route('/cobbler/<objects>', methods=['GET'])
@login_required
def display_cobbler(objects):
    predefined = cobbler_default_data[objects]
    result = request_rest_api("get", predefined["get"])
    result["data"].sort(key=lambda x: x["data"]["name"])
    append_select_data(objects, result)
    add_data = get_add_data_dict(objects, result)
    js_vars = {}
    for k in predefined["process_vars"]:
        js_vars[k] = ["'" + v + "'" for v in predefined["process_vars"][k]]
    return render_template("mesh/cobbler/cobbler_main.html",
                           object_type=objects,
                           result=result,
                           js_vars=js_vars,
                           filter=predefined["field_filter"]["normal"],
                           buttons=predefined["button"]["normal"],
                           add_data=add_data,
                           flag_collection=predefined["flag_collection"],
                           filter_collection=predefined["field_filter"],
                           )


@cobbler_module.route('/cobbler/<objects>/<item_name>', methods=['GET', 'PUT', 'POST', 'DELETE'])
@login_required
def process_cobbler_object(objects, item_name):
    if objects not in ["distros", "profiles", "systems", "kickstarts"]:
        return
    predefined = cobbler_default_data[objects]
    url_prefix = "/cm/v1/cobbler"
    url = "{0}/{1}/{2}".format(url_prefix, objects, item_name)
    method = request.method.lower()
    template = ""
    if method == "get":
        result = request_rest_api(method, url)
    else:
        result = request_rest_api(method, url, request.json)
        if result["result"] and method == "post":
            result = request_rest_api("get", url)
    if result["result"] and method in ["get", "post"]:
        append_select_data(objects, result)
        if predefined["flag_collection"]:
            accordion_panel = get_template_attribute(
                "mesh/cobbler/cobbler_macro.html", "CM_ACCORDION_PANEL_COLLECTION")
            result["template"] = accordion_panel(objects, result["data"][0]["data"], predefined[
                                                 "field_filter"]["normal"], predefined["button"]["normal"], predefined["field_filter"])
        else:
            accordion_panel = get_template_attribute(
                "mesh/cobbler/cobbler_macro.html", "CM_ACCORDION_PANEL")
            result["template"] = accordion_panel(objects, result["data"][0][
                                                 "data"], predefined["field_filter"]["normal"], predefined["button"]["normal"])
        if method == "post":
            if predefined["flag_collection"]:
                accordion_panel_add = get_template_attribute(
                    "mesh/cobbler/cobbler_macro.html", "CM_ACCORDION_PANEL_COLLECTION")
                add_data = get_add_data_dict(objects, result)
                add_template = accordion_panel_add(objects, add_data["data"], add_data[
                                                   "filter"], add_data["button"], predefined["field_filter"], True)
            else:
                accordion_panel_add = get_template_attribute(
                    "mesh/cobbler/cobbler_macro.html", "CM_ACCORDION_PANEL")
                add_data = get_add_data_dict(objects, result)
                add_template = accordion_panel_add(
                    objects, add_data["data"], add_data["filter"], add_data["button"], True)
            result["template"] += add_template
    return Response(json.dumps(result), status=200, mimetype="application/json")


@cobbler_module.route('/cobbler/<objects>/<item_name>/<if_name>', methods=['PUT', 'POST', 'DELETE'])
@login_required
def process_cobbler_object_collection(objects, item_name, if_name):
    if objects not in ["systems", ]:
        return
    predefined = cobbler_default_data[objects]
    url_prefix = "/cm/v1/cobbler"
    url = "{0}/{1}/{2}".format(url_prefix, objects, item_name)
    method = request.method.lower()
    if method in ["put", "post"]:
        system_data = {"name": item_name,
                       "interfaces": [request.json],
                       }
        result = request_rest_api("put", url, system_data)
    elif method in ["delete"]:
        url = "{0}/{1}".format(url, if_name)
        result = request_rest_api(method, url, request.json)
    return Response(json.dumps(result), status=200, mimetype="application/json")


def get_all_baremetal_request_users():
    """
      ONLY for test
    """
    return ["test"]


@cobbler_module.route('/provision/baremetal/users', methods=['GET', 'PUT'])
@login_required
def provision_baremetal_allocation():
    bmdb = BaremetalDB()
    method = request.method.lower()
    if method in ['get']:
        request_users = get_all_baremetal_request_users()
        baremetal_computers = bmdb.get_baremetal_computers()
        print "baremetal computers: ", baremetal_computers
        return render_template("mesh/provision/provision_main.html",
                               users=request_users,
                               computers=baremetal_computers["idle"],
                               flag_idle=True,
                               )
    elif method in ['put']:
        data = request.json
        result = bmdb.assign_baremetal_to_user(data["computers"], data["user"])
        return Response(json.dumps({"result": result}), status=200, mimetype="application/json")


@cobbler_module.route('/provision/baremetal/computers', methods=['GET', 'PUT'])
@login_required
def provision_baremetal_withdraw():
    bmdb = BaremetalDB()
    method = request.method.lower()
    if method in ['get']:
        get_result = bmdb.get_baremetal_computers()
        baremetal_computers = get_result["used"]
        bm_computer_info = {}
        for cluster in baremetal_computers:
            bm_computer_info[cluster] = {}
            for bm_comp in baremetal_computers[cluster]:
                bm_computer_info[cluster][
                    bm_comp] = bmdb.get_baremetal_computer_detail(bm_comp)
        return render_template("mesh/provision/provision_main.html",
                               computers=baremetal_computers,
                               computer_info=bm_computer_info,
                               flag_idle=False,
                               )
    elif method in ['put']:
        data = request.json
        result = bmdb.withdraw_baremetal_from_user(data["computers"])
        return Response(json.dumps({"result": result}), status=200, mimetype="application/json")


@cobbler_module.route('/baremetal/user/request', methods=['GET', 'PUT'])
@login_required
def baremetal_user_requests():
    bmdb = BaremetalDB()
    method = request.method.lower()
    if method in ['get']:
        get_result = bmdb.get_baremetal_computers()
        baremetal_computers = get_result["used"]
        bm_computer_info = {}
        for cluster in baremetal_computers:
            bm_computer_info[cluster] = {}
            for bm_comp in baremetal_computers[cluster]:
                bm_computer_info[cluster][
                    bm_comp] = bmdb.get_baremetal_computer_detail(bm_comp)
        return render_template("mesh/provision/provision_main.html",
                               computers=baremetal_computers,
                               computer_info=bm_computer_info,
                               flag_idle=False,
                               )
    elif method in ['put']:
        data = request.json
        result = bmdb.withdraw_baremetal_from_user(data["computers"])
        return Response(json.dumps({"result": result}), status=200, mimetype="application/json")


def append_select_data(objects, data):
    predefined = cobbler_default_data[objects]
    select_data = {}
    for s in predefined["select_data"]:
        s_result = request_rest_api("get", predefined["select_data"][s])
        select_data[s] = s_result["data"]
    for one_data in data["data"]:
        one_data["data"]["select"] = select_data


def get_add_data_dict(objects, data):
    predefined = cobbler_default_data[objects]
    add_data = {"data": {}}
    for f in predefined["process_vars"]["add"]:
        add_data["data"][f] = ""
    add_data["data"]["select"] = data["data"][0]["data"]["select"]
    add_data["filter"] = predefined["field_filter"]["add"]
    add_data["button"] = predefined["button"]["add"]
    add_data["data"]["name"] = "add_{0}".format(objects)
    if "collection" in predefined["field_filter"]:
        for (name, value) in predefined["field_filter"]["collection"]["add"]:
            add_data["data"][name] = {}
            for field_coll in predefined["field_filter"][name]:
                add_data["data"][name][field_coll[0]] = ""
    return add_data


def get_server_url():
    # ONLY for test
    # MUST changed to read info from yml file before commit
    server_config = cm_config_server()
    prot = server_config.get("cloudmesh.server.cobbler.prot")
    host = server_config.get("cloudmesh.server.cobbler.host")
    port = server_config.get("cloudmesh.server.cobbler.port")
    return "{0}://{1}:{2}".format(prot, host, port)


def request_rest_api(method, url, data=None):
    """
      method = [get, post, put, delete]
    """
    headers = {"content-type": "application/json",
               "accept": "application/json", }
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
        print r.json()
    return r.json()["cmrest"]["data"]

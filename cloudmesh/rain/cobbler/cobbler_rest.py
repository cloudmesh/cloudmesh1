from flask import Flask, request, Response
import json
from functools import wraps
from cobbler_provision import CobblerProvision

app = Flask(__name__)

SUPPORTED_OBJECTS = "distros profiles systems kickstarts".split()
KICKSTART_LOCATION = "/var/lib/cobbler/kickstarts"

"""
   NOT consider user authentication and authorization.
"""


def format_result_data(flag_success, msg="", data=None):
    return {
        "result": flag_success,
        "description": msg,
        "data": data,
    }


def not_supported_objects(object_type):
    """
      cobbler supports a lot of objects. However, this cobbler REST API only support part of them.
      The supported object defined in SUPPORTED_OBJECTS. 
    """

    return format_result_data(False, "Object {0} dose NOT supported in currently REST API.".format(object_type))


def response_json(func):
    @wraps(func)
    def wrap_response_json(*args, **kwargs):
        result = {"cmrest": {
            "operation": "cobbler",
            "data": func(*args, **kwargs),
        }
        }
        return Response(json.dumps(result), status=200, mimetype="application/json")
    return wrap_response_json


@app.route('/cm/v1/cobbler/<objects>', methods=['GET'])
@response_json
def list_objects(objects):
    """
      returns the names of all possible 'objects', objects defined in SUPPORTED_OBJECTS or "isos" means distribution iso file
      e.g. http://host:port/cm/v1/cobbler/distros
    """
    if objects not in SUPPORTED_OBJECTS and objects not in ["isos"]:
        return not_supported_objects(objects)
    # MUST know how to get user token, empty token ONLY for debug
    kwargs = {"user_token": ""}
    item = objects[:-1]  # value of objects does NOT contain the last 's'
    cp = CobblerProvision()
    func = getattr(cp, "list_{0}_names".format(item))
    return func(**kwargs)


@app.route('/cm/v1/cobbler/<objects>/<name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@response_json
def process_objects(objects, name):
    """
      returns the report of a specific name in 'objects', objects defined in SUPPORTED_OBJECTS
      e.g. http://host:port/cm/v1/cobbler/distros/test-x86_64
    """
    if objects not in SUPPORTED_OBJECTS:
        return not_supported_objects(objects)
    item = objects[:-1]  # value of objects does NOT contain the last 's'
    cp = CobblerProvision()
    method = request.method
    if method == "GET":
        # MUST know how to get user token, empty token ONLY for debug
        kwargs = {"user_token": ""}
        func = getattr(cp, "get_{0}_report".format(item))
        return func(name, **kwargs)

    data = request.json
    if method == "POST":
        if item == "distro":
            return cp.import_distro(name, **data)
        if item == "profile":
            kickstart_file = data.get("kickstart", None)
            if kickstart_file:
                if not kickstart_file.startswith("/"):
                    data[
                        "kickstart"] = "{0}/{1}".format(KICKSTART_LOCATION, kickstart_file)
            return cp.add_profile(name, **data)
        if item == "system":
            return cp.add_system(name, **data)
        if item == "kickstart":
            lines = data.get("contents", [])
            return cp.update_kickstart(name, lines, **data)
    if method == "PUT":
        if item == "distro":
            return cp.update_distro(name, **data)
        if item == "profile":
            kickstart_file = data.get("kickstart", None)
            if kickstart_file:
                if not kickstart_file.startswith("/"):
                    data[
                        "kickstart"] = "{0}/{1}".format(KICKSTART_LOCATION, kickstart_file)
            return cp.update_profile(name, **data)
        if item == "system":
            return cp.update_system(name, **data)
        if item == "kickstart":
            lines = data.get("contents", [])
            return cp.update_kickstart(name, lines, **data)
    if method == "DELETE":
        func = getattr(cp, "remove_{0}".format(item))
        return func(name, **data)


@app.route('/cm/v1/cobbler/systems/<system_name>/<if_name>', methods=['DELETE'])
@response_json
def process_system_interfaces(system_name, if_name):
    cp = CobblerProvision()
    data = request.json
    func = getattr(cp, "remove_{0}".format("system_interface"))
    return func(system_name, if_name, **data)


@app.route('/cm/v1/cobbler/baremetal/<system>', methods=['GET', 'POST', 'PUT'])
@response_json
def baremetal_system(system):
    cp = CobblerProvision()
    # monitor system
    if request.method == "GET":
        # MUST know how to get user token, empty token ONLY for debug
        kwargs = {"user_token": ""}
        return cp.monitor_system(system, **kwargs)
    data = request.json
    # deploy system
    if request.method == "POST":
        return cp.deploy_system(system, **data)
    # power system
    if request.method == "PUT":
        return cp.power_system(system, **data)


@app.route('/cm/v1/cobbler/<objects>/<name>/child', methods=['GET'])
@response_json
def list_child_objects(objects, name):
    """
      returns the child list of a specific name in 'objects', objects defined in SUPPORTED_OBJECTS
      e.g. http://host:port/cm/v1/cobbler/distros/test-x86_64/child
    """
    if objects not in SUPPORTED_OBJECTS:
        return not_supported_objects(objects)
    item = objects[:-1]  # value of objects does NOT contain the last 's'
    cp = CobblerProvision()
    method = request.method
    if method == "GET":
        # MUST know how to get user token, empty token ONLY for debug
        kwargs = {"user_token": ""}
        func = getattr(cp, "get_object_child_list")
        return func(item, name)
    return None


@app.route('/cm/v1/cobbler/kickstarts/<name>/profile', methods=['GET'])
@response_json
def list_kickstart_profiles(name):
    """
      returns the list of profile name matching the name of kickstart file
      e.g. http://host:port/cm/v1/cobbler/kickstarts/default.ks/profile
    """
    cp = CobblerProvision()
    method = request.method
    if method == "GET":
        # MUST know how to get user token, empty token ONLY for debug
        kwargs = {"user_token": ""}
        func = getattr(cp, "get_profile_match_kickstart")
        return func(name)
    return None

if __name__ == '__main__':
    print "start"
    app.run(host="0.0.0.0", debug=True)

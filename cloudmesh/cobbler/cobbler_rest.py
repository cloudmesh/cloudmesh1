#!/usr/bin/env python

from flask import Flask, jsonify

from cobbler_provision import CobblerProvision

app = Flask(__name__)



@app.route('/cm/v1.0/cobbler/token', methods = ['GET'])
def get_token():
    """returns the token of user if user/password authentication is correct."""
    user = request.args.get("user", "")
    password = request.args.get("password", "")
    if not user or not password:
        return format_result_data("token", "token", None, "Please provide a valid pair of user and password.")
    cp = CobblerProvision()
    token = cp.get_token(user, password)
    msg = "User authenticated {0}successfully.".format("" if token else "un")
    return format_result_data("token", "token", token, msg)

@app.route('/cm/v1.0/cobbler/list/<item>', methods = ['GET'])
def list_names(item):
    """returns the names of all possible 'item', item in [distro, profile, system, and etc.]"""
    items = "distro profile system".split()
    if item not in items:
        return format_not_support_operation("list", item)
    token = request.args.get("token", "")
    cp = CobblerProvision()
    func_item = getattr(cp, "list_{0}_names".format(item))
    result = func_item(token)
    msg = "success" if result else "Failed to authentication user token."
    return format_result_data("list", item, result, msg)

@app.route('/cm/v1.0/cobbler/report/<item>/<name>', methods = ['GET'])
def report_item(item, name):
    """returns the report of a specific name in item, item is in [distro, profile, system, and etc.]"""
    items = "distro profile system".split()
    if item not in items:
        return format_not_support_operation("report", item)
    token = request.args.get("token", "")
    cp = CobblerProvision()
    func_item = getattr(cp, "get_{0}_report".format(item))
    result = func_item(token)
    msg = "success" if result else "Failed to authentication user token."
    return format_result_data("report", item, result, msg)

@app.route('/cm/v1.0/cobbler/add/<item>', methods = ['GET'])
def add_item(item):
    """add a specific name in item, item is in [distro, profile, system, and etc.]"""
    items = "distro profile system".split()
    if item not in items:
        return format_not_support_operation("add", item)
    token = request.args.get("token", "")
    cp = CobblerProvision()
    if item == "distro":
        url = request.args.get("url", "")
        name = request.args.get("name", "")
        (result, msg) = cp.import_distro(token, url, name)
    elif item == "profile":
        profile = request.args.get("profile", "")
        distro = request.args.get("distro", "")
        kickstart = request.args.get("kickstart", "")
        (result, msg) = cp.add_profile(token, profile, distro, kickstart)
    elif item == "system":
        system = request.args.get("system", "")
        profile = request.args.get("profile", "")
        contents = request.args.get("contents", "")
        (result, msg) = cp.add_system(token, system, profile, contents)
    return format_result_data("add", item, result, msg)

@app.route('/cm/v1.0/cobbler/update/<item>', methods = ['GET'])
def update_item(item):
    """update a specific name in item, item is in [profile, system, and etc.]"""
    items = "profile system".split()
    if item not in items:
        return format_not_support_operation("update", item)
    token = request.args.get("token", "")
    cp = CobblerProvision()
    if item == "profile":
        profile = request.args.get("profile", "")
        kickstart = request.args.get("kickstart", "")
        (result, msg) = cp.update_profile(token, profile, kickstart)
    elif item == "system":
        system = request.args.get("system", "")
        contents = request.args.get("contents", "")
        (result, msg) = cp.update_system(token, system, contents)
    return format_result_data("update", item, result, msg)

@app.route('/cm/v1.0/cobbler/remove/<item>', methods = ['GET'])
def remove_item(item):
    """remove a specific name in item, item is in [distro, profile, system, and etc.]"""
    items = "distro profile system".split()
    if item not in items:
        return format_not_support_operation("remove", item)
    token = request.args.get("token", "")
    cp = CobblerProvision()
    name = request.args.get("name", "")
    func_item = getattr(cp, "remove_{0}".format(item))
    (result, msg) = func_item(token, name)
    return format_result_data("remove", item, result, msg)

@app.route('/cm/v1.0/cobbler/deploy/<system>', methods = ['GET'])
def deploy_item(system):
    """deploy a specific system, """
    token = request.args.get("token", "")
    cp = CobblerProvision()
    (result, msg) = cp.deploy_system(system)
    return format_result_data("deploy", system, result, msg)

@app.route('/cm/v1.0/cobbler/power/<system>', methods = ['GET'])
def power_item(system):
    """power on/off a specific system, """
    token = request.args.get("token", "")
    cp = CobblerProvision()
    onoff = request.args.get("onoff", "off")
    flag = True if onoff == "on" else False
    (result, msg) = cp.power_system(system, flag)
    return format_result_data("power", system, result, msg)

def format_not_support_operation(type, item):
    return format_result_data(type, item, None, "Operation {0} does NOT support {1}".format(type, item))

def format_result_data(type, item, data, msg):
    result_dict = {
                     "type": type,
                     "item": item,
                     "data": data,
                     "msg": msg,
                   }
    return jsonify({"cobbler": result_dict, })
    


if __name__ == '__main__':
    print "start"
    app.run(debug = True)
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
def report_names(item, name):
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
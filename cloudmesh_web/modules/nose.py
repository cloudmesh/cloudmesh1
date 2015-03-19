from ast import literal_eval
from cloudmesh_base.logger import LOGGER
from cloudmesh.util.ping import ping
from cloudmesh_common.util import cond_decorator
from datetime import datetime
from flask import Blueprint, render_template, redirect
from flask.ext.login import login_required
from flask.ext.principal import Permission, RoleNeed
from sh import nosetests, pwd

log = LOGGER(__file__)

nose_module = Blueprint('nose_module', __name__)

#
# ROUTE: PROFILE
#


admin_permission = Permission(RoleNeed('admin'))


@nose_module.route('/test/ping')
@login_required
@admin_permission.require(http_exception=403)
def display_pingtest():

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    hosts = ['india.futuregrid.org']
    results = []
    for host in hosts:
        results.append(ping(host))

    return render_template('admin/ping.html',
                           updated=time_now,
                           hosts=hosts,
                           results=results)


@nose_module.route('/test/nose')
@nose_module.route('/test/nose/')
@nose_module.route('/test/nose/<test>')
@login_required
@admin_permission.require(http_exception=403)
def display_nosetest(test=None):

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if test is None:
        filename = "/tmp/nosetests_all.json"
    else:
        testname = "../tests/test_{0}.py".format(test)
        filename = "/tmp/nosetests_{0}.json".format(test)
    try:
        with open(filename, "r") as myfile:
            tests = literal_eval(myfile.read())
    except:
        tests = {'name': 'please run test'}

    return render_template('admin/nosetest.html',
                           updated=time_now,
                           tests=tests,
                           filename=filename,
                           name=test)


@nose_module.route('/test/run')
@nose_module.route('/test/run/<test>')
@login_required
@admin_permission.require(http_exception=403)
def run_nosetest(test=None):

    if test is None:
        filename = "/tmp/nosetests_all.json"
        testname = ""
    else:
        filename = "/tmp/nosetests_{0}.json".format(test)
        testname = "../tests/test_{0}.py".format(test)

    print "PWD", pwd()
    try:
        result = nosetests("--with-json", "-w", "../tests",
                           "--json-file='{0}' {1}".format(filename, testname))
    except:
        pass
    print "RRRR", result
    return redirect("/test/nose")

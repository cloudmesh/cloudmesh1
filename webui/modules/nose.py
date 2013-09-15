import cloudmesh
from datetime import datetime
from flask import Blueprint
from flask import render_template, redirect
from cloudmesh.config.cm_config import cm_config
from cloudmesh.pbs.pbs import PBS
from cloudmesh.util.util import cond_decorator
from ast import literal_eval
from sh import pwd
from cloudmesh.util.ping import ping
from flask.ext.login import login_required

nose_module = Blueprint('nose_module', __name__)

#
# ROUTE: PROFILE
#

from sh import nosetests


@nose_module.route('/test/ping')
@cond_decorator(cloudmesh.with_login, login_required)
def display_pingtest():

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    hosts = ['alamo.futuregrid.org',
             'india.futuregrid.org',
             'sierra.futuregrid.org',
             'hotel.futuregrid.org',
             'bravo.futuregrid.org',
             'echo.futuregrid.org']
    results = []
    for host in hosts:
        results.append(ping(host))

    return render_template('ping.html',
                           updated=time_now,
                           hosts=hosts,
                           results=results)


@nose_module.route('/test/nose')
@nose_module.route('/test/nose/')
@nose_module.route('/test/nose/<test>')
@cond_decorator(cloudmesh.with_login, login_required)
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

    return render_template('nosetest.html',
                           updated=time_now,
                           tests=tests,
                           filename=filename,
                           name=test)

@nose_module.route('/test/run')
@nose_module.route('/test/run/<test>')
@cond_decorator(cloudmesh.with_login, login_required)
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


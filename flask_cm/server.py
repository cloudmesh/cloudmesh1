import sys
sys.path.insert(0, './')
sys.path.insert(0, '../')

import os
import time
from flask import Flask, render_template, request
from flask_flatpages import FlatPages

from cloudmesh.cloudmesh import cloudmesh
from datetime import datetime
from cloudmesh.cm_config import cm_config
from datetime import datetime
import yaml


DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

"""
import pkg_resources
version = pkg_resources.get_distribution("flask_cm").version
"""
version = "0.7.2"


clouds = cloudmesh()
clouds.refresh()


# clouds.load()
# AttributeError: cloudmesh instance has no attribute 'refresh'
# clouds.refresh()
# TEST CASE

######################################################################
# STARTING THE FLASK APP
######################################################################
app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)

######################################################################
# ACTIVATE STRUCTURE
######################################################################


def make_active(name):
    active = {'home': "",
              'table': "",
              'contact': "",
              'metric': "",
              'profile': ""}
    active[name] = 'active'
    return active

######################################################################
# ROUTE: /
######################################################################


@app.route('/')
def index():
    active = make_active('home')
    return render_template('index.html',
                           pages=pages,
                           active=active,
                           version=version)

######################################################################
# ROUTE: REFRESH
######################################################################


@app.route('/cm/refresh/')
@app.route('/cm/refresh/<cloud>/')
def refresh(cloud=None, server=None):
    print "-> refresh", cloud, server
    global clouds
    clouds.refresh()
    return table()

######################################################################
# ROUTE: KILL
######################################################################


@app.route('/cm/kill/')
def kill_vms():
    print "-> kill all"
    r = cm("--set", "quiet", "kill", _tty_in=True)
    return table()

######################################################################
# ROUTE: DELETE
######################################################################


@app.route('/cm/delete/<cloud>/<server>/')
def delete_vm(cloud=None, server=None):
    print "-> delete", cloud, server
    # if (cloud == 'india'):
    #  r = cm("--set", "quiet", "delete:1", _tty_in=True)
    clouds.delete(cloud, server)
    time.sleep(5)
    global clouds
    clouds.refresh()
    return table()

######################################################################
# ROUTE: START
######################################################################


@app.route('/cm/start/<cloud>/')
def start_vm(cloud=None, server=None):
    print "*********** STARTVM", cloud
    print "-> start", cloud, server
    # if (cloud == 'india'):
    #  r = cm("--set", "quiet", "start:1", _tty_in=True)
    clouds.create(cloud, "gvonlasz", "001", "dummy")
    return table()

'''
#gregorss test
@app.route('/cm/metric/<startdate>/<enddate>/<host>')
def list_metric(cloud=None, server=None):
    print "-> generate metric", startdate, endadte
    #r = fg-metric(startdate, enddate, host, _tty_in=True)
    return render_template('metric1.html',
                           startdate=startdate,
                           active=active,
                           version=version,
                           endate=enddate)
    #return table()
'''

######################################################################
# ROUTE: SAVE
######################################################################


@app.route('/save/')
def save():
    print "Saving the cloud status"
    global clouds
    clouds.save()
    return table()

######################################################################
# ROUTE: LOAD
######################################################################


@app.route('/load/')
def load():
    print "Loading the cloud status"
    global clouds
    clouds.load()
    return table()

######################################################################
# ROUTE: TABLE
######################################################################


@app.route('/table/')
def table():
    global clouds

    active = make_active('table')
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # clouds.refresh("sierra-openstack")

    # note thet call to sierra is fake it just goes to india and sets cloudname to sierra.
    # clouds.dump()
    # keys = clouds.get_keys()
    return render_template('table.html',
                           updated=time_now,
                           keys="",  # ",".join(clouds.get_keys()),
                           clouds=clouds.clouds,
                           image='myimage',
                           pages=pages,
                           active=active,
                           version=version)


######################################################################
# ROUTE: PROFILE
######################################################################
@app.route('/profile/')
def profile():
    global clouds
    config = cm_config()
    dict_t = config.get()
    makeCloudDict(dict_t)
    active = make_active('profile')
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    persolalinfo = {'name': 'abc', 'data1': 'pqr'}

    cloudinfo = {
        'openstak-india': {'type': 'openstack', 'host': 'india.futuregrid.org',
                           'username': 'shweta'}}

    return render_template('profile.html',
                           updated=time_now,
                           keys="",  # ",".join(clouds.get_keys()),
                           cloudinfo=makeCloudDict(dict_t),
                           persolalinfo=persolalinfo,
                           active=active,
                           version=version)


def makeCloudDict(dict_t):
    cloudDict = {}
    cloudSubDict = {}
    cloudSubsubDict = {}
    for key, value in dict_t.iteritems():
        if "india-openstack" in key:

            for innerKey, innerValue in value.iteritems():
                innerKey = innerKey.replace("OS_", "")
                innerKey = innerKey.replace("cm_", "")
                cloudSubDict[innerKey.upper()] = innerValue
            cloudDict[key.upper()] = cloudSubDict
            cloudSubDict = {}
            print (cloudDict)
        if "india-eucalyptus" in key:
            for innerKey, innerValue in value.iteritems():
                if "fg" in innerKey:
                    for innermostKey, innermostValue in innerValue.iteritems():
                        innermostKey = innermostKey.replace("EC2_", "")
                        cloudSubsubDict[innermostKey.upper()] = innermostValue
                    cloudDict[innerKey.upper()] = cloudSubsubDict
                    cloudSubsubDict = {}
                else:
                    innerKey = innerKey.replace("EC2_", "")
                    cloudSubDict[innerKey.upper()] = innerValue
            cloudDict[key.upper()] = cloudSubDict
            cloudSubDict = {}

        if "azure" in key:
            cloudSubDict = {}
            for innerKey, innerValue in value.iteritems():
                cloudSubDict[innerKey.upper()] = innerValue
            cloudDict[key.upper()] = cloudSubDict
            cloudSubDict = {}
    # print (cloudDict);

    return cloudDict

######################################################################
# ROUTE: METRIC
######################################################################
#@app.route('/metric/<s_date>/<e_date>/<user>/<cloud>/<host>/<period>/<metric>')


@app.route('/metric/main', methods=['POST', 'GET'])
def metric():
    global clouds
    args = {"s_date": request.args.get('s_date', ''),
            "e_date": request.args.get('e_date', ''),
            "user": request.args.get('user', ''),
            "cloud": request.args.get('cloud', ''),
            "host": request.args.get('host', ''),
            "period": request.args.get('period', ''),
            "metric": request.args.get('metric', '')}

    return render_template('metric.html',
                           clouds=clouds.get(),
                           metrics=clouds.get_metrics(args),
                           pages=pages,
                           active=make_active('metric'),
                           version=version)

######################################################################
# ROUTE: PAGES
######################################################################


@app.route('/<path:path>/')
def page(path):
    active = make_active(str(path))
    page = pages.get_or_404(path)
    return render_template('page.html',
                           page=page,
                           pages=pages,
                           active=active,
                           version=version)


if __name__ == "__main__":
    app.run()

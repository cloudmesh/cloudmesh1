from datetime import datetime
from flask import Blueprint
from flask import Flask, render_template, request, redirect
from cloudmesh.config.cm_keys import cm_keys

from cloudmesh.config.cm_projects import cm_projects
from cloudmesh.config.cm_config import cm_config
from cloudmesh.pbs.pbs import PBS

nose_module = Blueprint('nose_module', __name__)
from pprint import pprint
from ast import literal_eval
from sh import pwd

#
# ROUTE: PROFILE
#

from sh import nosetests


@nose_module.route('/nose/<test>')
def display_nosetest(test):

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    filename = "/tmp/nosetest.json"
    
    testname = "../tests/test_{0}.py".format(test)
    result = nosetests("--with-json", 
                       "--json-file='{0}' {1}".format(filename, testname))
    
    with open (filename, "r") as myfile:
        data=literal_eval(myfile.read())
        
    return render_template('nosetest.html',
			               updated = time_now,
                           tests=data,
                           filename=testname,
                           resultname=filename,
                           name=test)
                           
@nose_module.route('/pbsnodes/<host>')
def display_pbs_nodes(host):

    config = cm_config()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    user = config.data["cloudmesh"]["hpc"]["username"]
    
    pbs = PBS(user, host)
    data = pbs.pbsnodes()
    
    return render_template('pbsnodes.html',
			   updated = time_now,
                           host=host,
                           data=data)

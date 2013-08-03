from datetime import datetime
from flask import Blueprint
from flask import Flask, render_template, request, redirect
from cloudmesh.config.cm_keys import cm_keys

from cloudmesh.config.cm_projects import cm_projects
from cloudmesh.config.cm_config import cm_config
from cloudmesh.pbs.pbs import PBS

pbs_module = Blueprint('pbs_module', __name__)
from pprint import pprint

#
# ROUTE: PROFILE
#


@pbs_module.route('/pbs/<host>')
def display_pbs_qstat(host):

    config = cm_config()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    user = config.data["cloudmesh"]["hpc"]["username"]
    
    pbs = PBS(user, host)
    pbs.qstat()
    
    return render_template('qstat.html',
			   updated = time_now,
                           host=host,
                           qstat=pbs.pbs_qstat)

@pbs_module.route('/pbsnodes/<host>')
def display_pbs_nodes(host):

    config = cm_config()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    user = config.data["cloudmesh"]["hpc"]["username"]
    
    pbs = PBS(user, host)
    
    return render_template('pbsnodes.html',
			   updated = time_now,
                           host=host,
                           data=pbs.info)

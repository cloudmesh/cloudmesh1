from datetime import datetime
from flask import Blueprint
from flask import render_template
from cloudmesh.config.cm_config import cm_config
from cloudmesh.pbs.pbs import PBS
from flask.ext.login import login_required
from cloudmesh.pbs.pbs_mongo import pbs_mongo
from pprint import pprint

pbs_module = Blueprint('pbs_module', __name__)


#
# ROUTE: PROFILE
#

@pbs_module.route('/pbs/<action>/<host>')
#login_required
def display_pbs_action(action,host):

    error = ""
    config = cm_config()
    user = config.config["cloudmesh"]["hpc"]["username"]

    pbs = pbs_mongo()
    pbs.activate(host,user)
        
    time_now = datetime.now()
    if action == "nodes":
        data = pbs.get(host, "nodes")
        page = 'mesh_pbsnodes.html',
        
    elif action == "queue":
        #data = pbs.refresh_pbsnodes(host)
        data = pbs.get(host, "qstat")
        page = 'mesh_qstat.html'
    else:
        return render_template('error.html',
                               updated=time_now, 
                               error=error,
                               type="Page not found",
                               msg="action {0} does not exist".format(action))

    print "IIIIIIIIIIIIIIIIIIIIII"
    pprint (data.count())
    return render_template(page,
                           updated=time_now,
                           host=host,
                           table_data=data)



@pbs_module.route('/pbs/probe/<host>')
#login_required
def display_pbs_qstat(host):

    config = cm_config()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    user = config.config["cloudmesh"]["hpc"]["username"]

    pbs = PBS(user, host)
    data = pbs.qstat()

    return render_template('qstat.html',
                           updated=time_now,
                           host=host,
                           qstat=data)


@pbs_module.route('/pbsnodes/probe/<host>')
#login_required
def display_pbs_nodes(host):

    config = cm_config()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    user = config.config["cloudmesh"]["hpc"]["username"]

    pbs = PBS(user, host)
    data = pbs.pbsnodes()

    return render_template('pbsnodes.html',
                           updated=time_now,
                           host=host,
                           data=data)



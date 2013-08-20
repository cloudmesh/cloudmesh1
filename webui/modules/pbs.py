from datetime import datetime
from flask import Blueprint
from flask import render_template
from cloudmesh.config.cm_config import cm_config
from cloudmesh.pbs.pbs import PBS
from flask.ext.login import login_required

pbs_module = Blueprint('pbs_module', __name__)


#
# ROUTE: PROFILE
#


@pbs_module.route('/pbs/<host>')
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


@pbs_module.route('/pbsnodes/<host>')
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

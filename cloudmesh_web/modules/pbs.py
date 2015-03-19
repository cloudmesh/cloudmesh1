from datetime import datetime
from flask import Blueprint
from flask import render_template
from cloudmesh.config.cm_config import cm_config
from flask.ext.login import login_required
from cloudmesh.pbs.pbs_mongo import pbs_mongo
from flask.ext.principal import Permission, RoleNeed

from cloudmesh_base.logger import LOGGER

log = LOGGER(__file__)

pbs_module = Blueprint('pbs_module', __name__)

admin_permission = Permission(RoleNeed('admin'))

#
# ROUTE: PROFILE
#


@pbs_module.route('/pbs/<action>/<host>')
@login_required
@admin_permission.require(http_exception=403)
def display_pbs_action(action, host):

    error = ""
    config = cm_config()
    user = config.get("cloudmesh.hpc.username")

    pbs = pbs_mongo()
    pbs.activate(host, user)

    time_now = datetime.now()
    if action == "nodes":
        data = pbs.get(host, "nodes")
        # data = pbs.pbsnodes()
        page = 'mesh/cloud/mesh_pbsnodes.html',

    elif action == "queue":
        # data = pbs.refresh_pbsnodes(host)
        data = pbs.get(host, "qstat")
        # data = pbs.qstat()
        page = 'mesh/hpc/mesh_qstat.html'
    else:
        return render_template('error.html',
                               updated=time_now,
                               error=error,
                               type="Page not found",
                               msg="action {0} does not exist".format(action))

    return render_template(page,
                           updated=time_now,
                           host=host,
                           table_data=data)

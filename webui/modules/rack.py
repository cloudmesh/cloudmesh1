from flask import Blueprint
from flask import render_template, request, redirect

# from cloudmesh.config.cm_rack import cm_keys

from cloudmesh.util.util import cond_decorator

import cloudmesh
from flask.ext.login import login_required

rack_module = Blueprint('rack_module', __name__)

#
# ROUTE: rack
#


@rack_module.route('/inventory/rack/')
def display_rack():


    dir = path_expand(cm_config_server().get("rack.path"))

    # not so nice cludge, ask for location of statcic instead

    web_pwd = pwd().strip()
    basename = "/static/{0}/{1}".format(dir, filename)

    rack = None

    return render_template('rack.html',
                           rack=rack)

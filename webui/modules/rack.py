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
def display_all_racks():


    # dir = path_expand(cm_config_server().get("rack.path"))

    # not so nice cludge, ask for location of statcic instead

    # web_pwd = pwd().strip()
    # basename = "/static/{0}/{1}".format(dir, filename)

    rack = None

    return render_template('rack.html',
                           name="india",
                           rack=rack)


@rack_module.route('/inventory/rack/<name>')
@rack_module.route('/inventory/rack/<name>/<service>')
def display_rack(name, service=None):


    if service is None:
        service = "temperature"

    diag_dir = path_expand(cm_config_server().get("rack.input"))
    output_dir = path_expand(cm_config_server().get("rack.diagramms.{0}".format(service)))


    # not so nice cludge, ask for location of statcic instead

    # web_pwd = pwd().strip()
    basename = "/static/{0}/{1}".format(output_dir, name)

    #  /static/racks/diagrams/india
    # .svg
    # .png
    # -legend.png


    #
    # CREATE YOU IMAGES NOW
    #

    # if service == "temperature":
    #    do this
    # else:
    #    do that

    rack = name

    return render_template('rack.html',
                           service=service,
                           basename=basename,
                           name=name,
                           rack=rack)

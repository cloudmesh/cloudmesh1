from flask import Blueprint, g
from flask import render_template, request
from flask.ext.login import login_required
import requests
import yaml
from cloudmesh_base.logger import LOGGER
from pprint import pprint
from cloudmesh_base.ConfigDict import ConfigDict
import json
from cloudmesh_base.locations import config_file

log = LOGGER(__file__)

metric_module = Blueprint('metric_module', __name__)

# ============================================================
# ROUTE: METRIC
# ============================================================
# @app.route('/metric/<s_date>/<e_date>/<user>/<cloud>/<host>/<period>/<metric>')


@metric_module.route('/metric')
@login_required
def metric_index():

    metric = "metric-summary"
    term = "last_3_months"
    config = ConfigDict(filename=config_file(
        "/cloudmesh_server.yaml"))["cloudmesh"]["server"]["metric"]
    address = "{0}:{1}/{2}/{3}".format(
        config["host"], config["port"], metric, term)
    r = requests.get(address)

    return render_template('/metric/index.html', data=r.text)


@metric_module.route('/cm/metric/<cloud>/<instance_id>/')
@login_required
def metric_vm(cloud, instance_id):
    return metric_index()


@metric_module.route('/cm/metric/project/<project_id>/')
@login_required
def metric_project(project_id):

    config = ConfigDict(filename=config_file(
        "/cloudmesh_server.yaml"))["cloudmesh"]["server"]["metric"]
    base_url = "project-summary"

    address = "{0}:{1}/{2}/{3}".format(
        config["host"], config["port"], base_url, project_id)
    try:
        r = requests.get(address)
        pprint(r.json())
        data = dict(yaml.load(r.text))
        data = data["message"]
        return render_template('/metric/project.html', data=data)
    except Exception, e:
        print e
        error = str(e)
        return render_template('error.html', error=error)

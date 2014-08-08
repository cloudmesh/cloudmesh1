from flask import Blueprint, g
from flask import render_template, request
from flask.ext.login import login_required
import requests
import yaml
from cloudmesh_common.logger import LOGGER
from pprint import pprint
log = LOGGER(__file__)

metric_module = Blueprint('metric_module', __name__)

# ============================================================
# ROUTE: METRIC
# ============================================================
# @app.route('/metric/<s_date>/<e_date>/<user>/<cloud>/<host>/<period>/<metric>')

@metric_module.route('/metric')
@login_required
def metric_index():

    address="http://129.79.135.80:5001/metric-summary"

    r = requests.get(address)
    pprint (r.json())

         
    return render_template('/metric/index.html', data=r.json())


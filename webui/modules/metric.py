from flask import Blueprint
from flask import render_template, request
from cloudmesh.util.util import cond_decorator
from flask.ext.login import login_required
import cloudmesh

metric_module = Blueprint('metric_module', __name__)

# ============================================================
# ROUTE: METRIC
# ============================================================
# @app.route('/metric/<s_date>/<e_date>/<user>/<cloud>/<host>/<period>/<metric>')


@metric_module.route('/metric', methods=['POST', 'GET'])
def metric():
    args = {"s_date": request.args.get('s_date', ''),
            "e_date": request.args.get('e_date', ''),
            "user": request.args.get('user', ''),
            "cloud": request.args.get('cloud', ''),
            "host": request.args.get('host', ''),
            "period": request.args.get('period', ''),
            "metric": request.args.get('metric', '')}

    clouds = "TBD"

    return render_template('metric.html',
                           clouds=clouds.get(),
                           metrics=clouds.get_metrics(args))

'''
#gregors test
@app.route('/cm/metric/<startdate>/<enddate>/<host>')
def list_metric(cloud=None, server=None):
    print "-> generate metric", startdate, endadte
    #r = fg-metric(startdate, enddate, host, _tty_in=True)
    return render_template('metric1.html',
                           startdate=startdate,
                           endate=enddate)
    #return table()
'''

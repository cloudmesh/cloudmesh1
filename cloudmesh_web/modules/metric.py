from flask import Blueprint, g
from flask import render_template, request
from flask.ext.login import login_required
from flask import make_response

from cloudmesh_common.util import cond_decorator
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh_common.logger import LOGGER

from datetime import datetime
import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

log = LOGGER(__file__)

metric_module = Blueprint('metric_module', __name__)

# ============================================================
# ROUTE: METRIC
# ============================================================
# @app.route('/metric/<s_date>/<e_date>/<user>/<cloud>/<host>/<period>/<metric>')

@metric_module.route('/stats/table/<metric>/<period>/<cloud_name>/')
@login_required
def stats(metric=None, period=None, cloud_name=None):

    return render_template("status/stats.html", metric=metric, period=period,
                           cloud_name=cloud_name)

@metric_module.route('/stats/figure/<metric>/<period>/<cloud_name>/')
@login_required
def figure(metric=None, period=None, cloud_name=None):

    cm_user_id = g.user.id

    db_metric = cm_mongo("metric")
    db_metric.activate(cm_user_id)


    # Temporary
    data = db_metric.find({})[0]

    # vm count / user count / walltime
    list_of_date = []
    value_by_date = []
    total_value = data[metric]['total']

    for i in data[metric]['by_date']:
        date = datetime.strptime(i['date'], '%Y%m%d')
        list_of_date.append(date)
        if metric == "walltime":
            value_by_date.append(i['total'])
        else:
            value_by_date.append(i['count'])

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.plot_date(list_of_date, value_by_date, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.set_ylabel(get_metric_name(metric))
    ax.set_title(get_metric_title(metric, period, cloud_name))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

def get_metric_name(name):
    if name == "usercount":
        return "User Count"
    elif name == "walltime":
        return "Wall-clock time"
    else:
        return name.title()

def get_metric_title(name, period, source):
    if period == "daily":
        pr = "day"
    else:
        pr = period[:-2]
    if name == "usercount":
        return "Unique User count for %s \n (source:%s)" % (pr, source)
    elif name == "count":
        return "The number of VM instances deployed for %s \n (source:%s)" % (pr, source)
    elif name == "walltime":
        return "Wall-clock time of VM instances for %s \n (source:%s)" % (pr, source)

@metric_module.route('/metric', methods=['POST', 'GET'])
@login_required
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

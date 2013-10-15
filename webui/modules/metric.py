from flask import Blueprint
from flask import render_template, request
from flask.ext.login import login_required
from flask import make_response

from cloudmesh.util.util import cond_decorator
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.util.logger import LOGGER

from datetime import datetime
import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

log = LOGGER(__file__)

metric_module = Blueprint('metric_module', __name__)

db_metric = cm_mongo("metric")
db_metric.activate()

# ============================================================
# ROUTE: METRIC
# ============================================================
# @app.route('/metric/<s_date>/<e_date>/<user>/<cloud>/<host>/<period>/<metric>')

@metric_module.route('/stats/table/<cloud_name>/')
@login_required
def stats(cloud_name=None):

    # Temporary
    data = db_metric.find({})[0]

    # vm count
    list_of_date = []
    count_by_date = []
    total_count = data['count']['total']

    for i in data['count']['by_date']:
        date = datetime.strptime(i['date'], '%Y%m%d')
        list_of_date.append(date)
        count_by_date.append(i['count'])

   
    # user count
    list_of_date2 = []
    user_count_by_date = []
    total_user_count = data['usercount']['total']
    for j in data['usercount']['by_date']:
        date = datetime.strptime(j['date'], '%Y%m%d')
        list_of_date2.append(date)
        user_count_by_date.append(j['count'])

    # walltime
    list_of_date3 = []
    walltime_by_date = []
    total_walltime = data['walltime']['total']
    for k in data['walltime']['by_date']:
        date = datetime.strptime(k['date'],'%Y%m%d')
        list_of_date3.append(date)
        walltime_by_date.append(k['total'])

    fig=Figure()
    ax=fig.add_subplot(111)
    ax.plot_date(list_of_date, count_by_date, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.set_ylabel("count")
    ax.set_title("Number of VM instances deployed")
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

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

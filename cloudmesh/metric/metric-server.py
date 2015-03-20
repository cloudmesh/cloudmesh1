
from flask import Flask, url_for
from docopt import docopt
# from cloudmesh.metric.cm_metric import shell_command_metric
from cm_metric import shell_command_metric
import sh
from cloudmesh_base.logger import LOGGER

log = LOGGER(__file__)


app = Flask(__name__)


@app.route('/')
def get_index_page():
    print "The server is running"
    return "The server is running\n"


@app.route('/metric/cloud/<cloudname>/<username>/<metric>/<timestart>/<timeend>/<period>')
def get_metric_for_cloud(cloudname, username, metric, timestart, timeend, period):
    log.info("/metric/cloud/...")

    arguments = [
        cloudname,
        "-s", timestart,
        "-e", timeend,
        "-u", username,
        "-m", metric,
        "-p", period
    ]
    log.info(arguments)
    command = sh.Command("cm-metric")
    result = command(arguments)
    log.info(result)
    print 70 * "="
    print result
    print 70 * "="

    return str(result)


@app.route('/metric/cluster/<clustername>/<username>/<metric>/<timestart>/<timeend>/<period>')
def get_metric_for_cluster(clustername, username, metric, timestart, timeend, period):
    log.info("/metric/cluster/...")

    arguments = [
        "-c", clustername,
        "-s", timestart,
        "-e", timeend,
        "-u", username,
        "-m", metric,
        "-p", period
    ]
    log.info(arguments)
    command = sh.Command("cm-metric")
    result = command(arguments)
    log.info(result)
    print 70 * "="
    print result
    print 70 * "="

    return str(result)


"""
with app.test_request_context():
    print url_for('get_metric_cluster',
                  cluster="cluster_test",
                  user="user_test",
                  metric="metric_test",
                  start_time="start_time_test",
                  end_time="end_time_test",
                  period="period_test")

    print url_for('get_metric_cloud',
                  cloud="cloud_test",
                  user="user_test",
                  metric="metric_test",
                  start_time="start_time_test",
                  end_time="end_time_test",
                  period="period_test")
"""
if __name__ == "__main__":
    app.run(debug=True)

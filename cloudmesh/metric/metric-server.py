from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def get_index_page():
    print "The server is running"
    return "The server is running\n"

@app.route('/metric/cloud/<cloudname>/<username>/<metric>/<timestart>/<timeend>/<period>')
def get_metric_for_cloud(cloudname,username,metric,timestart,timeend,period):
    print "TEST"
    arguments = {
        'cloud': cloudname,
        'user': username,
        'metric': metric,
        'time_start': timestart,
        'time_end': timeend,
        'period': period
    }
    print arguments
    return str(arguments)

@app.route('/metric/cluster/<clustername>/<username>/<metric>/<timestart>/<timeend>/<period>')
def get_metric_for_cluster(clustername,username,metric,timestart,timeend,period):
    print "TEST"
    arguments = {
        'cloud': clustername,
        'user': username,
        'metric': metric,
        'time_start': timestart,
        'time_end': timeend,
        'period': period
    }
    print arguments
    return str(arguments)

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

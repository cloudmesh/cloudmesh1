import os
# cloud mesh
from flask import Flask, render_template, request
from flask_flatpages import FlatPages
#import cloud_mesh as fg
from cloudmesh import cloudmesh
from datetime import datetime
#from sh import cm 
from sh import fgmetric

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

filename = "VERSION.txt"
version = open(filename).read()

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)

# @hroelee (hyungro) commented March 1st, 2013
# Personally, I prefer to use class variables instead of using global variables.
# Example of using class in Flask: https://github.com/futuregrid/cloud-metrics/blob/master/fgws/FGWSApps.py
#
# Opinion from stackoverflow: Using global variables in a function other than the one that created them
# http://stackoverflow.com/questions/423379/using-global-variables-in-a-function-other-than-the-one-that-created-them
#
#clouds = fg.cloud_mesh()
clouds = cloudmesh.cloudmesh()
clouds.load()
# AttributeError: cloudmesh instance has no attribute 'refresh'
#clouds.refresh()
# TEST CASE
clouds.refresh_servers("openstack")

def make_active(name):
  active = {'home' : "", 
            'table' : "", 
            'contact' : "", 
            "metric" : ""}
  active[name] = 'active'
  return active


@app.route('/')
def index():
    active=make_active('home')
    return render_template('index.html', 
                           pages=pages, 
                           active=active,
                           version=version)

@app.route('/cm/refresh/')
@app.route('/cm/refresh/<cloud>/')
def refresh(cloud=None, server=None):
  print "-> refresh", cloud, server
  global clouds
  #AttributeError: cloudmesh instance has no attribute 'refresh'
  #clouds.refresh()
  clouds.save()
  return table()

@app.route('/cm/kill/')
def kill_vms():
  print "-> kill all"
  r = cm("--set", "quiet", "kill", _tty_in=True)
  return table()


@app.route('/cm/delete/<cloud>/<server>/')
def delete_vm(cloud=None, server=None):
  print "-> delete", cloud, server
  if (cloud == 'india'):
    r = cm("--set", "quiet", "delete:1", _tty_in=True)
  return table()

@app.route('/cm/start/<cloud>/')
def start_vm(cloud=None, server=None):
  print "-> start", cloud, server
  if (cloud == 'india'):
    r = cm("--set", "quiet", "start:1", _tty_in=True)
  return table()

'''
#gregorss test 
@app.route('/cm/metric/<startdate>/<enddate>/<host>')
def list_metric(cloud=None, server=None):
    print "-> generate metric", startdate, endadte
    #r = fg-metric(startdate, enddate, host, _tty_in=True)
    return render_template('metric1.html', 
                           startdate=startdate,
                           active=active,
                           version=version,
                           endate=enddate)
    #return table()
'''

@app.route('/save/')
def save():
  print "Saving the cloud status"
  global clouds
  clouds.save()
  return table()

@app.route('/load/')
def load():
  print "Loading the cloud status"
  global clouds
  clouds.load()
  return table()

@app.route('/table/')
def table():
    global clouds

    active=make_active('table')
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # note thet call to sierra is fake it just goes to india and sets cloudname to sierra.
    #clouds.dump()
    #keys = clouds.get_keys()
    return render_template('table.html', 
                           updated = time_now,
                           keys="",##",".join(clouds.get_keys()),
                           clouds=clouds.get(),
                           image='myimage',
                           pages=pages,
                           active=active,
                           version=version)

#@app.route('/metric/<s_date>/<e_date>/<user>/<cloud>/<host>/<period>/<metric>')
@app.route('/metric/main', methods=['POST','GET'])
def metric():
    global clouds
    args = {"s_date":request.args.get('s_date',''),
            "e_date":request.args.get('e_date',''),
            "user":request.args.get('user',''),
            "cloud":request.args.get('cloud',''),
            "host":request.args.get('host',''),
            "period":request.args.get('period',''),
            "metric":request.args.get('metric','')}

    return render_template('metric.html', 
                           clouds=clouds.get(),
                           metrics=clouds.get_metrics(args),
                           pages=pages,
                           active=make_active('metric'),
                           version=version)

@app.route('/<path:path>/')
def page(path):
    active=make_active(str(path))
    page = pages.get_or_404(path)
    return render_template('page.html', 
                           page=page, 
                           pages=pages, 
                           active=active, 
                           version=version)

if __name__ == '__main__':
  #app.run(debug=True)
  app.run(host=os.environ["FG_HOSTING_IP"] or "127.0.0.1", debug=True)

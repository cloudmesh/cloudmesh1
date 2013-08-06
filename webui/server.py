from ConfigParser import SafeConfigParser
from cloudmesh.inventory.inventory import FabricImage, FabricServer, \
    FabricService, Inventory
from cloudmesh.util.webutil import setup_imagedraw, setup_plugins, setup_noderenderers
from cloudmesh.provisioner.provisioner import *
from cloudmesh.util.util import table_printer
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory
from flask.ext.autoindex import AutoIndex
from flask.ext.wtf import Form
from flask_flatpages import FlatPages
from hostlist import expand_hostlist
from ast import literal_eval

all_modules = ['pbs',
               'flatpages',
               'nose',
               'inventory',
               'provisioner',
               'keys',
               'menu',
               'profile',
               'git',
               'cloud',
               'workflow']

exclude_modules =['workflow']

modules = [m for m in all_modules if m not in exclude_modules]
    
for m in modules:
    print "Loading module", m
    exec "from modules.{0} import {0}_module".format(m)

#from modules.pbs import pbs_module
#from modules.workflow import workflow_module
#from modules.flatpages import flatpages_module
#from modules.nose import nose_module
#from modules.inventory import inventory_module
#from modules.provisioner import provisioner_module
#from modules.keys import keys_module
#from modules.menu import menu_module
#from modules.profile import profile_module
#from modules.cloud import cloud_module
#from modules.git import git_module

from os.path import isfile, join
from pprint import pprint
from wtforms import TextField, SelectField
import base64
import hashlib
import json
import os
import pkg_resources
import struct
import sys
import time
import types
import yaml

sys.path.insert(0, '.')
sys.path.insert(0, '..')

debug = True

with_cloudmesh = False

# not sure what this is for ?????
server_config = SafeConfigParser(
    {'name': 'flasktest'})  # Default database name
server_config.read("server.config")

# ============================================================
# allowing the yaml file to be written back upon change
# ============================================================

with_write = True

# ============================================================
# setting up reading path for the use of yaml
# ============================================================

default_path = '.futuregrid/cloudmesh.yaml'
home = os.environ['HOME']
filename = "%s/%s" % (home, default_path)

# ============================================================
# global vars
# ============================================================

SECRET_KEY = 'development key'
DEBUG = debug
FLATPAGES_AUTO_RELOAD = debug
FLATPAGES_EXTENSION = '.md'



# ============================================================
# STARTING THE FLASK APP
# ============================================================

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = debug
pages = FlatPages(app)
app.register_blueprint(keys_module, url_prefix='',)
app.register_blueprint(inventory_module, url_prefix='',)
app.register_blueprint(provisioner_module, url_prefix='',)
app.register_blueprint(git_module, url_prefix='',)
app.register_blueprint(profile_module, url_prefix='',)
app.register_blueprint(menu_module, url_prefix='',)
app.register_blueprint(flatpages_module, url_prefix='',)
#app.register_blueprint(workflow_module, url_prefix='',)
app.register_blueprint(pbs_module, url_prefix='',)
app.register_blueprint(nose_module, url_prefix='',)
app.register_blueprint(cloud_module, url_prefix='',)


app.secret_key = SECRET_KEY

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))
            
# @app.context_processor
# def inject_pages():
#    return dict(pages=pages)
# app.register_blueprint(menu_module, url_prefix='/', )
#if debug:
#    AutoIndex(app, browse_root=os.path.curdir)

# ============================================================
# VERSION
# ============================================================

version = pkg_resources.get_distribution("cloudmesh").version

@app.context_processor
def inject_version():
    return dict(version=version)


# ============================================================
# ROUTE: sitemap
# ============================================================

"""
@app.route("/site-map/")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        print"PPP>",  rule, rule.methods, rule.defaults, rule.endpoint, rule.arguments
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        try:
            if "GET" in rule.methods and len(rule.defaults) >= len(rule.arguments):
                url = url_for(rule.endpoint)
                links.append((url, rule.endpoint))
                print "Rule added", url, links[url]
        except:
            print "Rule not activated"
    # links is now a list of url, endpoint tuples
"""


# ============================================================
# ROUTE: /
# ============================================================
@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/workflow')
#def display_diagram():
#    return render_template('workflow.html')



# ============================================================
# ROUTE: LOGIN
# ============================================================


@app.route('/login')
def login():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template('login.html',
                           updated=time_now)
                           

# ============================================================
# ROUTE: workflows
# ============================================================


@app.route('/workflows/<filename>')
def retrieve_files(filename):
    """    Retrieve files that have been uploaded    """
    return send_from_directory('workflows',filename)


# ============================================================
# FILTER: timesince
# ============================================================

@app.template_filter()
def timesince(dt, format="float", default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    if dt == "None" or dt == "" or dt == None or dt == "completed":
        return "completed"
    
    #now = datetime.utcnow()
    now = datetime.now()
    if format == 'float':
        diff = now - datetime.fromtimestamp(dt)
    else:
        diff = now - dt
        
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default

# ============================================================
# FILTER: get_tuple element from string
# ============================================================

@app.template_filter()
def get_tuple_element_from_string(obj,i):
    l = obj[1:-1].split(", ")
    return l[i][1:-1]

# ============================================================
# FILTER: is list
# ============================================================

@app.template_filter()
def is_list(obj):
    return isinstance(obj, types.ListType)

# ============================================================
# FILTER: only numbers
# ============================================================

@app.template_filter()
def only_numbers(str):
    return ''.join(c for c in str if c.isdigit())

# ============================================================
# FILTER: simple_data, cuts of microseconds
# ============================================================

@app.template_filter()
def simple_date(d):
    return str(d).rpartition(':')[0]

# ============================================================
# FILTER: state color
# ============================================================

@app.template_filter()
def state_color(state):
    s = state.lower()
    if s == "active":
        color = "#336600"
    else:
        color = "#FFCC99"
    return color

# ============================================================
# FILTER: state style
# ============================================================

@app.template_filter()
def state_style(state):
    color = state_color(state)
    return 'style="background:{0}; font:bold"'.format(color)


# ============================================================
# ROUTE: PAGES
# ============================================================


@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)


if __name__ == "__main__":
    setup_imagedraw()
    #setup_plugins()
    #setup_noderenderers()
    app.run()

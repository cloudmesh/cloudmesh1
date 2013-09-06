import cloudmesh
from flask.ext.login import login_required

from ConfigParser import SafeConfigParser
from cloudmesh.provisioner.provisioner import *
from cloudmesh.config.cm_config import cm_config
from cloudmesh.user.roles import Roles
# from cloudmesh.util.webutil import setup_imagedraw
from cloudmesh.user.cm_userLDAP import cm_userLDAP 
from datetime import datetime

from cloudmesh.util.util import path_expand
from cloudmesh.util.util import cond_decorator

from flask import Flask, render_template, flash, send_from_directory, redirect, g
# from flask.ext.autoindex import AutoIndex
from flask_flatpages import FlatPages

from flask import Flask, current_app, request, session
from flask.ext.login import LoginManager, login_user, logout_user, \
     login_required, current_user, UserMixin
from flask.ext.wtf import Form, TextField, PasswordField, Required, Email
from flask.ext.principal import Principal, Identity, AnonymousIdentity, \
     identity_changed, Permission

from flask.ext.principal import identity_loaded, RoleNeed, UserNeed
from cloudmesh.config.cm_config import cm_config_server
   
import sys

from pprint import pprint
import os
import pkg_resources
import sys
import types

sys.path.insert(0, '.')
sys.path.insert(0, '..')


# ============================================================
# DYNAMIC MODULE MANAGEMENT
# ============================================================

all_modules = ['pbs',
               'flatpages',
               'launch',
               'nose',
               'inventory',
               'provisioner',
               'keys',
               'menu',
               'profile',
               'git',
               'cloud',
               'workflow',
               'mesh',
               'mesh_hpc',
               'users']

exclude_modules = ['flatpages']

modules = [m for m in all_modules if m not in exclude_modules]
    
for m in modules:
    print "Loading module", m
    exec "from modules.{0} import {0}_module".format(m)


# ============================================================
# DYNAMIC MODULE MANAGEMENT
# ============================================================

debug = True

with_cloudmesh = False

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


# dynamic app loading from defined modules
# app.register_blueprint(keys_module, url_prefix='',)

for m in modules:
    print "Loading module", m
    exec "app.register_blueprint({0}_module, url_prefix='',)".format(m)

principals = Principal(app)
login_manager = LoginManager(app)

admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))
rain_permission = Permission(RoleNeed('rain'))

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
# if debug:
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
# ROUTE: /test
# ============================================================

# 

'''
@app.route('/test')
@cond_decorator(cloudmesh.with_login, login_required)
def restricted_index():
    return render_template('index.html')


@app.route('/rain')
@cond_decorator(cloudmesh.with_login, login_required)
@rain_permission.require(http_exception=403)
def rain_index():
    return render_template('rain.html')

@app.route('/admin')
@cond_decorator(cloudmesh.with_login, login_required)
@admin_permission.require(http_exception=403)
def admin_index():
    return render_template('admin.html')
'''

# ============================================================
# ROUTE: erros
# ============================================================

@app.errorhandler(404)
def page_not_found(error):
    error = 'This page does not exist {0}'.format(404)
    return render_template('error.html',
                           error=error,
                           type="Page not found",
                           msg="")
    
@app.errorhandler(403)
def page_not_found(error):
    error = 'Access denied {0}'.format(403)
    return render_template('error.html',
                           error=error,
                           type="Access Denied",
                           msg="You need to Login first")
    

# ============================================================
# ROUTE: /
# ============================================================


@app.route('/')
def index():
    return render_template('index.html')


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
    
    # now = datetime.utcnow()
    now = datetime.now()
    if format == 'float':
        diff = now - datetime.fromtimestamp(float(dt))
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
def get_tuple_element_from_string(obj, i):
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


# ============================================================
#  PRINCIPAL LOGIN
# ============================================================

if cloudmesh.with_login:
    idp = cm_userLDAP ()
    idp.connect("fg-ldap", "ldap")

"""
@app.before_request
def before_request():
    if 'user_id' in session:
        current_user = load_user(session['user_id'])
        g.user = current_user
"""

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    
    if 'user_id' in session:
        current_user = load_user(session['user_id'])
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
    
        # Assuming the User model has a list of roles, update the
        # identity with the roles that the user provides
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role))
    
    """
    identity.provides.add(RoleNeed("rain"))
    """
        
@login_manager.user_loader
def load_user(id):
    try:
        user = idp.find_one({'cm_user_id': id})
        # load from yaml the roles and check them
        role_server = Roles()
        roles = role_server.get(id)
        return User(id, id, roles)
    except:
        # TODO: this could bea bug
        return None

class User(UserMixin):
    
     def __init__(self, name, id, roles=['user'], active=True):
          self.name = name
          self.id = id
          self.active = active
          self.roles = roles

     def is_active(self):
        return True
     
     def is_anonymous(self):
        return False

     def get_id(self):
        return unicode(self.id)

     def is_authenticated(self):
        return True

class LoginForm(Form):

    username = TextField()
    password = PasswordField()

    def validate_on_submit(self):
        return True

@app.route('/login', methods=['GET', 'POST'])
def login():
    # A hypothetical login form that uses Flask-WTF
    form = LoginForm()
    
    if form.validate_on_submit():
        
        form.error = None                
        try:
            idp = cm_userLDAP ()
            idp.connect("fg-ldap", "ldap")
            user = idp.find_one({'cm_user_id': form.username.data})
        except Exception, e:
            error = "LDAP server not reachable"
            error += str(e)
            return render_template('error.html',
                           error=error,
                           type="Can not reach LDAP",
                           msg="")


         
        if user is None:
            form.error = 'Login Invalid'
        elif user['cm_user_id'] != form.username.data:
            form.error = 'Login Invalid'
        elif idp.authenticate(form.username.data, form.password.data):
            print "LOGIN USER"

            g.user = load_user(form.username.data)
                        
            ret = login_user(g.user)
            
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(g.user.id))

            return redirect(request.args.get('next') or '/')
        else:
            form.error = 'Login Invalid'
        
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(request.args.get('next') or '/')


if __name__ == "__main__":
    # setup_imagedraw()
    # setup_plugins()
    # setup_noderenderers()
    config = cm_config_server()
    web_host = config.get('webui.host')
    web_port = config.get('webui.port')
    app.run(host=web_host, port=web_port)

from ConfigParser import SafeConfigParser
from cloudmesh.provisioner.provisioner import *
from cloudmesh.config.cm_config import cm_config
from cloudmesh.util.webutil import setup_imagedraw
from cloudmesh.user.cm_userLDAP import cm_userLDAP 
from datetime import datetime


from flask import Flask, render_template, flash, send_from_directory
#from flask.ext.autoindex import AutoIndex
from flask_flatpages import FlatPages

from flask import current_app, request, session
from flask.ext.login import LoginManager, login_user, logout_user, \
     login_required, current_user, UserMixin
from flask import session, redirect, url_for, abort 

from flask.ext.wtf import Form, validators, TextField, TextAreaField, PasswordField, SubmitField, DataRequired, ValidationError

from flask.ext.principal import Principal, Identity, AnonymousIdentity, \
     identity_changed



from pprint import pprint
import os
import pkg_resources
import sys
import types


sys.path.insert(0, '.')
sys.path.insert(0, '..')

with_login = False

# ============================================================
# DYNAMIC MODULE MANAGEMENT
# ============================================================

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
               'workflow',
               'mesh',
               'users']

exclude_modules = ['workflow', 'cloud']

modules = [m for m in all_modules if m not in exclude_modules]
    
for m in modules:
    print "Loading module", m
    exec "from modules.{0} import {0}_module".format(m)


# ============================================================
# DYNAMIC MODULE MANAGEMENT
# ============================================================

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


# dynamic app loading from defined modules
# app.register_blueprint(keys_module, url_prefix='',)

for m in modules:
    print "Loading module", m
    exec "app.register_blueprint({0}_module, url_prefix='',)".format(m)

principal = Principal(app)
login_manager = LoginManager(app)


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


@app.route('/test')
@login_required
def restricted_index():
    return render_template('index.html')

# ============================================================
# ROUTE: /
# ============================================================


@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/workflow')
# def display_diagram():
#    return render_template('workflow.html')


'''
# ============================================================
# ROUTE: LOGIN
# ============================================================


@app.route('/login')
def login():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template('login.html',
                           updated=time_now)
                           
'''
# ============================================================
# ROUTE: workflows
# ============================================================


@app.route('/workflows/<filename>')
def retrieve_files(filename):
    """    Retrieve files that have been uploaded    """
    return send_from_directory('workflows', filename)


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



#
#  PRINCOIPAL LOGIN
#


@login_manager.user_loader
def load_user(userid):
    # Return an instance of the User model
    return get_user_object(userid)


class UserClass(UserMixin):
     def __init__(self, name, id, active=True):
          self.name = name
          self.id = id
          self.active = active

     def is_active(self):
         return self.active

def get_user_object(userid):

     # query database (again), just so we can pass an object to the callback
     #db_check = users_collection.find_one({ 'userid' : userid })
     #UserObject = UserClass(db_check['username'], userid, active=True)
     #if userObject.id == userid:
     #     return UserObject
     #else:
     #     return None

     return UserClass('gregor','1')

class LoginForm(Form):

    username = TextField('Username')
    password = PasswordField('Password')

    if with_login:
        idp = cm_userLDAP ()
        idp.connect("fg-ldap","ldap")

    user = None

    def validate(self):
        print "validate"

        if with_login:
            self.user =  self.idp.find_one({'cm_user_id': self.username.data})
        
            if self.user is None:
                print "user is None"
                self.error = 'Unknown user'
                return False
            else:
                print "user not None"
        
            if self.user['cm_user_id'] != self.username.data:
                print "username invalid"
                self.error = 'Invalid username'
                return False
            else:
                print "user found"
        
            test = self.idp.authenticate(self.username.data,self.password.data)
    
        else:
            test = True
        
        if not test:
            print "password invalid"
            self.error = 'Invalid password'
            return False
        else:
            print "password found"

        return True





@app.route('/login', methods=['GET', 'POST'])
def login():
    # A hypothetical login form that uses Flask-WTF
    form = LoginForm()

    print "DDD", form.__dict__
    print "UUU", form.user
    
    if form.validate_on_submit():
        flash(u'Successfully logged in as %s' % form.username.data)
        session['user_id'] = form.user["cm_user_id"]
        return redirect(url_for('index'))
        
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
    setup_imagedraw()
    # setup_plugins()
    # setup_noderenderers()
    app.run()

import sys
sys.path.insert(0, './')
sys.path.insert(0, '../')
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

from cloudmesh.cm_keys import cm_keys
from cloudmesh.cm_projects import cm_projects

import os
import time
from flask import Flask, render_template, request,redirect
from flask_flatpages import FlatPages
import base64,struct,hashlib
from cloudmesh.cloudmesh import cloudmesh
from datetime import datetime
from cloudmesh.cm_config import cm_config
from datetime import datetime
try:
    from sh import xterm
except:
    print "xterm not suppported"
    #TODO: THERE SHOULD BE A VARIABLE SET HERE SO THAT THE ARROW START UP BUTTON 
    #      CAN RETURN MEANINGFULL MESSAGE IF NOT SUPPORTED
import yaml

######################################################################
# allowing the yaml file to be written back upon change
######################################################################

with_write = True


######################################################################
# setting up reading path for the use of yaml
######################################################################

default_path = '.futuregrid/cloudmesh.yaml'
home = os.environ['HOME']
filename = "%s/%s" % (home, default_path)

######################################################################
# global vars
######################################################################

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

"""
import pkg_resources
version = pkg_resources.get_distribution("flask_cm").version
"""
version = "0.7.2"


clouds = cloudmesh()
# refresh, misses the search for display
                
clouds.refresh()
clouds.refresh_user_id()
config = cm_config()
configuration = config.get()
prefix = config.prefix
index = config.index

# DEFINING A STATE FOR THE CHECKMARKS IN THE TABLE

"""
for name in clouds.active():

        config.data['cloudmesh']['clouds']

for name in clouds.active():
    try:
        a = config.data['cloudmesh']['clouds'][name]['default']['filter']['state']
        print "- filter exist for cloud", name
    except:
        config.create_filter(name, clouds.states(name))
        config.write()
"""

print config

clouds.all_filter()

######################################################################
# STARTING THE FLASK APP
######################################################################

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)

######################################################################
# ACTIVATE STRUCTURE
######################################################################


def make_active(name):
    active = {'home': "",
              'table': "",
              'contact': "",
              'flavors': "",
              'images': "",
              'metric': "",
              'profile': "",
              'vm_info': "",
              'projects': "",
              'security': "",
              'keys': "",
              'clouds':""}
    
    active[name] = 'active'
    return active

######################################################################
# ROUTE: /
######################################################################


@app.route('/')
def index():
    active = make_active('home')
    return render_template('index.html',
                           pages=pages,
                           active=active,
                           version=version)

######################################################################
# ROUTE: REFRESH
######################################################################


@app.route('/cm/refresh/')
@app.route('/cm/refresh/<cloud>/')
def refresh(cloud=None, server=None):
    #print "-> refresh", cloud, server
    clouds.refresh()
    clouds.all_filter()
    return table()

######################################################################
# ROUTE: Filter
######################################################################

    
@app.route('/cm/filter/<cloud>/',methods=['GET','POST'])
def filter(cloud=None):
    #print "-> filter", cloud

    #
    # BUG: when cloud is none
    #
    name = cloud
    if request.method == 'POST':
        query_states = []
        state_table = {}
        for state in clouds.states(name):
            state_name = "%s:%s" % (name,state)
            state_table[state] = state_name in request.form
            if state_table[state]:
                query_states.append(state)
        config.set_filter(name, state_table, 'state')

        clouds.state_filter(name, query_states)

        
    return redirect("/table/")



######################################################################
# ROUTE: KILL
######################################################################


@app.route('/cm/kill/')
def kill_vms():
    print "-> kill all"
    r = cm("--set", "quiet", "kill", _tty_in=True)
    return table()

######################################################################
# ROUTE: DELETE
######################################################################


@app.route('/cm/delete/<cloud>/<server>/')
def delete_vm(cloud=None, server=None):
    print "-> delete", cloud, server
    # if (cloud == 'india'):
    #  r = cm("--set", "quiet", "delete:1", _tty_in=True)
    clouds.delete(cloud, server)
    time.sleep(5)
    #    clouds.refresh()
    return redirect("/table/")
#    return table()

######################################################################
# ROUTE: DELETE GROUP
######################################################################
@app.route('/cm/delete/<cloud>/')
def delete_vms(cloud=None):
# donot do refresh before delete, this will cause all the vms to get deleted  
    f_cloud = clouds.clouds[cloud]
    for id, server in f_cloud['servers'].iteritems():   
        print "-> delete", cloud, id
        clouds.delete(cloud, id)
    time.sleep(7)
    f_cloud['servers'] = {}
    return redirect("/table/")


######################################################################
# ROUTE: ASSIGN PUBLIC IP
######################################################################


@app.route('/cm/assignpubip/<cloud>/<server>/')
def assign_public_ip(cloud=None, server=None):
    try :
        if configuration['clouds'][cloud]['cm_automatic_ip'] == False:
            clouds.assign_public_ip(cloud,server)
            clouds.refresh(names = [cloud])
            return redirect("/table/")
        else:
            return "Manual public ip assignment is not allowed for %s cloud" % cloud
    except Exception, e:
         return str(e) + "Manual public ip assignment is not allowed for %s cloud" % cloud
     
######################################################################
# ROUTE: START
######################################################################

#
# WHY NOT USE cm_keys as suggested?
#
@app.route('/cm/start/<cloud>/')
def start_vm(cloud=None, server=None):
    print "*********** STARTVM", cloud
    print "-> start", cloud
    # if (cloud == 'india'):
    #  r = cm("--set", "quiet", "start:1", _tty_in=True)
    key = None

    if configuration.has_key('keys'):
        key = configuration['keys']['default']

    # THIS IS A BUG
    vm_flavor = clouds.default(cloud)['flavor']
    vm_image = clouds.default(cloud)['image']

    print "STARTING", config.prefix, config.index
    clouds.create(cloud, config.prefix, config.index, vm_image, vm_flavor, key)
    config.incr()
    config.write()
    
    
    return table()

'''
#gregors test
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

######################################################################
# ROUTE: SAVE
######################################################################


@app.route('/save/')
def save():
    print "Saving the cloud status"
    clouds.save()
    return table()

######################################################################
# ROUTE: LOAD
######################################################################


@app.route('/load/')
def load():
    print "Loading the cloud status"
    clouds.load()
    return table()

######################################################################
# ROUTE: TABLE
######################################################################


@app.route('/table/')
def table():
    active = make_active('table')
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    filter()
    return render_template('table.html',
                           updated=time_now,
                           keys="",  # ",".join(clouds.get_keys()),
			   cloudmesh=clouds,
                           clouds=clouds.clouds,
                           pages=pages,
                           active=active,
                           config=config,
                           version=version)




######################################################################
# ROUTE: VM Login
######################################################################


@app.route('/cm/login/<cloud>/<server>/')
def vm_login(cloud=None,server=None):
    global clouds
    message = ''
    active = make_active('vm_login')
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    server=clouds.clouds[cloud]['servers'][server]
     
    if len(server['addresses'][server['addresses'].keys()[0]]) < 2:  
        mesage = 'Cannot Login Now, Public IP not assigned'
        print message
        
    else :
        message = 'Logged in Successfully'
        ip = server['addresses'][server['addresses'].keys()[0]][1]['addr'] 
        # THIS IS A BUG AND MUST BE SET PER VM, E.G. sometimesvm type probably decides that?
        print "ssh",'ubuntu@'+ip
        xterm('-e','ssh','ubuntu@'+ip,_bg=True)
        
    return redirect("/table/")
######################################################################
# ROUTE: VM INFO
######################################################################


@app.route('/cm/info/<cloud>/<server>/')
def vm_info(cloud=None,server=None):

    active = make_active('vm_info')
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    clouds.clouds[cloud]['servers'][server]['cm_vm_id'] = server
    clouds.clouds[cloud]['servers'][server]['cm_cloudname'] = cloud
    
    return render_template('vm_info.html',
                           updated=time_now,
                           keys="", 
                           server=clouds.clouds[cloud]['servers'][server],
                           id = server,
                           cloudname = cloud, 
                           active=active,
                           version=version,
                           table_printer=table_printer )
                        
def table_printer(the_dict):
    return_str = ''
    if isinstance(the_dict, dict):
        for name,value in the_dict.iteritems() :
            return_str =return_str +'<tr><td>'+name.title() +'</td><td>'+str(table_printer(value))+'</td></tr>'
        return_str = '<table>' + return_str + '</table>'
        return return_str
    elif type(the_dict) is list: 
        for element in the_dict:
            for name,value in element.iteritems() :
                return_str =return_str +'<tr><td>'+name.title()+'</td><td>'+str(table_printer(value))+'</td></tr>'
        return_str = '<table>' + return_str + '</table>'
        return return_str
    else:
        return the_dict

######################################################################
# ROUTE: FLAVOR
######################################################################

#@app.route('/flavors/<cloud>/' )
@app.route('/flavors/', methods=['GET','POST'])
def display_flavors(cloud=None):

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")    
    active = make_active('flavors')

    if request.method == 'POST':
        for cloud in config.active():
            configuration['clouds'][cloud]['default']['flavor']=request.form[cloud] 
            config.write()

    return render_template(
        'flavor.html',
        updated=time_now,
        cloudmesh=clouds,
        clouds=clouds.clouds,
        config=config,
        active=active,
        version=version)



######################################################################
# ROUTE: IMAGES
######################################################################

#@app.route('/images/<cloud>/')
@app.route('/images/', methods=['GET','POST'])
def display_images():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")    
    active = make_active('images')

    if request.method == 'POST':
        for cloud in config.active():
            configuration['clouds'][cloud]['default']['image']=request.form[cloud] 
            config.write()

    return render_template(
        'images.html',
        active=active,
        updated=time_now,
        clouds=clouds.clouds,
        cloudmesh=clouds,
        config=config,
        version=version)


######################################################################
# ROUTE: PROFILE
######################################################################

@app.route('/profile/', methods=['GET','POST'])
def profile():
    # bug the global var of the ditc should be used

    active = make_active('profile')

    projects = cm_projects()
    person = configuration['profile']
    keys = cm_keys()

    
    if request.method == 'POST':
        projects.default = request.form['field-selected-project']
        configuration['security']['default']=request.form['field-selected-securityGroup']
        config.index = request.form['field-index']
        config.prefix = request.form['field-prefix']
        config.firstname = request.form['field-firstname']
        config.lastname = request.form['field-lastname']
        config.phone = request.form['field-phone']
        config.email = request.form['field-email']
        config.default_cloud = request.form['field-default-cloud']

        #print request.form["field-cloud-activated-" + value]
        config.write()

    
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    address = '<br>'.join(str(x) for x in person['address']) 
    return render_template('profile.html',
                           updated=time_now,
                           keys=keys,
                           projects=projects,
                           person=person,
                           address=address,
                           clouds=clouds,
                           active=active,
                           configuration=configuration,
                           version=version,
        )

######################################################################
# ROUTE: METRIC
######################################################################
#@app.route('/metric/<s_date>/<e_date>/<user>/<cloud>/<host>/<period>/<metric>')


@app.route('/metric/main', methods=['POST', 'GET'])
def metric():
    global clouds
    args = {"s_date": request.args.get('s_date', ''),
            "e_date": request.args.get('e_date', ''),
            "user": request.args.get('user', ''),
            "cloud": request.args.get('cloud', ''),
            "host": request.args.get('host', ''),
            "period": request.args.get('period', ''),
            "metric": request.args.get('metric', '')}

    return render_template('metric.html',
                           clouds=clouds.get(),
                           metrics=clouds.get_metrics(args),
                           pages=pages,
                           active=make_active('metric'),
                           version=version)

######################################################################
# ROUTE: PAGES
######################################################################


@app.route('/<path:path>/')
def page(path):
    active = make_active(str(path))
    page = pages.get_or_404(path)
    return render_template('page.html',
                           page=page,
                           pages=pages,
                           active=active,
                           version=version)

######################################################################
# ROUTE: KEYS
######################################################################

@app.route('/keys/',methods=['GET','POST'])
def managekeys():
    
    active = make_active('keys')
    keys = cm_keys()

    msg = ''
    error = False
    """
    keys:
      default: name 1 
      keylist:
         name 1: $HOME/.ssh/id_rsa.pub # this is automatically replaced with the key
         name 2: $HOME/.ssh/id_rsa2.pub # this is automatically replaced with the key
         bla: key ssh-rsa AAAAB3.....zzzz keyname
    """
    if request.method == 'POST' and request.form.has_key('keyname'):
        keyname = request.form['keyname']
        fileorstring = request.form['keyorpath']

        if keys.defined(keyname):
            
            msg = "Key name already exists. Please delete the key '%s' before proceeding." % keyname           
        else:
            try:
                keys.set(keyname, fileorstring, expand=True)
                msg = 'Key %s added successfully' % keyname
                keys.write()
            except Exception, e:
                keys.delete(keyname)
                msg = e
            
    elif request.method == 'POST' :
            keys['default'] = request.form['selectkeys']
            keys.write()

    return render_template('keys.html',
                           keys=keys,
                           active=active,
                           show=msg)
                        

@app.route('/keys/delete/<name>/')
def deletekey(name):

    active = make_active('keys')
    keys = cm_keys()

    try:
        keys.delete(name)
        keys.write()
    except:
        print "Error: deleting the key %s" % name
    return redirect("/keys/")


    
if __name__ == "__main__":
    app.run()

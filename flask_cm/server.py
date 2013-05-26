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

# DEFINING A STATE FOR THE CHECKMARKS IN THE TABLE

state_table = {}

for name in clouds.active():
	state_table[name] = {}
	for state in clouds.states(name):
		state_table[name][state] = True

# refresh, misses the search for display
                
clouds.refresh()
clouds.all_filter()

clouds.refresh_user_id()


config = cm_config()
configuration = config.get()

prefix = config.prefix
index = config.index

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
    print "-> refresh", cloud, server
    clouds.refresh()
    clouds.all_filter()
    return table()

######################################################################
# ROUTE: Filter
######################################################################

    
@app.route('/cm/filter/<cloud>/',methods=['GET','POST'])
def filter(cloud=None):
    print "-> filter", cloud

    #
    # BUG: when cloud is none
    #

    if request.method == 'POST':
        for c in state_table:
            query_states = []
            for state in clouds.states(name):
                state_name = "%s:%s" % (c,state)
                state_table[name][state] = state_name in request.form
                if state_table[name][state]:
                    query_states.append(state)

	    clouds.state_filter(c, query_states)
        
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
    d = clouds.default(cloud)
    vm_flavor = d['flavor']
    vm_image = d['image']

    clouds.create(cloud, config.prefix, config.index, vm_image, vm_flavor, key)
    config.incr()
    config.write()
    
    print "NEW", config.prefix, config.index
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
                           version=version,
			   state_table=state_table)


#######################################################################
# PREFIX MANAGEMENT
####################################################################### 
 
@app.route('/setPrefix', methods=['GET','POST'])
def setPrefix():
    if request.method == 'POST':
        configuration['prefix'] = request.form['prefix']
        config.write()

    return redirect("/profile/")

#######################################################################
# INDEX MANAGEMENT
####################################################################### 
    
@app.route('/setIndex', methods=['GET','POST'])
def setIndex():
    if request.method == 'POST':
        configuration['index'] = request.form['index']
        config.write()

    return redirect("/profile/")

#######################################################################
# PROJECT MANAGEMENT
####################################################################### 
######################################################################
# ROUTE: PROJECTS
######################################################################


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
    
    return render_template('vm_info.html',
                           updated=time_now,
                           keys="", 
                           server=clouds.clouds[cloud]['servers'][server],
                           id = server,
                           cloudname = cloud, 
                           active=active,
                           version=version,
                           table_fun=maketablefromdict )
                        
def maketablefromdict(the_dict):
    return_str = ''
    if isinstance(the_dict, dict):
        for name,value in the_dict.iteritems() :
            return_str =return_str +'<tr><td>'+name.title() +'</td><td>'+str(maketablefromdict(value))+'</td></tr>'
        return_str = '<table>' + return_str + '</table>'
        return return_str
    elif type(the_dict) is list: 
        for element in the_dict:
            for name,value in element.iteritems() :
                return_str =return_str +'<tr><td>'+name.title()+'</td><td>'+str(maketablefromdict(value))+'</td></tr>'
        return_str = '<table>' + return_str + '</table>'
        return return_str
    else:
        return the_dict

######################################################################
# ROUTE: FLAVOR
######################################################################
def set_default_flavor(name, flavor_names):
    global default_flavor
    default_flavor = name
    selected = {}
    for name in flavor_names:
        selected[name] = ""
    selected[default_flavor] = 'checked'
    return selected
        

def buildFlavorNamesArray(clouds):
    flavor_names=[]
    for name, cloud in clouds.iteritems():
        for id, flavor in cloud['flavors'].iteritems():
            flavor_names.append(flavor['name']);
    return flavor_names;



#@app.route('/flavors/<cloud>/' )
@app.route('/flavors/', methods=['GET','POST'])
def display_flavors(cloud=None):
    radioSelected={}
    flavor_names=buildFlavorNamesArray(clouds.clouds);
    # for debugging
    cloud = 'india-openstack'

    ############reading from yaml file ############

    activeClouds=config.active()
    for cloud in activeClouds:
        if 'openstack' in cloud:
            configurations= config.cloud(cloud)   
            default_flavor=configurations['default']['flavor']
            selected=set_default_flavor(default_flavor, flavor_names)
            radioSelected[cloud]=selected
            print radioSelected
            selected={};
    ############  end of reading from yaml file ############

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")    
    active = make_active('flavors')
    #selected = set_default_flavor(default_flavor, flavor_names)

    if request.method == 'POST':
        radioSelected={}
        for cloud in activeClouds:
            if 'openstack' in cloud:
                
                default_flavor= request.form[cloud] 
                print default_flavor
                
                ############ writing in yaml file ############
                configuration= config.get();
                configuration['clouds'][cloud]['default']['flavor']=default_flavor;
                config.write()
                ############ end of writing in yaml file ############
                selected = set_default_flavor(default_flavor, flavor_names)
                radioSelected[cloud]=selected
                print radioSelected
                selected={};
    
      

    if cloud == None:
        pass
    else:
        return render_template('flavor.html',
                               updated=time_now,
                               clouds=clouds.clouds,
                               active=active,
                               version=version,radioSelected=radioSelected)



######################################################################
# ROUTE: CLOUDS
######################################################################

def set_default_clouds(activeClouds, availableClouds):
    selected = {}
    for name in availableClouds:
        selected[name] = ""
        for activeCloud in activeClouds:
            if name in activeCloud:
                selected[name] = 'checked'
    return selected


#
# BUG: this is an inappropriate route name, it is something with projects ....
#
@app.route('/clouds/', methods=['GET','POST'])
def display_clouds():
    projectSelected={}
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M") 
    active = make_active('clouds')

    activeClouds=config.active()
    availableClouds=config.clouds()
    activeProjects=config.projects('active')
    selected=set_default_clouds(activeClouds, availableClouds)
    project_names=buildProjectNamesArray(activeProjects)

    for availableCloud in availableClouds:
        projectSelected[availableCloud]=set_default_project("", project_names,'selected');
        for cloud in activeClouds:
            if 'openstack' in cloud:
                configurations= config.cloud(cloud) 
                default_project=configurations['default']['project']
                projectSelected[cloud]=set_default_project(default_project, project_names,'selected')

    if request.method == 'POST':
        cloudNames = request.form.getlist("clouds")
        configuration=config.get()
        selected=set_default_clouds(cloudNames, availableClouds)
        for cloudName in cloudNames:
            projectName = request.form[cloudName]
            if "None" in projectName:
                projectName=configuration['projects']['default']
            configuration['clouds'][cloudName]['default']['project']=projectName;
        configuration['active']=cloudNames
        config.write()
        
        for availableCloud in availableClouds:
            projectSelected[availableCloud]=set_default_project("", project_names,'selected');
            for cloudName in cloudNames:
                if 'openstack' in cloudName:
                    configurations= config.cloud(cloudName) 
                    default_project=configurations['default']['project']
                    projectSelected[cloudName]=set_default_project(default_project, project_names,'selected')
    
    return render_template(
        'clouds.html',
        updated=time_now,
        clouds=availableClouds,
        active=active,
        version=version,
        projects=activeProjects,
        selected=selected,
        projectSelected=projectSelected)

######################################################################
# ROUTE: IMAGES
######################################################################

def set_default_image(name, image_names):
    global default_image
    default_image = name
    selected = {}
    for name in image_names:
        selected[name] = ""
    selected[default_image] = 'checked'
   # print default_image;
    return selected
        
default_image = "ktanaka/ubuntu1204-ramdisk.manifest.xml"

def buildImageNamesArray(clouds):
    image_names=[]
    for name, cloud in clouds.iteritems():
        for id, image in cloud['images'].iteritems():
            image_names.append(id);
    return image_names;


#@app.route('/images/<cloud>/')
@app.route('/images/', methods=['GET','POST'])
def display_images():
    radioSelected={}
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")    
    active = make_active('images')

    image_names=buildImageNamesArray(clouds.clouds);

    ############reading from yaml file ############

    activeClouds=config.active()
    for cloud in activeClouds:
        if 'openstack' in cloud:
                configurations= config.cloud(cloud)   
                default_image=configurations['default']['image']
                selected=set_default_image(default_image, image_names)
                radioSelected[cloud]=selected
                #print radioSelected #this dict will contain which image in whch cloud is checked
                selected={};

     ############  end of reading from yaml file ############

    if request.method == 'POST':
        radioSelected={}
        for cloud in activeClouds:
                if 'openstack' in cloud:
                        
                        default_image= request.form[cloud] 
                        #print default_image

                        ############ writing in yaml file ############
                        configuration= config.get();
                        configuration['clouds'][cloud]['default']['image']=default_image;
                        config.write()

                        ############ end of writing in yaml file ############
                        selected = set_default_image(default_image, image_names)
                        radioSelected[cloud]=selected
                        #print radioSelected
                        selected={};

    return render_template('images.html',
                               updated=time_now,
                               clouds=clouds.clouds,
                               active=active,
                               version=version,radioSelected=radioSelected)
    

######################################################################
# ROUTE: TEST 
######################################################################

##


def set_default_cloud(name, cloud_names):
    global default_cloud
    default_cloud = name
    selected = {}
    for name in cloud_names:
        selected[name] = ""
    selected[default_cloud] = 'checked = ""'
    return selected
        
default_cloud = "india-openstack"



######################################################################
# ROUTE: PROFILE
######################################################################
@app.route('/profile/', methods=['GET','POST'])
def profile():
    # bug the global var of the ditc should be used

    active = make_active('profile')

    projects = cm_projects()
        
    if request.method == 'POST':
        projects.default = request.form['selected_project']
        configuration['security']['default']=request.form['selected_securityGroup']
        config.write()

    keys = cm_keys()
    person = configuration['profile']
    
    #
    # ACTIVE CLOUDS
    #
    selectedClouds = clouds.active()
    defaultClouds = {} # this is wrong, but i just make it so for the mockup, all is contained in cm_config
    
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    address = '<br>'.join(str(x) for x in person['address']) 
    return render_template('profile.html',
                           updated=time_now,
                           defaultClouds=defaultClouds,
                           selectedClouds=selectedClouds,
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

import sys
sys.path.insert(0, './')
sys.path.insert(0, '../')

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
# setting up reading path for the use of yaml
######################################################################

with_write = True


######################################################################
# setting up view state and way to access viewstate
######################################################################
view_state  = {'table':{}}


def v(names):
    dict = view_state  
    print view_state  
    try:
        for name in names:
            dict = dict[name]
        return dict
    except :
        return ""


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
clouds.refresh()

clouds.refresh_user_id()

prefix = clouds.prefix()

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
              'updatekeypair':"",
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
    return table()

######################################################################
# ROUTE: Filter
######################################################################


@app.route('/cm/filter/<cloud>/',methods=['GET','POST'])
def filter(cloud=None):
    print "-> filter", cloud
    filterIds = []
    do_status_filter = False
    # DOCUMENTATION ABOUT WHERE AND HOW view_state is managed is missing
    if cloud==None and view_state.has_key('table') :
        allClouds = clouds.active()
        # VARIABLE NAME POOR CHOICE, CONFUSING
        for clud in allClouds:
            do_status_filter_inner = False
            filterIds = []
            if view_state['table'].has_key(clud):
                print 'filtering',clud
                ACTIVE = view_state['table'][clud].has_key('ACTIVE')
                STOPPED = view_state['table'][clud].has_key('STOPPED')
                ERROR = view_state['table'][clud].has_key('ERROR')
                SHUTOFF = view_state['table'][clud].has_key('SHUTOFF')
                ME = view_state['table'][clud].has_key('ME')
                if(ACTIVE or STOPPED or ERROR or SHUTOFF):
                            do_status_filter_inner = True
                if(ACTIVE or STOPPED or ERROR or SHUTOFF or ME) :
                    f_cloud = clouds.clouds[clud]
                    for id, server in f_cloud['servers'].iteritems():
                        if do_status_filter_inner and not server['status'] in request.form : 
                            filterIds.append(id)
                        elif  (ME and not server['user_id'] == f_cloud['user_id'] ) :
                            filterIds.append(id)
                    for id in filterIds :
                        del f_cloud['servers'][id]
            
    elif request.method == 'POST':
        
        ACTIVE = 'ACTIVE' in request.form
        STOPPED = 'STOPPED'in request.form
        ERROR = 'ERROR'in request.form
        SHUTOFF = 'SHUTOFF'in request.form
        ME = 'ME'in request.form
        view_state['table'][cloud] = {}
        #IF STATES WOULD BE IN A DICT, WE COULD NICELY ITTERATE OVER THEM
        if ACTIVE:
            view_state['table'][cloud]['ACTIVE'] = 'checked'
        if STOPPED:
            view_state['table'][cloud]['STOPPED'] = 'checked'
        if ERROR:
            view_state['table'][cloud]['ERROR'] = 'checked'
        if SHUTOFF:
            view_state['table'][cloud]['SHUTOFF'] = 'checked'
        if ME:
            view_state['table'][cloud]['ME'] = 'checked'
        
        clouds.refresh(names = [cloud])
        
        if(ACTIVE or STOPPED or ERROR or SHUTOFF):
            do_status_filter = True
        
        if(ACTIVE or STOPPED or ERROR or SHUTOFF or ME) :
            f_cloud = clouds.clouds[cloud]
            for id, server in f_cloud['servers'].iteritems():
                if do_status_filter and not server['status'] in request.form : 
                    filterIds.append(id)
                elif  (ME and not server['user_id'] == f_cloud['user_id'] ) :
                    filterIds.append(id)
            for id in filterIds :
                del f_cloud['servers'][id]
        
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
    clouds.refresh()
    return table()

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
    config = cm_config()
    dict_t = config.get()
    try :
        if dict_t['clouds'][cloud]['cm_automatic_ip'] == False:
            clouds.assign_public_ip(cloud,server)
            clouds.refresh(names = [cloud])
            return redirect("/table/")
        else:
            return "Manual public ip assignment is not allowed for "+cloud+" cloud"
    except Exception, e:
         return str(e) + "Manual public ip assignment is not allowed for "+cloud+" cloud"
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
    config = cm_config()
    dict_t = config.get()
    if dict_t.has_key('keys'):
        key = dict_t['keys']['default']
    d = clouds.default(cloud)
    vm_flavor = d['flavor']
    vm_image = d['image']
    
    clouds.create(cloud, prefix, "001", vm_image, vm_flavor, key)
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
    active_clouds = clouds.active()

    active = make_active('table')
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    filter()
    # keys = clouds.get_keys()
    return render_template('table.html',
                           updated=time_now,
                           keys="",  # ",".join(clouds.get_keys()),
                           clouds=clouds.clouds,
                           order=active_clouds,
                           image='myimage',
                           pages=pages,
                           active=active,
                           version=version,
                           v = v,
                           dir = dir)



######################################################################
# ROUTE: PROJECTS
######################################################################
#
# WHY NOT USE cm_projects as suggested, putting everything in one code becomes confusing and if separated 
#  increases code maintainability and readability
#
def set_default_project(name, project_names, type):
    global default_project;
    default_project = name
    selected = {}
    for name in project_names:
        selected[name] = ""
    selected[default_project] = type
    print selected
    return selected

def buildProjectNamesArray(projects):
     project_names=[]
     for project_name in projects:
        project_names.append(project_name);
     return project_names;

@app.route('/projects/', methods=['GET','POST'])
def display_project():
    global default_project;
    

    ############reading from yaml file ############
    config_project = cm_config()
    activeProjects=config_project.projects('active')
    project_names=buildProjectNamesArray(activeProjects)
    activeClouds=config_project.active()
    
    configurations= config_project.get() 
    default_project=configurations['projects']['default']
    selected=set_default_project(default_project, project_names,'checked')
     ############  end of reading from yaml file ############

    active = make_active('projects')
    
    if request.method == 'POST':
        radioSelected={}
        for cloud in activeClouds:
            if 'openstack' in cloud:
                default_project= request.form['selected_project'] 
                print default_project
                ############ writing in yaml file ############
                yamlFile= config_project.get();
                yamlFile['clouds'][cloud]['default']['project']=default_project;
                yamlFile['projects']['default']=default_project
                write_yaml(filename,yamlFile)
                ############ end of writing in yaml file ############
                selected = set_default_project(default_project, project_names,'checked')


    return redirect("/profile/")

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
    config_flavor = cm_config()
    activeClouds=config_flavor.active()
    for cloud in activeClouds:
        if 'openstack' in cloud:
            configurations= config_flavor.cloud(cloud)   
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
                yamlFile= config_flavor.get();
                yamlFile['clouds'][cloud]['default']['flavor']=default_flavor;
                write_yaml(filename,yamlFile)
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


@app.route('/clouds/', methods=['GET','POST'])
def display_clouds():
    projectSelected={}
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M") 
    active = make_active('clouds')
    config_cloud = cm_config()
    activeClouds=config_cloud.active()
    availableClouds=config_cloud.clouds()
    activeProjects=config_cloud.projects('active')
    selected=set_default_clouds(activeClouds, availableClouds)
    project_names=buildProjectNamesArray(activeProjects)

    for availableCloud in availableClouds:
        projectSelected[availableCloud]=set_default_project("", project_names,'selected');
        for cloud in activeClouds:
            if 'openstack' in cloud:
                configurations= config_cloud.cloud(cloud) 
                default_project=configurations['default']['project']
                projectSelected[cloud]=set_default_project(default_project, project_names,'selected')

    if request.method == 'POST':
        cloudNames = request.form.getlist("clouds")
        yamlFile=config_cloud.get()
        selected=set_default_clouds(cloudNames, availableClouds)
        for cloudName in cloudNames:
            projectName = request.form[cloudName]
            if "None" in projectName:
                projectName=yamlFile['projects']['default']
            yamlFile['clouds'][cloudName]['default']['project']=projectName;
        yamlFile['active']=cloudNames
        write_yaml(filename, yamlFile)
        
        for availableCloud in availableClouds:
            projectSelected[availableCloud]=set_default_project("", project_names,'selected');
            for cloudName in cloudNames:
                if 'openstack' in cloudName:
                    configurations= config_cloud.cloud(cloudName) 
                    default_project=configurations['default']['project']
                    projectSelected[cloudName]=set_default_project(default_project, project_names,'selected')
    
    return render_template('clouds.html',
                               updated=time_now,
                               clouds=availableClouds,
                               active=active,
                               version=version,projects=activeProjects,selected=selected,projectSelected=projectSelected)

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

    config_image = cm_config()
    activeClouds=config_image.active()
    for cloud in activeClouds:
        if 'openstack' in cloud:
                configurations= config_image.cloud(cloud)   
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
                        yamlFile= config_image.get();
                        yamlFile['clouds'][cloud]['default']['image']=default_image;
                        write_yaml(filename, yamlFile)

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


def set_default_cloud(name, cloud_names):
    global default_cloud
    default_cloud = name
    selected = {}
    for name in cloud_names:
        selected[name] = ""
    selected[default_cloud] = 'checked = ""'
    return selected
        
default_cloud = "india-openstack"


@app.route('/gregor', methods=['GET','POST'])
def gregor():
    global default_cloud
    #    default_cloud = "india-openstack"
    #added by shweta
    config_active = cm_config()
    dict_t = config_active.get('active')
    cloud_names = dict_t;
    #print cloud_names;
    #end of additon by shweta
    #cloud_names = ["india-openstack", "sierra-openstack"] code written by Gregor commented by shweta 
    selected = set_default_cloud(default_cloud, cloud_names)
    
    if request.method == 'POST':
        default_cloud= request.form['selected_cloud']
    #print default_cloud

    selected = set_default_cloud(default_cloud, cloud_names)

    return '''
            <form action="" method="post">
              <input type = "radio"
                 name = "selected_cloud"
                 id = "india-openstack"
                 value = "india-openstack"
                 %(india-openstack)s />
              <label>india-openstack</label>                 
              <input type = "radio"
                 name = "selected_cloud"
                 id = "sierra-openstack"
                 value = "sierra-openstack"
                 %(sierra-openstack)s/>
               <label>sierra-openstack</label>
              <input type=submit value=Update>
           </form>''' %selected


######################################################################
# ROUTE: SECURITY
######################################################################
def set_default_security(name, secGroup_names):
    print secGroup_names
    default_secGroup = name
    selectedSecurity = {}
    for name in secGroup_names:
        selectedSecurity[name] = ""
    selectedSecurity[default_secGroup] = 'checked'
    print selectedSecurity
    return selectedSecurity

@app.route('/security/', methods=['GET','POST'])
def security():
    
     ############reading from yaml file ############
    config_security = cm_config()
    yamlFile=config_security.get()
    securityGroupsList=(yamlFile['security']['security_groups']);
    default_secGroup=yamlFile['security']['default']
    securityGroups=securityGroupsList.keys();
    selectedSecurity=set_default_security(default_secGroup, securityGroups)
     ############  end of reading from yaml file ############
    
    active = make_active('security')
    
    if request.method == 'POST':
        default_secGroup= request.form['selected_securityGroup'] 
        
        ############ writing in yaml file ############
        yamlFile['security']['default']=default_secGroup;
        write_yaml(filename,yamlFile)
        ############ end of writing in yaml file ############
        selectedSecurity=set_default_security(default_secGroup, securityGroups)
    
    
    return redirect("/profile/")

######################################################################
# ROUTE: PROFILE
######################################################################
@app.route('/profile/')
def profile():
        # bug the global var of the ditc should be used
        active = make_active('profile')
        
        config = cm_config()
        activeProjects=config.projects('active')
        dict_t = config.get()
        person = dict_t['profile']
        #print person
        ###########projects radio button################
        activeProjects=config.projects('active')
        project_names=buildProjectNamesArray(activeProjects)
        default_project=dict_t['projects']['default']
        selected=set_default_project(default_project, project_names,'checked')
        ########### end of projects radio button################
        
        ###########security radio button################
        securityGroupsList=(dict_t['security']['security_groups']);
        securityGroups=securityGroupsList.keys();
        default_secGroup=dict_t['security']['default']
        selectedSecurity=set_default_security(default_secGroup, securityGroups)
        ###########end of security radio button################

        selectedClouds = clouds.active()
        defaultClouds = {} # this is wrong, but i just make it so for the mockup, all is contained in cm_config
        
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

        address = '\n'.join(str(x) for x in person['address']) 
        return render_template('profile.html',
                               updated=time_now,
                               # keys are also in dict_t, so we may not need that
                               keys="",  # ",".join(clouds.get_keys()),
                               defaultClouds=defaultClouds,
                               selectedClouds=selectedClouds,
                               person=person,
                               address=address,
                               active_clouds=clouds.active(),
                               active=active,
                               config=dict_t,
                               fun_print = lineToFingerprint,
                               selected=selected,
                               version=version,
                               projects=activeProjects,
                               securityGroups=securityGroups,
                               selectedSecurity=selectedSecurity,
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

#
# the key management does not belong in server.py but must be in a  separate class (as do other things in server ....)
# server is done to render things not to implement logig that belongs to cloudmesh.
# keymanagement and checking of keys is a function that should be in cloudmesh. To simplify that, we started a cm_keys code
# 
#
@app.route('/keys/',methods=['GET','POST'])
def managekeys():
    print ">>>>> KEY"
    
    active = make_active('profile')
    active_clouds = clouds.active()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    config = cm_config()
    yamlFile= config.get()    
    haskeys = False
    keydict = {}
    keylist = {}
    defaultkey = ''
    msg = ''
    error = False
    """
    keys:
      default: name 1 
      keylist:
         name 1: file $HOME/.ssh/id_rsa.pub
         name 2: file $HOME/.ssh/id_rsa2.pub
         bla: key ssh-rsa AAAAB3.....zzzz keyname
    """
    if(yamlFile.has_key('keys')):
       haskeys = True 
       keydict = config.userkeys()
       defaultkey = config.userkeys()['default']
       keylist = config.userkeys()['keylist']

    if request.method == 'POST' and request.form.has_key('keyname'):
        keyname = request.form['keyname']
        fileorpath = request.form['keyorpath']
        if not 'ssh-rsa' in fileorpath:
            type = 'file'
        else : 
            type = 'keystring'
        
        if type == "file" :
            fileorpath = os.path.expanduser(fileorpath)
        if keyname is "" or type is 'None' or fileorpath is "":
            error = True
            msg = "Invalid Data. Please Renter Data" 
            
        elif not validateKey(type ,fileorpath): 
            if type.lower() == "file":
                msg = "Invalid file path or Invalid key file" 
            else:
                msg = "Invalid key string"
        elif ' ' in  keyname:
            msg = "Invalid key name, cannot contain spaces"
        elif haskeys and keydict['keylist'].has_key(keyname):
            msg = "Key name already exists"
        else :
            if haskeys :
                keydict['keylist'][keyname] = fileorpath
            else :
                yamlFile['keys'] = {'default':keyname ,'keylist':{keyname: fileorpath}}
                keylist = yamlFile['keys']['keylist']
                defaultkey = yamlFile['keys']['default']
                haskeys = True
            for clud in active_clouds:
                (stat,msg) = clouds.add_key_pair(clud,getKey(fileorpath),keyname)
                print msg
            write_yaml(filename, yamlFile)
            msg = 'Key added successfully'
    elif request.method == 'POST' :
            yamlFile['keys']['default'] = request.form['selectkeys']
            defaultkey = yamlFile['keys']['default']
            write_yaml(filename, yamlFile)
    return render_template('keys.html',
                           haskeys=haskeys,
                           active=active,
                           keylist = keylist,
                           defaultkey =defaultkey,
                           fun_fprint = lineToFingerprint,
                           show = msg)
                        

@app.route('/keys/delete/<name>/')
def deletekey(name):
    active = make_active('profile')

    config = cm_config()
    yamlFile= config.get()
    keydict = yamlFile['keys']
    defaultkey = keydict['default']
    keylist = keydict['keylist']
    if len(keylist) ==1 :
        del yamlFile['keys']
    else :
        del keylist[name]
        if defaultkey == name:
            keydict['default'] = ''
    active_clouds = clouds.active()    
    for clud in active_clouds:
                (stat,msg) = clouds.del_key_pair(clud,name)
                print msg
    write_yaml(filename, yamlFile)
    return redirect("/keys/")

def validateKey(type,file):
    if type.lower() == "file":
        try :
            keystring = open(file, "r").read()
        except :
            return False
    else :
        keystring = file
    
    try :
        type, key_string, comment = keystring.split()
        data = base64.decodestring(key_string)
        int_len = 4
        str_len = struct.unpack('>I', data[:int_len])[0] # this should return 7

        if data[int_len:int_len+str_len] == type:
            return True
    except Exception, e:
        print e
        return False

def getKey(fileorpath):
    if not 'ssh-rsa' in fileorpath:
        fileorpath = os.path.expanduser(fileorpath)
        try :
            keystring = open(fileorpath, "r").read()
            return keystring
        except Exception, e :
            print e
    else : 
        return fileorpath
        


def lineToFingerprint(line,type=None):
    if not 'ssh-rsa' in line:
            type = 'file'
    else : 
            type = 'keystring'
    if type == "file":
        return line
    type,key_string, comment = line.split()
    key = base64.decodestring(key_string)
    fp_plain = hashlib.md5(key).hexdigest()
    return ':'.join(a+b for a,b in zip(fp_plain[::2], fp_plain[1::2]))

def write_yaml(filename, content_dict):
    if with_write:
        d = {}
        d['cloudmesh']=content_dict;
        print "WRITE YAML"
        f = open(filename, "w")
        yaml.safe_dump(d, f, default_flow_style=False, indent=4)
        f.close()

    
if __name__ == "__main__":
    app.run()

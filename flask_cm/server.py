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
import yaml

######################################################################
# setting up reading path for the use of yaml
######################################################################

with_write = False

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
              'updatekeypair':""}
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
# ROUTE: START
######################################################################


@app.route('/cm/start/<cloud>/')
def start_vm(cloud=None, server=None):
    print "*********** STARTVM", cloud
    print "-> start", cloud
    # if (cloud == 'india'):
    #  r = cm("--set", "quiet", "start:1", _tty_in=True)

    d = clouds.default(cloud)
    vm_flavor = d['flavor']
    vm_image = d['image']
    
    clouds.create(cloud, prefix, "001", vm_image, vm_flavor, "KEYMISSING")
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

    # keys = clouds.get_keys()
    return render_template('table.html',
                           updated=time_now,
                           keys="",  # ",".join(clouds.get_keys()),
                           clouds=clouds.clouds,
                           order=active_clouds,
                           image='myimage',
                           pages=pages,
                           active=active,
                           version=version)



######################################################################
# ROUTE: PROJECTS
######################################################################
def set_default_project(name, project_names):
    global default_project;
    default_project = name
    selected = {}
    for name in project_names:
        selected[name] = ""
    selected[default_project] = 'checked'
    print selected
    return selected

def buildProjectNamesArray(projects):
     project_names=[]
     for project_name, info in projects.iteritems():
        project_names.append(project_name);
     return project_names;

@app.route('/projects/', methods=['GET','POST'])
def display_project(cloud=None):
    global projects,default_project;
    active = make_active('projects')
    config = cm_config()
    dict_t = config.get()
    makeCloudDict(dict_t) #from the profile function
    project_names=buildProjectNamesArray(projects)
    ############reading from yaml file ############
    config_project = cm_config()
    activeClouds=config_project.active()
    for cloud in activeClouds:
        if 'openstack' in cloud:
            configurations= config_project.cloud(cloud)   # name of default cloud will come here
            default_project=configurations['default']['project']
            selected=set_default_project(default_project, project_names)
     ############  end of reading from yaml file ############

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")    
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
		write_yaml(filename,yamlFile)
                ############ end of writing in yaml file ############
                selected = set_default_project(default_project, project_names)


    if cloud == None:
        pass
    else:
        return render_template('projects.html',
                               projects=projects,
                               active=active,
                               version=version,selected=selected)


######################################################################
# ROUTE: VM Login
######################################################################


@app.route('/cm/login/<cloud>/<server>/')
def vm_login(cloud=None,server=None):
    global clouds

    active = make_active('vm_login')
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    server=clouds.clouds[cloud]['servers'][server]
     
    if len(server['addresses']['vlan102']) < 2:  
        mesage = 'Cannot Login Now, Public IP not assigned'
        
    else :
        message = 'Logged in Successfully'
        ip = server['addresses']['vlan102'][1]['addr']   
        xterm('-e','ssh', 'ubuntu@'+ip)
        
    return render_template('table.html',
                               updated=time_now,
                               keys="",  # ",".join(clouds.get_keys()),
                               clouds=clouds.clouds,
                               image='myimage',
                               pages=pages,
                               active=active,
                               loginmessage = message, 
                               version=version)
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
            configurations= config_flavor.cloud(cloud)   # name of default cloud will come here
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
# ROUTE: IMAGES
######################################################################

def set_default_image(name, image_names):
    global default_image
    default_image = name
    selected = {}
    for name in image_names:
        selected[name] = ""
    selected[default_image] = 'checked'
    print default_image;
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
def display_images(cloud=None):
    radioSelected={}
    # for debugging
    cloud = 'india-openstack'
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


    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")    
    active = make_active('images')
    if request.method == 'POST':
        radioSelected={}
        for cloud in activeClouds:
                if 'openstack' in cloud:
                        
                        default_image= request.form[cloud] 
                        print default_image

                        ############ writing in yaml file ############
                        yamlFile= config_image.get();
                        yamlFile['clouds'][cloud]['default']['image']=default_image;
			write_yaml(filename, yamlFile)

                        ############ end of writing in yaml file ############
                        selected = set_default_image(default_image, image_names)
                        radioSelected[cloud]=selected
                        print radioSelected
                        selected={};

    if cloud == None:
        pass
    else:
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
    print cloud_names;
    #end of additon by shweta
    #cloud_names = ["india-openstack", "sierra-openstack"] code written by Gregor commented by shweta 
    selected = set_default_cloud(default_cloud, cloud_names)
    
    if request.method == 'POST':
        default_cloud= request.form['selected_cloud']
    print default_cloud

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
# ROUTE: PROFILE
######################################################################
@app.route('/profile/')
def profile():
        # bug the global var of the ditc should be used
        active = make_active('profile')
        
        config = cm_config()
        dict_t = config.get()
        person = dict_t['profile']
        print person
        makeCloudDict(dict_t)


        time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

        # bug: the name of the clouds should be retrived from config. I guess this is left over from my example

        cloudinfo = {
            'openstak-india': {'type': 'openstack', 'host': 'india.futuregrid.org',
                               'username': 'shweta'}}

        address = '\n'.join(str(x) for x in person['address']) 
        return render_template('profile.html',
                               updated=time_now,
                               # keys are also in dict_t, so we may not need that
                               keys="",  # ",".join(clouds.get_keys()),
                               # NOT SURE WHY YOU NEED cloudinfo as most of the stuff is in dict_t
                               cloudinfo=makeCloudDict(dict_t),
                               person=person,
                               address=address,
                               active_clouds=clouds.active(),
                               active=active,
                               config=dict_t,
                               version=version)


def makeCloudDict(dict_t):
    cloudDict = {}
    cloudSubDict = {} # WHAT IS THIS?
    cloudSubsubDict = {} # WHAT IS THIS?
    ############# the below variables are used to display projects.html Here projects dict contains all the projects################
    project_content={}
    global projects;
    projects={};

    ########### end of variables for display of projects.html###########################
    for key, value in dict_t.iteritems():
        # BIG Bug: this should be changed based on a test of type and not the name of the cloud
        # IS THIS STILL WORKING WITH THE clouds: ?...it works now-shweta
        
        if "clouds" in key:
            for cloudKey, cloudValue in value.iteritems():
                if "india-openstack" in cloudKey:
                    for innerKey, innerValue in cloudValue.iteritems():
                        innerKey = innerKey.replace("OS_", "")
                        innerKey = innerKey.replace("cm_", "")
                        cloudSubDict[innerKey.upper()] = innerValue
                    cloudDict[key.upper()] = cloudSubDict
                    cloudSubDict = {}
                if "india-eucalyptus" in cloudKey:
                    for innerKey, innerValue in cloudValue.iteritems():
                        if "fg" in innerKey:
                            for innermostKey, innermostValue in innerValue.iteritems():
                                project_content[innermostKey]=innermostValue
                                innermostKey = innermostKey.replace("EC2_", "")
                                cloudSubsubDict[innermostKey.upper()] = innermostValue
                            cloudDict[innerKey.upper()] = cloudSubsubDict
                            cloudSubsubDict = {}
                            projects[innerKey]=project_content;
                            project_content={};
                        else:
                            innerKey = innerKey.replace("EC2_", "")
                            cloudSubDict[innerKey.upper()] = innerValue
                        cloudDict[key.upper()] = cloudSubDict
                        cloudSubDict = {}
                if "azure" in cloudKey:
                    cloudSubDict = {}
                    for innerKey, innerValue in value.iteritems():
                        cloudSubDict[innerKey.upper()] = innerValue
                    cloudDict[key.upper()] = cloudSubDict
                    cloudSubDict = {}
    # print (cloudDict);

    return cloudDict

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
    active = make_active('profile')

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
       """
       keydict = yamlFile['keys']
       defaultkey = keydict['default']
       keylist = keydict['keylist']
       """
       keydict = config.userkeys()
       defaultkey = config.userkeys('default')
       keylist = config.userkeys()['keylist']

    print "KKKK", keydict,
    print "LLLL", defaultkey
    print "MMMM", keylist
    
    if request.method == 'POST' and request.form.has_key('keyname'):
        type  = request.form.get('type','None')
        keyname = request.form['keyname']
        fileorpath = request.form['keyorpath']
        if type.lower() == "file" :
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
                keydict['keylist'][keyname] = type + " " + fileorpath
            else :
                yamlFile['keys'] = {'default':keyname ,'keylist':{keyname:type + " " + fileorpath}}
                keylist = yamlFile['keys']['keylist']
                defaultkey = yamlFile['keys']['default']
                haskeys = True
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
                           defaultkey =defaultkey ,
                           fun_fprint = lineToFingerprint,
                           show = msg)
                        
def write_yaml(filename, content_dict):
    if with_write:
        d = {}
	d['cloudmesh']=content_dict;
	print "WRITE YAML", d
	f = open(filename, "w")
	yaml.safe_dump(d, f, default_flow_style=False, indent=4)
	f.close()

def validateKey(type,file):
    if type.lower() == "file":
        try :
            f = open(file, "r")
            string = f.read()
        except :
            return False
    else :
        string = file
    
    try :
        openssh_pubkey = string
        type, key_string, comment = openssh_pubkey.split()
        data = base64.decodestring(key_string)
        int_len = 4
        str_len = struct.unpack('>I', data[:int_len])[0] # this should return 7
        print data
        if data[int_len:int_len+str_len] == type:
            return True
    except Exception, e:
        print e
        return False

def lineToFingerprint(line,type):
    if type.lower() == "file":
        return line
    print 
    print "LINE", line
    print
    key_string, comment = line.split()
    key = base64.decodestring(key_string)
    fp_plain = hashlib.md5(key).hexdigest()
    return ':'.join(a+b for a,b in zip(fp_plain[::2], fp_plain[1::2]))

@app.route('/keys/delete/<name>/',methods=['GET','POST'])
def deletekey(name):
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
    write_yaml(filename, yamlFile)
    #testDict={}
    #testDict['cloudmesh']=yamlFile;
    #f = open(filename, "w")
    #yaml.safe_dump(testDict, f, default_flow_style=False, indent=4)
    #f.close()
    return redirect("/keys/")

if __name__ == "__main__":
    app.run()

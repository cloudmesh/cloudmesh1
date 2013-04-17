import sys
sys.path.insert(0, './')
sys.path.insert(0, '../')

import os
import time
from flask import Flask, render_template, request
from flask_flatpages import FlatPages

from cloudmesh.cloudmesh import cloudmesh
from datetime import datetime
from cloudmesh.cm_config import cm_config
from datetime import datetime
import yaml


#### setting up reading path for the use of yaml################
default_path = '.futuregrid/cloudmesh.yaml'
home = os.environ['HOME']
filename = "%s/%s" % (home, default_path)

#### end of setting up reading path for the use of yaml################



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


# clouds.load()
# AttributeError: cloudmesh instance has no attribute 'refresh'
# clouds.refresh()
# TEST CASE

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
              'vm_info': ""}
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
    global clouds
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
    global clouds
    clouds.refresh()
    return table()

######################################################################
# ROUTE: START
######################################################################


@app.route('/cm/start/<cloud>/')
def start_vm(cloud=None, server=None):
    print "*********** STARTVM", cloud
    print "-> start", cloud, server
    # if (cloud == 'india'):
    #  r = cm("--set", "quiet", "start:1", _tty_in=True)
    clouds.create(cloud, "gvonlasz", "001", "dummy")
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
    global clouds
    clouds.save()
    return table()

######################################################################
# ROUTE: LOAD
######################################################################


@app.route('/load/')
def load():
    print "Loading the cloud status"
    global clouds
    clouds.load()
    return table()

######################################################################
# ROUTE: TABLE
######################################################################


@app.route('/table/')
def table():
    global clouds

    active = make_active('table')
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # clouds.refresh("sierra-openstack")

    # note thet call to sierra is fake it just goes to india and sets cloudname to sierra.
    # clouds.dump()
    # keys = clouds.get_keys()
    return render_template('table.html',
                           updated=time_now,
                           keys="",  # ",".join(clouds.get_keys()),
                           clouds=clouds.clouds,
                           image='myimage',
                           pages=pages,
                           active=active,
                           version=version)


######################################################################
# ROUTE: VM INFO
######################################################################


@app.route('/cm/info/<cloud>/<server>/')
def vm_info(cloud=None,server=None):
    global clouds

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
    global default_flavor;
    default_flavor = name
    selected = {}
    for name in flavor_names:
        selected[name] = ""
    selected[default_flavor] = 'checked'
    return selected
        
default_flavor = "m1.small"

def buildFlavorNamesArray(clouds):

    flavor_names=[]
    for name, cloud in clouds.iteritems():
        for id, flavor in cloud['flavors'].iteritems():
            flavor_names.append(flavor['name']);
    return flavor_names;



#@app.route('/flavors/<cloud>/' )
@app.route('/flavors/', methods=['GET','POST'])
def display_flavors(cloud=None):

    flavor_names=buildFlavorNamesArray(clouds.clouds);
    # for debugging
    cloud = 'india-openstack'

    ############reading from yaml file ############
    config_flavor = cm_config()
    configurations= config_flavor.get(cloud)   # name of default cloud will come here
    default_flavor=configurations['default_flavor']
     ############  end of reading from yaml file ############

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")    
    active = make_active('flavors')
    selected = set_default_flavor(default_flavor, flavor_names)

    if request.method == 'POST':
        default_flavor= request.form['selected_flavor'] 
    print default_flavor

     ############ writing in yaml file ############

    yamlFile= config_flavor.get();
    yamlFile['india-openstack']['default_flavor']=default_flavor;
    testDict={}
    testDict['cloudmesh']=yamlFile;
    f = open(filename, "w")
    yaml.safe_dump(testDict, f, default_flow_style=False, indent=4)
    f.close()

 ############ end of writing in yaml file ############

    selected = set_default_flavor(default_flavor, flavor_names)
      

    if cloud == None:
        pass
    else:
        return render_template('flavor.html',
                               updated=time_now,
                               clouds=clouds.clouds,
                               active=active,
                               version=version,selected=selected)



######################################################################
# ROUTE: IMAGES
######################################################################

def set_default_image(name, image_names):
    global default_image;
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
    # for debugging
    cloud = 'india-openstack'
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")    
    active = make_active('images')

    image_names=buildImageNamesArray(clouds.clouds);

    ############reading from yaml file ############
    config_image = cm_config()
    configurations= config_image.get(cloud)   # name of default cloud will come here
    default_image=configurations['default_image']
     ############  end of reading from yaml file ############

   # default_image=image_names[0];
    selected = set_default_image(default_image, image_names)

    if request.method == 'POST':
        default_image= request.form['selected-image'] 
    print default_image

############ writing in yaml file ############

    yamlFile= config_image.get();
    yamlFile['india-openstack']['default_image']=default_image;
    testDict={}
    testDict['cloudmesh']=yamlFile;
    f = open(filename, "w")
    yaml.safe_dump(testDict, f, default_flow_style=False, indent=4)
    f.close()

 ############ end of writing in yaml file ############

    selected = set_default_image(default_image, image_names)

    if cloud == None:
        pass
    else:
        return render_template('images.html',
                               updated=time_now,
                               clouds=clouds.clouds,
                               active=active,
                               version=version,selected=selected)
    


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
        config = cm_config()
        dict_t = config.get()
        makeCloudDict(dict_t)
        active = make_active('profile')
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

        persolalinfo = {'name': 'abc', 'data1': 'pqr'}
        # bug: I guess this is left over from my example

        # bug: the name of the clouds should be retrived from config. I guess this is left over from my example

        cloudinfo = {
            'openstak-india': {'type': 'openstack', 'host': 'india.futuregrid.org',
                               'username': 'shweta'}}

        return render_template('profile.html',
                               updated=time_now,
                               keys="",  # ",".join(clouds.get_keys()),
                               cloudinfo=makeCloudDict(dict_t),
                               persolalinfo=persolalinfo,
                               active=active,
                               version=version)


def makeCloudDict(dict_t):
    cloudDict = {}
    cloudSubDict = {}
    cloudSubsubDict = {}
    for key, value in dict_t.iteritems():
        # Bug: this should be changed based on a test of type
        
        if "india-openstack" in key:

            for innerKey, innerValue in value.iteritems():
                innerKey = innerKey.replace("OS_", "")
                innerKey = innerKey.replace("cm_", "")
                cloudSubDict[innerKey.upper()] = innerValue
            cloudDict[key.upper()] = cloudSubDict
            cloudSubDict = {}
            print (cloudDict)
        if "india-eucalyptus" in key:
            for innerKey, innerValue in value.iteritems():
                if "fg" in innerKey:
                    for innermostKey, innermostValue in innerValue.iteritems():
                        innermostKey = innermostKey.replace("EC2_", "")
                        cloudSubsubDict[innermostKey.upper()] = innermostValue
                    cloudDict[innerKey.upper()] = cloudSubsubDict
                    cloudSubsubDict = {}
                else:
                    innerKey = innerKey.replace("EC2_", "")
                    cloudSubDict[innerKey.upper()] = innerValue
            cloudDict[key.upper()] = cloudSubDict
            cloudSubDict = {}

        if "azure" in key:
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


if __name__ == "__main__":
    app.run()

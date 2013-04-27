import pickle
from sh import fgrep
from sh import nova
from sh import tail
from datetime import datetime
import json
import sys
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

# import shelve
from cm_config import cm_config
#from openstack.cm_compute import openstack as os_client

#Error Cannot Import Openstack
from openstack.cm_compute import openstack

from eucalyptus.eucalyptus_new import eucalyptus
try:
    from azure.cm_azure import cm_azure as azure 
except:
    print "AZURE NOT ENABLED"

class cloudmesh:

    ######################################################################
    # global variables that define the information managed by this class
    ######################################################################

    datastore = "data/clouds.txt"

    # dict that holds vms, flavors, images for al iaas
    clouds = {}

    # array with keys from the user
    keys = []

    configuration = {}
    
    ######################################################################
    # initialization methods
    ######################################################################

    def __init__(self):
        self.clear()
        #Read Yaml File to find all the cloud configurations present
        self.config()

    def clear(self):
        self.clouds = {}
        self.keys = []

    ######################################################################
    # the configuration method that must be called to get the cloud info
    ######################################################################

    def config(self):
        """
        reads the cloudmesh yaml file that defines which clouds build
        the cloudmesh
        """

        print "CONFIG"
        self.configuration = cm_config()


        #pp.pprint (configuration)


        active_clouds = self.configuration.active()
        print active_clouds
        
        for cloud_name in active_clouds:
            try:
                credential = self.configuration.get(cloud_name)
                cloud_type = self.configuration.get()['clouds'][cloud_name]['cm_type']

                if cloud_type in ['openstack','eucalyptus','azure']:
                    self.clouds[cloud_name] = {'name': cloud_name,
                                               'cm_type': cloud_type,
                                               'credential': credential}
            except: #ignore
                pass

        return

    ######################################################################
    # importnat get methods
    ######################################################################

    def get(self):
        """returns the dict that contains all the information"""
        return self.clouds

    def active(self):
        active_clouds = self.configuration.active()
        return active_clouds

    def prefix(self):
        return self.configuration.prefix()

    def profile(self):
        return self.configuration.profile()

    def default(self,cloudname):
        return self.configuration.default(cloudname)

    ######################################################################
    # important print methods
    ######################################################################

    def __str__(self):
        return str(self.clouds)
    
    def dump(self):
        print json.dumps(self.clouds, indent=4)


    ######################################################################
    # find 
    ######################################################################        
    #
    # returns dicts of a particular type
    #
    ######################################################################    

    def find (cloud=["all"], type="servers", project=["all"]):
        """
        Returns a dict with matching elements

        cloud = specifies an array of cloud names that are defined in
        our configuration and returns matching elements in a dict. The
        first level in the dict is the cloud, the second level are the
        elements. If all is specified we serach in all clouds

        type = "servers", "images", "flavors"

        The type specifies the kind of element that we look for
        (we only look for the first character e.g. s, i, f)

        project = an array of projects we search for. This only
        applies for servers for now. Till we have introduced the
        profile that restricts available images and flavors for a
        project.

        In all cases None can be used as an alternative to ["all"]
        
        """
        result = {}
        return result

    ######################################################################
    # the refresh method that gets upto date information for cloudmesh
    # If cloudname is provided only that cloud will be refreshed 
    # else all the clouds will be refreshed
    ######################################################################

    def cloud_provider (self, type):
        provider = None
        if type == 'openstack':
            provider = openstack
        elif type == 'eucalyptus':
            provider = eucalyptus
        elif type == 'azure':
            provider = azure
        return provider

    def info(self):
        print 70 * "="
        print "CLOUD MESH INFO"
        print 70 * "="
        try:
            for name in self.clouds.keys():
                cloud_type = self.clouds[name]['cm_type']
                provider = self.cloud_provider(cloud_type)
                cloud = provider(name)
                print
                print "Info", name
                print 70 * "-"
                cloud.refresh("all")
                cloud.info()
                
        except Exception, e:
            print e
        



    def refresh(self, names=["all"], types=["all"]):
        """
        This method obtians information about servers, images, and
        flavours that build the cloudmesh. The information is held
        internally after a refresh. Than the find method can be used
        to query form this information. To pull new information into
        this data structure a new refresh needs to be called.

        Usage is defined through arrays that are passed along.

        type = "servers", "images", "flavors"

        The type specifies the kind of element that we look for
        (we only look for the first character e.g. s, i, f)

        In all cases None can be used as an alternative to ["all"]
        
        if cloud name  == None and type = none update everything

        if cloud name !=None and type = none update everything in the
        specified clouds

        if cloud name != None and type != none
           refresh the given types for the given clouds
        
        """
        if types == ['all'] or type == None:
            types = ['servers','flavors','images']

        if names == ['all'] or names == None:
            names = self.clouds.keys()
            
        # at one point use a threadpool.
        try:
            for name in names:
                cloud_type = self.clouds[name]['cm_type']
                provider = self.cloud_provider(cloud_type)
                cloud = provider(name)
                print "Refresh cloud", name
                for type in types:
                    print "    Refresh ", type
                    cloud.refresh(type=type)
                    result = cloud.get(type)
                    self.clouds[name][type] = cloud.get(type)
                    #maye be need to use dict update ...
                    self.clouds[name].update({'name': name, 'cm_type': cloud_type})
                
        except Exception, e:
            print e
    
    def refresh_user_id(self, names=["all"]):
        if names == ['all'] or names == None:
            names = self.clouds.keys()        
        try:
            for name in names:
                cloud_type = self.clouds[name]['cm_type']
                provider = self.cloud_provider(cloud_type)
                cloud = provider(name)
                if not self.clouds[name].has_key('user_id'):
                    self.clouds[name]['user_id'] = cloud.find_user_id()
        except Exception, e:
            print e
    
    def add(self, name, type):
        try:
            self.clouds[name]
            print "Error: Cloud %s already exists" % name
        except:
            self.refresh(name, type)

    """
    def get_keys(self):
        return self.keys

    def refresh_keys(self):
        self.keys = []
        result = fgrep(tail(nova("keypair-list"), "-n", "+4"),"-v","+")
        for line in result:
            (front, name, signature, back) = line.split("|")
            self.keys.append(name.strip())
        return self.keys


    def refresh(self):
        keys = self.refresh_keys()
        for cloud in keys:
            self.refresh(cloud)

        # p = Pool(4)
        # update = self.refresh
        # output = p.map(update, keys)

    """

    ######################################################################
    # saves and reads the dict to and from a file
    ######################################################################
    def save(self):
        #tmp = self._sanitize()
        file = open(self.datastore, 'wb')
        # pickle.dump(self.keys, file)
        pickle.dump(tmp, file)
        file.close()

    def load(self):
        file = open(self.datastore, 'rb')
        # self.keys = pickle.load(file)
        self.clouds = pickle.load(file)
        ''' above returns:
        [u'gvonlasz']
         So, call pickle again to get more:
            {'india': {'name': 'india',
            'servers': {u'2731c421-d985-44ce-91bf-2a89ce4ba033': {'cloud': 'india',
            'id': u'2731c421-d985-44ce-91bf-2a89ce4ba033',
            'ip': u'vlan102=10.1.2.85, 149.165.158.7',
            'name': u'gvonlasz-001',
            'refresh': '2013-02-11 20:30:04.472583',
            'status': u'ACTIVE'},
            ...
        '''
        self.clouds = pickle.load(file)
        file.close()

    ######################################################################
    # TODO: convenient +, += functions to add dicts with cm_type
    ######################################################################

    def delete(self, cloud_name, server_id):
        try:
            cloud_type = self.clouds[cloud_name]['cm_type']
            provider = self.cloud_provider(cloud_type)
            cloud = provider(cloud_name)
            cloud.vm_delete(server_id) 
        except:
            print "Error: could not delete", cloud_name, server_id


    def add_key_pair(self,cloud_name,path,name):
        try:
            cloud_type = self.clouds[cloud_name]['cm_type']
            provider = self.cloud_provider(cloud_type)
            cloud = provider(cloud_name)
            return cloud.upload_key_pair(path,name) 
        except:
            print "Error: could not update keypair", cloud_name

    def create(self, cloud_name, prefix, index, image_id, flavor_name, key):
        # bug key has to be defined as parameter when calling this

        name = prefix + "-" + index
        
        cloud_type = self.clouds[cloud_name]['cm_type']
        print cloud_type
        provider = self.cloud_provider(cloud_type)

        cloud = provider(cloud_name)
        cloud.vm_create(name, flavor_name, image_id)

        """
        keyname = ''
        try:
            cloud_type = self.clouds[cloud_name]['cm_type']
            
            if cloud_type in "openstack":
                config = cm_config()
                yamlFile= config.get()
                if yamlFile[cloud_name]['cm_type'] in 'openstack':
                    if yamlFile[cloud_name].has_key('keypair') :
                        keyname = yamlFile[cloud_name]['keypair']['keyname']

            provider = self.cloud_provider(cloud_type)
            cloud = provider(cloud_name)
            if cloud_name == "india-openstack":
                flavor_name = "m1.tiny"  # this is a dummy and must be retrieved from flask
                image_id = "6d2bca76-8fff-4d57-9f29-50378539b4fa"
                name = prefix + "-" + index
                if (len(keyname) > 0) :
                    cloud.vm_create(name, flavor_name, image_id,keyname )
                else :
                    cloud.vm_create(name, flavor_name, image_id)
                # this is a dummy and must be retrieved from flask
        except Exception , e:
            print "Error: could not create", cloud_name, prefix, index, image_id, e
        """

    ######################################################################
    # TODO: convenient +, += functions to add dicts with cm_type
    ######################################################################

    def __add__(self, other):
        """
        type based add function c = cloudmesh(...); b = c + other
        other can be a dict that contains information about the object
        and it will be nicely inserted into the overall cloudmesh dict
        the type will be identified via a cm_type attribute in the
        dict Nn attribute cm_cloud identifies in which cloud the
        element is stored.
        """
        if other.cm_type == "image":
            print "TODO: not implemented yet"
            return
        elif other.cm_type == "vm":
            print "TODO: not implemented yet"
            return
        elif other.cm_type == "flavor":
            print "TODO: not implemented yet"
            return
        elif other.cm_type == "cloudmesh":
            print "TODO: not implemented yet"
            return
        else:
            print "Error: %s type does not exist", cm_type
            print "Error: Ignoring add"
            return

    def __iadd__(self, other):
        """
        type based add function c = cloudmesh(...); c += other other
        can be a dict that contains information about the object and
        it will be nicely inserted into the overall cloudmesh dict the
        type will be identified via a cm_type attribute in the dict.
        Nn attribute cm_cloud identifies in which cloud the element is
        stored.
        """
        if other.cm_type == "image":
            print "TODO: not implemented yet"
            return
        elif other.cm_type == "vm":
            print "TODO: not implemented yet"
            return
        elif other.cm_type == "flavor":
            print "TODO: not implemented yet"
            return
        elif other.cm_type == "cloudmesh":
            print "TODO: not implemented yet"
            return
        else:
            print "Error: %s type does not exist", cm_type
            print "Error: Ignoring add"
            return

##########################################################################
# MAIN METHOD FOR TESTING
##########################################################################

if __name__ == "__main__":

    c = cloudmesh()
    print c.clouds
    """
    c.config()

    c.dump()


    c = cloud_mesh()

    c.refresh()
    c.add('india', 'openstack')
    c.add('sierra', 'openstack')
    c.refresh_keys()
    c.dump()
    c.save()
    print 70 * "-"
    c.clear()
    c.dump()
    print 70 * "-"
    c.load()
    c.dump()
    print 70 * "-"
    """

    """
    india_os = {
        "OS_TENANT_NAME" : '',
        "OS_USERNAME" : '',
        "OS_PASSWORD" : '',
        "OS_AUTH_URL" : '',
        }


    (attribute, passwd) = fgrep("OS_PASSWORD","%s/.futuregrid/openstack/novarc" % os.environ['HOME']).replace("\n","").split("=")

    india_os['OS_PASSWORD'] = passwd



    username = india_os['OS_USERNAME']
    password = india_os['OS_PASSWORD']
    authurl = india_os['OS_AUTH_URL']
    tenant = india_os['OS_TENANT_NAME']

    print password
    '''
    username = os.environ['OS_USERNAME']
    password = os.environ['OS_PASSWORD']
    authurl = os.environ['OS_AUTH_URL']
    '''
    india = cloud_openstack("india", authurl, tenant, username, password)

    india._vm_show("gvonlasz-001")
    india.dump()
    india._vm_show("gvonlasz-001")
    india.dump()
    """

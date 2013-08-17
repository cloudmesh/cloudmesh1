import sys
import traceback
import pymongo
from pymongo import MongoClient
from pprint import pprint
from bson.objectid import ObjectId
from config.cm_config import cm_config
from util.stopwatch import StopWatch
from iaas.openstack.cm_compute import openstack
from iaas.eucalyptus.eucalyptus import eucalyptus
from config.cm_config import cm_config_server


from util.logger import LOGGER

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER('cm_mongo')


try:
    from iaas.azure.cm_azure import cm_azure as azure
except:
    log.warning("AZURE NOT ENABLED")


class cm_mongo:
    
    clouds = {}
    client = None
    db_clouds = None
    
    config = None
    
    def __init__(self, collection="clouds"):
        """initializes the cloudmesh mongo db. The name of the collection os passed."""
        db_name = cm_config_server().config["mongo"]["db"]
        
        self.client = MongoClient()    
        self.db = self.client[db_name]          
        self.db_clouds = self.db[collection]    
        self.config = cm_config()
        


    def cloud_provider(self, type):
        '''
        returns the cloud provider based on the type
        :param type: the type is openstack, eucalyptus, or azure (azure is not yet supported)
        '''
        provider = None
        if type == 'openstack':
            provider = openstack
        elif type == 'eucalyptus':
            provider = eucalyptus
        elif type == 'azure':
            provider = azure
        return provider
    
    def activate(self, names=None):
        '''
        activates a specific host by name. to be queried
        :param names: the array with the names of the clouds in the yaml file to be activated.
        '''
                
        if names is None:
            names = self.config.active()
                    
        for cloud_name in names:
            # print "Activating ->", cloud_name
          
            try:
                credential = self.config.get(cloud_name)
                cm_type = self.config.get()['clouds'][cloud_name]['cm_type']
                cm_type_version = self.config.get()['clouds'][cloud_name]['cm_type_version']
                if cm_type in ['openstack', 'eucalyptus', 'azure']:
                    self.clouds[cloud_name] = {'name': cloud_name,
                                               'cm_type': cm_type,
                                               'cm_type_version': cm_type_version }
#                                               'credential': credential}
                    provider = self.cloud_provider(cm_type)
                    cloud = provider(cloud_name)
                    self.clouds[cloud_name].update({'manager': cloud})
            
            except Exception, e:  
                print "ERROR: can not activate cloud", cloud_name
                print e
                # print traceback.format_exc()
                # sys.exit()


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

        if cloud name  is None and type = none update everything

        if cloud name !=None and type = none update everything in the
        specified clouds

        if cloud name != None and type != none
           refresh the given types for the given clouds

        """
        if types == ['all'] or types is None:
            types = ['servers', 'flavors', 'images']

        if names == ['all'] or names is None:
            names = self.clouds.keys()

        # at one point use a threadpool.
        try:
            for name in names:
                cloud = self.clouds[name]['manager']
                for type in types:
                    log.info("    Refresh {0} -> {1}".format(name, type))
                    cloud.refresh(type=type)
                    result = cloud.get(type)
                    self.clouds[name][type] = cloud.get(type)
                    self.clouds[name].update({'cm_data': type})
                    

        except Exception, e:
            print traceback.format_exc()
            log.error(str(e))
            
        watch = StopWatch()
        for name in names:
            for type in types:
                cloud = self.clouds[name]['manager']
                print "Refreshing {0}->".format(type), name
                watch.start(name)
                cloud.refresh(type)
                result = cloud.get(type)

                # add result to db,
                watch.stop(name)
                print 'Refresh time:', watch.get(name)

                watch.start(name)                   
                for element in result:
                    id = "{0}-{1}-{2}".format(name, type, result[element]['name']).replace(".", "-")
                    #print "ID", id
                    result[element]['cm_id'] = id 
                    result[element]['cm_cloud'] = name
                    result[element]['cm_type'] = self.clouds[name]['cm_type'] 
                    result[element]['cm_type_version'] = self.clouds[name]['cm_type_version'] 
                    result[element]['cm_kind'] = type
                    if 'manager' in result[element]:
                        del result[element]['manager']
                    try:
                        self.db_clouds.remove({"cm_id": id}, safe=True) 
                        self.db_clouds.insert(result[element], safe=True)
                    except Exception, e:
                        print "ERROR: user id duplicated", id
                        pprint (result[element])
                        print e
                        sys.exit()
                watch.stop(name)
                print 'Store time:', watch.get(name)

                
    def get_pbsnodes(self, host):
        '''
        returns the data associated with pbsnodes from mongodb.
        :param host:
        '''
        data = self.db_pbsnodes.find({"pbs_host": host})
        return data
    
    def find(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_clouds.find(query) 
       
    
    def _get_kind(self, kind):
        '''
        returns all the data from clouds of a specific type.
        :param kind:
        '''
        data = {}
        names = self.clouds.keys()
        for name in names:
            data[name] = {}
            result = self.find({'cm_kind' : kind, 'cm_cloud': name})
            for entry in result:
                data[name][entry['id']] = entry
        return data
   
    def users(self):
        '''
        returns all the servers from all clouds
        '''
        return self._get_kind('users')

    def tenants(self):
        '''
        returns all the servers from all clouds
        '''
        return self._get_kind('tenants')

    def servers(self):
        '''
        returns all the servers from all clouds
        '''
        return self._get_kind('servers')
        
    def flavors(self):
        '''
        returns all the flavors from the various clouds
        '''
        return self._get_kind('flavors')
        
    def images(self):
        '''
        returns all the images from various clouds
        '''
        return self._get_kind('images')
        

def main():
    c = cm_mongo()
    c.activate()
    # c.refresh(types=['flavors'])
    # c.refresh(types=['servers','images','flavors'])
    
    # data = c.find({})
    # data = c.find({'cm_kind' : 'servers'})
    # for entry in data:
    #   pprint (entry)
    
    pprint (c.servers())
    
if __name__ == "__main__":
    main()

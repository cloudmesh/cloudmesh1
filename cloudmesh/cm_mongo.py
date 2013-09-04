import sys
import traceback
import pymongo
from pymongo import MongoClient
from pprint import pprint
from bson.objectid import ObjectId
from cloudmesh.config.cm_config import cm_config
from cloudmesh.util.stopwatch import StopWatch
from cloudmesh.iaas.openstack.cm_compute import openstack
from cloudmesh.iaas.eucalyptus.eucalyptus import eucalyptus
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.util.util import path_expand
import yaml
from cloudmesh.util.logger import LOGGER
from cloudmesh.config.cm_config import get_mongo_db

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

    mongo_host = 'localhost'
    mongo_port = 27017
    mongo_db_name = "cloudmesh"
    mongo_collection = "cloudmesh"

    config = None

    def __init__(self, collection="cloudmesh"):
        """initializes the cloudmesh mongo db. The name of the collection os passed."""

        self.db_clouds = get_mongo_db(collection)

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
            print "Activating ->", cloud_name

            try:
                credential = self.config.get(cloud_name)
                cm_type = self.config.get()['clouds'][cloud_name]['cm_type']
                cm_type_version = self.config.get()[
                    'clouds'][cloud_name]['cm_type_version']
                if cm_type in ['openstack', 'eucalyptus', 'azure']:
                    self.clouds[cloud_name] = {'name': cloud_name,
                                               'cm_type': cm_type,
                                               'cm_type_version': cm_type_version}
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

        watch = StopWatch()
        for name in names:

            cloud = self.clouds[name]['manager']

            for type in types:

                print "Refreshing {0}->".format(type)

                watch.start(name)
                cloud.refresh(type)
                result = cloud.get(type)

                # add result to db,
                watch.stop(name)
                print 'Refresh time:', watch.get(name)

                watch.start(name)

                self.db_clouds.remove({"cm_cloud": name, "cm_kind": type})

                for element in result:
                    id = "{0}-{1}-{2}".format(
                        name, type, result[element]['name']).replace(".", "-")
                    # print "ID", id
                    result[element]['cm_id'] = id
                    result[element]['cm_cloud'] = name
                    result[element]['cm_type'] = self.clouds[name]['cm_type']
                    result[element]['cm_type_version'] = self.clouds[
                        name]['cm_type_version']
                    result[element]['cm_kind'] = type

                    self.db_clouds.insert(result[element])

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

    def _get_kind(self, kind, names=None):
        '''
        returns all the data from clouds of a specific type.
        :param kind:
        '''
        data = {}
        if names is None:
            names = self.clouds.keys()

        for name in names:
            data[name] = {}
            result = self.find({'cm_kind': kind, 'cm_cloud': name})
            for entry in result:
                data[name][entry['id']] = entry
        return data

    def users(self, clouds=None):
        '''
        returns all the servers from all clouds
        '''
        return self._get_kind('users', clouds)

    def tenants(self, clouds=None):
        '''
        returns all the servers from all clouds
        '''
        return self._get_kind('tenants', clouds)

    def servers(self, clouds=None):
        '''
        returns all the servers from all clouds
        '''
        return self._get_kind('servers', clouds)

    def flavors(self, clouds=None):
        '''
        returns all the flavors from the various clouds
        '''
        return self._get_kind('flavors', clouds)

    # need to make sure other clouds have the same flavor dict as in openstack
    # otherwide will need to put this into the openstack iaas class
    def flavor_name_to_id(self, cloud, flavor_name):
        ret = -1
        flavor_of_the_cloud = self.flavors([cloud])[cloud]
        for id, details in flavor_of_the_cloud.iteritems():
            if details["name"] == flavor_name:
                ret = id
                break
        return ret

    def images(self, clouds=None):
        '''
        returns all the images from various clouds
        '''
        return self._get_kind('images', clouds)

    def vm_create(self, cloud, prefix, index, vm_flavor, vm_image, key, meta):
        cloudmanager = self.clouds[cloud]["manager"]
        name = "%s_%s" % (prefix, index)
        return cloudmanager.vm_create(name=name, flavor_name=vm_flavor, image_id=vm_image, key_name=key, meta=meta)

    def assign_public_ip(self, cloud, server):
        cloudmanager = self.clouds[cloud]["manager"]
        ip = cloudmanager.get_public_ip()
        return cloudmanager.assign_public_ip(server, ip)

    def release_unused_public_ips(self, cloud):
        cloudmanager = self.clouds[cloud]["manager"]
        return cloudmanager.release_unused_public_ips()

    def vm_delete(self, cloud, server):
        cloudmanager = self.clouds[cloud]["manager"]
        return cloudmanager.vm_delete(server)


def main():
    c = cm_mongo()
    c.activate()
    # c.refresh(types=['flavors'])
    # c.refresh(types=['servers','images','flavors'])

    # data = c.find({})
    # data = c.find({'cm_kind' : 'servers'})
    # for entry in data:
    #   pprint (entry)

    pprint(c.servers())

if __name__ == "__main__":
    main()

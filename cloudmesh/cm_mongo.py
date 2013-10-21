from bson.objectid import ObjectId
from cloudmesh.config.cm_config import cm_config, cm_config_server, get_mongo_db
from cloudmesh.iaas.eucalyptus.eucalyptus import eucalyptus
from cloudmesh.iaas.openstack.cm_compute import openstack
from cloudmesh.iaas.ec2.cm_compute import ec2
from cloudmesh.iaas.openstack.cm_idm import keystone
from cloudmesh.util.logger import LOGGER
from cloudmesh.util.stopwatch import StopWatch
from cloudmesh.util.util import path_expand
from pprint import pprint
import pymongo
import sys
import traceback
import yaml

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)

try:
    from cloudmesh.iaas.azure.cm_compute import azure
except:
    log.warning("AZURE NOT ENABLED")

try:
    from cloudmesh.iaas.aws.cm_compute import aws
except:
    log.warning("Amazon NOT ENABLED")

class cm_MongoBase(object):

    def __init__(self):
        self.cm_type = "overwriteme"
        self.connect()

    def connect(self):
        self.db_mongo = get_mongo_db(self.cm_type)

    def get(self, username):
        return self.find_one({"cm_id": username, "cm_type": self.cm_type})


    def set(self, username, d):
        element = dict (d)
        element["cm_id"] = username
        element["cm_type"] = self.cm_type
        self.update({"cm_id": username, "cm_type": self.cm_type}, element)

    def update(self, query, values=None):
        '''
        executes a query and updates the results from mongo db.
        :param query:
        '''
        if values is None:
            return self.db_mongo.update(query, upsert=True)
        else:
            return self.db_mongo.update(query, values, upsert=True)


    def insert(self, element):
        self.db_mongo.insert(element)

    def find(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_mongo.find(query)

    def find_one(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_mongo.find_one(query)

    def clear(self):
        self.db_mongo.remove({"cm_type" : self.cm_type})


    def wipe(self):
        self.db_mongo.remove({})



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
        :param type: the type is openstack, eucalyptus, or azure (< is not yet supported)
        '''
        provider = None
        if type == 'openstack':
            provider = openstack
        elif type == 'eucalyptus':
            provider = eucalyptus
        elif type == 'azure':
            provider = azure
        elif type == 'aws':
            provider = aws
        elif type == 'ec2':
            provider = ec2
        return provider

    def get_cloud(self, cloud_name, force=False):
        cloud = None
        if not force and cloud_name in self.clouds:
            if 'manager' in self.clouds[cloud_name]:
                if self.clouds[cloud_name]['manager']:
                    cloud = self.clouds[cloud_name]['manager']
        else:
            try:
                credential = self.config.cloud(cloud_name)
                cm_type = credential['cm_type']
                cm_type_version = credential['cm_type_version']
                if cm_type in ['openstack', 'eucalyptus', 'azure', 'ec2', 'aws']:
                    self.clouds[cloud_name] = {'name': cloud_name,
                                               'cm_type': cm_type,
                                               'cm_type_version': cm_type_version}
                    provider = self.cloud_provider(cm_type)
                    cloud = provider(cloud_name)
                    if cm_type in ['openstack']:
                        tryauth = cloud.get_token()
                        if 'access' not in tryauth:
                            cloud = None
                            log.error("Credential not working, cloud is not activated")
                    self.clouds[cloud_name].update({'manager': cloud})
            except Exception, e:
                log.error("Cannot activate cloud <%s>\n%s" % (cloud_name, e))
        return cloud

    def activate(self, names=None):
        #
        # bug must come form mongo
        #
        #
        if names is None:
            names = self.config.active()

        for cloud_name in names:
            log.info("Activating -> {0}".format(cloud_name))
            cloud = self.get_cloud(cloud_name)
            if not cloud:
                log.info("Activation of cloud <%s> Failed!" % cloud_name)
            else:
                log.info("Activation of cloud <%s> Succeeded!" % cloud_name)

    def refresh(self, names=["all"], types=["all"]):
        """
        This method obtains information about servers, images, and
        flavors that build the cloudmesh. The information is held
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
            print "-"*80
            print "retrieving for %s" % name
            print "-"*80
            cloud = None
            for type in types:
                # for identity management operations, use the keystone class
                if type in ['users', 'tenants', 'roles']:
                    cloud = keystone(name)
                # else try compute/nova class
                elif 'manager' in self.clouds[name]:
                    cloud = self.clouds[name]['manager']

                print "Refreshing {0} {1} ->".format(type, name)

                watch.start(name)
                cloud.refresh(type)
                result = cloud.get(type)
                # print "YYYYY", len(result)
                # pprint(result)
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
                    result[element]['cm_type_version'] = self.clouds[name]['cm_type_version']
                    result[element]['cm_kind'] = type
                    # print "HPCLOUD_DEBUG", result[element]
                    for key in result[element]:
                        # print key
                        if '.' in key:
                            del result[element][key]
                    if 'metadata' in result[element].keys():
                        for key in result[element]['metadata']:
                            if '.' in key:
                                fixedkey = key.replace(".", "_")
                                # print "%s->%s" % (key,fixedkey)
                                value = result[element]['metadata'][key]
                                del result[element]['metadata'][key]
                                result[element]['metadata'][fixedkey] = value
                    # print "HPCLOUD_DEBUG - AFTER DELETING PROBLEMATIC KEYS", result[element]

                    # exception.
                    if "_id" in result[element]:
                        del(result[element]['_id'])

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

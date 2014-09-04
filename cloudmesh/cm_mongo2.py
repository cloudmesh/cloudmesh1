from cloudmesh.config.cm_config import cm_config, cm_config_server, get_mongo_db
# from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.iaas.eucalyptus.eucalyptus import eucalyptus
from cloudmesh.iaas.openstack.cm_compute import openstack
from cloudmesh.iaas.ec2.cm_compute import ec2
from cloudmesh.iaas.openstack.cm_idm import keystone
from cloudmesh.iaas.Ec2SecurityGroup import Ec2SecurityGroup
from cloudmesh_common.logger import LOGGER
from cloudmesh.util.stopwatch import StopWatch
# from pprint import pprint
import traceback
from cloudmesh.util.encryptdata import decrypt
import traceback

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
        element = dict(d)
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

    def remove(self, query):
        '''
        executes a query and removes the results from mongo db.
        :param query:
        '''
        return self.db_mongo.remoe(query)

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



class cm_mongo2:

    clouds = {}
    client = None
    db_clouds = None

    mongo_host = 'localhost'
    mongo_port = 27017
    mongo_db_name = "cloudmesh"
    mongo_collection = "cloudmesh"

    ssh_ec2_rule = Ec2SecurityGroup.Rule(22, 22)
    
    config = None

    def __init__(self, collection="cloudmesh"):
        """initializes the cloudmesh mongo db. The name of the collection os passed."""

        defaults_collection = 'defaults'
        passwd_collection = 'password'
        user_collection = "user"
        self.userdb_passwd = get_mongo_db(passwd_collection)
        self.db_defaults = get_mongo_db(defaults_collection)
        self.db_user = get_mongo_db(user_collection)

        self.db_clouds = get_mongo_db(collection)


        self.config = cm_config()

    def cloud_provider(self, kind):
        '''
        returns the cloud provider based on the kind
        :param kind: the kind is openstack, eucalyptus, or azure (< is not yet supported)
        '''
        provider = None
        if kind == 'openstack':
            provider = openstack
        elif kind == 'eucalyptus':
            provider = eucalyptus
        elif kind == 'azure':
            provider = azure
        elif kind == 'aws':
            provider = aws
        elif kind == 'ec2':
            provider = ec2
        return provider


    #
    #  BUG NO USER IS INVOLVED
    #


    def get_credential(self, cm_user_id, cloud):
        try:
            password = cm_config_server().get("cloudmesh.server.mongo.collections.password.key")
            safe_credential = (self.userdb_passwd.find_one({"cm_user_id": cm_user_id, "cloud":cloud}))["credential"]


            # print "SK", safe_credential

            for cred in safe_credential:
                t = safe_credential[cred]
                n = decrypt(t, password)
                safe_credential[cred] = n

            return safe_credential
        except:
            print traceback.format_exc()
            return None


    def get_cloud_info(self, cm_user_id, cloudname):
        cloud_config = self.config.cloud(cloudname)
        if cloud_config['cm_type'] in ['openstack']:
            del cloud_config['credentials']['OS_USERNAME']
            del cloud_config['credentials']['OS_PASSWORD']
            del cloud_config['credentials']['OS_TENANT_NAME']
        elif cloud_config['cm_type'] in ['ec2']:
             del cloud_config['credentials']['EC2_ACCESS_KEY']
             del cloud_config['credentials']['EC2_SECRET_KEY']
        elif cloud_config['cm_type'] in ['aws']:
            if 'EC2_ACCESS_KEY' in cloud_config['credentials']:
                del cloud_config['credentials']['EC2_ACCESS_KEY']
                del cloud_config['credentials']['EC2_SECRET_KEY']
        elif cloud_config['cm_type'] in ['azure']:
            del cloud_config['credentials']['subscriptionid']

        credential = self.get_credential(cm_user_id, cloudname)

        # print "C", credential

        for key in credential:
            if key not in  cloud_config['credentials']:
                cloud_config['credentials'][key] = credential[key]

        #
        # THIS SEEMS TO BE A BUG???? sos = sierra openstack, why only sierra?
        #
        if (cloud_config['cm_type'] in ['openstack']) and (cloud_config['cm_label'] in ['sos', 'ios_havana']):
            cloud_config['credentials']['OS_TENANT_NAME'] = self.active_project(cm_user_id)

        return cloud_config


    def get_cloud(self, cm_user_id, cloud_name, force=False):
        cloud = None
        # do we recreate a cloud instance?
        # recreate only when user/tenant is changed for a certain cloud
        recreate = False
        cloud_info = self.get_cloud_info(cm_user_id, cloud_name)

        # credential = self.config.cloud(cloud_name)
        cm_type = cloud_info['cm_type']
        cm_type_version = cloud_info['cm_type_version']

        credentials = cloud_info['credentials']
        # print "D",credentials
        
        # we can force an update
        if force:
            recreate = True
        # new user
        elif not cm_user_id in self.clouds:
            recreate = True
        # new cloud for that user
        elif not cloud_name in self.clouds[cm_user_id]:
            recreate = True
        # manager pointer does not exist
        elif 'manager' not in self.clouds[cm_user_id][cloud_name]:
            recreate = True
        # manager object ref is None
        elif not self.clouds[cm_user_id][cloud_name]['manager']:
            recreate = True
        # for openstack, we check if tenant_name was recently changed
        elif 'OS_TENANT_NAME' in credentials and\
              hasattr(self.clouds[cm_user_id][cloud_name]['manager'], 'user_token') and\
             'access' in self.clouds[cm_user_id][cloud_name]['manager'].user_token and\
             self.clouds[cm_user_id][cloud_name]['manager'].user_token['access']['token']['tenant']['name'] != credentials['OS_TENANT_NAME']:
                recreate = True
        # in most case we return the existing object ref
        else:
            return self.clouds[cm_user_id][cloud_name]['manager']
        
        # in case new object needs to be created
        if recreate:
            try:
                if cm_user_id not in self.clouds:
                    self.clouds[cm_user_id] = {}

                if cm_type in ['openstack', 'eucalyptus', 'azure', 'ec2', 'aws']:

                    self.clouds[cm_user_id][cloud_name] = {
                        'name': cloud_name,
                        'cm_type': cm_type,
                        'cm_type_version': cm_type_version}
                    provider = self.cloud_provider(cm_type)
                    cloud = provider(cloud_name, credentials)

                    log.debug("Created new cloud instance for cloud name: %s, type: %s" \
                              % (cloud_name, cm_type))
                    if cm_type in ['openstack', 'ec2']:
                        if cm_type in ['openstack']:
                            log.debug("\tfor tenant: %s" % credentials['OS_TENANT_NAME'])
                        if not cloud.auth():
                            cloud = None
                            log.error("Authentication Failed, cloud is not activated")

                    self.clouds[cm_user_id][cloud_name].update({'manager': cloud})
                    if cloud is not None:
                        self.refresh(cm_user_id, [cloud_name], ['servers'])
                        if cm_type in ['openstack']:
                            secgroups = cloud.list_security_groups()['security_groups']
                            for secgroup in secgroups:
                                if secgroup['name'] == 'default':
                                    foundsshrule = False
                                    for rule in secgroup['rules']:
                                        existRule = Ec2SecurityGroup.Rule(
                                            rule['from_port'],
                                            rule['to_port']
                                            )
                                        if existRule == self.ssh_ec2_rule:
                                            foundsshrule = True
                                            log.debug("Ec2 security group rule allowing ssh exists for cloud: %s, type: %s, tenant: %s" \
                                                      % (cloud_name, cm_type, credentials['OS_TENANT_NAME']))
                                    if not foundsshrule:
                                        iddefault = cloud.find_security_groupid_by_name('default')
                                        cloud.add_security_group_rules(iddefault,
                                                                       [self.ssh_ec2_rule])
                                        log.debug("Added Ec2 security group rule to allow ssh for cloud: %s, type: %s, tenant: %s" \
                                                  % (cloud_name, cm_type, credentials['OS_TENANT_NAME']))
                        
            except Exception, e:
                cloud = None
                log.error("Cannot activate cloud {0} for {1}\n{2}".format(cloud_name, cm_user_id, e))
                print traceback.format_exc()
        return cloud

    def active_clouds(self, cm_user_id):
        user = self.db_defaults.find_one({'cm_user_id': cm_user_id})
        try:
            return user['activeclouds']
        except:
            # If activeclouds is empty in defaults, user collection will be
            # looked up.
            user = self.db_user.find_one({'cm_user_id': cm_user_id})
            return user['activeclouds']

    def active_project(self, cm_user_id):
        user = self.db_defaults.find_one({'cm_user_id': cm_user_id})
        return user['project']


    def activate(self, cm_user_id, names=None):
        #
        # bug must come form mongo
        #

        if cm_user_id is None:
            cm_user_id = self.config.username() #added by Mark X on 8.12.2014
            if names is None:
                names = self.config.active()
        else:
            if names is None:     #added by Mark X on 8.12.2014
                names = self.active_clouds(cm_user_id)

        for cloud_name in names:
            log.info("Activating -> {0}".format(cloud_name))
            cloud = self.get_cloud(cm_user_id, cloud_name)
            if not cloud:
                log.info("Activation of cloud {0} and user {1} Failed!".format(cloud_name, cm_user_id))
            else:
                log.info("Activation of cloud {0} and user {1} Succeeded!".format(cloud_name, cm_user_id))



    def refresh(self, cm_user_id, names=["all"], types=["all"]):
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
            # names = self.clouds.keys()
            names = self.active_clouds(cm_user_id)

        watch = StopWatch()



        for name in names:
            print "*", name
            watch_name = "{0}-{1}".format(cm_user_id, name)
            log.info("-"*80)
            log.info("Retrieving data for %s" % name)
            log.info("-"*80)
            cloud = None
            for type in types:
                # for identity management operations, use the keystone class
                if type in ['users', 'tenants', 'roles']:
                    cloud = keystone(name)
                # else try compute/nova class
                elif 'manager' in self.clouds[cm_user_id][name]:
                    cloud = self.clouds[cm_user_id][name]['manager']

                print "Refreshing {0} {1} {2} ->".format(cm_user_id, type, name)



                watch.start(watch_name)
                cloud.refresh(type)
                result = cloud.get(type)
                # print "YYYYY", len(result)
                # pprint(result)
                # add result to db,
                watch.stop(watch_name)
                print 'Refresh time:', watch.get(watch_name)

                watch.start(watch_name)

                if type in ['servers']:
                    self.db_clouds.remove({"cm_user_id": cm_user_id, "cm_cloud": name, "cm_kind": type})
                else:
                    self.db_clouds.remove({"cm_cloud": name, "cm_kind": type})

                for element in result:
                    id = "{0}-{1}-{2}".format(
                        name, type, result[element]['name']).replace(".", "-")
                    # servers or security_groups is for each user.
                    if type in ['servers', 'e_security_groups']:
                        result[element]['cm_user_id'] = cm_user_id

                    result[element]['cm_id'] = id
                    result[element]['cm_cloud'] = name
                    result[element]['cm_type'] = self.clouds[cm_user_id][name]['cm_type']
                    result[element]['cm_type_version'] = self.clouds[cm_user_id][name]['cm_type_version']
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

                watch.stop(watch_name)
                print 'Store time:', watch.get(watch_name)

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

    def _get_kind(self, kind, names=None, cm_user_id=None):
        '''
        returns all the data from clouds of a specific type.
        :param kind:
        '''
        data = {}
        if names is None:
            names = self.active_clouds(cm_user_id)

        for name in names:
            data[name] = {}
            if kind in ['flavors', 'images', 'users', 'tenants']:
                result = self.find({'cm_kind': kind, 'cm_cloud': name})
            else:
                result = self.find({'cm_user_id': cm_user_id, 'cm_kind': kind, 'cm_cloud': name})
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

    #
    # BUG
    #
    def servers(self, clouds=None, cm_user_id=None):
        '''
        returns all the servers from all clouds
        '''
        return self._get_kind('servers', clouds, cm_user_id)

    def flavors(self, clouds=None, cm_user_id=None):
        '''
        returns all the flavors from the various clouds
        '''
        return self._get_kind('flavors', clouds, cm_user_id)

    def images(self, clouds=None, cm_user_id=None):
        '''
        returns all the images from various clouds
        '''
        return self._get_kind('images', clouds, cm_user_id)

    def security_groups(self, clouds=None, cm_user_id=None):
        '''
        returns all the security groups from various clouds
        '''
        return self._get_kind('e_security_groups', clouds, cm_user_id)

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

    def vm_create(self, cloud, prefix, index, vm_flavor, vm_image, key, meta, cm_user_id, givenvmname=None):
        '''
        BUG: missing security group
        '''
        cloudmanager = self.clouds[cm_user_id][cloud]["manager"]
        if givenvmname == None:
            name = "%s_%s" % (prefix, index)
        else:
            name = givenvmname
        return cloudmanager.vm_create(name=name, flavor_name=vm_flavor, image_id=vm_image, key_name=key, meta=meta)

    def vm_create_queue(self, cloud, prefix, index, vm_flavor, vm_image, key, meta, cm_user_id, givenvmname=None):
        '''
        same as vm_create but runs with a celery task queue
        
        apply_async places a function call in a specific queue named in 'queue='
        parameter
        
        BUG: missing security group
        '''
        cloudmanager = self.clouds[cm_user_id][cloud]["manager"]
        cm_type = self.get_cloud_info(cm_user_id, cloud)['cm_type']
        package = "cloudmesh.iaas.%s.queue" % cm_type
        name = "tasks"
        imported = getattr(__import__(package, fromlist=[name]), name)
        queue_name = "%s-%s" % (cm_type, "servers")
        if givenvmname == None:
            name = "%s_%s" % (prefix, index)
        else:
            name = givenvmname
        return imported.vm_create.apply_async(
            (
                name, 
                vm_flavor,
                vm_image
            ), 
            {
                'key_name': key,
                'meta': meta,
                'manager': cloudmanager
            },
            queue=queue_name)

    def assign_public_ip(self, cloud, server, cm_user_id):
        cloudmanager = self.clouds[cm_user_id][cloud]["manager"]
        type = self.clouds[cm_user_id][cloud]["cm_type"]
        if type == 'openstack':
            ip = cloudmanager.get_public_ip()
            ret = cloudmanager.assign_public_ip(server, ip)
        else:
            ret = None
        return ret

    def release_unused_public_ips(self, cloud, cm_user_id):
        cloudmanager = self.clouds[cm_user_id][cloud]["manager"]
        type = self.clouds[cm_user_id][cloud]["cm_type"]
        if type == 'openstack':
            ret = cloudmanager.release_unused_public_ips()
        else:
            ret = None
        return ret

    def vm_delete(self, cloud, server, cm_user_id):
        cloudmanager = self.clouds[cm_user_id][cloud]["manager"]
        return cloudmanager.vm_delete(server)
    
        

'''
def main():
    user = ???
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
'''

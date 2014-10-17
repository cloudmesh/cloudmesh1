from cloudmesh.config.cm_config import cm_config, cm_config_server, get_mongo_db
from cloudmesh.config.cm_config import DBConnFactory
# from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.iaas.eucalyptus.eucalyptus import eucalyptus
from cloudmesh.iaas.openstack.cm_compute import openstack
from cloudmesh.iaas.ec2.cm_compute import ec2
from cloudmesh.iaas.openstack.cm_idm import keystone
from cloudmesh.iaas.Ec2SecurityGroup import Ec2SecurityGroup
from cloudmesh_common.logger import LOGGER
from cloudmesh.util.stopwatch import StopWatch
from cloudmesh.util.encryptdata import decrypt
from cloudmesh.util.ssh import ssh_execute
import traceback
import time
import sys

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
    log.warning("AWS NOT ENABLED")


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
        self.db_mongo.remove({"cm_type": self.cm_type})

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

    ssh_ec2_rule = Ec2SecurityGroup.Rule(22, 22)

    config = None
    cm_user = None
    userinfo = None
    userid = None
    activated = False

    def __init__(self, collection="cloudmesh"):
        """initializes the cloudmesh mongo db. The name of the collection os passed."""

        # DEBUG
        try:
            _args = locals()
            del(_args['self'])
            log.debug("[{0}()] called with [{1}]".format(sys._getframe().f_code.co_name,
                                            str(_args)))
        except:
            pass

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
        # DEBUG
        try:
            _args = locals()
            if 'self' in _args:
                del(_args['self'])
            log.debug("[{0}()] called with [{1}]".format(sys._getframe().f_code.co_name,
                                            str(_args)))
        except:
            pass

        try:
            password = cm_config_server().get(
                "cloudmesh.server.mongo.collections.password.key")
            safe_credential = (self.userdb_passwd.find_one(
                {"cm_user_id": cm_user_id, "cloud": cloud}))["credential"]

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

        # DEBUG
        try:
            _args = locals()
            if 'self' in _args:
                del(_args['self'])
            log.debug("[{0}()] called with [{1}]".format(sys._getframe().f_code.co_name,
                                            str(_args)))
        except:
            pass

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
            if key not in cloud_config['credentials']:
                cloud_config['credentials'][key] = credential[key]

        #
        # THIS SEEMS TO BE A BUG???? sos = sierra openstack, why only sierra?
        #
        if (cloud_config['cm_type'] in ['openstack']) and (cloud_config['cm_label'] in ['sos', 'ios_havana']):
            cloud_config['credentials'][
                'OS_TENANT_NAME'] = self.active_project(cm_user_id)

        return cloud_config

    def get_cloud(self, cm_user_id, cloud_name, force=False):

        # DEBUG
        try:
            _args = locals()
            if 'self' in _args:
                del(_args['self'])
            log.debug("[{0}()] called with [{1}]".format(sys._getframe().f_code.co_name,
                                            str(_args)))
        except:
            pass

        cloud = None
        # do we recreate a cloud instance?
        # recreate only when user/tenant is changed for a certain cloud
        recreate = False
        cloud_info = self.get_cloud_info(cm_user_id, cloud_name)

        # credential = self.config.cloud(cloud_name)
        cm_type = cloud_info['cm_type']
        cm_type_version = cloud_info['cm_type_version']
        cm_service_url_type = 'publicURL'
        if 'cm_service_url_type' in cloud_info:
            cm_service_url_type = cloud_info['cm_service_url_type']
        credentials = cloud_info['credentials']
        # print "D",credentials

        # we can force an update
        if force:
            recreate = True
        # new user
        elif cm_user_id not in self.clouds:
            recreate = True
        # new cloud for that user
        elif cloud_name not in self.clouds[cm_user_id]:
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
                    if cm_type in ['openstack']:
                        cloud = provider(cloud_name, credentials, service_url_type=cm_service_url_type)
                    else:
                        cloud = provider(cloud_name, credentials)
                        
                    log.debug("Created new cloud instance for cloud name: %s, type: %s"
                              % (cloud_name, cm_type))
                    if cm_service_url_type == 'internalURL':
                        log.debug("The cloud is working in INTERNAL mode")
                    if cm_type in ['openstack', 'ec2']:
                        if cm_type in ['openstack']:
                            log.debug("\tfor tenant: %s" %
                                      credentials['OS_TENANT_NAME'])
                        if not cloud.auth():
                            cloud = None
                            log.error(
                                "Authentication Failed, cloud is not activated")

                    self.clouds[cm_user_id][
                        cloud_name].update({'manager': cloud})
                    if cloud is not None:
                        self.refresh(cm_user_id, [cloud_name], ['servers'])
                        if cm_type in ['openstack']:
                            secgroups = cloud.list_security_groups()[
                                'security_groups']
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
                                            log.debug("Ec2 security group rule allowing ssh exists for cloud: %s, type: %s, tenant: %s"
                                                      % (cloud_name, cm_type, credentials['OS_TENANT_NAME']))
                                    if not foundsshrule:
                                        iddefault = cloud.find_security_groupid_by_name(
                                            'default')
                                        cloud.add_security_group_rules(iddefault,
                                                                       [self.ssh_ec2_rule])
                                        log.debug("Added Ec2 security group rule to allow ssh for cloud: %s, type: %s, tenant: %s"
                                                  % (cloud_name, cm_type, credentials['OS_TENANT_NAME']))

            except Exception, e:
                cloud = None
                log.error(
                    "Cannot activate cloud {0} for {1}\n{2}".format(cloud_name, cm_user_id, e))
                print traceback.format_exc()
        return cloud

    def active_clouds(self, cm_user_id):
        ret_clouds = None

        # If the user has registered and activated some clouds from the web gui,
        # there will be entries in the db.
        user = self.db_defaults.find_one({'cm_user_id': cm_user_id})
        if 'activeclouds' in user:
            ret_clouds = user['activeclouds']
        else:
            # If activeclouds is empty in defaults, user collection will be
            # looked up.
            # As part of the user initialization, before the start of either
            # the web server or the command line shell, this should guarantee
            # that it exists in the db
            user = self.db_user.find_one({'cm_user_id': cm_user_id})
            if 'activeclouds' in user:
                ret_clouds = user['activeclouds']
        return ret_clouds

    def active_project(self, cm_user_id):
        # DEBUG
        try:
            _args = locals()
            if 'self' in _args:
                del(_args['self'])
            log.debug("[{0}()] called with [{1}]".format(sys._getframe().f_code.co_name,
                                            str(_args)))
        except:
            pass

        user = self.db_defaults.find_one({'cm_user_id': cm_user_id})
        return user['project']

    def activate(self, cm_user_id, cloudnames=None):

        # The cm_user_id should be ALWAYS set and passed through to this call
        # On Web gui the g.user.id has the username
        # On command line shell, we should maintain a global object/variable
        # similar to this upon the start of the shell, as though the user is
        # authenticated. However at this point we simply retrieve the name from
        # yaml file.
        # However for failsafe reason we do another check here.
        #
        if cm_user_id is None:
            cm_user_id = self.config.username()

        # the list of active clouds is always coming from Mongo.
        # In case of web gui, it is from the defaults db/collection as the user
        # will be required to register and activate some clouds before any
        # further action could be done.
        # In case of CLI, it could fail safe to the list from yaml file.
        #
        cloudnames = cloudnames or self.active_clouds(cm_user_id)

        if cloudnames:
            for cloud_name in cloudnames:
                log.info("Activating -> {0}".format(cloud_name))
                cloud = self.get_cloud(cm_user_id, cloud_name)
                if not cloud:
                    log.info(
                        "Activation of cloud {0} and user {1} Failed!".format(cloud_name, cm_user_id))
                else:
                    log.info("Activation of cloud {0} and user {1} Succeeded!".format(
                        cloud_name, cm_user_id))
        else:
            log.info(
                "No active clouds entries found in database so no clouds were activated!")

        self.activate_userinfo(cm_user_id)
        self.activated = True

    def activate_userinfo(self, cm_user_id):
        # Set userinfo
        from cloudmesh.user.cm_user import cm_user
        self.cm_user = cm_user()
        self.userinfo = self.cm_user.info(cm_user_id)
        self.userid = cm_user_id

    def get_userinfo(self, cm_user_id):
        if not self.userinfo:
            self.activate_userinfo(cm_user_id)
        return self.userinfo

    def check_activated(self):
        if not self.activated:
            log.error("Activation first!")
            return False
        return True

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
            log.info("-" * 80)
            log.info("Retrieving data for %s" % name)
            log.info("-" * 80)
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
                    self.db_clouds.remove(
                        {"cm_user_id": cm_user_id, "cm_cloud": name, "cm_kind": type})
                else:
                    self.db_clouds.remove({"cm_cloud": name, "cm_kind": type})

                for element in result:
                    # Stacks has different key name 'stack_name'
                    if type in ['t_stacks']:
                        t_name = 'stack_name'
                    else:
                        t_name = 'name'
                    id = "{0}-{1}-{2}".format(
                        name, type, result[element][t_name]).replace(".", "-")
                    # servers or security_groups is for each user.
                    # Stacks as well (10/17/2014)
                    if type in ['servers', 'e_security_groups', 't_stacks']:
                        result[element]['cm_user_id'] = cm_user_id

                    result[element]['cm_id'] = id
                    result[element]['cm_cloud'] = name
                    result[element]['cm_type'] = self.clouds[
                        cm_user_id][name]['cm_type']
                    result[element]['cm_type_version'] = self.clouds[
                        cm_user_id][name]['cm_type_version']
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
                    # print "HPCLOUD_DEBUG - AFTER DELETING PROBLEMATIC KEYS",
                    # result[element]

                    # exception.
                    if "_id" in result[element]:
                        del(result[element]['_id'])

                    self.db_clouds.insert(result[element])

                watch.stop(watch_name)
                print 'Store time:', watch.get(watch_name)

    """
    # See pbs_mongo in pbs directory
    # obsoleted in cm_mongo
    def get_pbsnodes(self, host):
        '''
        returns the data associated with pbsnodes from mongodb.
        :param host:
        '''
        data = self.db_pbsnodes.find({"pbs_host": host})
        return data
    """

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
                result = self.find(
                    {'cm_user_id': cm_user_id, 'cm_kind': kind, 'cm_cloud': name})
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

    def stacks(self, clouds=None, cm_user_id=None):
        '''
        returns all stacks from clouds
        '''
        return self._get_kind('t_stacks', clouds, cm_user_id)

    # need to make sure other clouds have the same flavor dict as in openstack
    # otherwise will need to put this into the openstack iaas class
    def flavor_name_to_id(self, cloud, flavor_name):
        for key, value in self.flavors([cloud])[cloud].iteritems():
            if value["name"] == flavor_name:
                return key
        return -1

    def flavor(self, cloudname, flavorname, cm_user_id=None):
        """Get a single flavor on a given cloud"""
        try:
            return self.flavors([cloudname])[cloudname][flavorname]
        except:
            for key, value in \
                    self.flavors([cloudname])[cloudname].iteritems():
                if value['name'] == flavorname:
                    return value
            return -1

    def image(self, cloudname, imagename, cm_user_id=None):
        """Get a single image on a given cloud"""
        for key, value in self.images([cloudname])[cloudname].iteritems():
            if value['name'] == imagename:
                return value
        return -1

    def default(self, cloudname, attribute, value, cm_user_id=None):
        """Set a default value on a given type between 'image' or 'flavor'"""

        if not cm_user_id:
            cm_user_id = self.userid

        defaults = self.cm_user.get_defaults(cm_user_id)
        if attribute == "image":
            # If the value is a python dict contains image information,
            # we use id in the dict, otherwise we treat it as a string.
            try:
                defaults['images'][cloudname] = value['id']
            except:
                defaults['images'][cloudname] = str(value)

            self.cm_user.set_default_attribute(cm_user_id, "images",
                                               defaults['images'])
        elif attribute == "flavor":
            try:
                defaults['flavors'][cloudname] = value['id']
            except:
                defaults['flavors'][cloudname] = str(value)

            self.cm_user.set_default_attribute(cm_user_id, "flavors",
                                               defaults['flavors'])
        return self.cm_user.get_defaults(cm_user_id)

    def start(self, cloud, cm_user_id, prefix=None, index=None, flavor=None,
              image=None, key=None, meta=None):
        """Launch a new VM instance with a default setting for flavor, image and
        key name"""

        

        arg_flavor = flavor
        arg_image = image
        
        if not self.check_activated():
            return None

        userinfo = self.get_userinfo(cm_user_id)
        prefix = prefix or userinfo['defaults']['prefix']
        index = index or userinfo['defaults']['index']

        
        try:
            flavor = flavor['id']
        except:
            flavor = self.flavor(cloud, arg_flavor)
            if flavor == -1:
                flavor = arg_flavor or userinfo['defaults']['flavors'][cloud]
            else:
                flavor = flavor['id']
                                                
        try:
            image = image['id']
        except:
            image = self.image(cloud, arg_image)
            if image == -1:
                image = arg_image or userinfo['defaults']['images'][cloud]
            else:
                image = image['id']

        # or image = '02cf1545-dd83-493a-986e-583d53ee3728' # ubuntu-14.04
        key = key or "%s_%s" % (cm_user_id, userinfo['defaults']['key'])
        meta = meta or {'cm_owner': cm_user_id}

        # Launch a vm instance
        result = self.vm_create(cloud, prefix, index, flavor, image, key, meta,
                                cm_user_id)

        # increase index after the completion of vm_create()
        next_index = int(index) + 1
        self.cm_user.set_default_attribute(cm_user_id, "index", next_index)
        self.userinfo['defaults']['index'] = str(next_index)
        #
        # BUG flavor name needs to be returned
        #
        result["flavor"] = self.flavors([cloud])[cloud][flavor]['name']
        result["image"] = self.images([cloud])[cloud][image]['name']
        
        return result

    def vm_create(self,
                  cloud,
                  prefix,
                  index,
                  vm_flavor,
                  vm_image,
                  key,
                  meta,
                  cm_user_id,
                  givenvmname=None):
        '''
        BUG: missing security group
        '''
        cloudmanager = self.clouds[cm_user_id][cloud]["manager"]
        if givenvmname is None:
            name = "%s_%s" % (prefix, index)
        else:
            name = givenvmname

        result = cloudmanager.vm_create(name=name, flavor_name=vm_flavor, image_id=vm_image, key_name=key, meta=meta)
        result["name"] = name
        result["flavor_id"] = vm_flavor
        result["image_id"] = vm_image
        result["cm_user_id"] = cm_user_id
        result["key"] = key
        result["cloud"] = cloud
        return result

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
        if givenvmname is None:
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

            # Retry
            _max = 5  # times
            _interval = 1  # second
            _expected = {'msg': 'success'}
            for i in range(_max):
                ret = cloudmanager.assign_public_ip(server, ip)
                # ret is
                # {u'badRequest': {u'message': u'No nw_info cache associated with
                # instance', u'code': 400}}
                # or
                # {'msg': 'success'}
                if ret == _expected:
                    break
                time.sleep(_interval)
            ret = ip
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

    def delete(self, cloud, server, cm_user_id):
        """Delete vm instances and release unused public ips"""

        # Hyungro Lee - Sep 4th, 2014
        res1 = self.vm_delete(cloud, server, cm_user_id)
        time.sleep(5)
        res2 = self.release_unused_public_ips(cloud, cm_user_id)
        res = {"vm_delete": res1, "release_unused_public_ips": res2}
        return res

    def vm_delete(self, cloud, server, cm_user_id):
        cloudmanager = self.clouds[cm_user_id][cloud]["manager"]
        return cloudmanager.vm_delete(server)

    def vmname(self, prefix=None, idx=None, cm_user_id=None):
        """Return a vm name to use next time. prefix or index can be
        given to update a vm name (optional)

        Args:
            prefix (str, optional): the name of prefix
            idx (int, str, optional): the index to increment. This can be a
            digit or arithmetic e.g. +5 or -3 can be used

        """
        userinfo = self.get_userinfo(cm_user_id)
        cm_user_id = cm_user_id or self.userid
        userinfo['defaults']['prefix'] = prefix or \
            userinfo['defaults']['prefix']
        if idx:
            if str(idx).isdigit():
                userinfo['defaults']['index'] = idx
            else:
                userinfo['defaults']['index'] = \
                    eval(str(userinfo['defaults']['index']) + idx)
        self.cm_user.set_defaults(cm_user_id, userinfo['defaults'])

        self.userinfo = self.cm_user.info(cm_user_id)
        return "%(prefix)s_%(index)s" % self.userinfo['defaults']

    def vmname_next(self):
        return self.vmname(idx="+1")

    def ssh_execute(self, ipaddr, username="ubuntu", command="ls -al", pkey=None):

        try:
            result = ssh_execute(username, ipaddr, command, pkey)
            return result
        except:
            err = sys.exc_info()[0]
            log.error("Can not execute ssh on {0}:{1}".format(ipaddr, err))
            raise err

    def wait(self, ipaddr, username="ubuntu", command=None, pkey=None, interval=5, retry=10):

        command = "echo $USER"
        success = False
        for i in range(retry):
            print str(i) + " try to execute via ssh..."
            try:
                result = self.ssh_execute(ipaddr, username=username,
                                          command=command, pkey=pkey)
                success = username in result
                return success
            except:
                err = sys.exc_info()[0]
                time.sleep(interval)
        raise err
        #
        # TODO: not sure if we can get rid of the raise error function
        #
        return success

class cm_mongo_status(object):

    def __init__(self):
        self.conn = DBConnFactory.getconn("admin")

    def serverStatus(self):
        return self.conn.command("serverStatus")

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

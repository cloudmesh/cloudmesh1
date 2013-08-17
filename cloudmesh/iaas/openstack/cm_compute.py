#! /usr/bin/env python

#
# see also http://docs.openstack.org/cli/quick-start/content/nova-cli-reference.html
#
import requests
from requests.auth import AuthBase

import sys
from pprint import pprint
import json

from collections import OrderedDict
import iso8601
import sys
import time
import base64
import urllib
import httplib
import json
import os
from urlparse import urlparse

sys.path.insert(0, '../..')

from sh import curl

from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)


from sh import fgrep
import novaclient
from sh import nova

# from cm_credential import credentials
from cloudmesh.iaas.openstack.cm_table import table as cm_table
from cloudmesh.config.cm_config import cm_config
from cloudmesh.iaas.ComputeBaseType import ComputeBaseType
from cloudmesh.cm_profile import cm_profile

from novaclient.v1_1 import client
from novaclient.v1_1 import security_groups
from novaclient.v1_1 import security_group_rules


def donotchange(fn):
    return fn


class openstack(ComputeBaseType):

    #: the type of the cloud. It is "openstack"
    type = "openstack"   # global var

    #: a dict with the flavors
    flavors = {}         # global var

    #: a dict with the images
    images = {}          # global var

    #: a dict with the servers
    servers = {}         # global var

    #: a dict with the users
    users = {}         # global var
    
    #: a dict containing the credentionls read with cm_config
    credential = None    # global var

    #: a unique label for the clous
    label = None         # global var

    # cm_type = "openstack"
    # name = "undefined"

    #: This is the cloud, should be internal though with _
    cloud = None         # internal var for the cloud client in openstack

    #: The user id
    user_id = None       # internal var

    _nova = nova

    #
    # initialize
    #
    # possibly make connext seperate
    def __init__(self, label, credential=None):
        """
        initializes the openstack cloud from a defould novaRC file
        locates at ~/.futuregrid.org/cloudmesh.yaml. However if the
        parameters are provided it will instead use them
        """
        self.clear()
        self.label = label
        self.credential = credential
        
        config = cm_config()
        if credential is None:
            self.credential = config.credential(label)
        else:
            self.credential = credential
        self.connect()

    def clear(self):
        """
        clears the data of this openstack instance, a new connection
        including reading the credentials and a refresh needs to be
        called to obtain again data.
        """
        # Todo: we may just use the name of the class instead as the type
        self._clear()
        self.type = "openstack"

    def connect(self):
        """
        establishes a connection to the OpenStack cloud,
        e.g. initializes the needed components to conduct subsequent
        queries.
        """
        
        if 'OS_CACERT' in self.credential:
            self.cloud = client.Client(
                                       self.credential['OS_USERNAME'],
                                       self.credential['OS_PASSWORD'],
                                       self.credential['OS_TENANT_NAME'],
                                       self.credential['OS_AUTH_URL'],
                                       cacert=self.credential['OS_CACERT']
                                       )
        else:
            self.cloud = client.Client(
                                       self.credential['OS_USERNAME'],
                                       self.credential['OS_PASSWORD'],
                                       self.credential['OS_TENANT_NAME'],
                                       self.credential['OS_AUTH_URL'],
                                       )
            
        self.auth_token = self.get_token(self.credential)

    # BIG BUG, MUST BE DICT
    # config should have dict as parameter
    def config(self, label, dict=None):
        """
        reads in the configuration file if specified, and does some
        internal configuration.
        """
        self.label = label
        if dict is None:
            config = cm_config()
            self.credential = config.get(label, expand=True)

            # print self.credential

            # self.user_id = self.credential['OS_USER_ID']
            # self.credential = credentials(label)
        else:
            # TODO: BUG: THIS PROBABLY CAN BE REMOVED AS PART OF THE CONFIG, cars do not exist or are self?
            self.credential = {}
            self.credential['OS_USERNAME'] = username
            self.credential['OS_PASSWORD'] = password
            self.credential['OS_AUTH_URL'] = authurl
            self.credential['label'] = label
            self.credential['OS_TENANT_NAME'] = project
            
            self.credential['OS_CACERT'] = cacert
        """
        self._nova = nova.bake("--os-username",    self.credential.username,
                               "--os-password",    self.credential.password,
                               "--os-auth-url",    self.credential.url,
                               "--os-tenant-name", self.credential.project)
        """

    #
    # TESTS
    #

    def intro(self, what):
        """ used to find some methods form novaclient"""
        import inspect

        print 70 * "="
        print "class ", what.__class__.__name__, ":"
        list = inspect.getmembers(what, predicate=inspect.ismethod)
        for element in list:
            print "    ", element[0]
        try:
            pp.pprint(what.__dict__)
        except:
            return

    def novaclient_dump(self):
        """a test function that is temporarily here to visualize novaclient output"""

        self.intro(self.cloud)
        self.intro(self.cloud.services)
        self.intro(self.cloud.servers)
        self.intro(self.cloud.client)

        self.intro(self.cloud.agents)
        self.intro(self.cloud.aggregates)
        self.intro(self.cloud.availability_zones)
        self.intro(self.cloud.certs)
        self.intro(self.cloud.client)
        self.intro(self.cloud.cloudpipe)
        self.intro(self.cloud.coverage)
        self.intro(self.cloud.dns_domains)
        self.intro(self.cloud.dns_entries)
        self.intro(self.cloud.fixed_ips)
        self.intro(self.cloud.flavor_access)
        self.intro(self.cloud.flavors)
        self.intro(self.cloud.floating_ip_pools)
        self.intro(self.cloud.floating_ips)
        self.intro(self.cloud.floating_ips_bulk)
        self.intro(self.cloud.fping)
        self.intro(self.cloud.hosts)
        self.intro(self.cloud.hypervisors)
        self.intro(self.cloud.images)
        self.intro(self.cloud.keypairs)
        self.intro(self.cloud.limits)
        self.intro(self.cloud.networks)
        self.intro(self.cloud.os_cache)
        self.intro(self.cloud.project_id)
        self.intro(self.cloud.quota_classes)
        self.intro(self.cloud.quotas)
        self.intro(self.cloud.security_group_rules)
        self.intro(self.cloud.security_groups)
        self.intro(self.cloud.servers)
        self.intro(self.cloud.services)
        self.intro(self.cloud.usage)
        self.intro(self.cloud.virtual_interfaces)
        self.intro(self.cloud.volume_snapshots)
        self.intro(self.cloud.volume_types)
        self.intro(self.cloud.volumes)

        now = datetime.now()

    #
    # FIND USER ID
    #

    def find_user_id(self, force=False):
        """
        this method returns the user id and stores it for later use.
        """
        config = cm_config()

        if not force:
            try:
                self.user_id = self.credential['OS_USER_ID']
                return self.user_id
            except:
                self.user_id = None
                print "OS_USER_ID not set"

        self.auth_token = self.get_token()
        self.user_id = self.auth_token['access']['user']['id']
        return self.user_id

    def get_token(self, credential=None):

        if credential is None:
            credential = self.credential
            
        param = {"auth": { "passwordCredentials": {
                                "username": credential['OS_USERNAME'],
                                "password":credential['OS_PASSWORD'],
                            },
                           "tenantName":credential['OS_TENANT_NAME']
                        }
             }
        url = "{0}/tokens".format(credential['OS_AUTH_URL'])
        headers = {'content-type': 'application/json'}

        verify = False
        
        if 'OS_CACERT' in credential: 
            if credential['OS_CACERT'] is not None and \
               credential['OS_CACERT'] != "None" and \
               os.path.isfile(credential['OS_CACERT']):            
                verify=credential['OS_CACERT']
                
        r = requests.post(url,
                          data=json.dumps(param),
                          headers=headers, 
                          verify=verify)

                                          
        return r.json()
    

    def _get_service(self, type, token=None):
        if token is None:
            token = self.auth_token
            
        for service in token['access']['serviceCatalog']:
            if service['type'] == type:
                break
        return service
    
    def _get_compute_service(self, token=None):
        return self._get_service("compute") 
    
    
    def _get(self, msg, token=None, url=None, credential=None, type=None,urltype=None):
        if urltype is None:
            urltype = 'publicURL'
        if credential is None:
            credential = self.credential
        if token is None:
            token = self.auth_token
        if url is None:
            conf = self._get_conf(type)
            url = conf[urltype]   
        url = "{0}/{1}".format(url, msg)

        headers = {'X-Auth-Token': token['access']['token']['id']}
        r = requests.get(url, headers=headers, verify=credential['OS_CACERT'])
        return r.json()

    # http

    def _get_conf(self,type):
        """what example %/servers"""
        if type is None:
            type = "compute"
        compute_service = self._get_service(type)
        #pp.pprint(compute_service)
        conf = {}
        conf['publicURL'] = str(compute_service['endpoints'][0]['publicURL'])
        conf['adminURL'] = str(compute_service['endpoints'][0]['adminURL'])
        conf['token'] = str(self.auth_token['access']['token']['id'])
        return conf


    def get_tenants(self,credential=None):
        """get the tenants dict for the vm with the given id"""
        if credential is None:
            p = cm_profile()
            credential = p.server.config["keystone"]["sierra-openstack-grizzly"]
    
        msg = "tenants"
        return self._get(msg,credential=credential, type="keystone")

    def get_users(self,credential=None):
        """get the tenants dict for the vm with the given id"""
        if credential is None:
            
            p = cm_profile()
            name = self.label
            credential = p.server.config["keystone"][name]
        
        cloud = openstack(name, credential=credential)
        msg = "users"
        return cloud._get(msg,credential=credential, type="keystone",urltype='adminURL')
        
    def get_meta(self, id):
        """get the metadata dict for the vm with the given id"""
        msg = "/servers/%s/metadata" % (id)
        return self._get("%s" + msg)

    def set_meta(self, id, metadata, replace=False):
        """set the metadata for the given vm with the id"""
        conf = self._get_conf()
        conf['serverid'] = id
        if replace:
            conf['set'] = "PUT"
        else:
            conf['set'] = "POST"

        apiurlt = urlparse(conf['publicURL'])
        url2 = apiurlt[1]

        params2 = '{"metadata":' + str(metadata).replace("'", '"') + '}'

        headers2 = {"X-Auth-Token": conf[
            'token'], "Accept": "application/json", "Content-type": "application/json"}

        print "%%%%%%%%%%%%%%%%%%"
        pp.pprint(conf)
        print "%%%%%%%%%%%%%%%%%%"
        print "PARAMS", params2
        print "HEADERS", headers2
        print "API2", apiurlt[2]
        print "API1", apiurlt[1]
        print "ACTIVITY", conf['set']
        print "ID", conf['serverid']
        print "####################"

        conn2 = httplib.HTTPConnection(url2)

        conn2.request(conf['set'], "%s/servers/%s/metadata" %
                      (apiurlt[2], conf['serverid']), params2, headers2)

        response2 = conn2.getresponse()
        data2 = response2.read()
        dd2 = json.loads(data2)

        conn2.close()
        return dd2

    #
    # refresh
    #
    def _get_users_dict(self):
        result = self.get_users()
        return result['users']
    
    def _update_users_dict(self,information):        
        user = information
        user['cloud'] = self.label 
        id = "{0}-{1}".format(user['id'],self.label)   
        return (id, user)

    def _get_tenants_dict(self):
        result = self.get_tenants()
        return result['tenants']
    
    def _update_tenants_dict(self,information):        
        tenants = information
        id = "{0}-{1}".format(tenents['id'],self.label)   
        tenants['cloud'] = self.label 
        return (id, tenants)
    
    def _get_images_dict(self):
        return self.cloud.images.list(detailed=True)

    def _update_images_dict(self, information):
        image = information.__dict__
        id = image['id']
        # clean not neaded info
        # del image['manager']
        del image['_info']
        del image['_loaded']
        # del information.links
        return (id, image)

    def _get_flavors_dict(self):
        return self.cloud.flavors.list()

    def _update_flavors_dict(self, information):
        flavor = information.__dict__
        # clean not neaded info
        # del flavor['manager']
        del flavor['_info']
        del flavor['_loaded']
        # del information.links
        id = information.name
        return (id, flavor)

    def _get_servers_dict(self):
        return self.cloud.servers.list(detailed=True)

    def _update_servers_dict(self, information):
        vm = information.__dict__
        # pp.pprint (vm)
        # pp.pprint(vm)
        delay = vm['id']
        # del vm['manager']
        del vm['_info']
        del vm['_loaded']
        # del information.links
        id = vm['id']
        return (id, vm)

    #
    # security Groups of VMS
    #
    # GVL: review
    # how does this look for azure and euca? Should there be a general framework for this in the BaseCloud class
    # based on that analysis?
    #
    # comments of wht these things do and how they work are missing
    #
    def createSecurityGroup(self, default_security_group, description="no-description"):
        """
        comment is missing
        """
        protocol = ""
        ipaddress = ""
        max_port = ""
        min_port = ""
        default_security_group_id = self.cloud.security_groups.create(
            default_security_group, description)
        default_security_group_id = default_security_group_id.id

        config_security = cm_config()
        yamlFile = config_security.get()
        ruleNames = yamlFile['security'][
            'security_groups'][default_security_group]
        for ruleName in ruleNames:
            rules = yamlFile['security']['rules'][ruleName]
            for key, value in rules.iteritems():
                if 'protocol' in key:
                    protocol = value
                elif 'max_port' in key:
                    max_port = value
                elif 'min_port' in key:
                    min_port = value
                else:
                    ip_address = value

            self.cloud.security_group_rules.create(
                default_security_group_id, protocol, min_port,
                max_port, ip_address)
        return default_security_group

    # GVL: review
    # how does this look for azure and euca? Should there be a general framework for this in the BaseCloud class
    # based on that analysis?
    #
    # comments of wht these things do and how they work are missing
    def checkSecurityGroups(self):
        """
        TODO: comment is missing
        """
        config_security = cm_config()
        names = {}

        securityGroups = self.cloud.security_groups.list()

        for securityGroup in securityGroups:

            names[securityGroup.name] = securityGroup.id

        yamlFile = config_security.get()
        if yamlFile.has_key('security'):
            default_security_group = yamlFile['security']['default']
        else:
            return None
        # default_security_group_id=names[default_security_group]

        if default_security_group in names:
            return default_security_group

        else:
            return self.createSecurityGroup(default_security_group)

    # GVL: review
    # how does this look for azure and euca? Should there be a general framework for this in the BaseCloud class
    # based on that analysis?
    #
    # comments of wht these things do and how they work are missing
    #
    def get_public_ip(self):
        """
        TODO: comment is missing
        """
        return self.cloud.floating_ips.create()

    # GVL: review
    # how does this look for azure and euca? Should there be a general framework for this in the BaseCloud class
    # based on that analysis?
    #
    # comments of wht these things do and how they work are missing
    #
    def assign_public_ip(self, serverid, ip):
        """
        comment is missing
        """
        self.cloud.servers.add_floating_ip(serverid, ip)

    #
    # set vm meta
    #

    def vm_set_meta(self, vm_id, metadata):
        """an experimental class to set the metadata"""
        print metadata
        is_set = 0

        # serverid = self.servers[id]['manager']

        while not is_set:
            try:
                print "set ",  vm_id, "to set", metadata

                result = self.cloud.servers.set_meta(vm_id, metadata)
                # body = {'metadata': metadata}
                # print body
                # result = self.cloud.servers._create("/servers/%s/metadata" %
                # vm_id, body, "metadata")
                print result
                is_set = 1
            except Exception, e:
                print "ERROR", e
                time.sleep(2)

        print result

    #
    # create a vm
    #
    def vm_create(self,
                  name=None,
                  flavor_name=None,
                  image_id=None,
                  security_groups=None,
                  key_name=None,
                  meta=None):
        """
        create a vm with the given parameters
        """

        if not key_name is None:
            if not self.check_key_pairs(key_name):
                config = cm_config()
                dict_t = config.get()
                key = dict_t['keys']['keylist'][key_name]
                if not 'ssh-rsa' in key and not 'ssh-dss' in key:
                    key = open(key, "r").read()
                self.upload_key_pair(key, key_name)

        config = cm_config()

        if flavor_name is None:
            flavor_name = config.default(self.label)['flavor']

        if image_id is None:
            image_id = config.default(self.label)['image']

        # print "CREATE>>>>>>>>>>>>>>>>"
        # print image_id
        # print flavor_name

        vm_flavor = self.cloud.flavors.find(name=flavor_name)
        vm_image = self.cloud.images.find(id=image_id)

        if key_name is None:
            vm = self.cloud.servers.create(name,
                                           flavor=vm_flavor,
                                           image=vm_image,
                                           security_groups=security_groups,
                                           meta=meta
                                           )
        else:
            # bug would passing None just work?
            vm = self.cloud.servers.create(name,
                                           flavor=vm_flavor,
                                           image=vm_image,
                                           key_name=key_name,
                                           security_groups=security_groups,
                                           meta=meta
                                           )
        delay = vm.user_id  # trick to hopefully get all fields
        data = vm.__dict__
        del data['manager']
        # data['cm_name'] = name
        # data['cm_flavor'] = flavor_name
        # data['cm_image'] = image_id
        # return {str(data['id']):  data}
        # should probably just be
        return data

    #
    # delete vm(s)
    #

    def vm_delete(self, id):
        """
        delete a single vm and returns the id
        """

        vm = self.cloud.servers.delete(id)
        # return just the id or None if its deleted
        return vm

    @donotchange
    def vms_delete(self, ids):
        """
        delete many vms by id. ids is an array
        """
        for id in ids:
            print "Deleting %s" % self.servers[id]['name']
            vm = self.vm_delete(id)

        return ids

    #
    # list user images
    #

    @donotchange
    def vms_user(self, refresh=False):
        """
        find my vms
        """
        user_id = self.find_user_id()

        time_stamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
        if refresh:
            self.refresh("servers")

        result = {}

        for (key, vm) in self.servers.items():
            if vm['user_id'] == self.user_id:
                result[key] = vm

        return result

    #
    # list project vms
    #

    def vms_project(self, refresh=False):
        """
        find my vms that arein this project. this method was needed for openstack essex deployment on fg
        """
        user_id = self.find_user_id()

        time_stamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
        if refresh:
            self.refresh("images")

        result = {}
        for (key, vm) in self.servers.items():
            result[key] = vm

        return result

    #
    # delete images from a user
    #

    @donotchange
    def vms_delete_user(self):
        """
        find my vms and delete them
        """

        user_id = self.find_user_id()
        vms = self.find('user_id', user_id)
        self.vms_delete(vms)

        return

    #
    # find
    #

    @donotchange
    def find(self, key, value=None):
        """find my vms"""
        ids = []
        if key == 'user_id' and value is None:
            value = self.user_id
        for (id, vm) in self.servers.items():
            if vm[str(key)] == value:
                ids.append(str(vm['id']))

        return ids

    #
    # rename
    #

    def rename(self, old, new, id=None):
        """rename the vm with the given name old to new. If more than
        one exist with the same name only the first one will be
        renamed. consider moving the code to the baseclass."""
        all = self.find('name', old)
        print all
        if len(all) > 0:
            id = all[0]
            vm = self.cloud.servers.update(id, new)
        return

    # TODO: BUG WHY ARE TGERE TWO REINDEX FUNCTIONS?

    @donotchange
    def reindex(self, prefixold, prefix, index_format):
        all = self.find('user_id')
        counter = 1
        for id in all:
            old = self.servers[id]['name']
            new = prefix + index_format % counter
            print "Rename %s -> %s, %s" % (old, new, self.servers[id]['key_name'])
            if old != new:
                vm = self.cloud.servers.update(id, new)
            counter += 1


    #
    # TODO
    #
    """
    refresh just a specific VM
    delete all images that follow a regualr expression in name
    look into sort of images, flavors, vms
    """

    #
    # EXTRA
    #
    # will be moved into one class

    @donotchange
    def table_col_to_dict(self, body):
        """converts a given list of rows to a dict"""
        result = {}
        for element in body:
            key = element[0]
            value = element[1]
            result[key] = value
        return result

    @donotchange
    def table_matrix(self, text, format=None):
        """converts a given pretty table to a list of rows or a
        dict. The format can be specified with 'dict' to return a
        dict. otherwise it returns an array"""
        lines = text.splitlines()
        headline = lines[0].split("|")
        headline = headline[1:-1]
        for i in range(0, len(headline)):
            headline[i] = str(headline[i]).strip()

        lines = lines[1:]

        body = []

        for l in lines:
            line = l.split("|")
            line = line[1:-1]
            entry = {}
            for i in range(0, len(line)):
                line[i] = str(line[i]).strip()
                if format == "dict":
                    key = headline[i]
                    entry[key] = line[i]
            if format == "dict":
                body.append(entry)
            else:
                body.append(line)
        if format == 'dict':
            return body
        else:
            return (headline, body)

    #
    # CLI call of ussage
    #

    # will be moved into utils
    @donotchange
    def parse_isotime(self, timestr):
        """Parse time from ISO 8601 format"""
        try:
            return iso8601.parse_date(timestr)
        except iso8601.ParseError as e:
            raise ValueError(e.message)
        except TypeError as e:
            raise ValueError(e.message)

    def usage(self, start, end, format='dict'):
        """ returns the usage information of the tennant"""

        # print 70 * "-"
        # print self.cloud.certs.__dict__.get()
        # print 70 * "-"

        # tenantid = "member"  # not sure how to get that
        iso_start = self.parse_isotime(start)
        iso_end = self.parse_isotime(end)
        # print ">>>>>", iso_start, iso_end
        # info = self.cloud.usage.get(tenantid, iso_start, iso_end)

        # print info.__dict__
        # sys.exit()

        (start, rest) = start.split("T")  # ignore time for now
        (end, rest) = end.split("T")  # ignore time for now
        result = fgrep(
            self._nova("usage", "--start", start, "--end", end), "|")

        (headline, matrix) = self.table_matrix(result)
        headline.append("Start")
        headline.append("End")
        matrix[0].append(start)
        matrix[0].append(end)

        if format == 'dict':
            result = {}
            for i in range(0, len(headline)):
                result[headline[i]] = matrix[0][i]
            return result
        else:
            return (headline, matrix[0])

    #
    # CLI call of absolute-limits
    #
    # def limits(self):
    #    conf = get_conf()
    #    return _get(conf, "%s/limits")

    def limits(self):
        """ returns the usage information of the tennant"""

        list = []

        info = self.cloud.limits.get()
        del info.manager
        rates = info.__dict__['_info']['rate']

        for rate in rates:
            limit_set = rate['limit']
            print limit_set
            for limit in limit_set:
                list.append(limit)

        return list

    def check_key_pairs(self, key_name):
        """simple check to see if a keyname is in the keypair list"""
        allKeys = self.cloud.keypairs.list()
        for key in allKeys:
            if key.name in key_name:
                return True
        return False

    #
    # Upload Key Pair
    #
    def upload_key_pair(self, publickey, name):
        """ Uploads key pair """

        try:
            self.cloud.keypairs.create(name, publickey)
        except Exception, e:
            return 1, e

        return (0, 'Key added successfully')

    #
    # Delete Key Pair
    #
    def delete_key(self, name):
        """ delets key pair """

        try:
            self.cloud.keypairs.delete(name)
        except Exception, e:
            return (1, e)

        return (0, 'Key deleted successfully')

    #
    # List Security Group
    #
    def sec_grp_list(self):
        """ lists all security groups """
        try:
            return self.cloud.security_groups.list()
        except Exception, e:
            print e

    states = [
        "ACTIVE",
        "ERROR",
        "BUILDING",
        "PAUSED",
        "SUSPENDED",
        "STOPPED",
        "DELETED",
        "RESCUED",
        "RESIZED",
        "SOFT_DELETED"
    ]

    def display(self, states, userid):
        """ simple or on states and check if userid. If userid is None
        all users will be marked. A new variable cm_display is
        introduced manageing if a VM should be printed or not"""

        for (id, vm) in self.servers.items():
            vm['cm_display'] = vm['status'] in states
            if userid is not None:
                vm['cm_display'] = vm['cm_display'] and (
                    vm['user_id'] == userid)

    def display_regex(self, state_check, userid):

        print state_check
        for (id, vm) in self.servers.items():
            vm['cm_display'] = eval(state_check)
            #            vm['cm_display'] = vm['status'] in states
            if userid is not None:
                vm['cm_display'] = vm['cm_display'] and (
                    vm['user_id'] == userid)


#
# MAIN FOR TESTING
#
if __name__ == "__main__":

    """
    cloud = openstack("india-openstack")

    name ="%s-%04d" % (cloud.credential["OS_USERNAME"], 1)
    out = cloud.vm_create(name, "m1.tiny", "6d2bca76-8fff-4d57-9f29-50378539b4fa")
    pp.pprint(out)

    """

    cloud = openstack("grizzly-openstack")
    keys = cloud.list_key_pairs()
    for key in keys:
        print key.name
    """
    print cloud.find_user_id()

    """

    """
    for i in range (1,3):
        name ="%s-%04d" % (cloud.credential["OS_USERNAME"], i)
        out = cloud.vm_create(name, "m1.tiny", "6d2bca76-8fff-4d57-9f29-50378539b4fa")
        pp.pprint(out)
    """

    """
    print cloud.find('name', name)
    """

    # cloud.rename("gvonlasz-0001","gregor")

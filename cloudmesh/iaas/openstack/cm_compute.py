#! /usr/bin/env python

#
# see also http://docs.openstack.org/cli/quick-start/content/nova-cli-reference.html
#

import requests
from requests.auth import AuthBase

from collections import OrderedDict
from datetime import datetime, timedelta
import iso8601
import sys
import time
import base64
import urllib
import httplib
import json
import os
from pprint import pprint
from urlparse import urlparse

from sh import fgrep
from sh import nova

# from cm_credential import credentials
from cloudmesh.util.cm_table import cm_table
from cloudmesh.config.cm_config import cm_config
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.iaas.ComputeBaseType import ComputeBaseType
from cloudmesh.iaas.Ec2SecurityGroup import Ec2SecurityGroup
from cloudmesh.cm_profile import cm_profile
from cloudmesh.util.logger import LOGGER

import novaclient
from novaclient.openstack.common import strutils

log = LOGGER(__file__)
    
def donotchange(fn):
    return fn


class openstack(ComputeBaseType):

    # : the type of the cloud. It is "openstack"
    type = "openstack"  # global var

    # : a dict with the images
    images = {}  # global var

    # : a dict with the images
    images = {}  # global var

    # : a dict with the servers
    servers = {}  # global var

    # : a dict with the users
    users = {}  # global var

    # : a dict containing the credentionls read with cm_config
    # credential = None  # global var
    user_credential = None  # global var
    admin_credential = None

    user_token = None
    admin_token = None


    # : a unique label for the clous
    label = None  # global var

    # cm_type = "openstack"
    # name = "undefined"

    # : This is the cloud, should be internal though with _
    cloud = None  # internal var for the cloud client in openstack
    keystone = None

    # : The user id
    user_id = None  # internal var

    _nova = nova

    #
    # initialize
    #
    # possibly make connext seperate
    def __init__(self, label, credential=None, admin_credential=None):
        """
        initializes the openstack cloud from a file
        located at ~/.futuregrid.org/cloudmesh.yaml.
        However if a credential dict is used it is used instead
        """
        self.clear()
        self.label = label

        user_credential = credential  # HACK to avoid changes in older code
        self.user_credential = user_credential
        self.admin_credential = admin_credential
        
        if user_credential is None:
            try:
                self.compute_config = cm_config()
                self.user_credential = self.compute_config.credential(label)
            except:
                log.error("No user credentail found! Please check your cloudmesh.yaml file.")
                #sys.exit(1)
            

        if admin_credential is None:
            try:
                self.admin_credential = cm_config_server().get("keystone", label)
            except:
                log.error("No admin credentail found! Please check your cloudmesh_server.yaml file.")
            
        self.connect()

    def clear(self):
        """
        clears the data of this openstack instance, a new connection
        including reading the credentials and a refresh needs to be
        called to obtain again data.
        """
        # Todo: we may just use the name of the class instead as the type
        self._clear()
        self.user_token = None
        self.admin_token = None
        self.user_credentials = None
        self.admin_credentials = None
        self.type = "openstack"



    def connect(self):
        """
        creates tokens for a connection
        """
        if self.user_credential is None:
            log.error("error connecting to openstack compute, credential is None")
        else:
            self.user_token = self.get_token(self.user_credentials)

        # check if keystone is defined, and if failed print log msg
        #
        if self.admin_credential is None:
            log.error("error connecting to openstack compute, credential is None")
        else:
            self.admin_token = self.get_token(self.admin_credential)


    def get_token(self, credential=None):

        if credential is None:
            credential = self.user_credential

        print "GET CRED", credential

        param = {"auth": { "passwordCredentials": {
                                "username": credential['OS_USERNAME'],
                                "password": credential['OS_PASSWORD'],
                            },
                           "tenantName":credential['OS_TENANT_NAME']
                        }
             }
        url = "{0}/tokens".format(credential['OS_AUTH_URL'])

        print "URL", url

        headers = {'content-type': 'application/json'}

        verify = False

        if 'OS_CACERT' in credential:
            if credential['OS_CACERT'] is not None and \
               credential['OS_CACERT'] != "None" and \
               os.path.isfile(credential['OS_CACERT']):
                verify = credential['OS_CACERT']


        print "PARAM", json.dumps(param)
        print "HEADER", headers
        print "VERIFY", verify

        r = requests.post(url,
                          data=json.dumps(param),
                          headers=headers,
                          verify=verify)


        return r.json()


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
                self.user_id = self.user_credential['OS_USER_ID']
                return self.user_id
            except:
                self.user_id = None
                print "OS_USER_ID not set"

        self.user_token = self.get_token()
        self.user_id = self.user_token['access']['user']['id']
        return self.user_id

    #not working yet
    #user role is disalowed to execute this by policy setting
    #admin role gives uninformative error
    def get_server_usage(self, serverid):
        apiurl = "servers/%s/diagnostics" % serverid
        return self._get(msg=apiurl,kind='admin',urltype='adminURL')
    
    def _get_service(self, kind="user"):

        token = self.user_token
        if kind == "admin":
            token = self.admin_token

        for service in token['access']['serviceCatalog']:
            if service['type'] == kind:
                break
        return service

    def _get_compute_service(self, token=None):
        return self._get_service("compute")

    def _post(self, posturl, params=None):
        #print posturl
        # print self.config
        conf = self._get_service_endpoint("compute")
        headers = {'content-type': 'application/json',
                   'X-Auth-Token': '%s' % conf['token']}
        #print headers
        r = requests.post(posturl, headers=headers,
                          data=json.dumps(params),
                          verify=self.user_credential['OS_CACERT'])
        ret = {"msg":"success"}
        if r.text:
            ret = r.json()
        return ret

    def _put(self, posturl, params=None):
        # print self.config
        conf = self._get_service_endpoint("compute")
        headers = {'content-type': 'application/json', 
                   'X-Auth-Token': '%s' % conf['token']}
        # print headers
        r = requests.put(posturl, headers=headers,
                          data=json.dumps(params),
                          verify=self.credential['OS_CACERT'])
        ret = {"msg":"success"}
        if r.text:
            ret = r.json()
        return ret
    
    #    
    def ks_get_extensions(self):
        pass
    #    conf = self._get_service_endpoint("identity")

        
    def vm_create(self, name,
                  flavor_name,
                  image_id,
                  security_groups=None,
                  key_name=None,
                  meta={},
                  userdata=None):
        """
        start a vm via rest api call
        """
        #
        # TODO: add logic for getting default image

        # if image_id is None:
        #    get image id from profile information (default image for that cloud)

        # TODO: add logic for getting label of machine
        #

        # if flavor_name is None:
        #    get flavorname from profile information (ther is a get label function ...)

        # if keyname is None:
        #    get the default key from the profile information

        conf = self._get_service_endpoint("compute")
        publicURL = conf['publicURL']
        posturl = "%s/servers" % publicURL
        # print posturl
        # keycontent = base64.b64encode(key_name)
        secgroups = []
        if security_groups:
            for secgroup in security_groups:
                secgroups.append({"name": secgroup})
        else:
            secgroups = [{"name":"default"}]

        params = {
                    "server" : {
                        "name" : "%s" % name,
                        "imageRef" : "%s" % image_id,
                        "flavorRef" : "%s" % flavor_name,
                        "security_groups" : secgroups,
                        "key_name": "%s" % key_name,
                        "metadata" : meta,
                        }
                  }

        if userdata:
            safe_userdata = strutils.safe_encode(userdata)
            params["server"]["user_data"] = base64.b64encode(safe_userdata)

        print params

        return self._post(posturl, params)

    def vm_delete(self, id):
        """
        delete a single vm and returns the id
        """
        conf = self._get_service_endpoint("compute")
        publicURL = conf['publicURL']
        url = "%s/servers/%s" % (publicURL, id)

        headers = {'content-type': 'application/json', 'X-Auth-Token': '%s' % conf['token']}
        # print headers
        # no return from http delete via rest api
        r = requests.delete(url, headers=headers, verify=self.user_credential['OS_CACERT'])
        ret = {"msg":"success"}
        if r.text:
            ret = r.json()
        return ret

    def get_public_ip(self):
        """
        Obtaining a floating ip from the pool via the rest api call
        """
        conf = self._get_service_endpoint("compute")
        publicURL = conf['publicURL']
        posturl = "%s/os-floating-ips" % publicURL
        ret = {"msg":"failed"}
        r = self._post(posturl)
        if r.has_key("floating_ip"):
            ret = r["floating_ip"]["ip"]
        return ret

    def assign_public_ip(self, serverid, ip):
        """
        assigning public ip to an instance
        """
        conf = self._get_service_endpoint("compute")
        publicURL = conf['publicURL']
        posturl = "%s/servers/%s/action" % (publicURL, serverid)
        params = {"addFloatingIp": {
                                    "address": "%s" % ip
                                    }
                  }
        print params
        return self._post(posturl, params)

    def delete_public_ip(self, idofip):
        """
        delete a public ip that is assigned but not currently being used
        """
        conf = self._get_service_endpoint("compute")
        publicURL = conf['publicURL']
        url = "%s/os-floating-ips/%s" % (publicURL, idofip)
        headers = {'content-type': 'application/json', 'X-Auth-Token': '%s' % conf['token']}
        r = requests.delete(url, headers=headers, verify=self.user_credential['OS_CACERT'])
        ret = {"msg":"success"}
        if r.text:
            ret = r.json()
        return ret

    def list_allocated_ips(self):
        """
        return list of ips allocated to current account
        """
        conf = self._get_service_endpoint("compute")
        publicURL = conf['publicURL']
        url = "%s/os-floating-ips" % publicURL
        headers = {'content-type': 'application/json', 'X-Auth-Token': '%s' % conf['token']}
        r = requests.get(url, headers=headers, verify=self.user_credential['OS_CACERT'])
        return r.json()["floating_ips"]

    def release_unused_public_ips(self):
        ips = self.list_allocated_ips()
        ips_id_to_instance = {}
        for ip in ips:
            ips_id_to_instance[ip['id']] = ip['instance_id']
        for id, instance in ips_id_to_instance.iteritems():
            if instance is None:
                self.delete_public_ip(id)
        return True

    def _get(self, msg, kind="user", service="compute", urltype="publicURL", payload=None, json=True):

        # kind = "admin", "user"
        # service = "publicURL, adminURL"
        # service=  "compute", "identity", ....


        # token=None, url=None, kind=None, urltype=None, json=True):

        credential = self.user_credential
        token = self.user_token
        if kind is "admin":
            credential = self.admin_credential
            token = self.admin_token

        conf = self._get_service_endpoint(service)
        url = conf[urltype]

        url = "{0}/{1}".format(url, msg)

        print url
        headers = {'X-Auth-Token': token['access']['token']['id']}
        r = requests.get(url, headers=headers, verify=credential['OS_CACERT'], params=payload)

        print "RRRRR", r

        if json:
            return r.json()
        else:
            return r
    # http

    def _get_service_endpoint(self, type=None):
        """what example %/servers"""
        if type is None:
            type = "compute"
        compute_service = self._get_service(type)
        # pprint(compute_service)
        conf = {}

        conf['publicURL'] = str(compute_service['endpoints'][0]['publicURL'])
        conf['adminURL'] = str(compute_service['endpoints'][0]['adminURL'])
        conf['token'] = str(self.user_token['access']['token']['id'])
        return conf

    # new
    def _now(self):
        return datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')

    # new
    def _list_to_dict(self, list, id, type, time_stamp):
        d = {}
        cm_type_version = self.compute_config.get('cloudmesh', 'clouds', self.label, 'cm_type_version')

        print "VVVVV", cm_type_version

        for element in list:
            element['cm_type'] = type
            element['cm_cloud'] = self.label
            element['cm_cloud_type'] = self.type
            element['cm_cloud_version'] = cm_type_version
            element['cm_refresh'] = time_stamp
            d[element[id]] = dict(element)
        return d

    # new
    def get_extensions(self):
        time_stamp = self._now()
        msg = "extensons"
        # list = self._get(msg)['extensions']
        result = self._get(msg, json=False)
        if result.status_code == 404:
            print "ERROR: extensions not available"
            return {}
        else:
            list = r.json()
        return self._list_to_dict(list, 'name', "extensions", time_stamp)

     # new
     # BUG not yet a dict
    def get_limits(self):
        time_stamp = self._now()
        msg = "limits"
        list = self._get(msg)['limits']
        return list

    # new
    def get_servers(self):
        time_stamp = self._now()
        msg = "servers/detail"
        list = self._get(msg)['servers']
        return self._list_to_dict(list, 'id', "server", time_stamp)

    # new
    def get_flavors(self):
        time_stamp = self._now()
        msg = "flavors/detail"
        list = self._get(msg)['flavors']
        return self._list_to_dict(list, 'name', "flavor", time_stamp)

    # new
    def get_images(self):
        time_stamp = self._now()
        msg = "images/detail"
        list = self._get(msg)['images']
        return self._list_to_dict(list, 'id', "image", time_stamp)

    # new
    def get_tenants(self, credential=None):
        time_stamp = self._now()
        """get the tenants dict for the vm with the given id"""
        if credential is None:
            p = cm_profile()
            name = self.label
            credential = p.server["keystone"][name]
        msg = "tenants"
        list = self._get(msg, kind="admin")['tenants']
        return self._list_to_dict(list, 'id', "tenants", time_stamp)



    # new
    def get_users(self, credential=None):
        time_stamp = self._now()
        """get the tenants dict for the vm with the given id"""
        if credential is None:

            p = cm_profile()
            name = self.label
            credential = p.server["keystone"][name]

        cloud = openstack(name, credential=credential)
        msg = "users"
        list = cloud._get(msg, kind="admin", service="identity", urltype='adminURL')['users']
        return self._list_to_dict(list, 'id', "users", time_stamp)

    def get_meta(self, id):
        """get the metadata dict for the vm with the given id"""
        msg = "/servers/%s/metadata" % (id)
        return self._get("%s" + msg)

    def set_meta(self, id, metadata, replace=False):
        """set the metadata for the given vm with the id"""
        conf = self._get_service_endpoint()
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
        pprint(conf)
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
        return result

    def _get_tenants_dict(self):
        result = self.get_tenants()
        return result

    def _get_images_dict(self):
        result = self.get_images()
        return result

    def _get_flavors_dict(self):
        result = self.get_flavors()
        return result

    def _get_servers_dict(self):
        result = self.get_servers()
        return result


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
    
    # return the security groups for a tenant, in dict format
    def list_security_groups(self, tenant_id):
        apiurl = "os-security-groups"
        return self._get(apiurl)
    
    # return the security group id given a name.
    # The id is used to identify a group when adding more rules to it
    def find_security_groupid_by_name(self, tenant_id, name):
        groupid = None
        secgroups = self.list_security_groups(tenant_id)
        for secgroup in secgroups["security_groups"]:
            if secgroup["name"] == name:
                groupid = secgroup["id"]
                break
        return groupid
    
    # creating a security group, and optionally add rules to it
    # This implementation is based on the rest api
    def create_security_group(self, tenant_id, secgroup, rules=[]):
        conf = self._get_service_endpoint("compute")
        publicURL = conf['publicURL']
        posturl = "%s/os-security-groups" % publicURL
        params = {"security_group":{
                                    "name": secgroup.name,
                                    "description": secgroup.description
                                    }
                  }
        #print params
        ret = self._post(posturl,params)
        groupid = None
        # upon successful, it returns a dict keyed by 'security_group',
        # otherwide may have failed due to some reason
        if "security_group" in ret:
            groupid = ret["security_group"]["id"]
        # if the security group object has rules included, add them first
        if len(secgroup.rules) > 0:
            self.add_security_group_rules(groupid, secgroup.rules)
        
        # only trying to add the additional rules if the empty group has been created successfully    
        if not groupid:
            log.error("Failed to create security group. Error message: '%s'" % ret)
        else:
            self.add_security_group_rules(groupid, rules)
        # return the groupid of the newly created group, or None if failed
        return groupid
    
    # add rules to an existing security group
    def add_security_group_rules(self, groupid, rules):
        conf = self._get_service_endpoint("compute")
        publicURL = conf['publicURL']
        posturl = "%s/os-security-group-rules" % publicURL
        ret = None
        for rule in rules:
            params = {"security_group_rule":{
                                            "ip_protocol": rule.ip_protocol,
                                            "from_port": rule.from_port,
                                            "to_port": rule.to_port,
                                            "cidr": rule.cidr,
                                            "parent_group_id": groupid
                                            }
                      }
            #print params
            ret = self._post(posturl, params)
            if "security_group_rule" not in ret:
                log.error("Failed to create security group rule(s). Error message: '%s'" % ret)
                break
        return ret
    #
    # security Groups of VMS
    #
    # GVL: review
    # how does this look for azure and euca? Should there be a general framework for this in the BaseCloud class
    # based on that analysis?
    #
    # comments of wht these things do and how they work are missing
    #

    '''
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

        vm_flavor = self.cloud.images.find(name=flavor_name)
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
    '''

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
    '''
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
    '''

    #
    # TODO
    #
    """
    refresh just a specific VM
    delete all images that follow a regualr expression in name
    look into sort of images, images, vms
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
    
    def usage(self, tenant_id=None, serverid=None, start=None, end=None, format='dict'):
        """ returns the usage information of the tennant"""
        DEFAULT_STAT_DURATION=30
        if not tenant_id:
            computePubUrl = self._get_service_endpoint("compute")["publicURL"]
            urlsplit = computePubUrl.split("/")
            tenant_id = urlsplit[len(urlsplit)-1]

        # print 70 * "-"
        # print self.cloud.certs.__dict__.get()
        # print 70 * "-"

        # tenantid = "member"  # not sure how to get that
        if not end:
            end = datetime.now()
            #end = self._now()
        if not start:
            start = end - timedelta(days=DEFAULT_STAT_DURATION)
            #start = start.strftime('%Y-%m-%dT%H-%M-%SZ')
        #iso_start = self.parse_isotime(start)
        #iso_end = self.parse_isotime(end)
        # print ">>>>>", iso_start, iso_end
        # info = self.cloud.usage.get(tenantid, iso_start, iso_end)

        # print info.__dict__
        # sys.exit()

        #(start, rest) = start.split("T")  # ignore time for now
        #(end, rest) = end.split("T")  # ignore time for now

        apiurl = "os-simple-tenant-usage/%s" % tenant_id
        payload = {'start': start, 'end': end}
        result = self._get(apiurl,payload=payload)['tenant_usage']
        instances = result['server_usages']
        numInstances = len(instances)
        ramhours = result['total_memory_mb_usage']
        cpuhours = result['total_hours']
        vcpuhours = result['total_vcpus_usage']
        diskhours = result['total_local_gb_usage']
        # if serverid provided, only return the server specific data
        ret = None
        if serverid:
            for instance in instances:
                if instance["instance_id"] == serverid:
                    ret = instance
                    break
        # else return tenant usage info
        else:
            ret = {'tenant_id': tenant_id,
                   'start': start.strftime('%Y-%m-%dT%H-%M-%SZ'),
                   'end': end.strftime('%Y-%m-%dT%H-%M-%SZ'),
                   'instances': numInstances,
                   'cpuHours': cpuhours,
                   'vcpuHours': vcpuhours,
                   'ramMBHours': ramhours,
                   'diskGBHours': diskhours}
        return ret
        
        #(headline, matrix) = self.table_matrix(result)
        #headline.append("Start")
        #headline.append("End")
        #matrix[0].append(start)
        #matrix[0].append(end)

        #if format == 'dict':
        #    result = {}
        #    for i in range(0, len(headline)):
        #        result[headline[i]] = matrix[0][i]
        #    return result
        #else:
        #    return (headline, matrix[0])

    #
    # CLI call of absolute-limits
    #
    # def limits(self):
    #    conf = get_conf()
    #    return _get(conf, "%s/limits")


    '''
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
    '''
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
    pprint(out)

    """

    # cloud = openstack("sierra-grizzly-openstack")
    # flavors = cloud.get_flavors()
    # for flavor in flavors:
    #    print(flavor)

    # keys = cloud.list_key_pairs()
    # for key in keys:
    #    print key.name
    """
    print cloud.find_user_id()

    """

    """
    for i in range (1,3):
        name ="%s-%04d" % (cloud.credential["OS_USERNAME"], i)
        out = cloud.vm_create(name, "m1.tiny", "6d2bca76-8fff-4d57-9f29-50378539b4fa")
        <pprint(out)
    """

    """
    print cloud.find('name', name)
    """

    # cloud.rename("gvonlasz-0001","gregor")

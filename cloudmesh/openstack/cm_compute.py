#! /usr/bin/env python

#
# see also http://docs.openstack.org/cli/quick-start/content/nova-cli-reference.html
#

import iso8601
import sys
sys.path.insert(0, '../..')
 
from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)
import json
import os

from sh import fgrep
import novaclient
from sh import nova

# from cm_credential import credentials
from cloudmesh.openstack.cm_table import table as cm_table
from cloudmesh.cm_config import cm_config

from novaclient.v1_1 import client

def donotchange(fn):
    return fn

class BaseCloud:

    """
    flavors = {}         # global var
    images = {}          # global var
    servers = {}         # global var
    credential = None    # global var
    label = None         # global var
    """

    def _clear(self):
        self.flavors = {}         # global var
        self.images = {}          # global var
        self.servers = {}         # global var
        self.credential = None    # global var
        self.label = None         # global var
        self.type = None

    def info(self):
        print "Label:", self.label
        print "Type:", self.type
        print "Flavors:", len(self.flavors)
        print "Servers:", len(self.servers)
        print "Images:", len(self.images)
 
    def connect(self):
        assert False, "Not implemented"
    def config (self, dict):
        assert False, "Not implemented"
    def find_user_id(self):
        assert False, "Not implemented"

    def get(self,type="server"):
        selection = type.lower()[0]
        list_function = self._get_servers_dict
        d = {}
        if selection == 'i':
            d = self.images
        elif selection == 'f':
            d = self.flavors
        elif selection == 's':
            d = self.servers
        elif type != None:
            print "refresh type not supported"
            assert False
        return d
    
    def _get_image_dict(self):
        print "BOOOH"
        assert False, "Not implemented"

    def _update_image_dict(self,information):
        print "BOOOH"
        assert False, "Not implemented"

    def _get_flavors_dict(self):
        print "BOOOH"
        assert False, "Not implemented"

    def _update_flavors_dict(self,information):        
        print "BOOOH"
        assert False, "Not implemented"

    def _get_servers_dict(self):
        print "BOOOH"
        assert False, "Not implemented"

    def _update_servers_dict(self,information):
        print "BOOOH"
        assert False, "Not implemented"

    def vm_create(self, name, flavor_name, image_id):
        assert False, "Not implemented"
    def vm_delete(self, id):
        assert False, "Not implemented"
    def vms_project(self, refresh=False):
        assert False, "Not implemented"
    def rename(self, old, new, id=None):
        assert False, "Not implemented"
    def usage(self, start, end, format='dict'):
        assert False, "Not implemented"
    def limits(self):        
        assert False, "Not implemented"
    def status(self, vm_id):
        assert False, "Not implemented"

    ######################################################################
    # print
    ######################################################################

    def __str__(self):
        """
        print everything but the credentials that is known about this
        cloud in json format.
        """
        information = {
            'label': self.label,
            'flavors': self.flavors,
            'servers': self.servers,
            'images': self.images}
        return json.dumps(information, indent=4)

    ######################################################################
    # get methods
    ######################################################################

    def type():
        return self.type

    def vms(self):
        return self.servers

    def status(self, vm_id):
        return self.servers[vm_id]['status']


    ######################################################################
    # set credentials
    ######################################################################

    def credentials(self, cred):
        self.credential = cred

    ######################################################################
    # set credentials
    ######################################################################

    def refresh(self, type=None):
        time_stamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
        selection = ""
        if type:
            selection = type.lower()[0]

        list_function = self._get_servers_dict
        update_function = self._update_servers_dict
        d = self.servers
        if selection == 'a' or type == None:
            self.refresh("images")
            self.refresh("flavors")
            self.refresh("servers")
            return
        elif selection == 'i':
            list_function = self._get_images_dict
            update_function = self._update_images_dict
            d = self.images
        elif selection == 'f':
            list_function = self._get_flavors_dict
            update_function = self._update_flavors_dict
            d = self.flavors
        elif selection == 's':
            list_function = self._get_servers_dict
            update_function = self._update_servers_dict
            d = self.servers
        elif type != None:
            print "refresh type not supported"
            assert False

        list = list_function()

        if len(list)  == 0:
           if selection == 'i':
               self.images = {}
           elif selection == 'f':
               self.flavors = {}
           elif selection == 's':
               self.servers = {}

        else:
            
            for information in list:
                (id, element) = update_function(information)
                d[id] = element
                d[id]['cm_refresh'] = time_stamp

    
class openstack(BaseCloud):

    type = "openstack"   # global var
    flavors = {}         # global var
    images = {}          # global var
    servers = {}         # global var
    credential = None    # global var
    label = None         # global var

    # cm_type = "openstack"
    # name = "undefined"
    
    cloud = None         # internal var for the cloud client in openstack
    user_id = None       # internal var

    _nova = nova


    ######################################################################
    # initialize
    ######################################################################
    # possibly make connext seperate
    def __init__(self, label,
                 authurl=None,
                 project=None,
                 username=None,
                 password=None,
                 cacert=None):
        """
        initializes the openstack cloud from a defould novaRC file
        locates at ~/.futuregrid.org/openstack. However if the
        parameters are provided it will instead use them
        """

        self.clear()
        self.label = label
        self.config(label)
        self.connect()
        
        
    def clear(self):
        """
        clears the data of this openstack instance, a new connection
        including reading the credentials and a refresh needs to be
        called to obtain again data.
        """
        #Todo: we may just use the name of the class instead as the type
        self._clear()
        self.type = "openstack"
        
    def connect(self):
        """
        establishes a connection to the OpenStack cloud,
        e.g. initializes the needed components to conduct subsequent
        queries.
        """
        """
           def __init__(self, username, api_key, project_id, auth_url=None,
                  insecure=False, timeout=None, proxy_tenant_id=None,
                  proxy_token=None, region_name=None,
                  endpoint_type='publicURL', extensions=None,
                  service_type='compute', service_name=None,
                  volume_service_name=None, timings=False,
                  bypass_url=None, os_cache=False, no_cache=True,
                  http_log_debug=False, auth_system='keystone',
                  auth_plugin=None,
                  cacert=None):
        """       
        self.cloud = client.Client(
            self.credential['OS_USERNAME'],
            self.credential['OS_PASSWORD'],
            self.credential['OS_TENANT_NAME'],
            self.credential['OS_AUTH_URL'],
            cacert=self.credential['OS_CACERT']
        )

    # BIG BUG, MUST BE DICT
    #config should have dict as parameter
    def config(self, label, dict=None):
        """
        reads in the configuration file if specified, and does some
        internal configuration.
        """
        self.label = label
        if dict == None:
            config = cm_config()
            self.credential = config.get(label,expand=True)

            print self.credential
            
            #self.user_id = self.credential['OS_USER_ID']
            # self.credential = credentials(label)
        else:
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

    ######################################################################
    # TESTS
    ######################################################################

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

        # playing around to discover methods
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

    ######################################################################
    # FIND USER ID
    ######################################################################

    def find_user_id(self):
        """
        this method returns the user id and stores it for later use.
        """
        # As i do not know how to do this properly, we just create a
        # VM and than get the userid from there

        #self.cloud.ensure_service_catalog_present(self.cloud)
        #catalog = self.cloud.client.service_catalog.catalog
        #pp.pprint(catalog['access']['user'], "User Credentials")
        #pp.pprint(catalog['access']['token'], "Token")

        #print(result)

        #sys.exit()

        try:
            self.user_id = self.credential['OS_USER_ID'] 
        except:
            if self.user_id == None:
                sample_flavor = self.cloud.flavors.find(name="m1.tiny")
                sample_image = self.cloud.images.find(
                    id="6d2bca76-8fff-4d57-9f29-50378539b4fa")
                sample_vm = self.cloud.servers.create(
                    "%s-id" % self.credential["OS_USERNAME"],
                    flavor=sample_flavor,
                    image=sample_image)
                self.credential['OS_USER_ID'] = self.user_id = sample_vm.user_id
                sample_vm.delete()
        return self.user_id

    ######################################################################
    # refresh
    ######################################################################

    def _get_images_dict(self):
        return self.cloud.images.list(detailed=True)

    def _update_images_dict(self,information):
        image = information.__dict__
        id =  image['id']
        # clean not neaded info
        del image['manager']
        del image['_info']
        del image['_loaded']
        # del information.links
        return (id, image)

    def _get_flavors_dict(self):
        return self.cloud.flavors.list()

    def _update_flavors_dict(self,information):
        flavor = information.__dict__
        # clean not neaded info
        del flavor['manager']
        del flavor['_info']
        del flavor['_loaded']
        # del information.links
        id = information.name
        return (id, flavor)

    def _get_servers_dict(self):
        return self.cloud.servers.list(detailed=True)


    def _update_servers_dict(self,information):
        vm = information.__dict__
        #pp.pprint (vm)
        #pp.pprint(vm)
        delay = vm['id']
        del vm['manager']
        del vm['_info']
        del vm['_loaded']
        # del information.links
        id = vm['id']
        return (id, vm)


    ######################################################################
    # create a vm
    ######################################################################
    def vm_create(self, name, flavor_name, image_id,key_name = None):
        """
        create a vm
        """

        vm_flavor = self.cloud.flavors.find(name=flavor_name)
        vm_image = self.cloud.images.find(id=image_id)
        
        if key_name == None :
            vm = self.cloud.servers.create(name,
                                           flavor=vm_flavor,
                                           image=vm_image,
                                           )
        else :
            vm = self.cloud.servers.create(name,
                                           flavor=vm_flavor,
                                           image=vm_image,
                                           key_name = key_name
                                           )
        delay = vm.user_id  # trick to hopefully get all fields
        data = vm.__dict__
        del data['manager']
        # data['cm_name'] = name
        # data['cm_flavor'] = flavor_name
        # data['cm_image'] = image_id
        return {str(data['id']):  data}

    ######################################################################
    # delete vm(s)
    ######################################################################

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

    ######################################################################
    # list user images
    ######################################################################

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

    ######################################################################
    # list project vms
    ######################################################################

    def vms_project(self, refresh=False):
        """
        find my vms
        """
        user_id = self.find_user_id()

        time_stamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
        if refresh:
            self.refresh("images")

        result = {}
        for (key, vm) in self.servers.items():
            result[key] = vm

        return result

    ######################################################################
    # delete images from a user
    ######################################################################

    @donotchange
    def vms_delete_user(self):
        """
        find my vms and delete them
        """

        user_id = self.find_user_id()
        vms = self.find('user_id', user_id)
        self.vms_delete(vms)

        return

    ######################################################################
    # find
    ######################################################################

    @donotchange
    def find(self, key, value=None):
        ids = []
        if key == 'user_id' and value == None:
            value = self.user_id
        for (id, vm) in self.servers.items():
            if vm[str(key)] == value:
                ids.append(str(vm['id']))

        return ids

    ######################################################################
    # rename
    ######################################################################

    def rename(self, old, new, id=None):
        all = self.find('name', old)
        print all
        if len(all) > 0:
            id = all[0]
            vm = self.cloud.servers.update(id, new)
        return

    ##### TODO: BUG WHY ARE TGERE TWO REINDEX FUNCTIONS?
    
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

    @donotchange
    def reindex(self, prefix, index_format):
        all = self.find('user_id')
        counter = 1
        for id in all:
            old = self.servers[id]['name']
            new = prefix + index_format % counter
            print "Rename %s -> %s, %s" % (old, new, self.servers[id]['key_name'])
            # if old != new:
            #    vm = self.cloud.servers.update(id, new)
            counter += 1

    ######################################################################
    # TODO
    ######################################################################
    """
    refresh just a specific VM
    delete all images that follow a regualr expression in name
    look into sort of images, flavors, vms
    """

    ######################################################################
    # EXTRA
    ######################################################################
    # will be moved into one class

    @donotchange
    def table_col_to_dict(self, body):
        result = {}
        for element in body:
            key = element[0]
            value = element[1]
            result[key] = value
        return result

    @donotchange
    def table_matrix(self, text, format=None):
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

    ######################################################################
    # CLI call of ussage
    ######################################################################

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

        #tenantid = "member"  # not sure how to get that
        iso_start = self.parse_isotime(start)
        iso_end = self.parse_isotime(end)
        #print ">>>>>", iso_start, iso_end
        #info = self.cloud.usage.get(tenantid, iso_start, iso_end)

        # print info.__dict__
        #sys.exit()

        (start,rest) = start.split("T") # ignore time for now
        (end,rest) = end.split("T") # ignore time for now
        result = fgrep(self._nova("usage", "--start", start, "--end", end), "|")
        
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

    ######################################################################
    # CLI call of absolute-limits
    ######################################################################
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

    ######################################################################
    # Upload Key Pair
    ######################################################################
    def upload_key_pair(self,path,name):
        """ Uploads key pair """
        
        try:
            path = os.path.expanduser(path)
            keyFile = open(path,"r");
            publickey = keyFile.read();
            self.cloud.keypairs.create(name,publickey)
        except Exception, e:
            return 1, e
            
        return (0 ,'Key added successfully')

    ######################################################################
    # Delete Key Pair
    ######################################################################
    def delete_key(self,name):
        """ delets key pair """
        
        try:
            self.cloud.keypairs.delete(name)
        except Exception, e:
            return (1, e)
            
        return (0 , 'Key deleted successfully')

##########################################################################
# MAIN FOR TESTING
##########################################################################

if __name__ == "__main__":

    """
    cloud = openstack("india-openstack")
    
    name ="%s-%04d" % (cloud.credential["OS_USERNAME"], 1)
    out = cloud.vm_create(name, "m1.tiny", "6d2bca76-8fff-4d57-9f29-50378539b4fa")
    pp.pprint(out)  
    
    """

    cloud = openstack("india-openstack")
    print cloud.upload_key_pair('~/.ssh/id_rsa.pub','PushkarKey')

    #cloud.novaclient_dump()

    # print json.dumps(cloud.limits(), indent=4)

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


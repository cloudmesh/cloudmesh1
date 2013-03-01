#! /usr/bin/env pytho

#
# see also http://docs.openstack.org/cli/quick-start/content/nova-cli-reference.html
#

import sys
sys.path.insert(0, '..') 

from datetime import datetime
import pprint 
pp = pprint.PrettyPrinter(indent=4)
import json
import os

from sh import fgrep
import novaclient
from sh import nova

#from cm_credential import credentials
from cloudmesh.openstack.cm_table import table as cm_table
from cloudmesh.cm_config import cm_config

from novaclient.v1_1 import client

class openstack:

    type = "openstack"
    flavors = {}
    images = {}
    servers = {}
    credential = None
    cloud = None
    label = None
    user_id = None
    
    _nova = nova

    def vms(self):
        return self.servers

    def credentials(self, cred):
        self.credential = cred

    def __init__(self,
                 label,
                 authurl=None,
                 project=None,
                 username=None,
                 password=None):
        """
        initializes the openstack cloud from a defould novaRC file
        locates at ~/.futuregrid.org/openstack. However if the
        parameters are provided it will instead use them
        """

        self.clear()
        self.label = label
        self.config(label, 
                    authurl=authurl, 
                    project=project, 
                    username=username, 
                    password=password)
        self.connect()

    def clear(self):
        """
        clears the data of this openstack instance, a new connection
        including reading the credentials and a refresh needs to be
        called to obtain again data.
        """
        type = "openstack"
        self.flavors = {}
        self.images = {}
        self.servers = {}
        self.credential = None
        self.cloud = None
        self.user_id = None
    
    def find_user_id(self):
        """
        this method returns the user id and stores it for later use.
        """
        # As i do not know how to do this properly, we just create a
        # VM and than get the userid from there
        
        sample_flavor = self.cloud.flavors.find(name="m1.tiny")
        sample_image = self.cloud.images.find(
            id="6d2bca76-8fff-4d57-9f29-50378539b4fa")
        sample_vm = self.cloud.servers.create(
            "%s-id" % self.credential["OS_USERNAME"],
            flavor=sample_flavor,
            image=sample_image)
        self.user_id = sample_vm.user_id
        sample_vm.delete()
        return self.user_id

    def connect(self):
        """
        establishes a connection to the OpenStack cloud,
        e.g. initializes the needed components to conduct subsequent
        queries.
        """

        print ">>>>>>", self.credential['OS_TENANT_NAME'],

        self.cloud = client.Client(
            self.credential['OS_USERNAME'], 
            self.credential['OS_PASSWORD'],
            self.credential['OS_TENANT_NAME'],
            self.credential['OS_AUTH_URL']
            )


    def config (self, label,
                authurl=None,
                project=None,
                username=None,
                password=None):
        """
        reads in the configuration file if specified, and does some
        internal configuration.
        """
        self.label= label 
        if username == None:
            config = cm_config()
            self.credential = config.get(label)
            print self.credential
            #self.credential = credentials(label)
        else:
            self.credential = {}
            self.credential['OS_USERNAME'] = username
            self.credential['OS_PASSWORD'] = password
            self.credential['OS_AUTH_URL'] = authurl
            self.credential['label'] = label
            self.credential['OS_TENANT_NAME'] = project
        """
        self._nova = nova.bake("--os-username",    self.credential.username,
                               "--os-password",    self.credential.password,
                               "--os-auth-url",    self.credential.url, 
                               "--os-tenant-name", self.credential.project)
        """
        
    def __str__ (self):
        """
        print everything but the credentials that is known about this
        cloud in json format.
        """
        information = {
            'label': self.label,
            'flavors': self.flavors,
            'vms': self.servers,
            'images' : self.images}
        return json.dumps(information, indent=4)

    def type():
        return self.type

    def refresh(self, type=None):

        time_stamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
        selection = ""
        if type:
            selection = type.lower()[0]
            all = selection == 'a'
        else:
            all = True
        
        if selection == 'i' or all:
            list = self.cloud.images.list(detailed=True)
            for information in list:
                image = information.__dict__
                del information.manager
                del information._info
                del information._loaded
                #del information.links
                self.images[information.id] = image
                self.images[information.id]['cm_refresh'] = time_stamp
                
        if selection == 'f' or all:
            list = self.cloud.flavors.list()
            for information in list:
                # clean not neaded info
                del information.manager
                del information._info
                del information._loaded
                #del information.links
                flavor = information.__dict__
                self.flavors[information.name] = flavor
                self.flavors[information.name]['cm_refresh'] = time_stamp

        if selection == 'v' or selection == None or all:
            list = self.cloud.servers.list(detailed=True)
            
            for information in list:
                vm = information.__dict__
                del information.manager
                del information._info
                del information._loaded
                #del information.links
                self.servers[information.id] = vm
                self.servers[information.id]['cm_refresh'] = time_stamp

    #
    #   GREGOR GOT TILL HERE
    #


    """
    create images
    delete images
    select images baesed on user
    delete all images that belong to me
    delete all images that follow a regualr expression in name
    reindex images
    rename images

    look into sort of images, flavors, vms
    """

    def vm_show_all(self, prefix):
        """show all the instances with prefix-*"""

        try:
            # instances = fgrep(self._nova('list'), prefix)
            # find only te once i do
            # ERROR
            servers = self.nova.servers.list(detailed=True)
            for server in servers:
                attributes = server.__dict__
                id = attributes.name
                id = attributes.id
                print 'Found %s to show' % name
                print _vm_show(id)
        except:
            print 'Found 0 instances to show'


    def _vm_show(self, name):
        print "vm show"
        try:
            server = {}
            now = str(datetime.now())
            out = self._nova("show", name).split("\n")

            out = out[3:-2]
            
            for line in out:
                (a, attribute, value, b)  = line.split("|")
                attribute = attribute.strip()
                value = value.strip()
                server[attribute] = str(value)

            server['cm_refresh'] = now.strip()

            try:
                id = server['id']
                for attribute in server:
                    id = server['id']
                    self.servers[id][attribute] = server[attribute]
            except:
                id = server['id']
                self.servers[id] = server
        except Exception, e:
            print e

        return server

    def vm_list(self):
        print "List Vms"
        try:
            servers = {}
            now = str(datetime.now())
            instances = fgrep(nova("list"), self.user)
            for line in instances:
                (a, id, name, status, ip, b) = line.split("|")
                id = id.strip()
                servers[id] = {
                    'id': id,
                    'cloud' : cloudname.strip(),
                    'name': name.strip(), 
                    'status' : status.strip(),
                    'ip' : ip.strip(),
                    'refresh' : now.strip()
                    }

        except Exception, e:
            print e

        return servers

    def vm_del(self, id):
        r = False
        try:
            r = nova("delete", id)
        except Exception, e:
            print e
        return r

    def vm_del_all(self,id):
        None


if __name__=="__main__":

    credential_test = False
    flavor_test = False
    table_test = False
    image_test = False
    vm_test = False
    cloud_test = False

    if credential_test:
        credential = cm_config('india-openstack')
        print credential


    cloud = openstack("india-openstack")


    if flavor_test or table_test:
        cloud.refresh('flavors')
        print json.dumps(cloud.flavors, indent=4)

    if table_test:
        table = cm_table()
        columns = ["id", "name", "ram", "vcpus"]
    
        table.create(cloud.flavors, columns, header=True)
        print table

        table.create(cloud.flavors, columns, format='HTML', header=True)
        print table

        table.create(cloud.flavors, columns, format='%12s', header=True)
        print table

    if image_test:
        cloud.refresh('images')
        print json.dumps(cloud.images, indent=4)
    
    if vm_test:
        cloud.refresh('vms')
        print json.dumps(cloud.images, indent=4)

    if cloud_test:
        cloud.refresh()
        print cloud


    print cloud.find_user_id()

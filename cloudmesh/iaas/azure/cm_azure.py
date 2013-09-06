#! /usr/bin/env python

from datetime import datetime
from fabric.api import *
from random import randint
import ConfigParser
import pickle
import os
import sys
import json

import commands
import getpass

from sh import azure as _azure
from sh import fgrep as _fgrep
import pprint


from multiprocessing import Pool as _Pool
from cloudmesh.config.cm_config import cm_config
global maxparallel


maxparallel = 5


#
# Baked sh azure functions to make azure client easier to use
#
vm_start = _azure.bake("--json", "vm", "start")
vm_restart = _azure.bake("--json", "vm", "restart")
vm_shutdown = _azure.bake("--json", "vm", "shutdown")
vm_list = _azure.bake("--json", "vm", "list")
vm_create = _azure.bake("--json", "vm", "create")
vm_show = _azure.bake("--json", "vm", "show")
vm_delete = _azure.bake("--json", "vm", "delete")
vm_image_list = _azure.bake("--json", "vm", "image", "list")

account = _azure.bake("account")

#
# azure class
#


class cm_azure:
    images = {}
    servers = {}
    cloud = None
    label = ""
    flavors = {}
    credentials = {}
    type = "azure"  # global var

    filename = "%(home)s/%(location)s" % {
        "home": os.environ['HOME'],
        "location": ".futuregrid/cloudmesh.yaml"
    }

    #
    # initialize
    #
    def __init__(self,
                 username=None,
                 password=None,
                 publish_settings_file_path=None,
                 default_image_name=None):
        """
        initializes the openstack cloud from a defould novaRC file
        locates at ~/.futuregrid.org/openstack. However if the
        parameters are provided it will instead use them
        """

        self.clear()
        self.config(username,
                    password,
                    publish_settings_file_path,
                    default_image_name)

    def config(self, username=None,
               password=None,
               publish_settings_file_path=None,
               default_image_name=None):

        if username is None:
            config = cm_config()
            configuration = config.get('azure')
            self.credentials['username'] = configuration['username']
            self.credentials['password'] = configuration['password']
            self.credentials[
                'settings'] = {'publishsettings_file_path': configuration['publishsettings_file_path'],
                               'defaultimage': configuration['defaultimage']}
        else:
            self.credentials['username'] = username
            self.credentials['password'] = password
            self.credentials[
                'settings'] = {'publishsettings_file_path': publish_settings_file_path,
                               'defaultimage': default_image_name}
        return

    #
    # get methods
    #
    def get(self):
        """returns the dict with all the sms"""
        return self.servers

    #
    # print methods
    #

    def __str__(self):
        """
        print everything but the credentials that is known about this
        cloud in json format.
        """
        information = {
            'label': self.label,
            'flavors': self.flavors,
            'vms': self.servers,
            'images': self.images}
        return json.dumps(information, indent=4)

    #
    # refresh
    #

    def refresh(self, type=None):

        time_stamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
        selection = ""
        if type:
            selection = type.lower()[0]
            all = selection == 'a'
        else:
            all = True

        if all:
            self.refresh('images')
            self.refresh('vms')
            self.refresh('flavors')
            return

        key = ""
        list_function = vm_list
        if selection == 'i':
            key = 'Name'
            list_function = vm_image_list
            store = self.images
        elif selection == 'v':
            key = 'VMName'
            list_function = vm_list
            store = self.servers

        if selection != 'f':
            list = json.loads(str(list_function()))
            for object in list:
                id = object[key]
                store[id] = object
                store[id]['cm_refresh'] = time_stamp

        if selection == 'f':
            # TODO: move to YAML fileas "flavors : { ...} under azure, copy from there and deal only with timestamp here
            # once in local dict at config time , no reason to reread this
            # portion of yaml file
            self.flavors = {
                'ExtraSmall': {
                    'CPU_Cores': 'Shared',
                    'Memory': '768 MB',
                    'Disk_Space_for_Web_&_Worker_Roles': '19,480 MB',
                    'Disk Spacein a VM Role': '20 GB',
                    'Bandwidth': '5 Mbps',
                    'cm_refresh': time_stamp
                },
                'Small': {
                    'CPU_Cores': '1',
                    'Memory': '1.75 GB',
                    'Disk_Space_for_Web_&_Worker_Roles': '229,400 MB',
                    'Disk Spacein a VM Role': '165 GB',
                    'Bandwidth': '100 Mbps',
                    'cm_refresh': time_stamp
                },
                'Medium': {
                    'CPU_Cores': '2',
                    'Memory': '3.5 GB',
                    'Disk_Space_for_Web_&_Worker_Roles': '500,760 MB',
                    'Disk Spacein a VM Role': '340 GB', 'Bandwidth': '200 Mbps',
                    'cm_refresh': time_stamp
                },
                'Large': {
                    'CPU_Cores': '4',
                    'Memory': '7 GB',
                    'Disk_Space_for_Web_&_Worker_Roles': '1,023,000 MB',
                    'Disk Spacein a VM Role': '850 GB',
                    'Bandwidth': '400 Mbps',
                    'cm_refresh': time_stamp
                },
                'ExtraLarge': {
                    'CPU_Cores': '8', 'Memory': '14 GB',
                    'Disk_Space_for_Web_&_Worker_Roles': '2,087,960 MB',
                    'Disk Spacein a VM Role': '1890 GB', 'Bandwidth': '800 Mbps',
                    'cm_refresh': time_stamp
                }
            }

    #
    # manage vms
    #
    def start(self, name):
        """starts a vm with the given name"""
        result = vm_start(name)
        # add result to internal cache
        print result

    def restart(self, name):
        """restarts a vm with the given name"""
        result = vm_restart(name)
        # add result to internal cache
        print result

    def shutdown(self, name):
        """shutdown of a vm with the given name"""
        result = vm_shutdown(name)
        # add result to internal cache
        print result

    def list(self):
            result = vm_list()
            # add result to internal cache
            print result

    def show(self, name):
            result = vm_show()
            # add result to internal cache
            print result

    def vm_delete(self, name):
            result = vm_delete(name)
            # add result to internal cache
            return result

    def vms_delete(self, names):

        for name in names:
            print "Deleting %s" % name
            result = vm_delete(name)
            # add result to internal cache
        return names

    def vms_find(self):
        ids = []
        for (id, vm) in self.servers.items():
                ids.append(id)

        return ids

    def vm_create(self, name=None, image_name=None, flavor_name=None):
        # cmd = 'azure vm create %(vmname)s %(image)s %(username)s --ssh --location "East US" %(password)s' % vm
        # print cmd

        #
        # there may also be parameter to start up multiple vms find out and integrate with np=None, if None than np=1
        #

        if flavor_name is None:
            result = vm_create(
                "%s" % self._vm_name(
                    randint(0, 1000)) if name is None else name,
                "%(defaultimage)s" % self.credentials[
                    'settings'] if image_name is None else image_name,
                "%(username)s" % self.credentials,
                "--ssh",
                "--location",
                "East US",
                "%(password)s" % self.credentials,
            )
        else:
            result = vm_create(
                "%s" % self._vm_name(
                    randint(0, 1000)) if name is None else name,
                "%(defaultimage)s" % self.credentials[
                    'settings'] if image_name is None else image_name,
                "%(username)s" % self.credentials,
                "--ssh",
                "--location",
                "East US",
                "%(password)s" % self.credentials,
                "-z",
                flavor_name
            )

        return result

    def _vm_name(self, index):
        number = str(index).zfill(3)
        name = '%s-%s' % (self.credentials['username'], number)
        return name

    #
    # activate azure
    #

    def activate(self):

        result = account('clear')
        print result

        errmsg = 'No account information found'
        cmd = 'azure account import \'%(publishsettings_file_path)s\'' % self.credentials[
            'settings']

        text = commands.getstatusoutput(cmd)
        if not errmsg in text[1]:
            print 'Activated'
        else:
            print 'There was an error while activation'

    #
    # functions we want to rewrite/replace
    #

    def _selectImage(self):
        # BUG: I AHVE NO IDEA WHAT THIS IS DUE TO NON INFORMATIVE VARIABLE NAMEING
        images = self._buildAzureImageDict()
        print 'Please select Image'

        # what is arg1, arg2?
        for (arg1, arg2) in images.items():
            print arg1 + "\t" + arg2[0] + "\t" + arg2[1] + "\t" + arg2[2]

        while 1:
            var = raw_input("Image : ")
            if images.has_key(var):
                print images[var][0]
                return images[var][0]
            else:
                print "Incorrect Image name"
        return var

    def _copy_image_list_to_dict(self):
        """
        method not needes as so simple, instead work on refresh from
        openstack
        """
        images = vm_list()
        # TODO: verify if this works
        for key in images:
            image = images[key]
            self.images[image['Name']] = image
            # see other attributes in openstack refersh class
        return

    def clear(self):
        """
        clears the data of this azure instance, a new connection
        including reading the credentials and a refresh needs to be
        called to obtain again data.
        """
        self.type = "azure"
        self.flavors = {}
        self.images = {}
        self.servers = {}
        self.credential = {}
        self.cloud = None


if __name__ == '__main__':

    cloud = cm_azure()
    cloud.refresh("all")
    print cloud.vms_find()
    # cloud.refresh("vms")
    # cloud.refresh("images")
    # print cloud.vm_create('ppnewaskar-228','b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-12_04_1-LTS-amd64-server-20121218-en-us-30GB',
    # 'large')
    # print cloud

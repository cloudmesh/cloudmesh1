#! /usr/bin/env python

from datetime import datetime
from fabric.api import *
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

global vmName, vmImage, vmPassword,maxparallel;

maxparallel = 5
CONFIGPATH='config.cfg'
DBFILEPATH='database.db'

######################################################################
# Baked sh azure functions to make azure client easier to use
######################################################################
vm_start = _azure.bake("--json","vm","start")
vm_restart = _azure.bake("--json","vm","restart")
vm_shutdown = _azure.bake("--json","vm","shutdown")
vm_list = _azure.bake("--json","vm","list")
vm_create = _azure.bake("--json","vm","create")
vm_show = _azure.bake("--json","vm","show")
vm_delete = _azure.bake("--json","vm","delete")
vm_image_list = _azure.bake("--json","vm","image", "list")

account = _azure.bake("account")

######################################################################
# azure class
######################################################################

class cm_azure:
    images = {}
    servers = {}
    cloud = None
    label = ""
    flavors = {}

    filename = "%(home)s/%(location)s" % {
        "home" : os.environ['HOME'], 
        "location" : ".futuregrid/cloudmesh.cfg"
        }

    ######################################################################
    # hack to hard code credentials DELETE
    ######################################################################
    """
    credentials = {
        'settings' : {'image' : 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-12_04_1-LTS-amd64-server-20121218-en-us-30GB'}
        }
    """

    ######################################################################
    # initialize
    ######################################################################

    def __init__(self):
        self.servers = {}
        return

    def config(self, filename=None):

        if filename == None:
            filename = self.filename 

        config = ConfigParser.ConfigParser()
        config.read(filename)
        self.credentials['username'] = config.get('azure','username');
        self.credentials['password'] = config.get('azure','password');
        self.credentials['settings'] = config.get('azure',
                                                  'publishsettings_file_path');
        return

    ######################################################################
    # unnecessary as handleded in cm_config
    ######################################################################
    def config_write():

        cfgFile = open(CONFIGPATH,'w')

        config.set('azure', 'password', value)
        config.set('azure', 'username', value)

        #config.set('azure','username') = self.credentials['username']
        #config.set('azure','password') = self.credentials['password']
        #config.set('azure','publishsettings_file_path') = self.credentials['settings'] 

        config.write(cfgFile)
        cfgFile.close()

    ######################################################################
    # get methods
    ######################################################################

    def get(self):
        """returns the dict with all the sms"""
        return self.servers

    ######################################################################
    # print methods
    ######################################################################

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


    ######################################################################
    # refresh 
    ######################################################################
    
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
            return

        key = ""
        list_function = vm_list
        if selection == 'i' :
            key = 'Name'
            list_function = vm_image_list
            store = self.images
        elif selection == 'v' :
            key = 'VMName'
            list_function = vm_list
            store = self.servers
            
        list = json.loads(str(list_function()))
        for object in list:
            id = object[key]
            store[id] = object
            store[id]['cm_refresh'] = time_stamp


        """
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
        """


    ######################################################################
    # manage vms 
    ######################################################################

    def start(self,name):
        """starts a vm with the given name"""
        result = vm_start(name)
        # add result to internal cache
        print result

    def restart(self,name):
        """restarts a vm with the given name"""
        result = vm_restart(name)
        # add result to internal cache
        print result

    def shutdown(self,name):
        """shutdown of a vm with the given name"""
        result = vm_shutdown(name)
        # add result to internal cache
        print result


    def list(self):
            result = vm_list()
            # add result to internal cache
            print result

    def show(self,name):
            result = vm_show()
            # add result to internal cache
            print result

    def delete(self,name):
            result = vm_delete()
            # add result to internal cache
            print result



    def _boot(self, index):
        #cmd = 'azure vm create %(vmname)s %(image)s %(username)s --ssh --location "East US" %(password)s' % vm
        #print cmd
        result = vm_create("%s" % self._vm_name(index),
                           "%(image)s" % self.credentials['settings'],
                           "%(username)s"% self.credentials,
                           "--ssh",
                           "--location",
                           "East US",
                           "%(password)s" % self.credentials)
                        
        print result
        return result
    
    
    def create(self, index, name, image=None) :

        
        """Creates a number of vms with the labels prefix-0 to prefix-<number-1>. It uses a threadpool"""
        pool = _Pool(processes=maxparallel)
        list = range(0, int(index))
        result = pool.map(self._boot,list)
        print result


    def _vm_name(self,index):
        number = str(index).zfill(3)
        name = '%s-%s' % (self.credentials['username'], number)
        return name

    ######################################################################
    # activate azure
    ######################################################################

    def activate(self):

        result = account('clear')
        print result

        errmsg = 'No account information found' 
        cmd = 'azure account import \'%(settings)\'' % credentials;

        text =  commands.getstatusoutput(cmd)
        if not errmsg in text[1] :
            print 'Activated'
        else :
            print 'There was an error while activation'

    ######################################################################
    # functions we want to rewrite/replace
    ######################################################################

    def _selectImage() :
        images = _buildAzureImageDict()
        print 'Please select Image'    ;

        # what is arg1, arg2?
        for (arg1, arg2) in images.items() :
            print arg1 + "\t" + arg2[0] +"\t" +arg2[1] + "\t" +arg2[2]

        while 1 :
            var = raw_input("Image : ")
            if images.has_key(var) :
                print images[var][0]
                return images[var][0]
            else :
                print "Incorrect Image name"
        return var



    def _copy_image_list_to_dict(self) :
        """
        method not needes as so simple, instead work on refresh from
        openstack
        """
        images = vm_list()

        for key in vms :
            image = image[key]
            self.images[image['Name']] = image
            #see other attributes in openstack refersh class
        return
    



    def servers_save(self):
        # this is still wrong but beats the complex parsing function
        vms = vm_list()
        azure={};
        
        for key in vms :
            azure[key]=vm_show(vmName)
        self.servers = azure
        return azure

    def save(self):
        
        azure = {}
        azure['name']='azure';
        azure['servers'] = self.servers_save();
        azure['images'] = self._buildAzureImageDict();
        pickle.dump( azure, open( DBFILEPATH, "wb" ) )
        azure = pickle.load( open( DBFILEPATH, "rb" ) )
        
        print azure
        #json.dumps(azure, indent=4)
    
   
if  __name__ =='__main__':
    
    cloud = cm_azure()
    cloud.refresh("all")
    #cloud.refresh("vms")
    #cloud.refresh("images")
    
    print cloud
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

import sys
#sys.path.insert(0, '..') 
from datetime import datetime
import pprint 
pp = pprint.PrettyPrinter(indent=4)
import json
import os

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.types import NodeState

import libcloud.security
import time
from sh import fgrep

from cm_table import table as cm_table
from cm_config import cm_config

class eucalyptus:

    type = "eucalyptus"
    sizes = {}
    images = {}
    nodes = {}
    cloud = None
    label = None
    credentials = {}

    filename = "%(home)s/%(location)s" % {
        "home" : os.environ['HOME'], 
        "location" : ".futuregrid/cloudmesh.yaml"
        }
   
    def vms(self):
        return self.servers

   
    def __init__(self,EC2accessKey=None,EC2secretKey=None):
        """
        initializes the openstack cloud from a defould novaRC file
        locates at ~/.futuregrid.org/openstack. However if the
        parameters are provided it will instead use them
        """
        self.clear()
        self.config(EC2accessKey,EC2secretKey)
        self.connect()

    def clear(self):
        """
        clears the data of this openstack instance, a new connection
        including reading the credentials and a refresh needs to be
        called to obtain again data.
        """
        type = "eucalyptus"
        self.sizes = {}
        self.images = {}
        self.nodes = {}
        self.credentials = {}
        self.cloud = None
        self.user_id = None
    
    def connect(self):
                
        Driver = get_driver(Provider.EUCALYPTUS)
        self.cloud = Driver(self.credentials['EC2accessKey'], self.credentials['EC2secretKey'],host="149.165.146.135", secure=False, port=8773,path="/services/Eucalyptus")
      

    def config(self,EC2accessKey=None,EC2secretKey=None):
        """
        reads in the configuration file if specified, and does some
        internal configuration.
        """ 
        
        if EC2accessKey == None:
            config = cm_config()
            configuration = config.get('india-eucalyptus')
            #print (configuration['fg-82']['EC2_ACCESS_KEY'])
            self.credentials['EC2accessKey']=configuration['fg-82']['EC2_ACCESS_KEY']
            self.credentials['EC2secretKey']=configuration['fg-82']['EC2_SECRET_KEY']

        else:
            self.credentials['EC2accessKey']=EC2accessKey
            self.credentials['EC2_SECRET_KEY']=EC2secretKey
   
        
    def __str__ (self):
        """
        print everything but the credentials that is known about this
        cloud in json format.
        """
        information = {
            'label': self.label,
            'sizes': self.sizes,
            'servers': self.nodes,
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

            list = self.cloud.list_images()


            for information in list:
                image=information.__dict__
                del information._uuid
                del information.driver
                self.images[information.id] = image
                self.images[information.id]['cm_refresh'] = time_stamp
                
        if selection == 'n' or all:

            list = self.cloud.list_nodes()


            for information in list:
                node=information.__dict__
                del information._uuid
                del information.driver
                self.nodes[information.id] = node
                self.nodes[information.id]['cm_refresh'] = time_stamp
        if selection == 's' or all:

            list = self.cloud.list_sizes()


            for information in list:
                size=information.__dict__
                #del information.virtualizationtype
                del information.driver
                del information._uuid
                self.sizes[information.id] = size
                self.sizes[information.id]['cm_refresh'] = time_stamp


                
if __name__ == "__main__":


  credential_test = False
  sizes_test = False
  table_test = False
  image_test = False
  nodes_test = False
  cloud_test = True

  cloud = eucalyptus()
  if image_test:
      cloud.refresh('images')
      print "hey shweta"
      print json.dumps(cloud.images, indent=4)
#-      pp.pprint (cloud.images)
  
  if nodes_test:
      cloud.refresh('nodes')
       
      print json.dumps(cloud.nodes, indent=4)
     
  if sizes_test:
      cloud.refresh('sizes')
      print json.dumps(cloud.sizes, indent=4)

  if cloud_test:
      cloud.refresh()
      print cloud

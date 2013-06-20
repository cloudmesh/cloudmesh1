import sys
sys.path.insert(0, '..') 
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


#from cm_table import table as cm_table
from openstack.cm_credential import credentials as credentials_rc
class eucalyptus:

    type = "eucalyptus"
    sizes = {}
    images = {}
    nodes = {}
    credentials = None
    accesskey = None
    secretkey = None
    project = "fg82"



    #
    # change to gregors credential class
    #

    def activate_project(self, project):

        self.credentials = credentials_rc("eucalyptus")
        self.credentials.location = ".futuregrid/india/eucalyptus/" + project + "/eucarc"

        self.credentials.type('eucalyptus')

        self.access_key = credentials._get_rc_variable ("accesskey")
        self.secret_key = credentials._get_rc_variable ("secretkey")

        print self.access_key
        print self.secret_key


    # url = 


    # don't forget to source your novarc file

    cloud = None
    label = None
    #user_id = None
    
   
    def vms(self):
        return self.servers

    """
    def credentials(self, cred):
        self.credential = cred
    """

    def __init__(self, label,project=None)
        """
        initializes the openstack cloud from a defould novaRC file
        locates at ~/.futuregrid.org/openstack. However if the
        parameters are provided it will instead use them
        """
        self.config(label,project)
        self.connect()

    def config(self,label,project=None):
        """
        reads in the configuration file if specified, and does some
        internal configuration.
        """
        self.clear()

        self.label= label 
        if project == None:
            self.activate_project("fg82")
        else:
            self.activate_project(project)


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
        #self.credential = None
        self.cloud = None
        self.user_id = None
    
    def connect(self):
        """
        establishes a connection to the eucalyptus cloud,
        e.g. initializes the needed components to conduct subsequent
        queries.
        """


        Driver = get_driver(Provider.EUCALYPTUS)
        self.cloud = Driver(self.accesskey, 
                            self.secretkey,
                            secure=False, 
                            host="149.165.146.50", # this is not quite right but will do for now 
                            port=8773, # this is not quite right but will do for now 
                            path="/services/Cloud") # this is not quite right but will do for now 
      

        
    def __str__ (self):
        """
        print everything but the credentials that is known about this
        cloud in json format.
        """
        information = {
            'label': self.label,
            'flavors': self.sizes,
            'vms': self.nodes,
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
            

                
if __name__ == "__main__":


  credential_test = False
  flavor_test = False
  table_test = False
  image_test = True
  vm_test = False
  cloud_test = False

  """
  if credential_test:
      credential = cm_config('india-openstack')
      print credential
  """


  cloud = eucalyptus("india-eucalyptus")
  """
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

      table.create(cloud.flavors, columns, format='%12s', header=True)11
      print table
  """
  if image_test:
      cloud.refresh('images')
      print "hey shweta"
      print json.dumps(cloud.images, indent=4)
#-      pp.pprint (cloud.images)
  """
  if vm_test:
      cloud.refresh('vms')
       
      print json.dumps(cloud.images, indent=4)
      
  if cloud_test:
      cloud.refresh()
      print cloud


  print cloud.find_user_id()
  """
                                                    

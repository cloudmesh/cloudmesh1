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

from openstack.cm_table import table as cm_table
from cm_config import cm_config

class eucalyptus:
    """
    requires a cloudmesh yaml file with the following structure:

    default: sierra-openstack

    cloudmesh:

        india-eucalyptus:
            BASEDIR: ~/.futuregrid/india/eucalyptus
            host: 127.127.127.127
            port: 8773
            fg-82:
                EC2_PRIVATE_KEY: euca2-user-05.....-pk.pem
                EC2_CERT: euca2-user-0429....-cert.pem
                EUCALYPTUS_CERT: cloud-cert.pem
                EC2_ACCOUNT_NUMBER: '709......'
                EC2_ACCESS_KEY: 'GF78F0E7......'
                EC2_SECRET_KEY: 'yf07e87fe.......'
                EC2_USER_ID: '09876....'

    """

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

   
    def __init__(self, label,
                 project=None,
                 accessKey=None,
                 secretKey=None):
        """
        initializes the openstack cloud from a defould novaRC file
        locates at ~/.futuregrid.org/openstack. However if the
        parameters are provided it will instead use them
        """
        self.clear()
        self.config(label,project,accessKey,secretKey)
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
        self.cloud = Driver(self.credentials['accessKey'], 
                            self.credentials['secretKey'],
                            host="149.165.146.135", 
                            secure=False, port=8773,
                            path="/services/Eucalyptus")
      

    def config(self,label=None,project=None,accessKey=None,secretKey=None):
        """
        reads in the configuration file if specified, and does some
        internal configuration.
        """ 
        if label == None and accessKey == None:
            label = 'india-eucalyptus'
            project = 'fg-82'

        if accessKey == None:
            self.label = label

            config = cm_config()
            configuration = config.get(label)
            
            pp.pprint(configuration)

            basedir = configuration['BASEDIR'] = configuration['BASEDIR'].replace('~',os.environ['HOME'])
            configuration[project]['EC2_PRIVATE_KEY']  = "%s/%s" % (basedir, configuration[project]['EC2_PRIVATE_KEY'] )
            configuration[project]['EUCALYPTUS_CERT']  = "%s/%s" % (basedir, configuration[project]['EUCALYPTUS_CERT'] )

            pp.pprint(configuration)


            self.credentials['accessKey']=configuration[project]['EC2_ACCESS_KEY']
            self.credentials['secretKey']=configuration[project]['EC2_SECRET_KEY']

        else:
            self.credentials['accessKey']=accessKey
            self.credentials['secretkey']=secretKey
   
        
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


    def getNodebyID(self,nodeid):        
        nodes = self.cloud.list_nodes()      
        for node in nodes :
            if node.id == nodeid :
                return node   
 
    def vm_delete(self,node):
        result = destroy_node(self, node)
            # add result to internal cache
        print ("vm Deleted")
        return result
    
    def restart(self,node):
        """restarts a vm with the given name"""
        result = reboot_node(self, node)
        # add result to internal cache
        print result
      

    def vm_create(self, name, flavor_name, image_id):
        """
        create a vm
        """
        flavours = self.cloud.list_sizes()
        vm_flavour= flavours[0]
        for flavour in flavours :
            if flavour.id == 'm1.small' :
                vm_flavour= flavour

        images = self.cloud.list_images()
        vm_image = images[0]
        for image in images :
            if image.id == 'ami-000000b4' :
                vm_image = image

        if (name== None):
            vm_name=self._generate_vmname(randint(0,1000))
        else:
            vm_name=name;
     
        self.vm = self.cloud.create_node(name=vm_name, image=vm_image, size=vm_flavour);
        
        while 1 :
            time.sleep(15)
            updatedNode = self.getNodebyID(self.vm.id)
            if updatedNode.state == 3 :
                print "pending " + updatedNode.id
            if updatedNode.state == 0 :
                print("successful creation of vm")
                time.sleep(60)
                break;
            if updatedNode.state == 4 :
                print(node.id, "Has Errored out");
                nodes.remove(vm)
                break;

        data = self.vm.__dict__
        del data['driver']
        pp.pprint(data)
        return {}


    def _generate_vmname(self,index):
        number = str(index).zfill(3)
        name = '%s-%s' % (self.credentials['username'], number)
        return name




                
if __name__ == "__main__":


  credential_test = False
  sizes_test = False
  table_test = False
  image_test = False
  nodes_test = False
  cloud_test = True

  cloud = eucalyptus('india-eucalyptus', 'fg-82')

  if image_test:
      cloud.refresh('images')
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

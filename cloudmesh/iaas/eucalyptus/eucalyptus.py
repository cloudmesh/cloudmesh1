import sys
sys.path.insert(0, '..')
from datetime import datetime
from pprint import pprint
import json
import os

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.types import NodeState

import libcloud.security
import time
from sh import fgrep
import urlparse

# from cm_table import table as cm_table
from cloudmesh.config.cm_config import cm_config
from cloudmesh.iaas.ComputeBaseType import ComputeBaseType

class eucalyptus(ComputeBaseType):

    type = "eucalyptus"
    sizes = {}
    images = {}
    nodes = {}
    credentials = None
    accesskey = None
    secretkey = None
    project = "fg82"
    config = None
    cloud = {}

    #
    # change to gregors credential class
    #
    def connect(self, label, project):
        """
        establishes a connection to the eucalyptus cloud,
        e.g. initializes the needed components to conduct subsequent
        queries.
        """
        self.label = label
        self.project = project
        print "Loading", self.label, self.project
        Driver = get_driver(Provider.EUCALYPTUS)
        
        self.config = cm_config()


        cred = self.config.get(self.label)

        euca_id = cred['EC2_ACCESS_KEY']
        euca_key = cred['EC2_SECRET_KEY']
        ec2_url = cred['EC2_URL']

        result = urlparse.urlparse(ec2_url)
        is_secure = (result.scheme == 'https')
        if ":" in result.netloc:
            host_port_tuple = result.netloc.split(':')
            host = host_port_tuple[0]
            port = int(host_port_tuple[1])
        else:
            host = result.netloc
            port = None
    
        path = result.path




        
        #pprint(self.config.__dict__)
        print "DDD", self.label        
        self.credential = self.config.get(self.label, expand=True)
        print "CCC"
        pprint(self.credential)
        print "XXXX", self.credential['EUCALYPTUS_CERT']
                
        print "YYYYY", self.config.cloud(self.label)['cm_host']
        
        #libcloud.security.CA_CERTS_PATH.append(self.credential['EUCALYPTUS_CERT'])
        #libcloud.security.VERIFY_SSL_CERT = False

        Driver = get_driver(Provider.EUCALYPTUS)
        self.cloud = Driver(key=euca_id, secret=euca_key, secure=False, host=host, path=path, port=port)

        print "YYYY"


    """
    # url =
    # don't forget to source your novarc file
    cloud = None
    label = None
    # user_id = None

    def vms(self):
        return self.nodes

    """

    def _retrief(self,f,exclude=[]):
        """ obtain information from libcloud, call with returns dicts

        
        Driver = get_driver(Provider.EUCALYPTUS)
        conn = Driver(key=euca_id, secret=euca_key, secure=False, host=host, path=path, port=port)

        images = retrief(conn.list_images, 
                      ['driver','ownerid','owneralias','platform','hypervisor','virtualizationtype','_uuid'])
        pprint (images)
        flavors = retrief(conn.list_sizes, ['_uuid'])
        pprint (flavors)


        vms = retrief(conn.list_nodes, ['private_dns','dns_name', 'instanceId', 'driver','_uuid'])

        pprint (vms)
        """
        vms = []
        nodes = f()
        for node in nodes:
            vm = {}
            for key in node.__dict__:
                value = node.__dict__[key]
                if key == 'extra':
                  for e in value:
                       vm[e] = value[e]
                else:
                    vm[key] = value
            for d in exclude:
                if d in vm: 
                    del vm[d]
            vms.append(vm)
        return vms

    def _clean_list(self,f,exclude=[]):
        """ obtain information from libcloud, call with returns dicts

        
        Driver = get_driver(Provider.EUCALYPTUS)
        conn = Driver(key=euca_id, secret=euca_key, secure=False, host=host, path=path, port=port)

        images = retrief(conn.list_images, 
                      ['driver','ownerid','owneralias','platform','hypervisor','virtualizationtype','_uuid'])
        pprint (images)
        flavors = retrief(conn.list_sizes, ['_uuid'])
        pprint (flavors)


        vms = retrief(conn.list_nodes, ['private_dns','dns_name', 'instanceId', 'driver','_uuid'])

        pprint (vms)
        """
        vms = []
        nodes = f()
        for node in nodes:
            vm = {}
            for key in node.__dict__:
                value = node.__dict__[key]
                if key == 'extra':
                  for e in value:
                       vm[e] = value[e]
                else:
                    vm[key] = value
            for d in exclude:
                if d in vm: 
                    del vm[d]
            vms.append(vm)
        return vms

    
    def __init__(self, label, project=None):
        """ initializes the openstack cloud from a defould novaRC file
        locates at ~/.futuregrid.org/openstack. However if the
        parameters are provided it will instead use them
        """
        self.connect(label, project)
        

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
        # self.credential = None
        self.cloud = None
        self.user_id = None


    def __str__(self):
        """
        print everything but the credentials that is known about this
        cloud in json format.
        """
        information = {
            'label': self.label,
            'flavors': self.sizes,
            'vms': self.nodes,
            'images': self.images}
        return json.dumps(information, indent=4)

    def vm_create(self, name=None,
                  flavor_name=None,
                  image_id=None,
                  security_groups=None,
                  key_name=None,
                  meta=None):
        """create a virtual machine with the given parameters"""
        return self.cloud.create_node(name=name, size=flavor_name,image=image_id)

    def _delete_keys_from_dict(self,elements, exclude):
        for d in exclude:
            if d in elements: 
                del elements[d]
        return elements

    def _get_flavors_dict(self):
        return self._retrief(self.cloud.list_sizes, ['_uuid','driver'])

    def _update_flavors_dict(self, information):
        id = information["id"]
        return (id, information)


    def _get_servers_dict(self):
        print "IOIOIOIOIO"
        print self.cloud.list_nodes()
        r = self._retrief(self.cloud.list_nodes, ['private_dns','dns_name', 'instanceId', 'driver','_uuid'])
        print "UIUIUIUIUIUI"
        pprint (r)
        return r
    
    def _update_servers_dict(self, information):
        id = information["id"]
        return (id, information)

    
    def _get_images_dict(self):
        r = self._retrief(self.cloud.list_images, 
                             ['driver',
                              'ownerid',
                              'owneralias',
                              'platform',
                              'hypervisor',
                              'virtualizationtype',
                              '_uuid'])
        print r
        return r

    def _update_images_dict(self, information):
        id = information["id"]
        return (id, information)
        

    
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

    cloud = eucalyptus("india-eucalyptus","fg-82")
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

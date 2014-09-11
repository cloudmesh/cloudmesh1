import sys

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

from cloudmesh.util.cm_table import cm_table
from cloudmesh.config.cm_config import cm_config
from cloudmesh.iaas.ComputeBaseType import ComputeBaseType
from cloudmesh_install import config_file

class eucalyptus(ComputeBaseType):

    """
    does not yet have proper yaml file management
    """

    """
    requires a cloudmesh yaml file with the following structure:

    default: sierra-openstack

    cloudmesh:

        india-eucalyptus:
            BASEDIR: ~/.cloudmesh/india/eucalyptus
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

    # filename not yet used
    filename = config_file("/cloudmesh.yaml")

    type = "eucalyptus"
    sizes = {}
    images = {}
    nodes = {}
    flavors_cache = None
    images_cache = None
    servers_cache = None
    credentials = None
    accesskey = None
    secretkey = None
    project = "fg82"
    config = None
    cloud = {}

    #
    # change to gregors credential class
    #
    def _get_vmname(self, prefix):
        return _generate_vmname(prefix, self.no)

    def _generate_vmname(self, prefix, index):
        number = str(index).zfill(3)
        name = '%s-%s' % (prefix, number)
        return name



    def connect(self, label, project):
        """
        establishes a connection to the eucalyptus cloud,
        e.g. initializes the needed components to conduct subsequent
        queries.
        """

        # from old eucalyptus_libcloud
        # path = os.environ['HOME'] + "/" + \
        # self.credentials.location.replace("/eucarc", "")
        # os.environ['CA_CERTS_PATH'] = path
        #         libcloud.security.CA_CERTS_PATH.append(self.credential['EUCALYPTUS_CERT'])



        self.label = label
        self.project = project

        # copied from deprecated code
        # if project is None:
        #    self.activate_project("fg82")
        # else:
        #    self.activate_project(project)

        print "Loading", self.label, self.project
        Driver = get_driver(Provider.EUCALYPTUS)

        self.config = cm_config()


        cred = self.config.get(self.label, expand=True)

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

        self.credential = self.config.get(self.label, expand=True)
        pprint(self.credential)

        # libcloud.security.CA_CERTS_PATH.append(self.credential['EUCALYPTUS_CERT'])
        # libcloud.security.VERIFY_SSL_CERT = False

        Driver = get_driver(Provider.EUCALYPTUS)
        self.cloud = Driver(key=euca_id, secret=euca_key, secure=False, host=host, path=path, port=port)

    """
    # url =
    # don't forget to source your novarc file
    cloud = None
    label = None
    # user_id = None

    def vms(self):
        return self.nodes

    """

    def _retrief(self, type, f, exclude=[]):
        """ obtain information from libcloud, call with returns dicts.
        
        Driver = get_driver(Provider.EUCALYPTUS)
        conn = Driver(key=euca_id, secret=euca_key, secure=False, host=host, path=path, port=port)

        images = retrief(conn.list_images, 
                      ['driver','ownerid','owneralias','platform','hypervisor','virtualizationtype','_uuid'])
        flavors = retrief(conn.list_sizes, ['_uuid'])
        vms = retrief(conn.list_nodes, ['private_dns','dns_name', 'instanceId', 'driver','_uuid'])

        pprint (vms)
        """
        element_array = []

        elements = f()
        if type == 'flavors':
            self.flavors_cache = elements
        elif type == 'servers':
            self.servers_cache = elements
        elif type == 'images':
            self.images_cache = elements

        for element in elements:
            vm = {}
            for key in element.__dict__:
                value = element.__dict__[key]
                if key == 'extra':
                    for e in value:
                        vm[e] = value[e]
                else:
                    vm[key] = value
            for d in exclude:
                if d in vm:
                    del vm[d]
            element_array.append(vm)
        return element_array


    def activate_project(self, project):
        """ this routine is wrong and has been copied from a deprecated code"""
        self.credentials = credentials_rc("eucalyptus")
        self.credentials.location = config_file("/india/eucalyptus/") + \
            project + "/eucarc"

        self.credentials.type('eucalyptus')

        self.access_key = self.credentials._get_rc_variable("accesskey")
        self.secret_key = self.credentials._get_rc_variable("secretkey")

        print self.access_key
        print self.secret_key

    def __init__(self, label,
                 project=None,
                 accessKey=None,
                 secretKey=None):
        """
        initializes the openstack cloud from a defould novaRC file
        locates at CONFIG/openstack. However if the
        parameters are provided it will instead use them
        """
        self.clear()
        # self.config(label, project, accessKey, secretKey)
        # self.connect()
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
        flavors_cache = None
        images_cache = None
        servers_cache = None
        self.credential = None
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

    def _delete_keys_from_dict(self, elements, exclude):
        for d in exclude:
            if d in elements:
                del elements[d]
        return elements

    def _get_flavors_dict(self):
        return self._retrief("flavors", self.cloud.list_sizes, ['_uuid', 'driver'])

    def _get_servers_dict(self):
        return self._retrief("servers", self.cloud.list_nodes, ['private_dns', 'dns_name', 'instanceId', 'driver', '_uuid'])

    def _get_images_dict(self):
        return self._retrief("images",
                             self.cloud.list_images,
                             ['driver',
                              'ownerid',
                              'owneralias',
                              'platform',
                              'hypervisor',
                              'virtualizationtype',
                              '_uuid'])

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

        """
        if not key_name is None:
            if not self.check_key_pairs(key_name):
                config = cm_config()
                dict_t = config.get()
                key = dict_t['keys']['keylist'][key_name]
                if not 'ssh-rsa' in key and not 'ssh-dss' in key:
                    key = open(key, "r").read()
                self.upload_key_pair(key, key_name)
        """

        config = cm_config()

        if flavor_name is None:
            flavor_name = config.default(self.label)['flavor']

        if image_id is None:
            image_id = config.default(self.label)['image']

        size = [s for s in self.flavors_cache if s.id == flavor_name][0]
        image = [i for i in self.images_cache if i.id == image_id][0]

        if key_name is None and security_groups is None:
            vm = self.cloud.create_node(name=name, image=image, size=size)
        else:
            print "not yet implemented"
            # bug would passing None just work?
            # vm = self.cloud.servers.create(name,
            #                               flavor=vm_flavor,
            #                               image=vm_image,
            #                               key_name=key_name,
            #                               security_groups=security_groups,
            #                               meta=meta
            #                               )
        data = vm.__dict__
        return data

    def vm_delete(self, id):
        """
        delete a single vm and returns the id
        """
        print "self.servers_cachec", self.servers_cache
        vm = [i for i in self.servers_cache if i.id == id][0]

        r = self.cloud.destroy_node(vm)

        return r.__dict__



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

    cloud = eucalyptus("india-eucalyptus", "fg-82")
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
# -      pp.pprint (cloud.images)
    """
    if vm_test:
      cloud.refresh('vms')

      print json.dumps(cloud.images, indent=4)

    if cloud_test:
      cloud.refresh()
      print cloud


    print cloud.find_user_id()
  """

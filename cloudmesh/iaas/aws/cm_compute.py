# -*- coding: utf-8 -*-

"""
cloudmesh.iaas.aws.cm_compute
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
# import boto
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.base import NodeImage, NodeSize

from cloudmesh.iaas.ComputeBaseType import ComputeBaseType
from cloudmesh.config.cm_config import cm_config

class aws(ComputeBaseType):
    """ Amazon Cloud service with the boto interface
    With boto interface, cloudmesh supports Amazon Web Services such as EC2, S3,
    EBS, etc.
    """

    name = "aws"
    DEFAULT_LABEL = name

    def __init__(self, label=DEFAULT_LABEL):
        self.load_default(label)
        self.connect()

    def load_default(self, label):
        """Load default values and set them to the object
        
        :param label: the section name to load from yaml
        :type label: str
        
        """

        self.compute_config = cm_config()
        self.user_credential = self.compute_config.credential(label)

        # Service certificate
        self.access_key_id = self.user_credential['access_key_id']
        self.secret_access_key = \
        self.user_credential['secret_access_key']

        # SSH
        self.ssh_userid = self.user_credential['userid']
        self.ssh_keyname = self.user_credential['keyname']
        self.ssh_pkey = self.user_credential['privatekeyfile']

        # set default flavor from yaml
        flavor = self.compute_config.default(label)['flavor']
        self.set_flavor(flavor)

        image_name = self.compute_config.default(label)['image']
        self.set_image_name(image_name)

        # set default location from yaml
        location = self.compute_config.default(label)['location']
        self.set_location(location)

    def connect(self):
        Driver = get_driver(Provider.EC2)
        conn = Driver(self.access_key_id, self.secret_access_key)
        self.conn = conn

    def vm_create(self, name,
                  flavor_name,
                  image_id,
                  security_groups=None,
                  key_name=None,
                  meta={},
                  userdata=None):
        self.create_vm()

    def create_vm(self):
        image = NodeImage(id=self.get_image_name(), name="", driver="")
        size = NodeSize(id=self.get_flavor(), name="", ram=None, disk=None,
                        bandwidth=None, price=None, driver="")
        self.conn.create_node(name=self.get_name(), image=image, size=size,
                              ex_keyname=self.get_keyname())
        return

    def list_vm(self):
        nodes = self.conn.list_nodes()
        vm_dict = {}
        for vm_obj in nodes:
            vm = vm_obj.__dict__
            instanceid = vm_obj.id
            vm_dict[instanceid] = vm

        self.nodes = vm_dict

        return self.nodes

    def vm_delete(self, name):
        self.delete_vm(name)

    def delete_vm(self, name):
        node = self.get_node_from_id(name)
        self.conn.destroy_node(node)
        return

    def get_node_from_id(self, id):
        nodelist = self.conn.list_nodes()
        for node in nodelist:
            if node.id == id:
                return node

    def set_location(self, name):
        self.location = name

    def set_image_name(self, name):
        self.image_name = name

    def set_flavor(self, name):
        self.flavor = name

    def get_name(self):
        return self.name

    def get_flavor(self):
        return self.flavor

    def get_keyname(self):
        return self.ssh_keyname

    def get_image_name(self):
        return self.image_name

    def _get_servers_dict(self):
        vm_list = self.list_vm()
        self.convert_to_openstack_style(vm_list)
        return vm_list

    def convert_to_openstack_style(self, vmlist):
        for vmid in vmlist:
            vm = vmlist[vmid]
            vm.update({"name": unicode(vm['id']), \
                       "status": self.convert_states(vm['extra']['status']), \
                       "addresses": self.convert_ips(vm['public_ips']), \
                       "flavor":
                       self.convert_flavors(vm['extra']['instancetype']), \
                       # "id": exists
                       "user_id": unicode(""), \
                       "metadata": {}, \
                       "key_name": unicode(vm['extra']['keyname']), \
                       "created": unicode(vm['extra']['launchdatetime'])\
                      })
            try:
                # deleting object to avoid mongodb errors when inserts
                vm.update({"driver":None})
            except:
                pass

    def convert_states(self, status):
        if status == "running":
            return "ACTIVE"
        elif status == "terminated":
            return "SHUTOFF"
        else:
            return status

    def convert_ips(self, ip):
        try:
            ip_address = ip[0]
        except IndexError:
            ip_address = ""
        ip_ver = 4
        ip_type = "fixed"
        res = {u'private':[ {u'version': ip_ver, u'addr': ip_address, \
                             u'OS-EXT-IPS:type': ip_type}]}
        return res

    def convert_flavors(self, flavor):
        res = {u'id': unicode(flavor), \
               u'links':\
               [ {u'href':None, \
                  u'rel':None}]}
        return res

    def release_unused_public_ips(self):
        return

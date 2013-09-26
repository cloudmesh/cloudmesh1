#import boto
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.base import NodeImage, NodeSize

from cloudmesh.config.cm_config import cm_config

class aws:
    """ Amazon Cloud service with the boto interface
    With boto interface, cloudmesh supports Amazon Web Services such as EC2, S3,
    EBS, etc.
    """

    name = "aws"

    def __init__(self):
        self.load_default(self.name)

    def load_default(self, label):
        """Load default values and set them to the object
        
        :param label: the section name to load from yaml
        :type label: str
        
        """

        self.compute_config = cm_config()
        self.user_credential = self.compute_config.credential(label)

        #Service certificate
        self.access_key_id = self.user_credential['access_key_id']
        self.secret_access_key =
        self.user_credential['secret_access_key']
       
        #SSH
        self.ssh_userid = self.user_credential['userid']
        self.ssh_keyname = self.user_credential['keyname']
        self.ssh_pkey = self.user_credential['privatekeyfile']
        
        #set default flavor from yaml
        flavor = self.compute_config.default(label)['flavor']
        self.set_flavor(flavor)

        image_name = self.compute_config.default(label)['image']
        self.set_image_name(image_name)

        #set default location from yaml
        location = self.compute_config.default(label)['location']
        self.set_location(location)

    def connect(self):
        Driver = get_driver(Provider.EC2)
        conn = Driver(self.access_key_id, self.secret_access_key)
        self.conn = conn
 
    def vm_create(self):
        self.create_vm()

    def create_vm(self):
        image = NodeImage(id=self.get_image_name(), name="", driver="")
        size = NodeSize(id=self.get_flavor(), name="", ram=None, disk=None,
                        bandwidth=None, price=None, driver="")
        self.conn.create_node(self.get_name(), image=image, size=size,
                              ex_keyname=self.get_keyname())
        return

    def list_vm(self):
        self.nodes = self.conn.list_nodes()
        return self.nodes

    def vm_delete(self):
        self.delete_vm()

    def delete_vm(self):
        return

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

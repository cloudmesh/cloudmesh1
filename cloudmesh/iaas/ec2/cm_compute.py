# -*- coding: utf-8 -*-

"""
cloudmesh.iaas.ec2.cm_compute
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from cloudmesh.config.cm_config import cm_config
from cloudmesh.config.cm_config import cm_config_flavor
from cloudmesh.iaas.ComputeBaseType import ComputeBaseType
from libcloud.compute.base import NodeImage, NodeSize
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider
import libcloud.security
import sys

import urlparse
import tempfile


class ec2(ComputeBaseType):

    """ 
    ec2 service with the libcloud interface
    With libcloud interface, cloudmesh supports Amazon Web Services such as EC2, S3,
    EBS, etc.
    """

    name = "ec2"
    DEFAULT_LABEL = name

    def __init__(self, label=DEFAULT_LABEL, credential=None,
                 admin_credential=None):
        self.load_default(label)
        self.set_credential(credential, admin_credential)
        self.connect()

    def set_credential(self, cred, admin_cred):
        if cred:
            self.user_credential = cred
            self.access_key_id = self.user_credential['EC2_ACCESS_KEY']
            self.secret_access_key = \
                self.user_credential['EC2_SECRET_KEY']
        if admin_cred:
            self.admin_credential = admin_cred

    def load_default(self, label):
        """Load default values and set them to the object

        :param label: the section name to load from yaml
        :type label: str

        """

        self.compute_config = cm_config()
        self.user_credential = self.compute_config.credential(label)

        # Service certificate
        self.access_key_id = self.user_credential['EC2_ACCESS_KEY']
        self.secret_access_key = \
            self.user_credential['EC2_SECRET_KEY']

        # SSH
        self.ssh_userid = self.user_credential['userid']
        self.ssh_keyname = self.user_credential['keyname']
        self.ssh_pkey = self.user_credential['EC2_PRIVATE_KEY']

        # set default flavor from yaml
        flavor = self.compute_config.default(label)['flavor']
        self.set_flavor(flavor)

        image_name = self.compute_config.default(label)['image']
        self.set_image_name(image_name)

        # set default location from yaml
        # location = self.compute_config.default(label)['location']
        # self.set_location(location)

        # Auth url
        self.ec2_url = self.user_credential['EC2_URL']
        self.hostname, self.port, self.path, self.is_secure = \
            self._urlparse(self.ec2_url)

        self.certfile = self.user_credential['EUCALYPTUS_CERT']
        libcloud.security.CA_CERTS_PATH.append(self.certfile)

        # Skip this step if you are launching nodes on an official
        # provider. It is intended only for self signed SSL certs in
        # test deployments.
        # Note: Code like this poses a security risk (MITM attack) and
        # that's the reason why you should never use it for anything else
        # besides testing. You have been warned.
        libcloud.security.VERIFY_SSL_CERT = False

        self.label = label

    def auth(self):
        return self.conn is not None

    def connect(self):
        Driver = get_driver(Provider.EUCALYPTUS)
        conn = None

        #
        # BUG, make sure we use the cert, confirm with team ....
        #
        try:
            conn = Driver(key=self.access_key_id,
                          secret=self.secret_access_key,
                          secure=self.is_secure,
                          host=self.hostname,
                          path=self.path,
                          port=self.port)

        except Exception, e:
            print e
            sys.exit()

        self.conn = conn

    def vm_create(self, name,
                  flavor_name,
                  image_id,
                  security_groups=None,
                  key_name=None,
                  meta={},
                  userdata=None):
        self.name = name
        self.create_vm(flavor_name, image_id, key_name)

    def create_vm(self, flavor_name, image_id, key_name):
        image = NodeImage(id=image_id, name="", driver="")
        size = NodeSize(id=flavor_name, name="", ram=None, disk=None,
                        bandwidth=None, price=None, driver="")
        self.conn.create_node(name=self.get_name(), image=image, size=size,
                              ex_keyname=key_name)
        return

    def list_vm(self):
        nodes = self.conn.list_nodes()
        vm_dict = {}
        for vm_obj in nodes:
            vm = vm_obj.__dict__
            instanceid = vm_obj.id
            vm_dict[instanceid] = vm

        self.servers = vm_dict
        return self.servers

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
        self.encode_output(vm_list)
        return vm_list

    def encode_output(self, vmlist):
        for vmid in vmlist:
            vm = vmlist[vmid]
            vm.update({"name": unicode(vm['id']),
                       "status": self.convert_states(vm['extra']['status']),
                       "addresses": self.convert_ips(vm['public_ips']),
                       "flavor":
                       self.convert_flavors(vm['extra']['instance_type']),
                       # "id": exists
                       "user_id": unicode(""),
                       "metadata": {},
                       "key_name": unicode(vm['extra']['key_name']),
                       "created": unicode(vm['extra']['launch_time'])
                       })
            try:
                # deleting object to avoid mongodb errors when inserts
                vm.update({"driver": None})
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
        res = {u'private': [
            {u'version': ip_ver,
             u'addr': ip_address,
             u'OS-EXT-IPS:type': ip_type}
        ]
        }
        return res

    def convert_flavors(self, flavor):
        res = {u'id': unicode(flavor),
               u'links': [
            {u'href': None,
             u'rel': None}
        ]
        }
        return res

    def release_unused_public_ips(self):
        return

    def _urlparse(self, ec2_url):
        """Return host, port and path from ec2_url"""

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

        return host, port, path, is_secure

    def _get_flavors_dict(self):

        try:
            result = self.get_flavors_from_yaml()
        except:
            result = None
        if not result:
            result_list = self.list_flavors()
            result = self.convert_to_dict(result_list)

        self.flavors = result
        return self.flavors

    def get_flavors_from_yaml(self):
        obj = cm_config_flavor()
        flavors = obj.get('cloudmesh.flavor')
        return flavors.get(self.label)

    def convert_to_dict(self, _list):
        res_dict = {}
        for row in _list:
            # row looks like
            # {'_uuid': None, 'name': 'Micro Instance', 'price': 0.02, 'ram':
            # 613, 'driver': <libcloud.compute.drivers.ec2.EucNodeDriver
            # object at 0x307e350>, 'bandwidth': None, 'disk': 15, 'id':
            # 't1.micro'}
            res_dict[row.id] = row.__dict__
            del(row.driver)
        return res_dict

    def list_flavors(self):
        return self.conn.list_sizes()

    def _get_images_dict(self):
        res = self.list_images()
        res_dict = self.convert_to_dict(res)
        self.images = res_dict
        return self.images

    def list_images(self):
        return self.conn.list_images()

    def keypair_list(self):
        """Return a keypair list. keypair_list() function name is fixed

        :returns: dict
        """

        keylist = self.conn.ex_describe_all_keypairs()
        res = {'keypairs': []}
        for keyname in keylist:
            tmp = {'keypair': {'name': keyname}}
            res['keypairs'].append(tmp)
        return res

    def keypair_add(self, name, content):
        """Add a keypair"""

        return self.conn.ex_import_keypair_from_string(name, content)
        '''

        keyfile = tempfile.NamedTemporaryFile(delete=False)
        keyfile.write(content)
        keyfile_name = keyfile.name
        keyfile.close()

        return self.conn.ex_import_keypair(name, keyfile_name)
        '''

    def keypair_remove(self, name):
        """Delete a keypair"""
        if self.conn.ex_delete_keypair(name):
            return {"msg": "success"}

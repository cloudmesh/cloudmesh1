# -*- coding: utf-8 -*-

"""
cloudmesh.iaas.azure.cm_compute
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import time
import tempfile
import json

from azure import *
from azure.servicemanagement import *
from cloudmesh.iaas.ComputeBaseType import ComputeBaseType
from cloudmesh.config.cm_config import cm_config
from cloudmesh.config.cm_config import cm_config_flavor
from cloudmesh_common.util import get_unique_name, get_rand_string

class azure(ComputeBaseType):

    DEFAULT_LABEL = "azure"
    name_prefix = "cm-"

    def_flavors = {u'ExtraSmall': {'id': "1", 'name':'ExtraSmall'},  \
                   u'Small': {'id': "2", 'name': 'Small'}, \
                   u'Medium': {'id': "3", 'name': 'Medium'}, \
                   u'Large': {'id': "4", 'name': 'Large'}, \
                   u'ExtraLarge': {'id': "5", 'name': 'ExtraLarge'} }

    linux_config = None
    thumbprint = None

    def __init__(self, label=DEFAULT_LABEL, credential=None,
                 admin_credential=None):

        self.set_vars()
        self.load_default(label)
        self.set_credential(credential, admin_credential)
        self.connect()

    def set_credential(self, cred, admin_cred):
        if cred:
            self.user_credential = cred
        if admin_cred:
            self.admin_credential = admin_cred

    def set_vars(self):
        """Set default variables for the azure class"""

        # Set a default name from uuid random string
        name = get_unique_name(self.name_prefix)
        self.set_name(name)


        self.blob_domain = "blob.core.windows.net"
        self.blob_ext = ""
        self.container = "os-image"
        # Use a same name with blob and vm deployment
        self.blobname = self.name

        # account for the vm
        self.userid = 'azureuser'
        self.user_passwd = 'azureuser@password'

        self.cloud_services = None

    def load_default(self, label):
        """Load default values and set them to the object
        
        :param label: the section name to load from yaml
        :type label: str
        
        """

        self.compute_config = cm_config()
        self.user_credential = self.compute_config.credential(label)

        # SSH
        self.thumbprint_path = self.user_credential['thumbprint']

        # Service certificate & SSH
        self.service_certificate_path = self.user_credential['servicecertfile']

        # set default location from yaml
        location = self.compute_config.default(label)['location']
        self.set_location(location)

        # Set a default os image name
        os_image_name = self.compute_config.default(label)['image']
        self.set_os_image(os_image_name)

        # Set a default flavor (role size between ExtraSmall, Small, Medium,
        # Large, ExtraLarge
        flavor = self.compute_config.default(label)['flavor']
        self.set_flavor(flavor)
        
        self.label = label

    def connect(self):
        subscription_id = self.user_credential['subscriptionid']
        certificate_path = self.user_credential['managementcertfile']

        self.sms = ServiceManagementService(subscription_id,
                                            certificate_path)

    # FOR refresh
    def _get_images_dict(self):
        return self.get_images()

    def get_images(self):
        """Return available operating systems images on Windows Azure

        :returns: dict.

        """

        images = self.sms.list_os_images()
        res = {}
        for image in images:
            name = image.name
            res[name] = image.__dict__
            res[name]['id'] = name

        self.images = res
        return res

    # FOR refresh
    def _get_servers_dict(self):
        """Return running virtual machines

        :returns: dict.
        """
        deployments = self.list_deployments()
        self.encode_output(deployments)
        return deployments

    def _get_services_dict(self):
        return self.list_services()

    def list_services(self):
        """Return the cloud services available on the account.
        cloud service is required to create a deployment.

        :returns: dict.

        """

        cloud_services = self.sms.list_hosted_services()
        res = {}
        for service in cloud_services:
            name = service.service_name
            main_properties = service.__dict__
            sub_properties = service.hosted_service_properties.__dict__
            merged_properties = dict(main_properties.items() +
                                     sub_properties.items())
            res[name] = merged_properties
            res[name]['id'] = name

        self.cloud_services = cloud_services

        return res

    def list_deployments(self):
        """Return the deployments available on the account.
        A launched vm instance is a deployment.

        """
        # if not self.cloud_services:
        self.cloud_services = self.sms.list_hosted_services()

        deployments = {}
        self.cloud_services_props = {}
        for cloud_service in self.cloud_services:
            name = cloud_service.service_name
            props = self.sms.get_hosted_service_properties(name, True)
            self.cloud_services_props[name] = props
            for deployment in props.deployments:
                id = deployment.private_id
                deployments[id] = deployment.__dict__

        self.deployments = deployments
        self.servers = deployments
        return deployments

    def azure_naming_convention(self, name):
        # Azure Naming convention
        # The name can contain only letters, numbers, and hyphens. The name must
        # start with a letter and must end with a letter or a number.
        # The hosted service name is invalid.
        # Set a name from uuid random string
        #vm_name = get_unique_name(name)
        vm_name = name.replace("_","-")
        vm_name = vm_name #+ "-" + get_rand_string()
        return vm_name

    def vm_create(self, name,
                  flavor_name,
                  image_id,
                  security_groups=None,
                  key_name=None,
                  meta={},
                  userdata=None):

        vm_name = self.azure_naming_convention(name)
        self.set_name(vm_name)

        # Set a os image name
        os_image_name = image_id
        self.set_os_image(os_image_name)

        # set a flavor
        self.set_flavor_by_idx(flavor_name)

        self.create_vm()

    def set_linux_cfg(self, refresh=False):
        if refresh or not self.linux_config:
            self.linux_config = LinuxConfigurationSet(self.get_name(), self.userid, None, True)

    def create_vm(self):
        """Create a Window Azure Virtual Machine

        :returns: azure.servicemanagement.AsynchronousOperationResult

        """
        self.create_hosted_service()
        # Load the os image information
        self.load_os_image()

        # Get the url for the blob image file of the vm to be generated
        self.get_media_url()

        os_hd = OSVirtualHardDisk(self.os_image_name, self.media_url)
        self.set_linux_cfg()
        linux_config = self.linux_config#LinuxConfigurationSet(self.get_name(), self.userid, None, True)
        # self.userid, self.user_passwd, True)

        self.set_ssh_keys(linux_config)
        self.set_network()
        self.set_service_certs()
        # can't find certificate right away.
        time.sleep(7)

        result = \
        self.sms.create_virtual_machine_deployment(service_name=self.get_name(), \
                                                   deployment_name=self.get_name(), \
                                                   deployment_slot='production', \
                                                   label=self.get_name(), \
                                                   role_name=self.get_name(), \
                                                   system_config=linux_config, \
                                                   os_virtual_hard_disk=os_hd, \
                                                   network_config=self.network, \
                                                   role_size=self.get_flavor())

        time.sleep(7)
        self.result = result
        return result

    def vm_delete(self, name):
        self.delete_vm(name)

    def delete_vm(self, name):
        """Tear down the virtual machine deployment (instance).
        It requires several steps to clear up all allocated resources.

        1. delete deployment
        2. delete cloud (hosted) service
        3. delete os image
        4. delete blob storage disk

        :param name: the name of the cloud service
        :type name: str.

        """

        disk_names = []
        props = self.sms.get_hosted_service_properties(name, True)
        for deployment in props.deployments:
            try:
                for role in deployment.role_list:
                    role_props = self.sms.get_role(name, deployment.name,
                                                   role.role_name)
                    d_name = role_props.os_virtual_hard_disk.disk_name
                    if d_name not in disk_names:
                        disk_names.append(d_name)
            except:
                pass
            result = self.sms.delete_deployment(name, deployment.name)
            time.sleep(5)
        self.sms.delete_hosted_service(name)
        # result = self.sms.delete_os_image(self.os_image_name)
        time.sleep(5)
        for disk_name in disk_names:
            try:
                self.sms.delete_disk(disk_name)
            except:
                pass
        # self.bc.delete_container(self.container_name)

    def list_cloud_services(self):
        return self.sms.list_hosted_services()

    def set_name(self, name):
        """Set a name of the virtual machine to deploy. Unique name is required
        to avoid duplication.

        :param name: the name of the virtual machine to use
        :type name: str

        """
        self.name = name

    def get_name(self):
        return self.name

    def create_hosted_service(self):
        """Create a cloud (hosted) service via create_hosted_service()
        :param name: (optional) the name of a cloud service to use
        :type name: str.
        :param location: (optional) the name of a
        location for the cloud service 
        :type location: str.
                                    
        """

        self.sms.create_hosted_service(service_name=self.name,
                                       label=self.name,
                                       location=self.location)

    def set_location(self, name):
        """Set a geographical location for the virtual machine

        :param name: the location
        :type name: str

        """
        self.location = name

    def get_location(self):
        return self.location

    def set_os_image(self, name):
        """Set os image for the virtual machine

        :param name: the name of the operating system image to use
        :type name: str

        """
        self.os_image_name = name

    def load_os_image(self, name=None):
        """Load the os image information from Windows Azure

        :param name: the name of the os image to load
        :type name: str

        """
        if not name:
            name = self.os_image_name
        self.os_image = self.sms.get_os_image(name)

    def get_media_url(self):
        """Return a media url to create a http url for the blob file
        
        :returns: str.
        
        """

        storage_account = self.get_storage_account()
        blob_domain = self.get_blob_domain()
        blobname = self.get_blobname()
        container = self.get_container()
        blob_filename = blobname + self.blob_ext
        media_url = "http://" + storage_account + "." + blob_domain \
                + "/" + container + "/" + blob_filename
        self.media_url = media_url

        return media_url

    def get_storage_account(self):
        """Return a storage account.

        If there is a selected image to deploy, the same storage account will be
        used where the image's located.
        Otherwise, the last storage account of the subscription will be used.

        Note. 
        The disk's VHD must be in the same account as the VHD of the source
        image (source account: xxx.blob.core.windows.net, target
        account: xxx.blob.core.windows.net).

        :returns: str.

        """

        if self.os_image and self.os_image.media_link:
            account_name = self.get_hostname(self.os_image.media_link)
        else:
            account_name = self.get_last_storage_account()

        self.storage_account = account_name
        return account_name

    def get_last_storage_account(self):
        """Return the last storage account name of a subscription id
 
        :returns: str.

        """
        result = self.sms.list_storage_accounts()
        for account in result:
            storage_account = account.service_name
        try:
            return storage_account
        except:
            self.create_storage_account()
            storage_account = self.get_name()
            return storage_account

    def create_storage_account(self):
        name = self.get_name()[:24].replace("-", "")
        # A name for the storage account that is unique within Windows Azure.
        # Storage account names must be between 3 and 24 characters in
        # length
        # and use numbers and lower-case letters only.
        desc = name + "description"
        labe = name + "label"
        loca = self.get_location()
        self.sms.create_storage_account(service_name=name,
                                        description=desc,
                                        label=labe,
                                        location=loca)

    def get_hostname(self, url):
        """Return a hostname from the url.
        top hostname indicates a storage account name

        :param url: a media_link
        :type url: str.

        """
        try:
            o = urlparse(url)
            host = o.hostname.split(".")[0]
        except:
            host = None

        return host

    def get_container(self):
        return self.container

    def get_blobname(self):
        return self.blobname

    def get_os_name(self):
        return self.os_image_name

    def get_blob_domain(self):
        return self.blob_domain

    def set_ssh_keys(self, config):
        """Configure the login credentials with ssh keys for the virtual machine.
        This is only for linux OS, not Windows.

        :param config: the return value of LinuxConfigurationSet()
        :type config: class LinuxConfigurationSet

        """

        # fingerprint captured by 'openssl x509 -in myCert.pem -fingerprint
        # -noout|cut -d"=" -f2|sed 's/://g'> thumbprint'
        # (Sample output) C453D10B808245E0730CD023E88C5EB8A785ED6B
        self.thumbprint = open(self.thumbprint_path, 'r').readline().split('\n')[0]
        publickey = PublicKey(self.thumbprint, self.get_authorized_keys_path())
        # KeyPair is a SSH kay pair both a public and a private key to be stored
        # on the virtual machine.
        # http://msdn.microsoft.com/en-us/library/windowsazure/jj157194.aspx#SSH
        keypair = KeyPair(self.thumbprint, self.get_key_pair_path())
        config.ssh.public_keys.public_keys.append(publickey)
        config.ssh.key_pairs.key_pairs.append(keypair)

        # Note
        # Since PKCS#10 X.509 is not fully supported by pycrypto, paramiko can
        # not use the key generated with PKCS, for example, openssl req ...
        # To do bypass, ssh-keygen can be used in the following order
        #
        # Generate a key pair
        # 1. ssh-keygen -f myPrivateKey.key (default is rsa and 2048 bits)
        #
        # Get certificate from a private key
        # 2. openssl req -x509 -nodes -days 365 -new -key myPrivateKey.key
        # -out myCert.pem
        #
        # .cer can be generated
        # openssl x509 -outform der -in myCert.pem -out myCert.cer
        #
        # .pfx
        # openssl pkcs12 -in myCert.pem -inkey myPrivateKey.key
        # -export -out myCert.pfx

        # reference:
        # http://www.sslshopper.com/article-most-common-openssl-commands.html

    def keypair_list(self):
        return []

    def keypair_add(self, name, content):
        self.load_thumbprint()
        fp = tempfile.NamedTemporaryFile(delete=False)
        fp.write(b'%s' % content)
        fp.close()
        publickey_path = fp.name
        publickey = PublicKey(self.thumbprint, publickey_path)
        # KeyPair is a SSH kay pair both a public and a private key to be stored
        # on the virtual machine.
        # http://msdn.microsoft.com/en-us/library/windowsazure/jj157194.aspx#SSH
        self.set_linux_cfg()
        self.linux_config.ssh.public_keys.public_keys.append(publickey)

    def load_thumbprint(self):
        if not self.thumbprint:
            self.thumbprint = open(self.thumbprint_path, 'r').readline().split('\n')[0]

    def set_network(self):
        """Configure network for a virtual machine.
        End Points (ports) can be opened through this function.
        For example, opening ssh(22) port will be configured.

        """
        network = ConfigurationSet()
        network.configuration_set_type = 'NetworkConfiguration'
        network.input_endpoints.input_endpoints.append(ConfigurationSetInputEndpoint('ssh', 'tcp', '22', '22'))
        self.network = network

    def set_service_certs(self):
        """Add a certificate to cloud (hosted) service.
        Personal Information Exchange (.pfx) should exist in the azure config
        directory (e.g. $HOME/.azure/.ssh/myCert.pfx). Python SDK only support
        .pfx at this time.

        """
        # command used:
        # openssl pkcs12 -in myCert.pem -inkey myPrivateKey.key
        # -export -out myCert.pfx

        cert_data_path = self.service_certificate_path
        with open(cert_data_path, "rb") as bfile:
            cert_data = base64.b64encode(bfile.read())

        cert_format = 'pfx'
        cert_password = ''
        cert_res = self.sms.add_service_certificate(service_name=self.get_name(),
                                                    data=cert_data,
                                                    certificate_format=cert_format,
                                                    password=cert_password)
        self.cert_return = cert_res

    def set_userid(self, name):
        self.userid = name

    def set_user_password(self, passwd):
        self.user_passwd = passwd

    def get_authorized_keys_path(self):
        self.authorized_keys_path = "/home/" + self.userid + \
        "/.ssh/authorized_keys"

        return self.authorized_keys_path

    def get_key_pair_path(self):
        path = "/home/" + self.userid + '/.azure/myPrivateKey.key'
        return path

    def set_flavor(self, size):
        """Set role size (flavor)
        
        :param size: ExtraSmall|Small|Medium|Large|ExtraLarge
        :type size: str
        """

        self.flavor = size

    def set_flavor_by_idx(self, idx):
        flavors = self.def_flavors
        for i in flavors:
            if flavors[i]['id'] == str(idx):
                self.set_flavor(flavors[i]['name'])
                return

    def get_flavor(self):
        """Return the image size to deploy

        :returns: str.
        """

        return self.flavor

    def get_status(self, name=None):
        """Get information about the deployed service by the name

        :param name: the name of the deployment
        :type name: str
        :returns: object
        """

        if not name:
            name = self.get_name()

        return self.sms.get_deployment_by_name(service_name=name,
                                               deployment_name=name)

    def encode_output(self, deployments):
        """Chance key names of the deployments to fit into openstack's list.
           name, status, addresses, flavor, id, user_id, metadata, key_name,
           created are required in openstack's list.

        :param deployments: list of deployments
        :type deployments: dict
        """

        for deployment_id in deployments:
            deployment = deployments[deployment_id]
            deployment.update({  # "name": exist
                               "status": self.convert_states(deployment['status']), \
                               "addresses":
                               self.convert_ips(deployment['role_instance_list']), \
                               "flavor":
                               self.convert_flavors(deployment['role_instance_list']), \
                               "id": deployment['name'], \
                               "user_id": unicode(""), \
                               "metadata": {}, \
                               "key_name": unicode(""), \
                               "created": deployment['created_time'] \
                              })

            '''
            try:
                # flattening class variables to the top level dict
                deployment.update({"role_list":
                                   deployment['role_list'][0].__dict__, \
                                   "role_instance_list":
                                   deployment['role_instance_list'][0].__dict__})
            #except IndexError:
            except:
                deployment.update({"role_list": None, \
                                   "role_instance_list": None})
            deployment = oJSONEncoder().encode(deployment)
            deployment = json.JSONDecoder().decode(deployment)
            '''
            deployment.update({"role_list": None})
            try:
                public_ip = \
                deployment['role_instance_list'][0].__dict__['instance_endpoints'][0].__dict__['vip']
            except:
                public_ip = ""
            deployment.update({"vip": public_ip})
            deployment.update({"role_instance_list": None})
 
    def convert_states(self, state):
        if state == "Running":
            return "ACTIVE"
        else:
            return state

    def convert_ips(self, role_instance_list):
        """Convert azure's data into openstack's type

        role_instance_list is an azure class which contains, for example,

        {'instance_upgrade_domain': 0, 'instance_size': u'ExtraSmall', 
        'fqdn': u'', 'instance_fault_domain': 0, 
        'instance_name': u'cm-e7a65a9e29dd11e39a290026b9852d93', 
        'role_name': u'cm-e7a65a9e29dd11e39a290026b9852d93', 
        'power_state': u'Started', 'instance_error_code': u'', 
        'ip_address': u'100.67.38.83', 'instance_status': u'ReadyRole',
        'instance_state_details': u''}

        :param role_instance_list: role instance list class of azure
        :type role_instance_list: class
        :returns: dict

        """

        try:
            ril = role_instance_list[0]
            ip_address = ril.ip_address
        except IndexError:
            ip_address = ""

        ip_ver = 4  # can we see it is ipv6 in azure?
        ip_type = u'fixed'  # determine if it is a fixed address or a floating

        # Openstack's type
        res = {  # u'private':[ {u'version':None, u'addr':None, \
               #              u'OS-EXT-IPS:type': None} ],
               u'private':[
                           {u'version':ip_ver, u'addr':ip_address, \
                            u'OS-EXT-IPS:type': ip_type}
                           ] 
               }
        return res

    def convert_flavors(self, role_instance_list):
        """Convert azure's data into openstack's type

        :param role_instance_list: role instance list class of azure
        :type role_instance_list: class
        :returns: dict

        """

        try:
            ril = role_instance_list[0]
            flavor = ril.instance_size
        except IndexError:
            flavor = ""
        res = {u'id': unicode(flavor), \
               u'links': \
               [{u'href':None, \
                 u'rel':None}]}
        return res

    def release_unused_public_ips(self):
        return

    def _get_flavors_dict(self):
        try:
            result = self.get_flavors_from_yaml()
        except:
            result = None
        if not result:
            return self.list_flavors()

        self.flavors = result
        return self.flavors

    def get_flavors_from_yaml(self):
        obj =  cm_config_flavor()
        flavors = obj.get('cloudmesh.flavor')
        return flavors.get(self.label)

    def list_flavors(self):

        self.flavors = self.def_flavors
        return self.flavors

class oJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if not isinstance(o, dict):
            return vars(o)
        return json.JSONEncoder.default(self, o)

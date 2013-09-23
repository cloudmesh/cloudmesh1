# -*- coding: utf-8 -*-

"""
cloudmesh.iaas.azure.cm_compute
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import time

from azure import *
from azure.servicemanagement import *
from cloudmesh.iaas.ComputeBaseType import ComputeBaseType
from cloudmesh.config.cm_config import cm_config
from cloudmesh.util.util import get_unique_name

class azure(ComputeBaseType):

    DEFAULT_LABEL = "windows_azure"
    name_prefix = "cm-"

    def __init__(self, label=DEFAULT_LABEL):

        self.set_vars()
        self.load_default(label)
        self.connect()

    def set_vars(self):
        """Set default variables for the azure class"""

        #Set a default name from uuid random string
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

    def load_default(self, label):
        """Load default values and set them to the object
        
        :param label: the section name to load from yaml
        :type label: str
        
        """

        self.compute_config = cm_config()
        self.user_credential = self.compute_config.credential(label)

        #SSH
        self.thumbprint_path =  self.user_credential['thumbprint']

        #Service certificate & SSH
        self.service_certificate_path = self.user_credential['servicecertfile']
      
        #set default location from yaml
        location = self.compute_config.default(label)['location']
        self.set_location(location)

        #Set a default os image name
        os_image_name = self.compute_config.default(label)['image']
        self.set_os_image(os_image_name)

        #Set a default flavor (role size between ExtraSmall, Small, Medium,
        # Large, ExtraLarge
        flavor = self.compute_config.default(label)['flavor']
        self.set_flavor(flavor)

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

        return res

    # FOR refresh
    def _get_services_dict(self):
        return self.get_services()

    def get_services(self):
        """Return the cloud services available on the account.
        A launched vm instance is the cloud service.
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

        return res

    def vm_create(self):
        self.create_vm()

    def create_vm(self):
        """Create a Window Azure Virtual Machine

        :returns: azure.servicemanagement.AsynchronousOperationResult

        """
        self.create_hosted_service()
        #Load the os image information
        self.load_os_image()

        #Get the url for the blob image file of the vm to be generated
        self.get_media_url()

        os_hd = OSVirtualHardDisk(self.os_image_name, self.media_url)
        linux_config = LinuxConfigurationSet(self.get_name(), self.userid, None, True)
        #self.userid, self.user_passwd, True)

        self.set_ssh_keys(linux_config)
        self.set_network()
        self.set_service_certs()
        # can't find certificate right away.
        time.sleep(5)

        result = \
        self.sms.create_virtual_machine_deployment(service_name=self.get_name(), \
                                                   deployment_name=self.get_name(), \
                                                   deployment_slot='production',\
                                                   label=self.get_name(), \
                                                   role_name=self.get_name(), \
                                                   system_config=linux_config, \
                                                   os_virtual_hard_disk=os_hd, \
                                                   network_config=self.network,\
                                                   role_size=self.get_flavor())

        self.result = result
        return result

    def vm_delete(self):
        self.delete_vm()

    def delete_vm(self):
        return

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
        name = self.get_name()[:24].replace("-","")
        # A name for the storage account that is unique within Windows Azure. 
        # Storage account names must be between 3 and 24 characters in
        # length 
        # and use numbers and lower-case letters only.
        desc = name + "description"
        labe = name + "label"
        loca = self.get_location()
        self.sms.create_storage_account(service_name = name,
                                        description = desc,
                                        label = labe,
                                        location = loca)

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

    def get_flavor(self):
        """Return the image size to deploy

        :returns: str.
        """

        return self.flavor


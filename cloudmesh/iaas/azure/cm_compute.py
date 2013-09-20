# -*- coding: utf-8 -*-

"""
cloudmesh.iaas.azure.cm_compute
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from azure import *
from azure.servicemanagement import *
from cloudmesh.iaas.ComputeBaseType import ComputeBaseType
from cloudmesh.config.cm_config import cm_config
from cloudmesh.util.util import get_unique_name

class azure(ComputeBaseType):

    DEFAULT_LABEL = "windows_azure"
    name_prefix = "cm-"

    def __init__(self, label=DEFAULT_LABEL):

        self.compute_config = cm_config()
        self.user_credential = self.compute_config.credential(label)

        self.load_default(label)
        self.connect()

    def load_default(self, label):
        """Load default values and set them to the object
        
        :param label: the section name to load from yaml
        :type label: str
        
        """
        
        #Set a default name from uuid random string
        name = get_unique_name(self.name_prefix)
        self.set_name(name)

        #set default location from yaml
        location = self.compute_config.default(label)['location']
        self.set_location(location)

        #Set a default os image name
        os_image_name = self.compute_config.default(label)['image']
        self.set_os_image(os_image_name)

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
        """Create a Window Azure Virtual Machine

        :returns: azure.servicemanagement.AsynchronousOperationResult

        """
        self.create_hosted_service()
        #Load the os image information
        self.load_os_image()

        self.get_media_link(blobname=name)

        os_hd = OSVirtualHardDisk(self.image_name, self.media_link)
        linux_config = LinuxConfigurationSet(self.get_name(), self.linux_user_id,
                                             self.linux_user_passwd, True)

        self.set_ssh_keys(linux_config)
        self.set_network()
        self.set_service_certs()
        # can't find certificate right away.
        sleep(5)

        result = \
        self.sms.create_virtual_machine_deployment(service_name=self.get_name(), \
                                                   deployment_name=self.get_name(), \
                                                   deployment_slot='production',\
                                                   label=self.get_name(), \
                                                   role_name=self.get_name(), \
                                                   system_config=linux_config, \
                                                   os_virtual_hard_disk=os_hd, \
                                                   network_config=self.network,\
                                                   role_size=self.get_role_size())

        self.result = result
        return result

    def set_name(self, name):
        """Set a name of the virtual machine to deploy. Unique name is required
        to avoid duplication.

        :param name: the name of the virtual machine to use
        :type name: str

        """
        self.name = name

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

    def set_os_image(self, name):
        """Set os image for the virtual machine

        :param name: the name of the operating system image to use
        :type name: str

        """
        self.os_image = name

    def load_os_image(self, name=None):
        """Load the os image information from Windows Azure

        :param name: the name of the os image to load
        :type name: str

        """
        if not name:
            name = self.os_image
        self.image = self.sms.get_os_image(name)

    def get_media_link(self, blobname):
        """"""


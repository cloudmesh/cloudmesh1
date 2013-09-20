# -*- coding: utf-8 -*-

"""
cloudmesh.iaas.azure.cm_compute
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from azure import *
from azure.servicemanagement import *
from cloudmesh.iaas.ComputeBaseType import ComputeBaseType
from cloudmesh.config.cm_config import cm_config

class azure(ComputeBaseType):

    DEFAULT_LABEL = "windows_azure"

    def __init__(self, label=DEFAULT_LABEL):
        self.compute_config = cm_config()
        self.user_credential = self.compute_config.credential(label)

        self.connect()

    def connect(self):
        subscription_id = self.user_credential['subscriptionid']
        certificate_path = self.user_credential['managementcertfile']

        self.sms = ServiceManagementService(subscription_id,
                                            certificate_path)

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

    def vm_create(self, name=None, location=None):
        """Create a Window Azure Virtual Machine

        :param name: (optional) the name of a virtual machine to use.
        :type name: str.
        :param location: (optional) the name of a
        location to use for the
        virtual machine.
        :type location: str.
        :returns: azure.servicemanagement.AsynchronousOperationResult

        """
        self.set_name(name)
        self.connect_service()
        self.create_cloud_service(name, location)
        self.set_image()
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

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

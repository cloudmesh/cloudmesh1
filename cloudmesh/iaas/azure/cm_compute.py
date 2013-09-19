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
        return self._get_registered_image()

    def _get_registered_image(self, label=None, name=None):
        """Return available operating systems images on Windows Azure

        :param label: (optional) a simple description of images. not unique
        value
        :type label: str.
        :param name: (optional) a unique name of images.
        :type name: str.
        :returns: dict.

        """

        images = self.sms.list_os_images()
        if not label and not name:
            return images

        for image in images:
            if name and image.name == name:
                return image
            if label and image.label == label:
                lastone = image

        if lastone:
            return lastone

        return images

""" run with

nosetests -v --nocapture

or

nosetests -v

individual tests can be run with

nosetests -v  --nocapture test_cm_compute.py:Test.test_06

"""

from sh import head
from sh import fgrep
import string
import os
import time


from cloudmesh.config.cm_config import cm_config
from cloudmesh.util.cm_table import cm_table
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

from cloudmesh.util.util import HEADING


class Test:

    # assuming first - is the prefered cloud
    cloudmesh_yaml = os.path.expandvars("$HOME/.futuregrid/cloudmesh.yaml")
    print cloudmesh_yaml
    cloud_label = head(fgrep("-", cloudmesh_yaml), "-n", "1")
    cloud_label = cloud_label.replace(" - ", "").strip()

    def setup(self):
        """setup azure"""
        from cloudmesh.iaas.azure.cm_compute import azure
        self.azure_cloud = azure("windows_azure")

    def test_14_azure(self):
        """test azure"""
        HEADING()
        self.setup()
        self.azure_cloud.refresh("images")
        print json.dumps(self.azure_cloud.dump('images'), indent=4)

    def test_azure_services(self):
        """test azure services"""
        HEADING()
        self.setup()
        self.azure_cloud.refresh("services")
        print json.dumps(self.azure_cloud.dump('services'), indent=4)

    def test_create_azure_vm(self):
        """test to create azure vm"""
        HEADING()
        self.setup()
        self.azure_cloud.vm_create()
        print json.dumps(self.azure_cloud.get_deployment(), indent=4)

    def test_delete_azure_vm(self, name):
        """Test to tear down azure vm"""
        HEADING()
        self.setup()
        self.azure_cloud.vm_delete(name)

    def test_azure_deployments(self):
        """Test to list deployments"""
        HEADING()
        self.setup()
        res = self.azure_cloud.list_deployments()
        print json.dumps(res, indent=4)

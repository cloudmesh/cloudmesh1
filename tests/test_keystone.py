""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh.config.cm_config import cm_config
from cloudmesh.config.mock_user import mock_user
from cloudmesh.config.mock_cloud import mock_cloud
from cloudmesh.openstack_grizzly_cloud import openstack_grizzly_cloud
import mock_keystone
import json
import os
import warnings
import pprint
pp = pprint.PrettyPrinter(indent=4)

from cloudmesh_common.util import HEADING


class Test_cloudmesh_keystone:

    def test18_initialize(self):
        HEADING()
        username = 'misterbojangles'
        self.config.userdata_handler = mock_user
        self.config.cloudcreds_handler = mock_cloud
        self.config.initialize(username)

        assert 'cloudmesh' in self.config.data
        assert len(self.config.data.keys()) == 1

        cmdata = self.config.data['cloudmesh']
        assert 'prefix' in cmdata
        assert 'profile' in cmdata
        assert 'username' in cmdata['profile']
        assert cmdata['profile']['username'] == username
        assert 'keys' in cmdata
        assert 'projects' in cmdata
        assert 'active' in cmdata
        assert 'default' in cmdata
        assert 'clouds' in cmdata
        assert 'security' in cmdata
        assert 'default' in cmdata['keys']
        assert 'india-openstack' in cmdata['clouds']
        assert 'sierra' in cmdata['clouds']
        assert 'credentials' in cmdata['clouds']['sierra']
        assert cmdata['clouds']['sierra'][
            'credentials']['OS_VERSION'] == 'grizzly'
        assert cmdata['clouds']['sierra'][
            'credentials']['OS_USERNAME'] == username
        assert cmdata['prefix'] == username

    def test19_openstack_grizzly(self):
        HEADING()
        username = 'misterbojangles'
        self.config.userdata_handler = mock_user
        self.config.cloudcreds_handler = openstack_grizzly_cloud
        self.config.cloudcreds_handler._client = mock_keystone.Client
        self.config.cloudcreds_handler._client.mockusername = username
        self.config.cloudcreds_handler._client.mocktenants = self.config.data[
            'cloudmesh']['active']
        self.config.initialize(username)
        cmdata = self.config.data['cloudmesh']
        assert cmdata['clouds']['sierra'][
            'credentials']['OS_VERSION'] == 'grizzly'
        assert cmdata['clouds']['sierra'][
            'credentials']['OS_USERNAME'] == username
        assert 'OS_PASSWORD' in cmdata['clouds'][
            'sierra']['credentials']
        assert 'project' in cmdata['clouds'][
            'sierra']['default']

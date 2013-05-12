""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import sys
#sys.path.insert(0, '..')

from cm_config import cm_config
from mock_user import mock_user
from mock_cloud import mock_cloud
from openstack_grizzly_cloud import openstack_grizzly_cloud
import mock_keystone
import json
import os
import warnings
import pprint
pp = pprint.PrettyPrinter(indent=4)

header = False

def HEADING(txt):
    if header:
        print
        print "#", 70 * '#'
        print "#", txt
        print "#", 70 * '#'

class Test_cloudmesh:


    filename = "credentials-example.yaml"
    #filename = None

    def setup(self):
        if self.filename == None:
            self.config = cm_config()
        else:
            self.config = cm_config(self.filename)

    def tearDown(self):
        pass

    def test01_print(self):
        print self.config

    def test02_active(self):
        HEADING("LIST ACTIVE PROJECTS")
        result = self.config.projects('active')
        assert result == ['fg-82', 'fg-101']
        
    def test03_completed(self):
        HEADING("LIST COMPLETED PROJECTS")
        result = self.config.projects('completed')		
        assert result == ['fg-81', 'fg-102']

    def test04_active(self):
	HEADING("LIST ACTIVE PROJECTS")
        result = self.config.projects('default')
        assert result == 'fg-82'

    def test05_india(self):
	HEADING("LIST India")
        result = self.config.get('india-openstack')
        assert result["OS_VERSION"] == "essex"

    def test06_keys_india_openstack(self):
	HEADING("KEY india-openstack")
        keys = self.config.keys()
        assert 'india-openstack' in keys

    def test07_keys_india_eucalyptus(self):
	HEADING("KEY india-eucalyptus")
	keys = self.config.keys()
        assert 'india-eucalyptus' in keys

    def test08_keys_grizzly_openstack(self):
	HEADING("KEY sierra-openstack-grizzly")
	keys = self.config.keys()
        assert 'sierra-openstack-grizzly' in keys

    def test09_keys_india_eucalyptus(self):
	HEADING("KEY azure")
	keys = self.config.keys()
        assert 'azure' in keys

    def test10_grizzly(self):
	HEADING("LIST GRIZZLY")
        result = self.config.get('sierra-openstack-grizzly')
	assert result["OS_VERSION"] == 'grizzly'

    def test11_grizzly(self):
	HEADING("LIST GRIZZLY EXPANDED")
        result = self.config.get('sierra-openstack-grizzly', expand=True)
	assert result["OS_VERSION"] == 'grizzly'

    def test12_clouds(self):
        HEADING("CLOUD")
        clouds = self.config.clouds()
        assert isinstance(clouds, dict)
        assert 'india-openstack' in clouds

    def test13_cloud(self):
        HEADING("CLOUD")
        india_cloud = self.config.cloud('india-openstack')
        assert isinstance(india_cloud, dict)
        assert 'cm_host' in india_cloud
        assert india_cloud['cm_host'] == 'india.futuregrid.org'

    def test14_cloud_default(self):
        HEADING("CLOUD")
        assert self.config.cloud_default('india-openstack', 'flavor') == 'm1.tiny'
        assert self.config.cloud_default('india-openstack', 'not defined') is None

    def test15_project_default(self):
        HEADING("PROJECT")
        project = self.config.projects('default')
        assert project == 'fg-82'

    def test16_write(self):
        HEADING("WRITE")
        warnings.filterwarnings('ignore', 'tempnam', RuntimeWarning)  # we open the file securely
        name = os.tempnam()
        print self.config
        self.config.write(name)
        print open(name,"rb").read()
        os.remove(name)

    def test17_key(self):
        HEADING("KEY")
        keys = self.config.userkeys()

        #print "DEFAULT>", self.config.userkeys('default')
        #print "TEST>", self.config.userkeys('test')

        print keys, keys['default'], keys['keylist'][keys['default']]
        assert ('default' in keys) and (keys['default'] in keys['keylist'])


    def test18_initialize(self):
        HEADING("INITIALIZATION")
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
        assert 'sierra-openstack-grizzly' in cmdata['clouds']
        assert 'credentials' in cmdata['clouds']['sierra-openstack-grizzly']
        assert cmdata['clouds']['sierra-openstack-grizzly']['credentials']['OS_VERSION'] == 'grizzly'
        assert cmdata['clouds']['sierra-openstack-grizzly']['credentials']['OS_USERNAME'] == username
        assert cmdata['prefix'] == username

    def test19_openstack_grizzly(self):
        HEADING("INITIALIZATION")
        username = 'misterbojangles'
        self.config.userdata_handler = mock_user
        self.config.cloudcreds_handler = openstack_grizzly_cloud
        self.config.cloudcreds_handler._client = mock_keystone.Client
        self.config.cloudcreds_handler._client.mockusername = username
        self.config.cloudcreds_handler._client.mocktenants = self.config.data['cloudmesh']['active']
        self.config.initialize(username)
        cmdata = self.config.data['cloudmesh']
        assert cmdata['clouds']['sierra-openstack-grizzly']['credentials']['OS_VERSION'] == 'grizzly'
        assert cmdata['clouds']['sierra-openstack-grizzly']['credentials']['OS_USERNAME'] == username
        assert 'OS_PASSWORD' in cmdata['clouds']['sierra-openstack-grizzly']['credentials']
        assert 'project' in cmdata['clouds']['sierra-openstack-grizzly']['default']

    def test20_set_index_and_prefix(self):
        print
        print "INDEX:", self.config.index
        print "PREFIX:", self.config.prefix

        self.config.prefix = "hallo"
        self.config.index = "3"
        
        print "INDEX:", self.config.index
        print "PREFIX:", self.config.prefix
        print "NAME:", self.config.vmname


        self.config.incr()

        
        print "INDEX:", self.config.index
        print "PREFIX:", self.config.prefix
        print "NAME:", self.config.vmname

        assert self.config.index == 4 and self.config.prefix == "hallo"

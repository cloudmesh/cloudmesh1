""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.config.cm_config import cm_config
from cloudmesh.config.ConfigDict import ConfigDict

import json
import os
import warnings
from pprint import pprint

from cloudmesh_common.util import HEADING
from cloudmesh_install.util import path_expand
from cloudmesh_install import config_file


class Test_cloudmesh:

    filename = config_file("/cloudmesh.yaml")

    project = 82

    def setup(self):
        print "READING THE FILE", self.filename
        if self.filename is None:
            self.config = cm_config()
        else:
            self.config = cm_config(self.filename)

    def tearDown(self):
        pass

    def test_print(self):
        HEADING()
        print self.config

    def test_active(self):
        HEADING()
        result = self.config.projects('active')
        print self.project, result, type(self.project)
        assert self.project in result

    def test_completed(self):
        HEADING()
        result = self.config.projects('completed')
        assert True

    def test_default(self):
        HEADING()
        result = self.config.projects('default')
        assert result == self.project

    def test_sierra_version(self):
        HEADING()
        result = self.config.cloud('sierra')
        pprint(result)
        assert result["credentials"]["OS_VERSION"] == 'grizzly'

    def test_sierra_cloudnames(self):
        HEADING()
        keys = self.config.cloudnames()
        assert 'sierra' in keys

    def test_expand(self):
        HEADING()
        result = self.config.get('cloudmesh.clouds.sierra')
        dir = result['credentials']['OS_CACERT']
        print dir
        assert dir.startswith("~")
        dir = path_expand(dir)
        print dir
        assert not dir.startswith("~")

    """
    def test07_keys_india_eucalyptus(self):
        HEADING()
        keys = self.config.keys()
        assert 'india-eucalyptus' in keys

    def test09_keys_india_eucalyptus(self):
        HEADING()
        keys = self.config.keys()
        assert 'azure' in key

    """

    def test_clouds(self):
        HEADING()
        clouds = self.config.clouds()
        assert isinstance(clouds, dict)
        assert 'sierra' in clouds

    def test_cloud(self):
        HEADING()
        sierra_cloud = self.config.cloud('sierra')
        assert isinstance(sierra_cloud, dict)
        assert 'cm_host' in sierra_cloud
        assert sierra_cloud['cm_host'] == 'sierra.futuregrid.org'

    def test14_cloud_default(self):
        HEADING()
        assert self.config.cloud_default(
            'sierra', 'flavor') == 'm1.tiny'
        assert self.config.cloud_default(
            'sierra', 'not defined') is None

    def test15_project_default(self):
        HEADING()
        project = self.config.projects('default')
        assert project == self.project

    """
    def test16_write(self):
        HEADING()
        warnings.filterwarnings(
            'ignore', 'tempnam', RuntimeWarning)  # we open the file securely
        name = os.tempnam()
        print self.config
        self.config.write(name)
        print open(name, "rb").read()
        os.remove(name)
    """

    def test17_key(self):
        HEADING()
        keys = self.config.userkeys()

        # print "DEFAULT>", self.config.userkeys('default')
        # print "TEST>", self.config.userkeys('test')

        print keys, keys['default'], keys['keylist'][keys['default']]
        assert ('default' in keys) and (keys['default'] in keys['keylist'])

    def test20_set_index_and_prefix(self):
        HEADING()
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

    def test21_default(self):
        HEADING()
        self.config.default = "hallo"
        print self.config.default
        assert self.config.default == "hallo"
    """
    def test22_filter(self):
        HEADING()
        print self.config.get_filter('sierra')
    """

    def test_launcher(self):
        HEADING()
        filename = config_file("/cloudmesh_launcher.yaml")
        config = ConfigDict(filename=filename)
        print config
        existing = config.get("cloudmesh.launcher.recipies")
        test1 = existing is not None
        print existing
        try:
            none_existing = config.get("cloudmesh.launcher.recipies.xyz")
            test2 = False
        except:
            print "Error"
            test2 = True
        assert test1 and test2

    def test_server(self):
        HEADING()
        filename = config_file("/cloudmesh_server.yaml")
        config = ConfigDict(filename=filename)
        # print config
        existing = config.get("cloudmesh.server.mongo.db")
        test1 = existing is not None
        print "mongo.db =", existing
        try:
            none_existing = config.get("cloudmesh.server.mongo.xyz")
            test2 = False
        except:
            print "Error"
            test2 = True
        assert test1 and test2

    def test_getitem_server(self):
        HEADING()
        filename = config_file("/cloudmesh_server.yaml")
        config = ConfigDict(filename=filename)
        print config
        existing = config.get("cloudmesh.server.mongo.db")
        test1 = existing is not None
        print "QUERY", existing
        print "Port", config.get("cloudmesh.server.mongo.port")

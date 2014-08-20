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
from cloudmesh_common.util import path_expand
from cloudmesh_install import config_file

import os.path

class Test_yaml:

    filename = config_file("/cloudmesh.yaml")

    project = 82

    def setup(self):
        pass

    def tearDown(self):
        pass


    def test_01_exists(self):
        HEADING()
        filenames = ["/cloudmesh.yaml",
                 "/cloudmesh_celery.yaml",
                 "/cloudmesh_cluster.yaml",
                 "/cloudmesh_flavor.yaml",
                 "/cloudmesh_hpc.yaml",
                 "/cloudmesh_launcher.yaml",
                 "/cloudmesh_mac.yaml",
                 "/cloudmesh_rack.yaml",
                 "/cloudmesh_server.yaml"]


        for file in filenames:
            filename = config_file(file)
            print "testing if file exists ->", filename    
            assert os.path.isfile(filename)

    def test_02_authentication(self):
        HEADING()
        self.config = cm_config()
        cloudnames = self.config.cloudnames()
        print cloudnames

        failed = []
        for cloud in cloudnames:
            print "authenticate -> ", cloud,
            try:
                assert False
                #
                # to do put the authentication code here
                #
                print "ok"
            except:
                print "failed"
                failed.append(cloud)
        if len(failed) > 0:
            print "Failed:", failed
            assert False 
        else:
            assert True
        

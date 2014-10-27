""" run with

nosetests -v --nocapture

or

nosetests -v

"""
from __future__ import print_function
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.config.cm_config import cm_config
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.iaas.eucalyptus.eucalyptus import eucalyptus
from cloudmesh.iaas.openstack.cm_compute import openstack
from cloudmesh.iaas.ec2.cm_compute import ec2
try:
    from cloudmesh.iaas.azure.cm_compute import azure
except:
    log.warning("AZURE NOT ENABLED")

try:
    from cloudmesh.iaas.aws.cm_compute import aws
except:
    log.warning("Amazon NOT ENABLED")

import json
import os
import warnings
from pprint import pprint

from cloudmesh_common.util import HEADING
from cloudmesh_install.util import path_expand
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
            print("testing if file exists ->", filename)
            assert os.path.isfile(filename)

    def test_02_authentication(self):
        HEADING()
        self.config = cm_config()
        cloudnames = self.config.cloudnames()
        print(cloudnames)

        failed = []
        succeeded = []
        for cloudname in cloudnames:
            print("authenticate -> ", cloudname, end=' ')
            try:
                # assert False
                #
                # to do put the authentication code here
                cm_type = self.config['cloudmesh'][
                    'clouds'][cloudname]['cm_type']
                credential = self.config['cloudmesh'][
                    'clouds'][cloudname]['credentials']
                print(cm_type, end=' ')
                # print credential

                cloud = globals()[cm_type](cloudname, credential)
                if cm_type in ['openstack', 'ec2']:
                    if cm_type in ['openstack']:
                        print("\tfor tenant: %s" % credential['OS_TENANT_NAME'], end=' ')
                    if cloud.auth():
                        succeeded.append(cloudname)
                        print("ok")
                    else:
                        failed.append(cloudname)
                        print("failed")
                else:
                    failed.append(cloudname)
                    print("failed")
            except:
                print("failed")
                failed.append(cloudname)

        if len(failed) > 0:
            print("Failed:", failed)
            print("Succeeded:", succeeded)
            assert False
        else:
            assert True

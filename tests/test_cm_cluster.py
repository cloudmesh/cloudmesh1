""" run with

nosetests -v
nosetests -v --nocapture

TODO:: rest cloud commands

"""
from __future__ import print_function
from cloudmesh_common.util import HEADING
from cloudmesh_common.logger import LOGGER
import os
import unittest
import cloudmesh
from pprint import pprint

log = LOGGER(__file__)


class Test(unittest.TestCase):

    def setUp(self):
        print ("setup")
        self.cloudname = "india"
        self.cloudmesh_yaml = "~/.cloudmesh/cloudmesh.yaml"
        self.data = {
            "user": cloudmesh.load().username(),
            "cloud": self.cloudname
        }
        r = cloudmesh.shell("cloud on {cloud}".format(**self.data))
        print (r)
        r = cloudmesh.shell("cloud select {cloud}".format(**self.data))
        print (r)
        r = cloudmesh.shell("project default fg82")
        print (r)
        print ("Cloud: ", self.data["cloud"])
        pass

    def tearDown(self):
        print ("teardown")
        os.system("python ../bin/cursor_on.py")
        pass

    def test_01_setup(self):
        HEADING()
        print ("hallo")

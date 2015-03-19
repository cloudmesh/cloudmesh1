""" run with

nosetests -v
nosetests -v --nocapture

TODO:: rest cloud commands

"""
from cloudmesh_base.util import HEADING
from cloudmesh_base.logger import LOGGER
import os
import unittest


log = LOGGER(__file__)

class Test(unittest.TestCase):

    def setUp(self):
        
        self.cloudname = "india"
        
        print ("CLOUD: ", self.cloudname)
        
    def test_01_cloud_on_1(self):
        HEADING()
        res = os.popen("cm \"cloud on {0}\"".format(self.cloudname)).read()
        assert res.find("cloud '{0}' activated.".format(self.cloudname)) != -1
        
    def test_02_cloud_off(self):
        HEADING()
        res = os.popen("cm \"cloud off {0}\"".format(self.cloudname)).read()
        assert res.find("cloud '{0}' deactivated.".format(self.cloudname)) != -1
    
    def test_03_cloud_on_2(self):
        HEADING()
        res = os.popen("cm \"cloud on {0}\"".format(self.cloudname)).read()
        assert res.find("cloud '{0}' activated.".format(self.cloudname)) != -1
        
    def test_04_cloud(self):
        HEADING()
        res = os.popen("cm \"cloud\" |"
                       "grep {0} |".format(self.cloudname) +
                       "grep True |"
                       "wc -l").read()
        assert res.strip() == "1"
                       
    def test_05_cloud_list(self):
        HEADING()
        res = os.popen("cm \"cloud list\" |"
                       "grep {0} |".format(self.cloudname) +
                       "grep True |"
                       "wc -l").read()
        assert res.strip() == "1"
        
    def test_06_cloud_select(self):
        HEADING()
        res = os.popen("cm \"cloud select {0}\"".format(self.cloudname)).read()
        assert res.find("cloud '{0}' is selected".format(self.cloudname)) != -1
        
    def test_07_cloud_alias(self):
        HEADING()
        name = self.cloudname + "_test"
        res = os.popen("echo y | cm \"cloud alias {0} {1}\"".format(name, self.cloudname))
        res = os.popen("cm \"cloud select {0}\"".format(name)).read()
        assert res.find("cloud '{0}' is selected".format(name)) != -1 
        
        res = os.popen("echo y | cm \"cloud alias {1} {0}\"".format(name, self.cloudname))
        res = os.popen("cm \"cloud select {0}\"".format(self.cloudname)).read()
        assert res.find("cloud '{0}' is selected".format(self.cloudname)) != -1
        
    
    
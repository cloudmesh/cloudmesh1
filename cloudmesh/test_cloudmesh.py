""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import sys
#from cloudmesh.openstack.cm_table import table as cm_table
#from cloudmesh.cm_config import cm_config
#from cloudmesh.openstack.cm_compute import openstack
from cloudmesh import cloudmesh

import json
import pprint
pp = pprint.PrettyPrinter(indent=4)


class Test_cloudmesh:

    def setup(self):
        self.c = cloudmesh()
        
    def tearDown(self):
        pass
        #print self.c.clouds

    def test_001_refresh(self):
        print self.c



    def test_101_refresh(self):

        self.c.refresh("india-openstack")

    def test_103_refresh_all(self):
        print self.c.refresh()
         
    def test_102_str(self):
        print self.c
         
    def test_103_str(self):
        print self.c.dump()

    def test_103_info(self):
        self.c.refresh()
        self.c.info()


    

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

header = True

def HEADING(txt):
    if True:
        print
        print "#", 70 * '#'
        print "#", txt
        print "#", 70 * '#'


class Test_cloudmesh:

    def setup(self):
        self.c = cloudmesh()
        self.c.config()
        print self.c

    def tearDown(self):
        pass
        #print self.c.clouds

    def test_001_print(self):
        HEADING("test_001_refresh")
        print self.c



    def test_101_refresh(self):
        HEADING("test_101_refresh")
        self.c.refresh("india-openstack")
        self.c.dump()

    def test_103_refresh_all(self):
        HEADING("test_103_refresh_all")
        print self.c.refresh()
         
    def test_102_str(self):
        HEADING("test_102_str")
        print self.c
         
    def test_103_str(self):
        HEADING("test_103_str")
        print self.c.dump()

    def test_103_info(self):
        HEADING("test_103_info")
        self.c.refresh()
        self.c.info()


    


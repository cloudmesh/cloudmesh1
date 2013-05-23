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
        self.name = self.c.active()[0]
#        print self.c

    def tearDown(self):
        pass
        #print self.c.clouds

    def test_001_print(self):
        HEADING("test_001_print")
        print self.c

    def test_101_refresh(self):
        HEADING("test_101_refresh")
        self.c.refresh([self.name])
        self.c.dump()

    def test_102_refresh_all(self):
        HEADING("test_102_refresh_all")
        print self.c.refresh()
         
    def test_104_dump(self):
        HEADING("test_104_dump")
        print self.c.dump()

    def test_105_info(self):
        HEADING("test_105_info")
        self.c.refresh()
        print self.c.info()

    def test_106_active(self):
        HEADING("test_106_active")
        print self.c.active()

    def test_107_profile(self):
        HEADING("test_107_profile")
        print self.c.profile()

    def test_108_prefix(self):
        HEADING("test_108_prefix")
        print self.c.prefix()

    def test_109_findall(self):
        HEADING("test_109_findall")
        print self.c.find()



            


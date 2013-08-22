""" run with

nosetests -v --nocapture --nologcapture
nosetests -v  --nocapture test_inventory.py:Test_Inventory.test_06
nosetests -v

"""
from datetime import datetime

from cloudmesh.inventory.ninventory import ninventory
import json
from  pprint import pprint

from cloudmesh.util.util import HEADING
import time
import sys


class Test_Inventory:


    def setup(self):
        self.name = "b010"
        self.inventory = ninventory()
        
        
    def tearDown(self):
        pass
    
    def test_clear(self):
        HEADING()
        self.inventory.clear()

    def test_find(self):
        HEADING()
        r = self.inventory.find ({})
        print r.count()
        assert r.count > 0
        
    def test_host(self):
        HEADING()
        data = self.inventory.host(self.name)
        pprint(data)

               
    def test_ipaddr(self):
        HEADING()
        
        print self.inventory.ipadr (self.name, "public")
        print self.inventory.ipadr (self.name, "internal")

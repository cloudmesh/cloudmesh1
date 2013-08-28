""" run with

nosetests -v --nocapture --nologcapture
nosetests -v  --nocapture test_inventory.py:Test_Inventory.test_06
nosetests -v

"""
from datetime import datetime

from cloudmesh.util.util import HEADING
from cloudmesh.inventory.ninventory import ninventory
from  pprint import pprint


class Test_Inventory:

    def setup(self):
        self.cluster = "bravo"
        self.name = "b010"
        self.inventory = ninventory()
        self.inventory.clear()
        self.inventory.generate()
        print "GENERATION COMPLETE"
        
        
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

    def test_list(self):
        HEADING()
        data = self.inventory.hostlist(self.cluster)
        #pprint(data)

    def test_combine(self):        
        
        attribute = "cm_temp"
        value = "32"
        
        print "SET ATTRIBUTE"
        print 70 * '='
        data = self.inventory.set_attribute(self.name, attribute, value)
        print 70 * '='
        print data

        print "GET ATTRIBUTE"
        data = self.inventory.get_attribute(self.name, attribute)
        print data

        data = self.inventory.host(self.name)
        pprint(data)
        
        
        
    def test_set(self):
        HEADING()
        
        """
        data = self.inventory.find({'cm_id': self.name})
        
        for e in data:
            pprint (e)
        """
        print 70 * '='
        """
        print "BEFORE"
        
        
        data = self.inventory.host(self.name)
        pprint(data)
        """

        attribute = "cm_temp"
        value = "32"
        
        print "SET ATTRIBUTE"
        print 70 * '='
        data = self.inventory.set_attribute(self.name, attribute, value)
        print 70 * '='
        print data
        
        
        print "GET ATTRIBUTE"
        data = self.inventory.get_attribute(self.name, attribute)
        print data
        
        

        """    
        data = self.inventory.host(self.name)
        print "AFTER"
        pprint(data)
    
        
               
    def test_ipaddr(self):
        HEADING()
        
        print self.inventory.ipadr (self.name, "public")
        print self.inventory.ipadr (self.name, "internal")
    """

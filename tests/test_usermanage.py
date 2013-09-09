""" run with

nosetests -v --nocapture --nologcapture
nosetests -v  --nocapture test_inventory.py:Test_Inventory.test_06
nosetests -v

"""
from datetime import datetime

from cloudmesh.util.util import HEADING
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.user.cm_template import cm_template
from  pprint import pprint


class Test_Inventory:

    def setup(self):
        
        self.sample_user = ConfigDict(filename="~/.futuregrid/etc/sample_user.yaml")
        
        print
        print self.sample_user
        
        t = cm_template("~/.futuregrid/etc/cloudmesh.yaml")
        pprint (set(t.variables()))
    
        self.config = t.replace(format="dict", **self.sample_user)
        
    def tearDown(self):
        pass

    def test_print(self):
        print self.config

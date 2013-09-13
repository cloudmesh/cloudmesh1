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

from cloudmesh.user.cm_userLDAP import cm_userLDAP 
from cloudmesh.util.util import HEADING
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.util.util import path_expand

class Test_Inventory:

    def setup(self):
        
        self.sample_user = ConfigDict(filename="~/.futuregrid/etc/sample_user.yaml")
        
        self.portalname = ConfigDict(filename="~/.futuregrid/cloudmesh.yaml").get("cloudmesh.hpc.username")
        
        print
        print self.sample_user
        
        t = cm_template("~/.futuregrid/etc/cloudmesh.yaml")
        pprint (set(t.variables()))
    
        self.config = t.replace(format="dict", **self.sample_user)
        
        print type(self.config)

        self.idp = cm_userLDAP ()
        self.idp.connect("fg-ldap","ldap")
        self.idp.refresh()
        
        ldap_info = self.idp.get(self.portalname)
        print ldap_info
        print type(self.config)
        
        self.config['cloudmesh']['projects'] = ldap_info['projects']
        self.config['cloudmesh']['keys'] = ldap_info['keys']
        try:
            self.config['cloudmesh']['projects']['deafult'] = ldap_info['projects']['active'][0]
        except:
            print "ERROR: you have no projects"
        
    def tearDown(self):
        pass

    def test_print(self):
        pprint (self.config)

    def test_projects(self):
        projects = dict()
        
        keys = dict()
        
        
        # read the yaml
        # read projects info from ldap
        # write out new dict/json file
        pass
    
    def test_keys(self):
        # read the yaml
        
        # read KEYS from ldap
        # write out new dict/json file
        pass

    def test_user(self):
        #read yaml
        #read projects from ldap
        #read keys from ldap
        #write dict
        pass
        
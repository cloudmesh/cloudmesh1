""" run with

nosetests -v --nocapture

or

nosetests -v

"""
#import sys
#sys.path.insert(0, '..')

from cm_config import cm_config

import json
import pprint
pp = pprint.PrettyPrinter(indent=4)


def HEADING(txt):
    print
    print "#", 70 * '#'
    print "#", txt
    print "#", 70 * '#'

class Test_cloudmesh:

    def setup(self):
        #        self.config = cm_config()
        self.config = cm_config("credentials-example.yaml")
        
    def tearDown(self):
        pass

    def test01_print(self):
        print self.config

    def test02_active(self):
        HEADING("LIST ACTIVE PROJECTS")
        print self.config.projects('active')
        assert self.config.projects('active') == ['fg-82', 'fg-101']
        
    def test03_completed(self):
        HEADING("LIST COMPLETED PROJECTS")
        print self.config.projects('completed')
        assert self.config.projects('completed') == ['fg-81', 'fg-102']

    def test04_active(self):
        print self.config.projects('default')
        assert self.config.projects('default') == 'fg-82'

    def test05_india(self):
        result = self.config.get('india-openstack')
        #print result
        assert result["OS_VERSION"] == "essex"

    def test07_get(self):
        print self.config.get()

    def test08_keys(self):
        keys = self.config.keys()
        print keys
        assert 'india-openstack' in keys

    def test09_rc(self):
        print self.config.rc('india-openstack')

    def test10_default(self):
        print self.config.default()

    def test11_grizzly(self):
        print self.config.get('grizzly-openstack')

    def test11_grizzly(self):
        print self.config.get('grizzly-openstack', expand=True)


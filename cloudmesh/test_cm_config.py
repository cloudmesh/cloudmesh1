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


class Test_cloudmesh:

    def setup(self):
        self.config = cm_config()
        
    def tearDown(self):
        pass

    def test01_print(self):
        print self.config

    def test02_active(self):
        print self.config.projects('active')

    def test03_active(self):
        print self.config.projects('completed')

    def test04_active(self):
        print self.config.projects('default')

    def test05_india(self):
        print self.config.get('india-openstack')

    def test07_get(self):
        print self.config.get()

    def test08_keys(self):
        print self.config.keys()

    def test09_rc(self):
        print self.config.rc('india-openstack')

    def test10_rc(self):
        print self.config.default()

    def test11_grizzly(self):
        print self.config.get('grizzly-openstack')

    def test11_grizzly(self):
        print self.config.get('grizzly-openstack', expand=True)


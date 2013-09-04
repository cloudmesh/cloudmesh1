""" run with

nosetests -v --nocapture

or

nosetests -v

"""

# from cloudmesh.openstack.cm_table import table as cm_table
# from cloudmesh.cm_config import cm_config
# from cloudmesh.openstack.cm_compute import openstack
from cloudmesh.cm_mesh import cloudmesh

import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

from cloudmesh.util.util import HEADING


class Test_cloudmesh:

    def setup(self):
        self.c = cloudmesh()
        self.c.config()
        self.name = self.c.active()[0]
#        print self.c

    def tearDown(self):
        pass
        # print self.c.clouds

    def test_100_print(self):
        HEADING()
        print self.c

    def test_101_refresh(self):
        HEADING()
        self.c.refresh([self.name])
        self.c.dump()

    def test_102_refresh_all(self):
        HEADING()
        print self.c.refresh()

    def test_104_dump(self):
        HEADING()
        print self.c.dump()

    def test_105_info(self):
        HEADING()
        self.c.refresh()
        print self.c.info()

    def test_106_active(self):
        HEADING()
        print self.c.active()

    def test_107_profile(self):
        HEADING()
        print self.c.profile()

    def test_108_prefix(self):
        HEADING()
        print self.c.prefix()

    def test_109_findall(self):
        HEADING()
        print self.c.find()

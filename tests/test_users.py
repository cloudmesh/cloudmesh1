""" run with

nosetests -v --nocapture --nologcapture
nosetests -v  --nocapture test_inventory.py:Test_Inventory.test_06
nosetests -v

"""
from datetime import datetime

from cloudmesh.user.cm_user import cm_user

import json
from  pprint import pprint

from cloudmesh.util.util import HEADING
import time
import sys


class Test_Users:

    def setup(self):
        self.user = cm_user()

    def tearDown(self):
        pass

    def test_get(self):
        HEADING()
        print self.user.info("fuwang")
        print self.user.info("gvonlasz")
        print self.user.info("nonexistuser")
        print self.user.info("nova")
        print self.user.info("fuwang", ["sierra_openstack_grizzly"])
        print self.user.info("fuwang", ["cloud-non-exist"])
        print "============================"
        pprint (self.user["gvonlasz"])
        print self.user.get_name('gvonlasz')

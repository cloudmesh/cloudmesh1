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
        self.usersobj = cm_user()

    def tearDown(self):
        pass

    def test_get(self):
        HEADING()
        print self.usersobj.info("fuwang")
        print self.usersobj.info("gvonlasz")
        print self.usersobj.info("nonexistuser")
        print self.usersobj.info("nova")
        print self.usersobj.info("fuwang", ["sierra_openstack_grizzly"])
        print self.usersobj.info("fuwang", ["cloud-non-exist"])
        print "============================"
        pprint (self.usersobj["gvonlasz"])
        print self.usersobj.get_name('gvonlasz')

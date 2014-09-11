""" run with

nosetests -v --nocapture --nologcapture
nosetests -v  --nocapture test_inventory.py:Test_Inventory.test_06
nosetests -v

"""
from datetime import datetime

from cloudmesh.user.roles import Roles

import json
from pprint import pprint

from cloudmesh_common.util import HEADING
import time
import sys


class Test_Roles:

    def setup(self):
        self.roles = Roles()

    def tearDown(self):
        pass

    def test_clear(self):
        HEADING()
        self.roles.clear()
        print self.roles

    def test_print(self):
        HEADING()
        print self.roles

    def test_users(self):
        HEADING()
        role = "rain"
        print "getting role", role
        print self.roles.users(role)

    def test_roles(self):
        HEADING()
        user = "gvonlasz"
        print "getting roles", user
        print self.roles.get(user)

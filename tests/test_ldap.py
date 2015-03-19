""" run with

nosetests -v --nocapture

or

nosetests -v

"""
from __future__ import print_function
import sys
import getpass

from cloudmesh.user.cm_userLDAP import cm_userLDAP
from cloudmesh_base.util import HEADING
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh_base.util import path_expand

from pprint import pprint
from cloudmesh_install import config_file


class Test_cloudmesh:

    username = ConfigDict(
        filename=config_file("/cloudmesh.yaml")).get("cloudmesh.hpc.username")

    filename = "etc/cloudmesh.yaml"

    def setup(self):
        self.idp = cm_userLDAP()
        self.idp.connect("fg-ldap", "ldap")
        self.idp.refresh()

    def tearDown(self):
        pass

    def test_me(self):
        print("USERNAME", self.username)
        user = self.idp.find_one({'cm_user_id': self.username})
        print(user)

    def test_list(self):
        users = self.idp.list()
        pprint(users)
        pprint(self.idp.users)

    def test_auth(self):
        password = getpass.getpass()
        if self.idp.authenticate(self.username, password):
            print("SUCCESS")
        else:
            print("FAILED")

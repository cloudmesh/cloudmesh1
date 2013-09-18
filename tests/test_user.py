""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import sys

from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.util.util import HEADING
from cloudmesh.util.util import path_expand
from cloudmesh.user.cm_template import cm_template
from cloudmesh.user.cm_mesh_auth import cm_userauth
from cloudmesh.user.cm_user import cm_user
from cloudmesh.user.cm_userLDAP import cm_userLDAP
from pprint import pprint

class Test_cloudmesh:

    d = {
      "portalname": "gvonlasz"
    }
    filename = "etc/cloudmesh.yaml"

    def setup(self):
        self.t = cm_template(path_expand(self.filename))
        self.user = cm_user()
        try:
            self.setup_inventory()
        except:
            print "=" * 40
            print "setup_inventory() failed. ldap test will not be performed"
            print "=" * 40

    def tearDown(self):
        pass

    def test_variables(self):
        HEADING()
        print self.t.variables()
        assert "portalname" in self.t.variables()

    def test_replace_incomplete(self):
        try:
            print self.t.replace(self.d, format="dict")
        except:
            pass
        assert True

    def test_user(self):
        d = {
            "portalname" : "gvonlasz",
            "sierra_openstack_password" : "sierra",
            "project_default" : "fg82",
            "india_openstack_password" : "india",
            "projects" : "82, 83",  # this is still wrong
            }
        print self.t.replace(d=d)
        # self.t.complete does not exist in cm_template?
        #assert self.t.complete 

#    if not t.complete():
#       print "ERROR: undefined variables"
#       print t.variables()

    def test_auth(self):
        auth = cm_userauth()
        auth.set("dummy", {"a": "1"})
        r = auth.get("dummy")
        pprint (r)

    def test_userinfo(self):
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

    def setup_inventory(self):

        self.sample_user = ConfigDict(filename="~/.futuregrid/etc/sample_user.yaml")
        self.portalname = ConfigDict(filename="~/.futuregrid/cloudmesh.yaml").get("cloudmesh.hpc.username")

        print
        print self.sample_user

        t = cm_template("~/.futuregrid/etc/cloudmesh.yaml")
        pprint (set(t.variables()))

        self.config = t.replace(format="dict", **self.sample_user)

        print type(self.config)
        print self.config

        self.idp = cm_userLDAP ()
        self.idp.connect("fg-ldap", "ldap")
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
        # read yaml
        # read projects from ldap
        # read keys from ldap
        # write dict
        pass

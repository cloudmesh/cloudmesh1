""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import sys

from cloudmesh.user.cm_template import cm_template
from cloudmesh.util.util import HEADING
from cloudmesh.util.util import path_expand
from cloudmesh.user.cm_mesh_auth import cm_userauth
from cloudmesh.user.cm_user import cm_user
from pprint import pprint

class Test_cloudmesh:

    d = {
      "portalname": "gvonlasz"
    }
    filename = "etc/cloudmesh.yaml"

    def setup(self):
        self.t = cm_template(path_expand(self.filename))
        self.user = cm_user()

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




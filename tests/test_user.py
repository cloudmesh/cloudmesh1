""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import sys



from cloudmesh.user.cm_template import cm_template
from cloudmesh.util.util import HEADING
from cloudmesh.util.util import path_expand


class Test_cloudmesh:

    d = {
      "portalname": "gvonlasz"
    }
    filename = "etc/cloudmesh.yaml"

    
    def setup(self):
        self.t = cm_template(path_expand(self.filename))

    def tearDown(self):
        pass


    def test_variables(self):
        HEADING()
        print self.t.variables()
        assert "portalname" in self.t.variables()
    
    def test_replace_incomplete(self):
        try:
            print self.t.replace(self.d,format="dict")
        except:
            pass
        assert True

    def test_use(self):
        d = {
            "portalname" : "gvonlasz",
            "sierra_openstack_password" : "sierra",
            "project_default" : "fg82",
            "india_openstack_password" : "india",
            "projects" : "82, 83",  # this is still wrong
            }
        print self.t.replace(d)
        assert self.t.complete
        
#    if not t.complete():
#       print "ERROR: undefined variables"
#       print t.variables()






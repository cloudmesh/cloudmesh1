""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh.cm_config import cm_config
from cloudmesh.openstack.cm_compute import openstack
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)


class Test_openstack:

    def setup(self):
        self.cloud = openstack("india-openstack")

    def tearDown(self):
        pass

    def test_images(self):
        self.cloud.refresh('images')
        print json.dumps(self.cloud.flavors, indent=4)
        # pp.pprint(self.cloud.images)
        # doing a simple test as tiny is usually 512
        #assert self.cloud.flavors['m1.tiny']['ram'] == 512
        print "Currently running vms:", len(self.cloud.images)
        #we assume cloud is always busy which may actually not true
        # we shoudl start our own vm and than probe for it for now > 0 will do
        assert self.cloud.images > 0

    def test_check_label(self):
        assert self.cloud.label == "india-openstack"

    def test_flavor(self):
        self.cloud.refresh('flavors')
        print json.dumps(self.cloud.flavors, indent=4)

        # doing a simple test as tiny is usually 512
        assert self.cloud.flavors['m1.tiny']['ram'] == 512

    def test_vms(self):
        self.cloud.refresh('servers')
        print json.dumps(self.cloud.servers, indent=4)
        # we assume that there are always images running
        assert len(self.cloud.servers) > 0

    def test_refresh(self):
        self.cloud.refresh()
        pp.pprint(self.cloud)

        assert self.cloud.images > 0

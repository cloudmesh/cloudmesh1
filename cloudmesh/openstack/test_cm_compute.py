""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import sys
from cloudmesh.openstack.cm_table import table as cm_table
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
    def test_00_check_label(self):
        assert self.cloud.label == "india-openstack"

    def test_00_limit(self):
        print >> sys.stderr, json.dumps(self.cloud.limits(), indent=4)

    def test_01_images(self):
        self.cloud.refresh('images')
        print json.dumps(self.cloud.flavors, indent=4)
        # pp.pprint(self.cloud.images)
        # doing a simple test as tiny is usually 512
        #assert self.cloud.flavors['m1.tiny']['ram'] == 512
        print "Currently running vms:", len(self.cloud.images)
        #we assume cloud is always busy which may actually not true
        # we shoudl start our own vm and than probe for it for now > 0 will do
        assert self.cloud.images > 0

    def test_02_flavor(self):
        self.cloud.refresh('flavors')
        print json.dumps(self.cloud.flavors, indent=4)

        # doing a simple test as tiny is usually 512
        assert self.cloud.flavors['m1.tiny']['ram'] == 512

    def test_03_vms(self):
        self.cloud.refresh('servers')
        print json.dumps(self.cloud.servers, indent=4)
        # we assume that there are always images running
        assert len(self.cloud.servers) > 0

    def test_04_refresh(self):
        self.cloud.refresh()
        pp.pprint(self.cloud)

        assert self.cloud.images > 0

    """
    def test_05_usage(self):
        result = self.cloud.usage("2000-01-01T00:00:00", "2013-12-31T00:00:00")
        print json.dumps(result, indent=4)
        assert ['Instances'] > 0 
    """
        
    def test_06_table(self):
        self.test_02_flavor()
        table = cm_table()
        columns = ["id", "name", "ram", "vcpus"]

        table.create(self.cloud.flavors, columns, header=True)
        print table

        table = cm_table()
        columns = ["id", "name", "ram", "vcpus"]

        table.create(self.cloud.flavors, columns, format='HTML', header=True)
        print table

        table = cm_table()
        columns = ["id", "name", "ram", "vcpus"]

        table.create(self.cloud.flavors, columns, format='%12s', header=True)
        print table

        assert table != None

    def test_07_start_delete_vm(self):        
        name ="%s-%04d" % (self.cloud.credential["OS_USERNAME"], 1)
        out = self.cloud.vm_create(name, "m1.tiny", "6d2bca76-8fff-4d57-9f29-50378539b4fa")

        pp.pprint(out)
        print json.dumps(out, indent=4)

        key = out.keys()[0]
        id = out[key]["id"]
        print id

        vm = self.cloud.vm_delete(id)
        print vm


    def test_user_vms(self):
        list = self.cloud.vms_user()
        print json.dumps(list, indent=4)








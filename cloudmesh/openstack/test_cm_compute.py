""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import time
import sys
from cloudmesh.openstack.cm_table import table as cm_table
from cloudmesh.cm_config import cm_config
from cloudmesh.openstack.cm_compute import openstack
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

def HEADING(txt):
    print
    print "#", 70 * '#'
    print "#", txt
    print "#", 70 * '#'

class Test_openstack:

    cloud_label = "grizzly-openstack"

    def setup(self):
        self.cloud = openstack(self.cloud_label)

    def tearDown(self):
        pass
    def test_00_check_label(self):
        HEADING("INFO OPENSTACK LABEL")
        assert self.cloud.label == self.cloud_label

    def test_00_limit(self):
        HEADING("INFO OPENSTACK LIMIT")
        print >> sys.stderr, json.dumps(self.cloud.limits(), indent=4)

    def test_01_images(self):
        HEADING("INFO OPENSTACK IMAGES")
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
        HEADING("INFO OPENSTACK FLAVORS")
        self.cloud.refresh('flavors')
        print json.dumps(self.cloud.flavors, indent=4)

        # doing a simple test as tiny is usually 512
        assert self.cloud.flavors['m1.tiny']['ram'] == 512

    def test_03_vms(self):
        HEADING("INFO OPENSTACK VMS")
        self.cloud.refresh('servers')
        print json.dumps(self.cloud.servers, indent=4)
        # we assume that there are always images running
        assert len(self.cloud.servers) > 0

    def test_04_refresh(self):
        HEADING("INFO OPENSTACK REFRESH")
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
        HEADING("INFO OPENSTACK TABLES")
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

    """
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
    """

    def test_08_user_vms(self):
        HEADING("INFO OPENSTACK LIST VMS FROM USER")
        list = self.cloud.vms_user()
        print json.dumps(list, indent=4)

    def test_09_delete_all_user_vms(self):
        HEADING("INFO OPENSTACK DELETE VMS FROM USER")
        self.cloud.refresh()
        list = self.cloud.vms_delete_user()
        print ">>>>> vms", list
        self.cloud.refresh()
        user_id = self.cloud.find_user_id()
        print ">>>>> userid", user_id


        # start a vm

        print self.cloud["images"]

        print "UUUUUUUUUUUUUUUU"

        vms = self.cloud.find('user_id', user_id)
        print self.cloud
        print vms
        assert vms == []

    def test_10_info(self):
        HEADING("INFO OPENSTACK TEST")
        self.cloud.refresh()
        time.sleep(3)
        self.cloud.info()
        self.cloud.info()






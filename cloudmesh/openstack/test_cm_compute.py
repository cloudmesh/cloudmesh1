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

        self.configuration = cm_config()
        #pp.pprint (configuration)

        self.name = self.configuration.active()[0]
        self.cloud = openstack(self.name)
        print "CLOUD:", self.name

    def tearDown(self):
        pass
    def test_00_check_label(self):
        HEADING("00 INFO OPENSTACK LABEL")
        print self.cloud_label
        assert self.cloud.label == self.cloud_label

    def test_01_limit(self):
        HEADING("01 INFO OPENSTACK LIMIT")
        print >> sys.stderr, json.dumps(self.cloud.limits(), indent=4)

    def test_02_images(self):
        HEADING("02 INFO OPENSTACK IMAGES")
        self.cloud.refresh('images')
        print json.dumps(self.cloud.images, indent=4)
        # pp.pprint(self.cloud.images)
        # doing a simple test as tiny is usually 512
        #assert self.cloud.flavors['m1.tiny']['ram'] == 512
        print "Currently running vms:", len(self.cloud.images)
        #we assume cloud is always busy which may actually not true
        # we shoudl start our own vm and than probe for it for now > 0 will do
        assert self.cloud.images > 0

    def test_03_flavor(self):
        HEADING("03 INFO OPENSTACK FLAVORS")
        self.cloud.refresh('flavors')
        print json.dumps(self.cloud.flavors, indent=4)

        # doing a simple test as tiny is usually 512
        assert self.cloud.flavors['m1.tiny']['ram'] == 512

    def test_04_start_vm(self):
        HEADING("04 START VM")
        result = self.cloud.vm_create("gregor-test-001","m1.tiny","e503bcb4-28c8-4f9f-8303-d99b9bffd568")
        print result
        assert len(result.keys()) > 0
        
    def test_04_vms(self):
        HEADING("04 INFO OPENSTACK VMS")
        self.cloud.refresh('servers')
        print json.dumps(self.cloud.servers, indent=4)
        # we assume that there are always images running
        assert len(self.cloud.servers) > 0

    def test_05_refresh(self):
        HEADING("05 INFO OPENSTACK REFRESH")
        self.cloud.refresh()
        pp.pprint(self.cloud)

        assert self.cloud.images > 0

    """
    def test_0??_usage(self):
        result = self.cloud.usage("2000-01-01T00:00:00", "2013-12-31T00:00:00")
        print json.dumps(result, indent=4)
        assert ['Instances'] > 0 
    """
        
    def test_06_table(self):
        HEADING("06 INFO OPENSTACK TABLES")
        self.test_03_flavor()
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
        HEADING("08 INFO LIST VMS FROM USER")
        list = self.cloud.vms_user(refresh=True)
        print json.dumps(list, indent=4)

    def test_09_delete_all_user_vms(self):
        HEADING("09 INFO OPENSTACK DELETE VMS FROM USER")

        
        self.cloud.refresh()

        user_id = self.cloud.find_user_id()
        vm_ids = self.cloud.find('user_id', user_id)

        servers = self.cloud.servers
        print servers

        list = self.cloud.vms_delete_user()

        self.cloud = openstack(self.cloud_label)
        self.cloud.refresh()
        self.cloud.info()
        
        vm_ids = self.cloud.find('user_id', user_id)
        self.cloud.info()
        
        time.sleep(2)
        self.cloud.refresh()

        while len(vm_ids) > 0:
            vm_ids = self.cloud.find('user_id', user_id)
            self.cloud.refresh("servers")
            self.cloud.info()
            time.sleep(1)
        
        print "vms",  vm_ids
        assert vm_ids == []

    def test_10_info(self):
        HEADING("10 INFO OPENSTACK TEST")
        self.cloud.refresh()
        time.sleep(3)
        self.cloud.info()

    def test_11_states(self):
        HEADING("10 INFO OPENSTACK TEST")
        self.cloud.refresh()
        time.sleep(3)
        print self.cloud.states

        search_states = ('ACTIVE','PAUSED')

        state = 'ACTIVE'
        userid = None
        
        print state in search_states
        
        #self.cloud.display(search_states, userid)
        
        #print json.dumps(self.cloud.servers, indent=4)        

        self.cloud.display_regex("vm['status'] in ['ACTIVE']", userid)

        print json.dumps(self.cloud.servers, indent=4)        

        #        self.cloud.display_regex("vm['status'] in ['ERROR']", userid)

        #print json.dumps(self.cloud.servers, indent=4)        

""" run with

nosetests -v --nocapture

or

nosetests -v

individual tests can be run with

nosetests -v  --nocapture test_cm_compute.py:Test.test_06

"""
from __future__ import print_function
from cloudmesh.shell.Shell import Shell
import string
import os
import time


from cloudmesh.config.cm_config import cm_config
from cloudmesh.iaas.eucalyptus.eucalyptus import eucalyptus
from cloudmesh.util.cm_table import cm_table
import json
from pprint import pprint

from cloudmesh_base.util import HEADING
from cloudmesh_base.locations import config_file


class Test:

    # assuming first - is the prefered cloud
    print(os.path.expandvars(cloudmesh_yaml=config_file("/cloudmesh.yaml")))
    cloud_label = Shell.head(
        Shell.fgrep("-", cloudmesh_yaml=config_file("/cloudmesh.yaml")), "-n", "1")
    cloud_label = cloud_label.replace(" - ", "").strip()

    def setup(self):
        self.configuration = cm_config()
        euca_clouds = []
        for name in self.configuration.config['cloudmesh']['clouds'].keys():
            if self.configuration.config['cloudmesh']['clouds'][name]['cm_type'] == 'eucalyptus':
                euca_clouds.append(name)
        self.name = euca_clouds[0]
        print("LOADING EUCA CLOUD", self.name)
        self.cloud = eucalyptus(self.name)
        print("LOADED CLOUD")

    def tearDown(self):
        pass

    def start(self):
        HEADING()
        image = self.configuration.default(self.name)['image']
        flavor = self.configuration.default(self.name)['flavor']
        self.configuration.prefix = "gvonlasz-test"
        self.configuration.incr()
        name = self.configuration.vmname
        print("STARTING IMAGE", name, image, flavor)
        result = self.cloud.vm_create(name, flavor, image)
        print(result)

    def test_label(self):
        HEADING()
        print(self.cloud.label)
        print(self.cloud.credentials)
        assert True

    # def test_01_limit(self):
    #    HEADING()
    #    print json.dumps(self.cloud.limits(), indent=4)

    def test_info(self):
        HEADING()
        self.cloud.refresh('images')
        print(json.dumps(self.cloud.dump('images'), indent=4))
        # pprint(self.cloud.dump('images', with_manager=True))
        pprint(self.cloud.images)
        # doing a simple test as tiny is usually 512
        # assert self.cloud.flavors['m1.tiny']['ram'] == 512
        print("Currently running vms:", len(self.cloud.images))
        # we assume cloud is always busy which may actually not true
        # we should start our own vm and than probe for it for now > 0 will do
        assert self.cloud.images > 0

    def test_list_flavors(self):
        HEADING()
        self.cloud.refresh('flavors')

        print(json.dumps(self.cloud.dump('flavors'), indent=4))

        # doing a simple test as tiny is usually 512
        assert self.cloud.flavors['m1.small']['ram'] == 512

    def test_list_images(self):
        HEADING()
        self.cloud.refresh('images')

        print(json.dumps(self.cloud.dump('images'), indent=4))

        # doing a simple test as tiny is usually 512
        # assert self.cloud.flavors['m1.small']['ram'] == 512
        assert True

    def test_list_servers(self):
        HEADING()
        self.cloud.refresh('servers')

        print(json.dumps(self.cloud.dump('servers'), indent=4))

        # doing a simple test as tiny is usually 512
        # assert self.cloud.flavors['m1.small']['ram'] == 512
        assert True

    def test_start_vm(self):
        HEADING()
        configuration = cm_config()
        print("NAME", self.name)

        print("Getting Flavours")
        self.cloud.refresh('flavors')
        flavor = configuration.default(self.name)['flavor']

        print("Getting Images")
        self.cloud.refresh('images')
        image = configuration.default(self.name)['image']

        print(self.cloud.flavors_cache)
        print(self.cloud.images_cache)

        print("STARTING IMAGE", image, flavor)
        result = self.cloud.vm_create(
            "gregor-test-001", flavor_name=flavor, image_id=image)
        print(result)
        assert len(result.keys()) > 0

    def test_delete_vm(self):
        HEADING()
        configuration = cm_config()
        print("NAME", self.name)

        print("Getting Flavours")
        self.cloud.refresh('flavors')
        flavor = configuration.default(self.name)['flavor']

        print("Getting Images")
        self.cloud.refresh('images')
        image = configuration.default(self.name)['image']

        # print self.cloud.flavors_cache
        # print self.cloud.images_cache

        print("STARTING VM", image, flavor)
        result = self.cloud.vm_create(
            "gregor-test-del", flavor_name=flavor, image_id=image)
        print(result)

        print("DELETE VM", image, flavor)
        self.cloud.refresh('servers')
        result = self.cloud.vm_delete("gregor-test-del")
        print(result)

        assert len(result.keys()) > 0

    def test_refresh(self):
        HEADING()
        self.cloud.refresh()
        pprint(self.cloud.get(self.name))
        assert self.cloud.images > 0

    def test_05_print_vms(self):
        HEADING()
        self.cloud.refresh('servers')
        print(json.dumps(self.cloud.dump('servers'), indent=4))
        # we assume that there are always images running
        assert len(self.cloud.servers) > 0

    """
    def test_0??_usage(self):
        result = self.cloud.usage("2000-01-01T00:00:00", "2013-12-31T00:00:00")
        print json.dumps(result, indent=4)
        assert ['Instances'] > 0
    """

    def test_07_print_tables(self):
        HEADING()
        self.test_03()
        table = cm_table()
        columns = ["id", "name", "ram", "vcpus"]

        table.create(self.cloud.flavors, columns, header=True)
        print(table)

        table = cm_table()
        columns = ["id", "name", "ram", "vcpus"]

        table.create(self.cloud.flavors, columns, format='HTML', header=True)
        print(table)

        table = cm_table()
        columns = ["id", "name", "ram", "vcpus"]

        table.create(self.cloud.flavors, columns, format='%12s', header=True)
        print(table)

        assert table is not None
    """
    def test_07_start_delete_vm(self):
        name ="%s-%04d" % (self.cloud.credential["OS_USERNAME"], 1)
        out = self.cloud.vm_create(name, "m1.tiny", "6d2bca76-8fff-4d57-9f29-50378539b4fa")

        pprint(out)
        print json.dumps(out, indent=4)

        key = out.keys()[0]
        id = out[key]["id"]
        print id

        vm = self.cloud.vm_delete(id)
        print vm
    """

    def test_08_delete_vms_of_user(self):
        HEADING()

        self.cloud.refresh()

        user_id = self.cloud.find_user_id(force=True)
        vm_ids = self.cloud.find('user_id', user_id)
        print("userid", user_id)
        config = cm_config()
        config.data['cloudmesh']['clouds'][self.name][
            'credentials']['OS_USER_ID'] = user_id
        config.write()

        #
        # delete all vms of the user
        #
        servers = self.cloud.servers
        print(servers)

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

        print("vms", vm_ids)

        assert vm_ids == []

    def test_09_start_two_vms(self):
        HEADING()
        configuration = cm_config()
        image = configuration.default(self.name)['image']
        print("STARTING IMAGE", image)
        result = self.cloud.vm_create("gregor-test-001", "m1.tiny", image)
        # print result
        result = self.cloud.vm_create("gregor-test-002", "m1.tiny", image)
        # print result
        self.cloud.refresh()
        self.cloud.info()

        config = cm_config()
        print("CONFIG")
        user_id = config.data['cloudmesh']['clouds'][
            self.name]['credentials']['OS_USER_ID']
        print(user_id)

        vm_ids = self.cloud.find('user_id', user_id)
        print(vm_ids)

        assert len(vm_ids) == 2

    def test_10_list_user_vms(self):
        HEADING()
        list = self.cloud.vms_user(refresh=True)
        pprint(list)

    def test_11_refresh_all(self):
        HEADING()
        self.cloud.refresh()
        self.cloud.info()

    def test_12_print_states(self):
        HEADING()
        self.cloud.refresh()
        print(self.cloud.states)

        search_states = ('ACTIVE', 'PAUSED')

        state = 'ACTIVE'
        userid = None

        print(state in search_states)

        # self.cloud.display(search_states, userid)

        # print json.dumps(self.cloud.servers, indent=4)

        self.cloud.display_regex("vm['status'] in ['ACTIVE']", userid)

        print(json.dumps(self.cloud.dump('servers'), indent=4))

        #        self.cloud.display_regex("vm['status'] in ['ERROR']", userid)

        # print json.dumps(self.cloud.servers, indent=4)

    def test_13_meta(self):
        HEADING()
        self.clean()
        image = self.configuration.default(self.name)['image']
        flavor = self.configuration.default(self.name)['flavor']
        self.configuration.prefix = "gvonlasz-test"
        self.configuration.incr()
        name = self.configuration.vmname
        print(name)
        result = self.cloud.vm_create(name, flavor, image)
        id = result['id']
        print(id)
        result = self.cloud.wait(id, 'ACTIVE')
        result = self.cloud.set_meta(id, {"owner": "gregor"})
        print("RESULT", result)
        meta = self.cloud.get_meta(id)
        print(meta)

    def info(self):
        HEADING()
        self.cloud.refresh()
        self.cloud.info()

    def clean(self):
        HEADING()

        self.cloud.refresh()
        self.cloud.info()

        user_id = self.cloud.find_user_id()
        print("Cleaning", user_id)

        list = self.cloud.vms_delete_user()
        print("Cleaning", list)

        vm_ids = self.cloud.find('user_id', user_id)
        while len(vm_ids) > 0:
            vm_ids = self.cloud.find('user_id', user_id)
            self.cloud.refresh("servers")
            self.cloud.info()
            time.sleep(1)

        print("vms", vm_ids)

        assert vm_ids == []

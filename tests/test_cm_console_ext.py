""" run with

nosetests -v --nocapture test_cm_console_ext.py

or

nosetests -v --nocapture test_cm_console_ext.py -s CLOUD_NAME e.g. india

"""
from cloudmesh_base.util import HEADING
from cloudmesh_base.logger import LOGGER, LOGGING_ON, LOGGING_OFF
import sys
import os
import cloudmesh
import unittest
import random
import time
        
log = LOGGER(__file__)

vm = []


class Test(unittest.TestCase):

    def setUp(self):

        self.cloudname = "india"
        if "-s" in sys.argv:
            self.cloudname = sys.argv[-1:][0]

        self.config = cloudmesh.load("user")
        self.username = self.config.get("cloudmesh.hpc.username")
    
    def test_01_activate_cloud(self):
        HEADING()
        res = os.popen("cm cloud on {0}".format(self.cloudname)).read()
        assert res.find("cloud '{0}' activated.".format(self.cloudname)) != -1

    def test_02_validate_activation(self):
        HEADING()
        res = os.popen('cm cloud list |'
                       'grep india |'
                       'grep True |'
                       'wc -l').read()
        assert res.strip() == "1"

    def test_03_start_a_vm(self):
        HEADING()
        global vm
        vmname = "{0}_{1}_{2}".format(self.username, "test",str(random.randint(1,100)))
        cmd = ('cm "vm start'
               ' --name={0}'
               ' --cloud=india'
               ' --image=futuregrid/ubuntu-14.04'
               ' --flavor=m1.small"'.format(vmname))

        res = os.popen(cmd).read()
        vm.append(vmname)
        assert ("job status: PENDING" in res 
                or "job status: STARTED" in res) == True
        time.sleep(1)

    def test_04_validate_vm_running(self):
        HEADING()
        global vm
        for vmname in vm:
            res = os.popen('cm "list vm india --refresh" '
                           ' | grep {0} | wc -l'.format(vmname)).read()
            assert res.strip() == "1"

    def test_05_delete_vms(self):
        HEADING()
        global vm
        for vmname in vm:
            cmd = ('cm "vm delete {0} --cloud=india --force"'.format(vmname))
            res = os.popen(cmd).read()
            assert res.find("{'msg': 'success'}") != -1
    
    def test_06_validate_vm_deleted(self):
        HEADING()
        global vm
        for vmname in vm:
            res = os.popen('cm "list vm india --refresh" '
                           '| grep {0}|wc -l'.format(vmname)).read()
            assert res.strip() == "0"
            vm.remove(vmname)

    def test_07_default_flavor(self):
        HEADING()
        res = os.popen('cm "cloud set flavor india --id=2"').read()
        assert res.find("'m1.small' is selected") != -1

    def test_08_validate_default_flavor(self):
        HEADING()
        res = os.popen("cm cloud default | grep m1.small | wc -l").read()
        assert res.strip() == "1"

    def test_09_default_image(self):
        HEADING()
        res = os.popen('cm "cloud set image india'
                 ' --name=futuregrid/ubuntu-14.04"').read()
        assert res.find("'futuregrid/ubuntu-14.04' is selected") != -1

    def test_10_validate_default_image(self):
        HEADING()
        res = os.popen("cm cloud default|grep ubuntu-14.04|wc -l").read()
        assert res.strip() == "1"

    def test_11_quick_start(self):
        HEADING()
        global vm
        vmname = "nosetests_" + str(random.randint(1,100))
        res = os.popen('cm "vm start --name={0}"'.format(vmname)).read()
        assert ("job status: PENDING" in res 
                or "job status: STARTED" in res) == True
        vm.append(vmname)
        time.sleep(1)

    def test_12_validate_vm_running(self):
        HEADING()
        global vm
        for vmname in vm:
            res = os.popen('cm "list vm india --refresh" '
                           '| grep {0} | wc -l'.format(vmname)).read()
            assert res.strip() == "1"

    def test_13_delete_vms(self):
        HEADING()
        global vm
        for vmname in vm:
            cmd = ('cm "vm delete {0} --cloud=india --force"'.format(vmname))
            res = os.popen(cmd).read()
            assert res.find("{'msg': 'success'}") != -1
            #cls.vm.remove(vmname)

    def test_14_validate_vm_deleted(self):
        HEADING()
        global vm
        for vmname in vm:
            res = os.popen('cm "list vm india --refresh" '
                           ' | grep {0} | wc -l'.format(vmname)).read()
            assert res.strip() == "0"
            vm.remove(vmname)

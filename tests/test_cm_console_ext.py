""" run with

nosetests -v --nocapture test_cm_console_ext.py

"""
from cloudmesh_common.util import HEADING
from cloudmesh_common.logger import LOGGER, LOGGING_ON, LOGGING_OFF
import sys
import os
import cloudmesh
import unittest

log = LOGGER(__file__)

class Test(unittest.TestCase):
    vm = []

    def test_01_activate_cloud(self):
        HEADING()
        os.system("cm cloud on india")

    def test_02_validate_activation(self):
        HEADING()
        res = os.popen("cm cloud list | grep india| grep True |wc -l").read()
        assert res.strip() == "1"

    @classmethod
    def test_03_start_a_vm(cls):
        HEADING()
        import random
        vm_name = "nosetests_"+str(random.randint(1,100))
        cmd = "cm \"vm start --name={0} --cloud=india \
                        --image=futuregrid/ubuntu-14.04 \
                        --flavor=m1.small\"".format(vm_name)
        print cmd
        os.system(cmd)
        cls.vm.append(vm_name)

    def test_04_validate_vm_running(self):
        HEADING()
        for vmname in self.vm:
            res = os.popen("cm \"list vm india --refresh\"|grep " + \
                           " {0} | wc -l".format(vmname)).read()
            assert res.strip() == "1"

    def test_05_delete_vms(self):
        HEADING()
        for vm_name in self.vm:
            cmd = ("cm \"vm delete {0} --cloud=india --force\"".format(vm_name))
            os.system(cmd)
    
    @classmethod
    def test_06_validate_vm_deleted(cls):
        HEADING()
        for vmname in cls.vm:
            res = os.popen("cm \"list vm india --refresh\"|grep {0}|wc " + \
                           " -l".format(vmname)).read()
            assert res.strip() == "0"
            cls.vm.remove(vmname)

    def test_07_default_flavor(self):
        HEADING()
        os.system("cm \"cloud set flavor india --flavorid=2\"")

    def test_08_validate_default_flavor(self):
        HEADING()
        res = os.popen("cm cloud default|grep m1.small|wc -l").read()
        assert res.strip() == "1"

    def test_09_default_image(self):
        HEADING()
        os.system("cm \"cloud set image india --image=futuregrid/ubuntu-14.04\"")

    def test_10_validate_default_image(self):
        HEADING()
        res = os.popen("cm cloud default|grep ubuntu-14.04|wc -l").read()
        assert res.strip() == "1"

    @classmethod
    def test_11_quick_start(cls):
        HEADING()
        import random
        vm_name = "nosetests_"+str(random.randint(1,100))
        os.system("cm \"vm start --name={0}\"".format(vm_name))
        cls.vm.append(vm_name)

    def test_12_validate_vm_running(self):
        HEADING()
        for vmname in self.vm:
            res = os.popen("cm \"list vm india --refresh\"|grep " + \
                           " {0} | wc -l".format(vmname)).read()
            assert res.strip() == "1"

    def test_13_delete_vms(self):
        HEADING()
        for vm_name in self.vm:
            cmd = ("cm \"vm delete {0} --cloud=india --force\"".format(vm_name))
            os.system(cmd)
            #cls.vm.remove(vm_name)

    @classmethod
    def test_14_validate_vm_deleted(cls):
        HEADING()
        for vmname in cls.vm:
            res = os.popen("cm \"list vm india --refresh\"|grep {0}|wc " + \
                           " -l".format(vmname)).read()
            assert res.strip() == "0"
            cls.vm.remove(vmname)

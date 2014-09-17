""" run with

nosetests -v --nocapture test_cm_api.py

"""
from cloudmesh_common.util import HEADING
from cloudmesh_common.logger import LOGGER, LOGGING_ON, LOGGING_OFF

log = LOGGER(__file__)

import sys
import os
import cloudmesh

import unittest

class Test(unittest.TestCase):
    mesh = None
    username = ""
    cloudname = ""
    vm = []
    ip = []

    @classmethod
    def test_01_init(cls):
        HEADING()
        cls.mesh = cloudmesh.mesh("mongo")
      
    @classmethod
    def test_02_get_username(cls):
        HEADING()
        cls.username = cloudmesh.load().username()

    def test_03_activate(self):
        HEADING()
        self.mesh.activate(self.username)

    @classmethod
    def test_04_set_cloud_refresh(cls):
        HEADING()
        cls.cloudname = "india"
        cls.mesh.refresh(cls.username)

    def test_05_list_flavors(self):
        HEADING()
        self.mesh.flavors(cm_user_id=self.username, clouds=[self.cloudname])

    def test_06_list_images(self):
        HEADING()
        self.mesh.images(cm_user_id=self.username, clouds=[self.cloudname])

    @classmethod
    def test_07_get_flavor(cls):
        HEADING()
        cls.flavor = cls.mesh.flavor(cls.cloudname, "m1.small")

    @classmethod
    def test_08_get_image(cls):
        HEADING()
        cls.image = cls.mesh.image(cls.cloudname, "futuregrid/ubuntu-14.04")

    def test_09_set_default_flavor(self):
        HEADING()
        self.mesh.default(self.cloudname, "flavor", self.flavor)

    def test_10_set_default_image(self):
        HEADING()
        self.mesh.default(self.cloudname, "image", self.image)

    @classmethod
    def test_11_start_a_vm(cls):
        HEADING()
        result = cls.mesh.start(cls.cloudname, cls.username)
        cls.vm.append(result)

    @classmethod
    def test_12_assign_public_ip(cls):
        HEADING()
        for vm in cls.vm:
            vm_id = vm['server']['id']
            ip = cls.mesh.assign_public_ip(cls.cloudname, vm_id, cls.username)
            log.info("{0} allocated to {1}".format(ip, vm_id))
            cls.ip.append(ip)

    def test_13_ssh_vm(self):
        HEADING()
        for ip in self.ip:
            result = self.mesh.wait(ipaddr=ip, command="uname -a", interval=10, retry=5)
            log.info("ssh call to [{0}]: {1}".format(ip, str(result)))

    @classmethod
    def test_14_delete_a_vm(cls):
        HEADING()
        for vm in cls.vm:
            vm_id = vm['server']['id']
            cls.mesh.delete(cls.cloudname, vm_id, cls.username)
            cls.vm.remove(vm)

    @classmethod
    def test_15_start_3_vms(cls):
        HEADING()
        for i in range(3):
            result = cls.mesh.start(cls.cloudname, cls.username)
            cls.vm.append(result)

    @classmethod
    def test_16_delete_3_vms(cls):
        HEADING()
        for vm in cls.vm:
            vm_id = vm['server']['id']
            cls.mesh.delete(cls.cloudname, vm_id, cls.username)
            cls.vm.remove(vm)


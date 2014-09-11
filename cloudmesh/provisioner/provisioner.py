from abc import ABCMeta, abstractmethod
from multiprocessing import Pool
import logging
from cloudmesh_common.logger import LOGGER
import time
from random import randrange
from cloudmesh.inventory import Inventory

#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)


class BaremetalProvisinerABC:
    __metaclass__ = ABCMeta

    # hosts = ['host1', 'host2']
    # image = 'hpc'

    hosts = []
    image = []

    def __init__(self):
        self.inventory = Inventory()

    @abstractmethod
    def provision(self, hosts, image):
        self.hosts = hosts
        self.image = image
        pass

    def set_status(self, host_label, status):
        print "SIM setting", host_label, status
        self.inventory.set_attribute(host_label, "cm_provision_status", status)
        print "SIM ok setting", host_label, status


class ProvisionerSimulator(BaremetalProvisinerABC):

    # needs Inventory
    # status = get_attribute(self, host_label, "cm_provision_status", attribute)

    def __init__(self):
        BaremetalProvisinerABC.__init__(self)

    def provision(self, hosts, provisioned):
        self.hosts = hosts
        for host in hosts:

            print "PROVISION", host, provisioned
            log.info("Provision {0}<-{1}".format(host, provisioned))

            self.set_status(host, "INITIATING")
            time.sleep(randrange(1, 3))

            self.set_status(host, "PREPARING_IMAGE")
            # image = inventory.get("server",host)
            time.sleep(randrange(1, 3))

            self.set_status(host, "BOOTING")
            # image = inventory.get("server",host)
            time.sleep(randrange(1, 3))

            self.set_status(host, "AVAILABLE")
            # image = inventory.get("server",host)
            time.sleep(randrange(1, 3))

            self.set_status(host, "SUCCESS")
            # image = inventory.get("server",host)
            time.sleep(randrange(1, 3))

        return (True, None)

    def provision_image(self, hosts, image):

        for host in hosts:
            log.info("Provision {0}->{1}".format(image, host))
            # image = inventory.get("server",host)
            time.sleep(randrange(0, 3))


class ProvisionerCobbler(BaremetalProvisinerABC):

    def provision(self, hosts, image):
        for host in hosts:
            log.info("Provision {0}->{1}".format(image, host))


class ProvisionerOpenStack(BaremetalProvisinerABC):

    def provision(self, hosts, image):
        for host in hosts:
            log.info("Provision {0}->{1}".format(image, host))

if __name__ == "__main__":

    hosts = ["1", "2", "3", "a1", "a2", "a3",
             "b1", "b2", "b3", "c1", "c2", "c3", ]
    image = "a"

    provisioner = ProvisionerSimulator

    p = provisioner()
    p.provision(hosts, image)

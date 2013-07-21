from abc import ABCMeta, abstractmethod
from multiprocessing import Pool
import logging
from cloudmesh.util.logger import LOGGER
import time
from random import randrange
from cloudmesh.inventory.inventory import FabricImage, FabricServer, \
    FabricService, Inventory

#
# SETTING UP A LOGGER
#

log = LOGGER('provision')

inventory = Inventory("nosetest")

class BaremetalProvisinerABC:
    __metaclass__ = ABCMeta

    # hosts = ['host1', 'host2']
    # image = 'hpc'

    hosts = []
    images = []

    @abstractmethod
    def provision(self, hosts, image):
        pass



class ProvisionerSimulator(BaremetalProvisinerABC):

    def set_status(self, element, status):
        element.status = status
        element.save(cascade=True)

        
    def provision(self, hosts, provisioned):
        for host in hosts:
            print "PROVISION", host, provisioned
            log.info("Provision {0}<-{1}".format(host, provisioned))
            server = inventory.get("server",host)

            server.provisioned = provisioned
            self.set_status(server, "INITIATING")
            time.sleep(randrange(0, 3))

            self.set_status(server, "PREPARING_IMAGE")
            # image = inventory.get("server",host)
            time.sleep(randrange(0, 3))

            self.set_status(server, "BOOTING")
            # image = inventory.get("server",host)
            time.sleep(randrange(0, 3))

            self.set_status(server, "AVAILABLE")
            # image = inventory.get("server",host)
            time.sleep(randrange(0, 3))

            self.set_status(server, "SUCCESS")
            # image = inventory.get("server",host)
            time.sleep(randrange(0, 3))

            

        
    def provision_image(self, hosts, image):

        for host in hosts:
            log.info("Provision {0}->{1}".format(image, host))
            server = inventory.get("server",host)
            # image = inventory.get("server",host)
            
            time.sleep(randrange(0, 3))

class ProvisionerTeefaa(BaremetalProvisinerABC):

    def provision(self, hosts, image):
        for host in hosts:
            log.info("Provision {0}->{1}".format(image, host))


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

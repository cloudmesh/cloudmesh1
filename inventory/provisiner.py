from abc import ABCMeta, abstractmethod  
from multiprocessing import Pool
import logging

######################################################################
# SETTING UP A LOGGER
######################################################################

log = logging.getLogger('provision')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('CM Provision: [%(levelname)s] %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)

class BaremetalProvisinerABC:
    __metaclass__ = ABCMeta
    
    #hosts = ['host1', 'host2']
    #image = 'hpc'

    hosts = []
    images= []

    @abstractmethod
    def provision(self, hosts, image):
        pass


import multiprocessing
import subprocess


class ProvisionerSimulator(BaremetalProvisinerABC):

    def provision(self, hosts, image):
        for host in hosts:
            log.info("Provision {0}->{1}".format(image, host))

    
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

    hosts = ["1", "2", "3", "a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3", ]
    image = "a"


    provisioner = ProvisionerSimulator

    p = provisioner()
    p.provision(hosts, image)




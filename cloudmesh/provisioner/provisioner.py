from abc import ABCMeta, abstractmethod
from multiprocessing import Pool
import logging
from cloudmesh.util.logger import LOGGER

#
# SETTING UP A LOGGER
#

log = LOGGER('provision')


class BaremetalProvisinerABC:
    __metaclass__ = ABCMeta

    # hosts = ['host1', 'host2']
    # image = 'hpc'

    hosts = []
    images = []

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

    hosts = ["1", "2", "3", "a1", "a2", "a3",
             "b1", "b2", "b3", "c1", "c2", "c3", ]
    image = "a"

    provisioner = ProvisionerSimulator

    p = provisioner()
    p.provision(hosts, image)

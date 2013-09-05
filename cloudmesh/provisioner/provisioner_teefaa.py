from abc import ABCMeta, abstractmethod
from multiprocessing import Pool
import logging
from cloudmesh.util.logger import LOGGER
import time
from random import randrange
from cloudmesh.inventory import Inventory

from cloudmesh.provisioner.provisioner import BaremetalProvisinerABC
from cloudmesh.util.config import read_yaml_config
from sh import ssh 
import sys
#
# SETTING UP A LOGGER
#

"""

[172.29.200.130] run: test -e "/tftpboot/pxelinux.cfg/i66" && echo OK ; true
[172.29.200.130] out: OK
[172.29.200.130] out: 

[172.29.200.130] run: cat /tftpboot/pxelinux.cfg/localboot > /tftpboot/pxelinux.cfg/i66

Done.
Disconnecting from 172.29.200.130... done.
Disconnecting from root@i66... done.

real    5m51.929s
user    0m3.476s
sys    0m1.076s


imageman@i130:~/teefaa$ 
"""

log = LOGGER('provision')



class ProvisionerTeefaa(BaremetalProvisinerABC):

    def __init__(self):
        """read config"""
        BaremetalProvisinerABC.__init__(self)
        
        self.filename = "~/.futuregrid/cloudmesh_server.yaml"
        self.teefaa_config = read_yaml_config (self.filename, check=True)   
        

    def provision(self, host, image):
        """returns a verctor (success, log) where success is True, False and log contains the teefaa log"""
        
        cursor = self.inventory.get("server", "cm_id", host)
        server = cursor['cm_id'] 
        label = cursor['label'] 
        
        
        print "GGGG", server
        
        
        self.set_status(server, "INITIATING")
        
        print self.teefaa_config
        log.info("Provision {0}->{1}".format(image, host))
        self.host = label
        self.image = image
        
        parameters = ["-t", "{0}@{1}".format(self.teefaa_config["teefaa"]["username"],self.teefaa_config["teefaa"]["hostname"]), 
                     "cd", "{0}".format(self.teefaa_config["teefaa"]["dir"]), ";", 
                     "fab", "baremetal.provisioning:{0},{1}".format(host,image)]
        print "ssh", " ".join(parameters)

        print 70 * "="
        sys.stdout.flush()
        
        result = ""
        for line in ssh(parameters, _iter=True,_out_bufsize=1):
            line = line[:-1]
            print line
            sys.stdout.flush()
            result = result+line+"\n"
            if line.startswith("CM STATUS"):
                (ignore, status) = line.split(":")
                self.set_status(server, status)


        # self.set_status(server, "PREPARING_IMAGE")
        # self.set_status(server, "BOOTING")
        # self.set_status(server, "AVAILABLE")


        
        #To check if things are ok we just do 

        # Done.
        # Disconnecting from {ip form bmc}... done.
        # Disconnecting from root@{hostname}... done.
        #
        # will need better checking as currently depends on os, e.g. rot@ may be os dependent
        # also can not login into provisioned host
        #

        print 70 * "P"
        print result
                
        result = result.strip().split("\n")
        
        print 70 * "Q"
        print result
        
        condition_a = result[-1] == "Disconnecting from root@{0}... done.".format(host)
        condition_b = result[-2] == "Disconnecting from {0}... done.".format(self.teefaa_config["teefaa"]["bmcname"])
        condition_c = result[-3] == "Done."
        
        success = condition_a and condition_b and condition_c, result
        if success:
       
            self.set_status(server, "SUCCESS")
        else:
            self.set_status(server, "FAILED")
    
        
        return (success, None)

        # check status



if __name__ == "__main__":

    #hosts = ["1", "2", "3", "a1", "a2", "a3",
    #         "b1", "b2", "b3", "c1", "c2", "c3", ]
    #image = "a"

    provisioner = ProvisionerTeefaa

    
    host = "i66"
    image = "ubuntu1304v2btsync"

    p = provisioner()
    (success, result) = p.provision(host, image)
    
    print result
    print success
 
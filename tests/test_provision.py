""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import sys
import json
import pprint

from cloudmesh.util.util import HEADING
from cloudmesh.util.util import path_expand
from cloudmesh.provisioner.provisioner import ProvisionerSimulator   
from cloudmesh.provisioner.provisioner_teefaa import ProvisionerTeefaa 

class Test_cloudmesh:

    filename = path_expand("$HOME/.futuregrid/cloudmesh.yaml")

    def setup(self):
        pass
    
    def tearDown(self):
        pass


    def test_policy(self):
        HEADING()
        pass


    def test_simulator(self):
        HEADING()

        
        #hosts = ["1", "2", "3", "a1", "a2", "a3",
        #         "b1", "b2", "b3", "c1", "c2", "c3", ]
        #image = "a"

        hosts = ["i066"]
        image = "ubuntu1304v2btsync"

        Provisioner = ProvisionerSimulator   

        (success, result) = (None, None)

        p = Provisioner()
        (success, result) = p.provision(hosts, image)
    
        print result
        print success

        
        pass

    def test_teefaa(self):
        HEADING()
        
        
            

        host = "i066"
        image = "ubuntu1304v2btsync"

        Provisioner = ProvisionerTeefaa 

        p = Provisioner()
        (success, result) = p.provision(host, image)
    
        print result
        print success

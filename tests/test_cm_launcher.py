""" run with

nosetests -v --nocapture --nologcapture
nosetests -v  --nocapture test_inventory.py:Test_Inventory.test_06
nosetests -v

"""

from cloudmesh.provisioner.cm_launcher import SimulatorLauncher
from  pprint import pprint

from cloudmesh.util.util import HEADING
import sys


class Test_Launcher:

    # filename = "$HOME/.futuregrid/cloudmesh-new.yaml"

    def setup(self):
        provider = SimulatorLauncher
        self.launcher = provider()
        
    def tearDown(self):
        pass
        
    def test_register(self):
        HEADING()
        assert (self.launcher.register(None) )
        
    def test_states(self):
        HEADING()
        assert self.launcher.states() == self.launcher.states_list
        
    def test_status(self):
        HEADING()
        states = self.launcher.states()
        assert self.launcher.status in states
        
    def test_run(self):
        HEADING()
        self.launcher.register(None)   
        for host in self.launcher.recipies:
            recipie_list = self.launcher.recipies[host]
            for recipie in recipie_list:
                assert (self.launcher.run(host,recipie["name"]))         #assuming "name" to be the key in the dictionary

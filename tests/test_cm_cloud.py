""" run with

nosetests -v --nocapture

"""
from cloudmesh_common.util import HEADING
from cloudmesh_common.logger import LOGGER




log = LOGGER(__file__)

class Test(unittest.TestCase):

    def setUp(self):
        
        self.cloudname = "india"
        
        print ("CLOUD: ", self.cloudname)
        
    def test
        
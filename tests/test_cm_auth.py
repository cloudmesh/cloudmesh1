""" run with

nosetests -v --nocapture test_cm_auth.py

"""
from cloudmesh_base.util import HEADING
from cloudmesh_base.logger import LOGGER, LOGGING_ON, LOGGING_OFF

log = LOGGER(__file__)

import sys
import os

class Test:

    def test_01_debug_on(self):
        HEADING()
        os.system("cm debug on")
        
    def test_02_cloud_on(self):
        HEADING()
        os.system("cm cloud on india")

    def test_03_debug_on(self):
        HEADING()
        os.system("cm debug on")
 

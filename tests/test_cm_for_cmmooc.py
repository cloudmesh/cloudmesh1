""" run with

nosetests -v --nocapture test_cm_cmmooc.py

"""
from cloudmesh_common.util import HEADING
from cloudmesh_common.logger import LOGGER, LOGGING_ON, LOGGING_OFF
import sys
import os
import cloudmesh
import unittest
import random
import time
        
log = LOGGER(__file__)

def activate_cloud(self):
    res = os.popen("cm cloud on india").read()
    assert res.find("cloud 'india' activated.") != -1

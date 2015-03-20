""" run with

nosetests -v --nocapture test_cm_cmmooc.py

"""
from cloudmesh_base.util import HEADING
from cloudmesh_base.logger import LOGGER, LOGGING_ON, LOGGING_OFF
import sys
import os
import cloudmesh
import unittest
import random
import time

log = LOGGER(__file__)


def activate_cloud():
    res = os.popen("cm cloud on india").read()
    assert res.find("cloud 'india' activated.") != -1

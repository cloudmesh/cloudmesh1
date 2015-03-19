""" run with

nosetests -v --nocapture

or

nosetests -v

individual tests can be run with

nosetests -v  --nocapture test_cm_compute.py:Test.test_06

"""
from __future__ import print_function
import string
import os
import time
import json
from pprint import pprint

from cloudmesh.pbs.pbs_mongo import pbs_mongo
from cloudmesh.config.cm_config import cm_config
from cloudmesh_base.util import HEADING


class Test:

    def setup(self):
        config = cm_config()
        self.user = config.get()["hpc"]["username"]

        self.host = "india.futuregrid.org"
        self.pbs = pbs_mongo()
        self.pbs.activate(self.host, "gvonlasz")
        print("SETUP PBS HOSTS", self.pbs.hosts)

    def tearDown(self):
        pass

    def dump(self, msg, action):
        print(70 * "=")
        print(msg, self.user, self.host)
        print(70 * "=")
        if action == "qstat":
            d = self.pbs.get_qstat(self.host)
            for e in d:
                pprint(e)

    def test_qstat(self):
        HEADING()
        self.pbs.refresh_qstat(self.host)
        self.dump("refresh", "qstat")

    def test_nodes(self):
        HEADING()
        d = self.pbs.refresh_pbsnodes(self.host)
        self.dump("refresh", d)

    def test_get_qstat(self):
        d = self.pbs.get(self.host, "qstat")
        self.dump("get qstat", d)

    def test_get_nodes(self):
        d = self.pbs.get(self.host, "nodes")
        self.dump("get nodes", d)

    def test_i_get_qstat(self):
        d = self.pbs.get_qstat(self.host)
        self.dump("get qstat", d)

    def test_i_get_nodes(self):
        d = self.pbs.get_pbsnodes(self.host)
        self.dump("get nodes", d)

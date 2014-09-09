""" run with

nosetests -v --nocapture

or

nosetests -v

individual tests can be run with

nosetests -v  --nocapture test_cm_compute.py:Test.test_06

"""

from sh import head
from sh import fgrep
import string
import os
import time

from sh import ssh
import json
from pprint import pprint

from cloudmesh.pbs.pbs import PBS
from cloudmesh.config.cm_config import cm_config
from cloudmesh_common.util import HEADING
from cloudmesh import banner

class Test:

    hosts = ["india.futuregrid.org",
             "sierra.futuregrid.org",
             "hotel.futuregrid.org",
             "alamo.futuregrid.org"]


    def setup(self):
        # self.configuration = cm_config()
        # pprint (self.configuration.__dict__)
        self.user = "gvonlasz"
        self.host = "india.futuregrid.org"


        # pprint (_create_pbsinfo_dict(data))

    def tearDown(self):
        pass

    def get_qstat(self, host):
        HEADING()
        self.pbs = PBS(self.user, host)
        results = self.pbs.qstat()
        for name in results:
            element = results[name]
            pprint (element)

    def get_qinfo(self, host):
        HEADING()
        self.pbs = PBS(self.user, host)
        results = self.pbs.qinfo()
        for name in results:
            element = results[name]
            pprint (element)

    def test_all(self):
        HEADING()
        for host in self.hosts:
            banner(host)
            self.get_qstat(host)


    def test_info(self):
        HEADING()

        for host in self.hosts:
            self.pbs = PBS(self.user, host)
            results = self.pbs.qstat()

            print host, " =", len(results), "jobs"

    def test_qinfo(self):
        for host in self.hosts:
            banner(host)
            self.get_qinfo(host)




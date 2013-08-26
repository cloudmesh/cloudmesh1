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
from cloudmesh.util.util import HEADING

class Test:

    def setup(self):
        #self.configuration = cm_config() 
        #pprint (self.configuration.__dict__)
        self.user = "gvonlasz" 
        self.host = "india.futuregrid.org" 

        
        #pprint (_create_pbsinfo_dict(data))

    def tearDown(self):
        pass

    def test_qstat(self):
        HEADING()
        self.pbs = PBS(self.user, self.host)
        results = self.pbs.qstat()
        for name in results:
            element = results[name]
            pprint (element)

    def test_qstat_alamo(self):
        HEADING()
        self.host = "alamo.futuregrid.org"
        self.pbs = PBS(self.user, self.host)
        self.pbs.qstat()
        pprint (self.pbs.qstat)

    def test_info(self):
        HEADING()
        self.pbs = PBS(self.user, self.host)
        self.pbs.refresh()
        pprint (self.pbs.info)

        
        
        # ssh gvonlasz@alamo.futuregrid.org pbsnodes -a
        

""" run with

nosetests -v --nocapture

"""
from __future__ import print_function
from cloudmesh_base.util import HEADING
from cloudmesh_base.logger import LOGGER, LOGGING_ON, LOGGING_OFF

log = LOGGER(__file__)


class Test:

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_01_onoff(self):
        HEADING()
        LOGGING_ON(log)
        print("LOGGING ON - all levels should show")
        log.info("You should see me 1")
        log.debug("You should see me 2")
        LOGGING_OFF(log)
        print("LOGGING OFF - Only critical would show")
        log.info("You should not see me 1")
        log.error("You should not see me 2")
        log.critical("You should see me 3")
        LOGGING_ON(log)
        print("LOGGING ON again - all levels should show")
        log.debug("You should see me again 4")
        log.error("You should see me again 5")
        assert True

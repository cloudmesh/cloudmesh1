""" run with

nosetests -v --nocapture test_cm.py

"""
from cloudmesh_common.util import HEADING
from cloudmesh_common.logger import LOGGER, LOGGING_ON, LOGGING_OFF

log = LOGGER(__file__)

import cloudmesh

class Test:

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_01_help(self):
        HEADING()

        cloud_commands = [
            "cloud",
            "group",
            "inventory",
            "rain",
            "storm",
            "yaml",
            "keys",
            "defaults",
            "image",
            "list",
            "register",
            "user",
            "debug",
            "project",
            "flavor",
            "init",
            "metric",
            "security_group",
            "vm",
            "loglevel",
            ]

        success = True
        for command in cloud_commands:
            execution = "help {0}".format(command)
            print "testing", execution,
            try:
                result = cloudmesh.shell(execution)
            except Exception, e:
                success = False
                print e
            if "Usage" not in result:
                print command, "ERROR", result
                success = False
            else:
                success = success 
                print "ok"
        assert success 

""" run with

nosetests -v --nocapture

or

nosetests -v

individual tests can be run with

nosetests -v  --nocapture test_shell.py:Test.test_list

"""
from __future__ import print_function
import string
import os
import time
import json
from pprint import pprint
from cloudmesh.shell.Shell import Shell
from cloudmesh_base.util import HEADING


class Test:

    def setup(self):
        self.host = "india.futuregrid.org"

        # pprint (_create_pbsinfo_dict(data))

    def tearDown(self):
        pass

    def test_help(self):
        HEADING()
        r = Shell.cm("help")
        print(r)
        assert "vm" in r and "cloud" in r and "list" in r

    def message(self, state, word):
        if state:
            return word + " passed"
        else:
            return word + " failed"

    def grep_command(self, command, valid, invalid):
        ok = True
        r = Shell.cm(command)
        print(r)
        if valid is not None:
            for word in valid:
                msg = "passed"
                testing = word in r
                print("Testing", command, self.message(testing, word))
                ok = ok and testing
        if invalid is not None:
            for word in invalid:
                msg = "passed"
                testing = word not in r
                print("Testing", command, self.message(testing, word))
                ok = ok and testing
        return ok

    def test_help_commands(self):
        HEADING()
        help_commands = [("cloud", "cloud on", None),
                         ("flavor", "", "<"),
                         ("init", "KIND", None),
                         ("list", "projects", None),
                         ("rain", "KIND", None),
                         ("reservation", "duration", None),
                         ("storm", "ID", None),
                         ("vm", "CLOUD", "<"),
                         ("defaults", "clean", None),
                         ("image", "CLOUD", "<"),
                         ("inventory", "exists", None),
                         ("metric", "CLOUD", None),
                         ("register", "CLOUD", None),
                         ("security_group", "CLOUD", "<"),
                         ]
        allok = True
        for (command, valid, invalid) in help_commands:
            r = Shell.cm("help " + command)
            testing = True
            if valid is not None:
                testing = valid in r
            if invalid is not None:
                testing = testing and invalid not in r
            if testing:
                msg = "pass"
            else:
                msg = "fail"
            print("TESTING help", command, msg)
            allok = allok and testing
        assert allok

    def test_list(self):
        print()
        a = self.grep_command("list", ["india"], None)

    def test_metrics(self):
        a = self.grep_command(
            "metric", ["eucalyptus", "openstack", "nimbus"], None)

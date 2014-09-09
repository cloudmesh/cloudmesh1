""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import sys

from sh import grep
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)


from cloudmesh.config.cm_keys import cm_keys
from cloudmesh_common.util import HEADING
from cloudmesh_install.util import path_expand

from cloudmesh_install import config_file

class Test_cloudmesh:

    # filename = None
    # filename = "credentials-example-keys.yaml"
    filename = config_file("/cloudmesh.yaml")

    def setup(self):
        self.keys = cm_keys(self.filename)

    def tearDown(self):
        pass


    def test00_file(self):
        HEADING()
        try:
            self.keys = cm_keys("wrong file")
        except:
            pass


    def test01_print(self):
        HEADING()
        print self.keys
        pass

    def test02_names(self):
        HEADING()
        print self.keys.names()

        names = []
        lines = grep("ssh-", path_expand(self.filename))
        for line in lines:
            (name, rest) = line.strip().split(":")
            if name not in self.keys.names():
                print "Key", name, "not found"
                assert false
                return
            else:
                names.append(name)
        print "keys found", names
        assert len(names) == len(self.keys.names())

    def test03_default(self):
        HEADING()
        print self.keys.default()

    def test04_getvalue(self):
        HEADING()
        for key in self.keys.names():
            print self.keys._getvalue(key)

    def test05_set(self):
        HEADING()
        first_key = self.keys.names()[0]
        self.keys.setdefault(first_key)
        print self.keys.default()

    def test06_get(self):
        HEADING()
        first_key = self.keys.names()[0]
        print self.keys[first_key]

    def test07_get(self):
        HEADING()
        print self.keys["default"]

    def test08_set(self):
        HEADING()

        print self.keys["keys"]

        self.keys["gregor"] = "~/.ssh/id_rsa.pub"
        self.keys["hello"] = "~/.ssh/id_rsa"

        print self.keys["keys"]

        self.keys["default"] = "hello"
        print self.keys["keys"]

        # assert (self.keys._getvalue("default") == "hello") and
        # (self.keys._getvalue("gregor") == "world")

    def test09_type(self):
        HEADING()
        print "Find key type of gregor:", self.keys.type("gregor")
        for name in self.keys.names():
            print name
            value = self.keys[name]
            print self.keys.type(name), name, value

        assert True
        # assert (self.keys.type("gregor") == "file")

    def test10_fingerprint(self):
        HEADING()
        for name in self.keys.names():
            print self.keys.fingerprint(name)

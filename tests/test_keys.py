""" run with

nosetests -v --nocapture tests/test_keys.py

or

nosetests -v tests/test_keys.py

"""
from __future__ import print_function
import os
from cloudmesh.config.cm_keys import cm_keys_yaml, keytype
from cloudmesh_common.util import HEADING
from cloudmesh.util.keys import get_fingerprint
from cloudmesh_install import config_file


class Test_cloudmesh:

    # filename = None
    # filename = "credentials-example-keys.yaml"
    filename = config_file("/cloudmesh.yaml")

    def __init__(self):
        self.key_store = cm_keys_yaml(self.filename)
        self.username = os.environ['USER']
        self.mykey = "{0}-key".format(self.username)

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test00_file(self):
        HEADING()
        try:
            self.key_store = cm_keys_yaml("wrong file")
        except:
            pass
        assert True

    def test01_print(self):
        HEADING()
        print(self.key_store)
        assert True

    def test02_names(self):
        HEADING()
        names = self.key_store.names()
        print(names)
        assert len(names) > 0

    def test03_default(self):
        HEADING()
        print(self.key_store.default())
        assert True

    def test04_getvalue(self):
        HEADING()
        for key in self.key_store.names():
            print(self.key_store._getvalue(key))
        assert True

    def test05_set(self):
        HEADING()
        first_key = self.key_store.names()[0]
        self.key_store.setdefault(first_key)
        print(self.key_store.default())
        assert True

    def test06_get(self):
        HEADING()
        first_key = self.key_store.names()[0]
        print(self.key_store[first_key])
        assert True

    def test07_get(self):
        HEADING()
        print(self.key_store["default"])
        assert True

    def test08_set(self):
        HEADING()

        print(self.key_store["keys"])
        print(self.key_store["default"])

        assert type(self.key_store["keys"]) == dict

    def test09_type(self):
        HEADING()
        print("Find key type of {0}:".format(self.mykey), keytype(self.mykey))
        for name in self.key_store.names():
            print(name)
            value = self.key_store[name]
            print(keytype(name), name, value)

        assert True
        # assert (keytype(self.mykey) == "file")

    def test10_fingerprint(self):
        HEADING()
        for name in self.key_store.names():
            key = self.key_store[name]
            print(name, key)
            print(get_fingerprint(key))
        assert True

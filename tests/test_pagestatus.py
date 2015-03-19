""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import sys

import json
import pprint
pp = pprint.PrettyPrinter(indent=4)


from cloudmesh.config.cm_keys import cm_keys
from cloudmesh_base.util import HEADING
from cloudmesh_base.util import path_expand


class Test_cloudmesh:

    def setup(self):
        config = cm_config_pagestatus()
        self.db = cm_mongo_pagestatus()
        self.db.kill()

    def tearDown(self):
        # TODO decide teardown
        db.kill()

    def test_add(self):
        HEADING()
        self.db.add('gregor', '/hello', 'VMs', '100')
        self.db.add('gregor', '/hello', 'images', '99')

        vms = self.db.get('gregor', '/hello', 'VMs')
        images = self.db.get('gregor', '/hello', 'images')
        assert vms == 100
        assert images == 99

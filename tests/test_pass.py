""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.config.cm_config import cm_config
from cloudmesh.config.ConfigDict import ConfigDict

import json
import os
import warnings
from pprint import pprint

from cloudmesh_base.util import HEADING
from cloudmesh_install.util import path_expand
from cloudmesh_install import config_file


class Test_pass:

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_dummy(self):
        HEADING()
        assert True

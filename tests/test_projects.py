""" run with

nosetests -v --nocapture

or

nosetests -v

"""
from __future__ import print_function
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

from cloudmesh.config.cm_projects import cm_projects
from cloudmesh_base.util import HEADING
from cloudmesh_install import config_file


class Test_cloudmesh:

    # filename = None
    # filename = "credentials-example-keys.yaml"
    # filename = config_file("/cloudmesh-new.yaml")
    filename = config_file("/cloudmesh.yaml")

    def setup(self):
        self.projects = cm_projects(self.filename)

    def tearDown(self):
        pass

    def test00_wrong_file(self):
        HEADING()
        try:
            self.projects = cm_projects("wrong file")
        except:
            pass

    def test01_print(self):
        HEADING()
        print(self.projects)
        pass

    def test02_dump(self):
        HEADING()
        print(self.projects.dump())
        pass

    def test03_active(self):
        HEADING()
        print(self.projects.names("active"))
        pass

    def test04_default(self):
        HEADING()
        print(self.projects.names("default"))
        pass

    def test05_default(self):
        HEADING()
        print(self.projects.names("completed"))
        pass

    def test06_wrong_status(self):
        HEADING()
        try:
            print(self.projects.names("wrong"))
        except Exception, e:
            print(e)
            pass

    def test07_add(self):
        HEADING()
        print(self.projects.add("gregor"))
        print(self.projects.dump())
        pass

    def test07_delete(self):
        HEADING()
        print(self.projects.add("gregor"))
        print(self.projects.dump())
        print(self.projects.delete("gregor"))
        print(self.projects.dump())
        pass

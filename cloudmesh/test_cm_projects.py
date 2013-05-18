""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import sys
#sys.path.insert(0, '..')

from cm_projects import cm_projects
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

header = True

def HEADING(txt):
    if header:
        print
        print "#", 70 * '#'
        print "#", txt
        print "#", 70 * '#'

class Test_cloudmesh:

    #filename = None
    #filename = "credentials-example-keys.yaml"
    filename = "$HOME/.futuregrid/cloudmesh-new.yaml"


    def setup(self):
        self.projects = cm_projects(self.filename)

    def tearDown(self):
        pass

    def test00_file(self):
        HEADING("00 FILE")
        try:
            self.projects = cm_projects("wrong file")
        except:
            pass
            

    def test01_print(self):
        HEADING("01 PRINT")
        print self.projects
        pass

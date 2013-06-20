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
    #filename = "$HOME/.futuregrid/cloudmesh-new.yaml"
    filename = "$HOME/.futuregrid/cloudmesh.yaml"


    def setup(self):
        self.projects = cm_projects(self.filename)

    def tearDown(self):
        pass

    def test00_wrong_file(self):
        HEADING("00 WRONG FILE")
        try:
            self.projects = cm_projects("wrong file")
        except:
            pass
            

    def test01_print(self):
        HEADING("01 PRINT")
        print self.projects
        pass

    def test02_dump(self):
        HEADING("02 DUMP")
        print self.projects.dump()
        pass

    def test03_active(self):
        HEADING("03 ACTIVE")
        print self.projects.names("active")
        pass

    def test04_default(self):
        HEADING("04 DEFAULT")
        print self.projects.names("default")
        pass

    def test05_default(self):
        HEADING("05 COMPLETED")
        print self.projects.names("completed")
        pass


    def test06_wrong_status(self):
        HEADING("06 WRONG STATUS")
        try:
            print self.projects.names("wrong")
        except Exception, e:
            print e
            pass

    def test07_add(self):
        HEADING("05 ADD")
        print self.projects.add("gregor")
        print self.projects.dump()
        pass

    def test07_delete(self):
        HEADING("05 DELETTE")
        print self.projects.add("gregor")
        print self.projects.dump()
        print self.projects.delete("gregor")
        print self.projects.dump()
        pass

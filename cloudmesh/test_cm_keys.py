""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import sys
#sys.path.insert(0, '..')

from cm_keys import cm_keys
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


    filename = "credentials-example.yaml"
    #filename = None

    def setup(self):
        self.keys = cm_keys()

    def tearDown(self):
        pass

    def test01_print(self):
        #print self.keys
        pass
    
    def test01_names(self):
        HEADING("NAMES")
        print self.keys.names()
        
    def test02_default(self):
        HEADING("DEFAULT")
        print self.keys.default()

    def test03_getvalue(self):
        HEADING("GET VALUE")
        print self.keys._getvalue("gregor")
        print self.keys._getvalue("default")
        print self.keys._getvalue("keys")

    def test03_set(self):
        HEADING("SET DEFAULT")
        self.keys.setdefault("gregor")
        print self.keys.default()

    def test04_get(self):
        HEADING("GET GREGOR")
        print self.keys["gregor"]

    def test05_get(self):
        HEADING("GET")
        print self.keys["default"]
        print self.keys["gregor"]
        
    def test06_set(self):
        HEADING("SET HELLO WORLD")
        print self.keys["keys"]
        
        self.keys["default"] = "hello"
        self.keys["gregor"] = "world"

        print self.keys["keys"]
        
        assert (self.keys._getvalue("default") == "hello") and (self.keys._getvalue("gregor") == "world")

    def test07_type(self):
        HEADING("TYPE")
        print "LLL", self.keys.type("gregor") 
        for name in self.keys.names():
            print name
            value =  self.keys[name]
            print self.keys.type(name), name, value
            
        assert (self.keys.type("gregor") == "file")

    def test08_fingerprint(self):
        HEADING("FINGERPRINT")
        print "LLL", self.keys.fingerprint("gregor")
        print "LLL", self.keys.fingerprint("default") 


    

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

    #filename = None
    #filename = "credentials-example-keys.yaml"
    filename = "$HOME/.futuregrid/cloudmesh-new.yaml"


    def setup(self):
        self.keys = cm_keys(self.filename)

    def tearDown(self):
        pass

    def test00_file(self):
        HEADING("00 FILE")
        try:
            self.keys = cm_keys("wrong file")
        except:
            pass
            

    def test01_print(self):
        HEADING("01 PRINT")
        print self.keys
        pass
    
    def test02_names(self):
        HEADING("02 NAMES")
        print self.keys.names()
        
    def test03_default(self):
        HEADING("03 DEFAULT")
        print self.keys.default()

    def test04_getvalue(self):
        HEADING("04 GET VALUE")
        print self.keys._getvalue("gregor")
        print self.keys._getvalue("default")
        print self.keys._getvalue("keys")

    def test05_set(self):
        HEADING("05 SET DEFAULT")
        self.keys.setdefault("gregor")
        print self.keys.default()

    def test06_get(self):
        HEADING("06 GET GREGOR")
        print self.keys["gregor"]

    def test07_get(self):
        HEADING("07 GET")
        print self.keys["default"]
        print self.keys["gregor"]

    def test06_set(self):
        HEADING("06 SET HELLO WORLD")

        print self.keys["keys"]

        self.keys["gregor"] = "~/.ssh/id_rsa.pub"
        self.keys["hello"] = "~/.ssh/id_rsa"
        
        print self.keys["keys"]

        self.keys["default"] = "hello"
        print self.keys["keys"]
                
        #assert (self.keys._getvalue("default") == "hello") and (self.keys._getvalue("gregor") == "world")

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
        print self.keys.fingerprint("gregor")
        print self.keys.fingerprint("default") 




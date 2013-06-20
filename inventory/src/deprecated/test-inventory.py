""" run with

nosetests -v --nocapture

or

nosetests -v

"""
import sys
sys.path.insert(0, '..')

from Inventory import Inventory
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

class Test_Inventory:

    #filename = "$HOME/.futuregrid/cloudmesh-new.yaml"

    def setup(self):
        self.inventory = Inventory()

    def tearDown(self):
        self.inventory.disconnect()

    def test00_disconnect(self):
        HEADING("00 DISCONNECT")
        pass


    def test01_file(self):
        HEADING("01 FILE")
        self.inventory.load("example.json")

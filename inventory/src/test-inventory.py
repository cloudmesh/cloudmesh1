""" run with

nosetests -v --nocapture --nologcapture

or

nosetests -v

"""
import sys
sys.path.insert(0, '..')
from datetime import datetime
from pprint import pprint

from Inventory import Inventory
from Inventory import FabricService
from Inventory import FabricServer
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
        self.inventory = Inventory("nosetest")

    def tearDown(self):
        pass
        #self.inventory.disconnect()

    def test00_disconnect(self):
        HEADING("00 DISCONNECT")
        print "NOT YET IMPLEMENTED"

    def test01_clean(self):
        HEADING("test01_clean")
        self.inventory.clean()

    def test02_add_Service(self):
        HEADING("test02_add_Service")
        now =  datetime.now()
        service = FabricService(
            name='Euca',
            date_start=now,
            date_update=now,
            date_stop=now
            )
        self.inventory.save(service)

    def test03_add_Server(self):
        HEADING("test03_add_Server")
        now =  datetime.now()
        service = FabricService(
            name='OpenStack',
            date_start=now,
            date_update=now,
            date_stop=now
            )
        self.inventory.save(service)

        server = FabricServer(
            name='Hallo4',
            date_start=now,
            date_update=now,
            date_stop=now,
            services = [service]
            )

        self.inventory.save(server)

    def test05_create(self):
        HEADING("test05_create")
        self.inventory.create("server","dynamic", "india[9-11].futuregrid.org,india[01-02].futuregrid.org")
        print self.inventory.pprint()
        assert self.inventory.exists("server", "india01.futuregrid.org") 

    def test06_loop_print(self):
        HEADING("test06_loop_print")
        for server in self.inventory.servers:
            print server.data

    def test07_exists(self):
        HEADING("test07_exists")
        assert self.inventory.exists("server", "india01.futuregrid.org") == True

    def test08_print(self):
        HEADING("test08_print")
        self.inventory.pprint()    

    def test09_count(self):
        HEADING("test09_count")
        print self.inventory.servers.count(), self.inventory.services.count()
        assert (self.inventory.servers.count() == 6) and (self.inventory.services.count() == 2)


    def test10_set(self):
        HEADING("test10_set")
        self.inventory.clean()
        self.inventory.create(
            "server",
            "dynamic",
            "india01.futuregrid.org")
        
        print self.inventory.pprint()
        print self.inventory.exists("server", "india01.futuregrid.org")
            

        self.inventory.set_service(
            "india01-opensatck",
            "india01.futuregrid.org",
            "openstack")

        self.inventory.pprint()

    def test11_add(self):
        HEADING("test11_add")
        self.inventory.clean()
        self.inventory.create(
            "server",
            "dynamic",
            "india01.futuregrid.org")
        
        print self.inventory.pprint()
        print self.inventory.exists("server", "india01.futuregrid.org")
            

        self.inventory.add_service(
            "india01-opensatck",
            "india01.futuregrid.org",
            "openstack")

        self.inventory.pprint()

    def test12_logging(self):
        self.test11_add()
        HEADING("test12_logging")
        s = self.inventory.get("server","india01.futuregrid.org")[0]
        print s.data
        s.stop()
        s.start()
        s.start()

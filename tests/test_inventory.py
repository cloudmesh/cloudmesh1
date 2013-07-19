""" run with

nosetests -v --nocapture --nologcapture
nosetests -v  --nocapture test_inventory.py:Test_Inventory.test_06
nosetests -v

"""
from datetime import datetime

from cloudmesh.inventory.inventory import Inventory
from cloudmesh.inventory.inventory import FabricService
from cloudmesh.inventory.inventory import FabricServer
import json
from  pprint import pprint

from cloudmesh.util.util import HEADING
import time

class Test_Inventory:

    # filename = "$HOME/.futuregrid/cloudmesh-new.yaml"

    def setup(self):
        self.inventory = Inventory("nosetest")
        self.inventory.clean()
        
    def tearDown(self):
        self.inventory.print_info()
        # self.inventory.disconnect()

    def test_clean(self):
        HEADING("test01_clean")
        self.inventory.clean()
        self.inventory.print_info()
        assert (
            len(self.inventory.servers) + 
            len(self.inventory.clusters) + 
            len(self.inventory.images) + 
            len(self.inventory.services) == 0)
        
    def test_cluster(self):
        HEADING("CREATE CLUSTER")
        self.inventory.create_cluster("bravo", "b-[001-016]", "101.102.203.[11-26]", "b[001]")
        self.inventory.print_info()
        self.inventory.refresh()
        assert len(self.inventory.servers) == 16 and len(self.inventory.clusters) == 1        
    def test_server(self):
        HEADING("TEST_SERVERS")
        self.inventory.create("server","i[001-003]")
        self.inventory.refresh()
        assert len(self.inventory.servers) == 3 and len(self.inventory.clusters) == 0     

    def test_service(self):
        HEADING("TEST_SERVICES")
        self.inventory.create("service","service-i[001-003]")
        self.inventory.refresh()
        assert len(self.inventory.services) == 3 and len(self.inventory.clusters) == 0    

    def test_image(self):
        HEADING("TEST_image")
        self.inventory.create("image","image[001-003]")
        self.inventory.refresh()
        assert len(self.inventory.images) == 3 and len(self.inventory.clusters) == 0    

    def test_info(self):
        HEADING("TEST_INFO")
        self.inventory.print_info()
        
    def test00_disconnect(self):
        HEADING("00 DISCONNECT")
        print "NOT YET IMPLEMENTED"
        
    def test_euca_service(self):
        HEADING("test02_add_Service")
        now = datetime.now()
        service = FabricService(
            name='Euca',
            date_start=now,
            date_update=now,
            date_stop=now
        )
        pprint (service.__dict__)
        service.save(cascade=True)
        self.inventory.refresh()
        assert (self.inventory.services[0].name == 'Euca')

    def test_date(self):
        HEADING("test03_add_Server")
        now = datetime.now()
        service = FabricService(
            name='OpenStack',
            date_start=now,
            date_update=now,
            date_stop=now
        )
        service.save()
        self.inventory.refresh()
        pprint(service.__dict__)
        print "name     :", self.inventory.services[0].name
        print "now      :", now
        print "date_start:", self.inventory.services[0].date_start
        print "date_update:", self.inventory.services[0].date_update
        print "date_stop:", self.inventory.services[0].date_stop
        print ("WARNING: there is a rounding error wen reading the values. therfore"
                 "ignore the last three digits of the date")
        assert (str(self.inventory.services[0].date_stop)[:-3] == str(now)[:-3])


    def test_add(self):
        HEADING("test_add")
        self.inventory.clean()

        self.inventory.create("server","i001")
        self.inventory.create("service","service-i001")


        service = self.inventory.get("service","service-i001")
        service.save(cascade=True)

        server = self.inventory.get("server", "i001")
        server.save(cascade=True)
        
        pprint(server.__dict__)
        pprint(service.__dict__)

        server.services = [service]
        server.save(cascade=True)
        
        pprint(server.__dict__)
        self.inventory.refresh()
        assert (self.inventory.servers[0].services[0].name == "service-i001")

    def test_append(self):
        HEADING("test_add")
        self.inventory.clean()

        self.inventory.create("service","service-i001")
        self.inventory.create("server","i001")

        service = self.inventory.get("service","service-i001")
        service.save(cascade=True)

        server = self.inventory.get("server", "i001")
        server.save(cascade=True)
        
        pprint(server.__dict__)
        pprint(service.__dict__)

        server.append(service)
        server.save(cascade=True)
        
        pprint(server.__dict__)
        self.inventory.refresh()
        assert (self.inventory.servers[0].services[0].name == "service-i001")


    def test_logging(self):
        HEADING("TEST_LOGGING")

        self.inventory.create("server","i001")
        server = self.inventory.get("server", "i001")
        server.save(cascade=True)

        pprint (server.__dict__)
        server.stop()
        server.start()
        server.start()
        server.stop()
        server.save(cascade=True)
        
        pprint (server.__dict__)

        assert(server.date_stop is not None)

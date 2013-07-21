""" run with

nosetests -v --nocapture --nologcapture
nosetests -v  --nocapture test_inventory.py:Test_Inventory.test_06
nosetests -v

"""
from datetime import datetime

from cloudmesh.inventory.inventory import Inventory
from cloudmesh.inventory.inventory import FabricService
from cloudmesh.inventory.inventory import FabricServer
from cloudmesh.inventory.inventory import FabricImage
import json
from  pprint import pprint

from cloudmesh.util.util import HEADING
import time
import sys


class Test_Inventory:

    # filename = "$HOME/.futuregrid/cloudmesh-new.yaml"

    def setup_fg(self):

        inventory = Inventory("nosetest")
        inventory.clean()

        inventory.create_cluster("bravo", "b-[001-016]", "101.102.203.[11-26]", "b[001]")
        inventory.create_cluster("delta", "d-[001-016]", "102.202.204.[1-16]", "d-[001]")
        inventory.create_cluster("gamma", "g-[001-016]", "302.202.204.[1-16]", "g-[001]")
        inventory.create_cluster("india", "i-[001-128]", "402.202.204.[1-128]", "i-[001]")
        inventory.create_cluster("sierra", "s-[001-128]", "502.202.204.[1-128]", "s-[001]")

        centos = FabricImage(
            name="centos6",
            osimage='/path/to/centos0602v1-2013-06-11.squashfs',
            os='centos6',
            extension='squashfs',
            partition_scheme='mbr',
            method='put',
            kernel='vmlinuz-2.6.32-279.19.1.el6.x86_64',
            ramdisk='initramfs-2.6.32-279.19.1.el6.x86_64.img',
            grub='grub',
            rootpass='reset'
        ).save()

        redhat = FabricImage(
            name="ubuntu",
            osimage='/BTsync/ubuntu1304/ubuntu1304v1-2013-06-11.squashfs',
            os='ubuntu',
            extension='squashfs',
            partition_scheme='mbr',
            method='btsync',
            kernel='vmlinuz-2.6.32-279.19.1.el6.x86_64',
            ramdisk='initramfs-2.6.32-279.19.1.el6.x86_64.img',
            grub='grub2',
            rootpass='reset'
        ).save()

        inventory.print_info()

    def setup(self):
        self.inventory = Inventory("nosetest")
        self.inventory.clean()
        
    def tearDown(self):
        self.inventory.print_info()
        # self.inventory.disconnect()

    def test_clean(self):
        HEADING()
        self.inventory.clean()
        self.inventory.print_info()
        assert (
            len(self.inventory.servers) + 
            len(self.inventory.clusters) + 
            len(self.inventory.images) + 
            len(self.inventory.services) == 0)

    def test_names(self):
        HEADING()
        self.setup_fg()
        names = self.inventory.names("cluster")
        print names
        assert [u'bravo', u'delta', u'gamma', u'india', u'sierra'] == names
        
    def test_cluster(self):
        HEADING()
        self.inventory.create_cluster("bravo", "b-[001-016]", "101.102.203.[11-26]", "b[001]")
        self.inventory.print_info()
        self.inventory.refresh()
        assert len(self.inventory.servers) == 16
        assert len(self.inventory.clusters) == 1 
               
    def test_server(self):
        HEADING()
        self.inventory.create("server","i[001-003]")
        self.inventory.refresh()
        assert len(self.inventory.servers) == 3 
        assert len(self.inventory.clusters) == 0     

    def test_service(self):
        HEADING()
        self.inventory.create("service","service-i[001-003]")
        self.inventory.refresh()
        assert len(self.inventory.services) == 3 
        assert len(self.inventory.clusters) == 0    

    def test_image(self):
        HEADING()
        self.inventory.create("image","image[001-003]")
        self.inventory.refresh()
        assert len(self.inventory.images) == 3 
        assert len(self.inventory.clusters) == 0    

    def test_info(self):
        HEADING()
        self.inventory.print_info()
        
    def test_euca_service(self):
        HEADING()
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
        HEADING()
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
        HEADING()
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
        HEADING()
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
        HEADING()

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

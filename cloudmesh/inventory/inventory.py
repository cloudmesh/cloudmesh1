import sys
from hostlist import expand_hostlist
from datetime import datetime
from mongoengine import *
from pprint import pprint
from cloudmesh.util.logger import LOGGER

log = LOGGER('inventory')

db = connect ("nosetest")


PROVISIONING_CHOICES = ('openstack',
                        'eucalyptus',
                        'hpc')

SERVICE_CHOICES = ('ganglia',
                   'nagios')

SERVER_CHOICES = ('dynamic', 'static')

class FabricObject(DynamicDocument):

    kind =  StringField(default="basic",required=True)
    name = StringField(required=True, unique=True)
    labels = ListField(StringField(),default=list)
    tags = ListField(StringField(),default=list)
    groups = ListField(StringField(),default=list)
    cluster =  StringField()
    
    date_start = DateTimeField()
    date_stop = DateTimeField()
    date_update = DateTimeField()

    date_creation = DateTimeField(default=datetime.now())
    date_modified = DateTimeField(default=datetime.now())

    uptime = LongField(default=0)

    
    def stamp(self):
        if not self.date_creation:
            self.date_creation = datetime.now()
        self.date_modified = datetime.now()


    def save(self, *args, **kwargs):
        self.stamp()
        return super(FabricObject, self).save(*args, **kwargs)
        
    def start(self):
        if self.status == "start":
            log.warning(
                "{0} is already started at {1}".format(self.name, self.date_start))
        else:
            self.status = "start"
            self.date_start = datetime.now()
            self.date_stop = None
            self.save(cascade=True)
            log.info("START: {0} {1}".format(self.name, self.date_start))

    def stop(self):
        if self.status == "stop":
            log.warning(
                "{0} is already started at {1}".format(self.name, self.date_start))
        elif self.status == "start":
            self.status = "stop"
            self.date_stop = datetime.now()
            log.info("STOP: {0} {1}".format(self.name, self.date_start))
            # calculate the time difference and add to uptime
            delta = self.date_stop - self.date_start
            self.uptime = self.uptime + delta.seconds
            self.date_start = None
            self.save(cascade=True)
        else:
            log.warning(
                "{0} is not running to be stopped {1}".format(self.name, self.date_start))

    meta = {
        'allow_inheritance': True
    }

    
    
class FabricService(FabricObject):
    kind = StringField(default="service")
    utility = StringField()
    
class FabricServer(FabricObject):
    kind = StringField(default="server")
    ip = StringField()
    provisioned = StringField(choices=PROVISIONING_CHOICES,default="hpc")
    services = ListField(ReferenceField(
        FabricService,
        reverse_delete_rule=CASCADE))

class FabricCluster(FabricObject):
    kind = StringField(default="server")
    servers = ListField(ReferenceField(
        FabricServer,
        reverse_delete_rule=CASCADE))

class Inventory:
    
    def __init__(self):
        self.clusters = []
        self.servers = []
        self.services = []
        pass

    def create_cluster(self, 
                       name, 
                       names,
                       ips,
                       management):
        name_list = expand_hostlist(names)
        ip_list = expand_hostlist(ips)
        management_list = expand_hostlist(management)
        server_list = zip(name_list, ip_list)
        servers = []
        for (server_name, server_ip) in server_list:
            server = FabricServer(name=server_name,
                                  cluster=name,
                                  ip=server_ip)
            if server_name in management_list:
                server.tags = ["manage"]
            else:
                server.tags = ["compute"]
            server.save(cascade=True)
            servers.append(server)
            
        cluster = FabricCluster(name=name)
        cluster.servers = servers
        cluster.save(cascade=True)
            
        pass

    def get (self,kind, name=None):
        if name is not None:
            if kind == "cluster":
                return FabricCluster.objects(name=name)[0]
            elif kind == "server":
                return FabricServer.objects(name=name)[0]
            elif kind == "service":
                return FabricService.objects(name=name)[0]
            else:
                log.error("ERROR")
                sys.exit()
        else:
            if kind == "cluster":
                return FabricCluster.objects
            elif kind == "server":
                return FabricServer.objects
            elif kind == "service":
                return FabricService.objects
            else:
                log.error("ERROR")
                sys.exit()

    def print_server (self, object=None, name=None):
        if name is not None:
            server = get("server",name)
        print server.name

            
    def print_cluster (self, name):
        cluster = self.get("cluster", name=name)
        print cluster.name, cluster.date_modified
        for server in cluster.servers:
            print "{0} {1}".format(server.name, "manage" in server.tags)

    def refresh(self):
        self.clusters = self.get("cluster")
        self.servers = self.get("server")
        self.services = self.get("service")

    def print_info(self):
        self.refresh()
        #print "%15s:" % "dbname", self.inventory_name
        print "%15s:" % "clusters", len(self.clusters), "->", ', '.join([c.name for c in self.clusters])
        print "%15s:" % "services", len(self.services)
        print "%15s:" % "servers", len(self.servers)
        #print "%15s:" % "images", len(self.images) , "->", ', '.join([c.name for c in self.inventory.images])
        print

#server = FabricServer(name="i")

#server.tags = ["hallo"]
#server.save()

#pprint (server.__dict__)

inventory = Inventory()

inventory.create_cluster(name="india", 
                         names="i[003-010]", 
                         ips="india[003-010].futuregrid.org", 
                         management="i[003,004]")

inventory.print_cluster ("india")
inventory.print_info()

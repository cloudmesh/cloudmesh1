import sys
from hostlist import expand_hostlist
from datetime import datetime
from mongoengine import *
from pprint import pprint
from cloudmesh.util.logger import LOGGER

log = LOGGER('inventory')

db = connect ("nosetest")

FABRIC_TYPES = ["cluster", "server", "service", "iamge"]

PROVISIONING_CHOICES = ('openstack',
                        'eucalyptus',
                        'hpc')

SERVICE_CHOICES = ('ganglia',
                   'nagios')

SERVER_CHOICES = ('dynamic', 'static')

class FabricObject(DynamicDocument):

    kind = StringField(default="basic", required=True)
    name = StringField(required=True, unique=True)
    labels = ListField(StringField(), default=list)
    tags = ListField(StringField(), default=list)
    groups = ListField(StringField(), default=list)
    cluster = StringField()
    status = StringField(default="defined")    
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

    
class FabricImage(FabricObject):
    kind = StringField(default="image")
    
class FabricService(FabricObject):
    kind = StringField(default="service")
    utility = StringField()
    
class FabricServer(FabricObject):
    kind = StringField(default="server")
    ip = StringField()
    provisioned = StringField(choices=PROVISIONING_CHOICES, default="hpc")
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
        self.images = []
        pass

    def set (self, elements, attribute, value, namespec=None):
        if namespec is None:
            for element in elements:
                element[attribute] = value
                element.save(cascade=True)
        else:
            name_list = expand_hostlist(namespec)
            for element in elements:
                if element.name in name_list:
                    element[attribute] = value
                    element.save(cascade=True)

    
    def create (self, kind, namespec):
        elements = []
        names = expand_hostlist(namespec)
        for name in names:
            if kind == "server":
                element = FabricServer(name=name, kind=kind)
            elif kind == "service":
                element = FabricService(name=name, kind=kind)
                log.info("creating {0} {1} {2}".format(name, kind))
            elif kind == "cluster":
                element = FabricCluster(name=name, kind=kind)
                log.info("creating {0} {1} {2}".format(name, kind))
            else:
                log.error(
                    "kind is not defined, creation of objects failed, kind, nameregex")
                return
            element.save(cascade=True)
            elements.append(object)
        return elements
    
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

    def get (self, kind, name=None):
        if name is not None:
            if kind == "cluster":
                return FabricCluster.objects(name=name)[0]
            elif kind == "server":
                return FabricServer.objects(name=name)[0]
            elif kind == "service":
                return FabricService.objects(name=name)[0]
            elif kind == "images":
                return FabricImage.objects(name=name)[0]
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
            elif kind == "images":
                return FabricImage.objects
            else:
                log.error("ERROR")
                sys.exit()


            
    def print_cluster (self, name):
        self.refresh()
        cluster = self.get("cluster", name=name)
        print "%15s:" % "cluster", name
        print "%15s:" % "modified", cluster.date_modified
        #        print "%15s:" % "dbname", self.inventory_name
        print "%15s:" % "cluster", name
        print

        for s in self.servers:
            if "manage" in s.tags:
                c = "m"
            elif "compute" in s.tags:
                c = "c"
            else:
                c = " "

            line = " ".join(["%15s:" % s.name, "%-8s" % s.status, "%-15s" % s.ip, c, ""])
            service_line = ', '.join([str(service.subkind) for service in s["services"]])
            service_line = service_line.replace("openstack", "o")
            line += service_line
            print line
        print

        print "%15s:" % "Legend"
        print "%15s =" % "M", "Management"
        print "%15s =" % "S", "Server"
        print "%15s =" % "o", "OpenStack"
        print "%15s =" % "e", "OpenStack"
        print "%15s =" % "h", "HPC"

    def print_kind (self, kind, name=None):
        if kind in FABRIC_TYPES or name is not None:
            element = self.get(kind, name)   
            for key in element:
                print "%15s =" % key, element[key]
            
    def refresh(self, kind=None):
        if kind in FABRIC_TYPES or kind is None:
            if kind == "cluster" or kind is None:
                self.clusters = self.get("cluster")

            if kind == "server" or kind is None:
                self.servers = self.get("server")

            if kind == "service" or kind is None:
                self.servces = self.get("service")

        else:
            log.error("ERROR: can not find kind: '{0}'".format(kind))
            sys.exit()


    def print_info(self):
        self.refresh()
        # print "%15s:" % "dbname", self.inventory_name
        print "%15s:" % "clusters", len(self.clusters), "->", ', '.join([c.name for c in self.clusters])
        print "%15s:" % "services", len(self.services)
        print "%15s:" % "servers", len(self.servers)
        print "%15s:" % "images", len(self.images) , "->", ', '.join([c.name for c in self.images])
        print

def main():
    # server = FabricServer(name="i")

    # server.tags = ["hallo"]
    # server.save()

    # pprint (server.__dict__)

    inventory = Inventory()

    inventory.create_cluster(name="india",
                             names="i[003-010]",
                             ips="india[003-010].futuregrid.org",
                             management="i[003,004]")

    servers = FabricServer.objects
    inventory.set(servers, "status", "running", "i[003-010]")
    inventory.set(servers, "status", "done", "i[005-007]")

    inventory.print_cluster ("india")


    inventory.print_info()

if __name__ == "__main__":
    main()

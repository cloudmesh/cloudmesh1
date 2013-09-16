import sys
import random
from hostlist import expand_hostlist
from datetime import datetime
from mongoengine import *
from pprint import pprint
from cloudmesh.util.logger import LOGGER
from cloudmesh.util.util import check_file_for_tabs
from cloudmesh.util.util import path_expand
from cloudmesh.util.config import read_yaml_config


log = LOGGER(__file__)

inventory_config_filename = "~/.futuregrid/cloudmesh-db.yaml"



FABRIC_TYPES = ["cluster", "server", "service", "iamge"]
"""The types a fabric server can have"""

PROVISIONING_CHOICES = ['openstack',
                        'eucalyptus',
                        'hpc']
"""the provisioning choices for a fabric server"""

SERVICE_CHOICES = ('ganglia',
                   'nagios')
"""the service choices for a service"""

SERVER_CHOICES = ('dynamic', 'static')
"""the server choices we have"""

class FabricObject(DynamicDocument):
    '''
    the base class that can be inherited to define a fabric object. this object
    shoul dnot be directly used, but only inherited from.
    '''

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
        '''
        an internal method to provide a time stap for a global modification data
        in inventory. Calling of the inventory or any other save will create a
        new time stamp
        '''
        if not self.date_creation:
            self.date_creation = datetime.now()
        self.date_modified = datetime.now()


    def save(self, *args, **kwargs):
        '''
        saves the inventory objects
        '''
        self.stamp()
        return super(FabricObject, self).save(*args, **kwargs)

    def start(self):
        '''
        cecods the starting time
        '''
        if self.status == "start":
            log.warning(
                "{0} is already started at {1}".format(self.name, self.date_start))
        else:
            self.status = "start"
            self.date_start = datetime.now()
            self.date_stop = None
            self.stamp()
            self.save(cascade=True)
            log.info("START: {0} {1}".format(self.name, self.date_start))

    def stop(self):
        '''
        records the stop time
        '''
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
            self.stamp()
            self.save(cascade=True)
        else:
            log.warning(
                "{0} is not running to be stopped {1}".format(self.name, self.date_start))

    meta = {
        'allow_inheritance': True
    }


class FabricImage(FabricObject):
    '''
    an object to hold fabric images and their metadata for image provisioning
    '''
    kind = StringField(default="image")

class FabricService(FabricObject):
    '''
    an object to hold fabric services and their meta data
    '''
    kind = StringField(default="service")
    utility = StringField()

class FabricServer(FabricObject):
    '''
    an object to hold fabric servers and their meta data
    '''
    kind = StringField(default="server")
    ip = StringField()
    provisioned = StringField(choices=PROVISIONING_CHOICES, default="hpc")
    services = ListField(ReferenceField(
        FabricService,
        reverse_delete_rule=CASCADE))

    def append(self, service):
        self.services.append(service)

    def set(self, services):
        self.services = services

    @property
    def load_vms(self):
        ''' Simulated load on the server '''
        return map(lambda r: random.random() * 24, range(0, 25))

    @property
    def load_users(self):
        ''' Simulated load on the server '''
        return map(lambda r: random.random() * 10, range(0, 25))


class FabricCluster(FabricObject):
    '''
    an object to hold fabric clusters and their meta data
    '''
    definition = StringField(default=None)
    kind = StringField(default="cluster")
    provision_choices = ListField(StringField(), default=PROVISIONING_CHOICES)

    servers = ListField(ReferenceField(
        FabricServer,
        reverse_delete_rule=CASCADE))
    images = ListField(ReferenceField(
        FabricImage,
        reverse_delete_rule=CASCADE))

class Inventory:
    '''
    holds a simple <ory of a data center
    '''

    def clean(self):
        """removes all services and servers"""
        for kind in self.fabrictype("all").keys():
            log.info("Deleting all {0}".format(kind))
            data = self.fabrictype(kind)
            for element in data:
                element.delete()

    def stamp(self):
        '''
        an internal method to provide a time stap for a global modification data
        in inventory. Calling of the inventory or any other save will create a
        new time stamp
        '''
        self.date_modified = datetime.now()

    def clean(self):
        '''
        cleans the database. 
        '''
        name = self.configuration['dbname']
        print name
        self.db.drop_database(name)

        # database = FabricCluster._get_db()
        # pprint (database.__dict__)
        # name = FabricCluster._get_collection_name()
        # print "NAME", name
        # database.drop_collection(name)

    def config(self, filename=None):
        '''
        reads from the specified yaml file the server configuration
        :param filename: name of the yaml file
        '''
        self.configuration = read_yaml_config(inventory_config_filename, check=False)
        if self.configuration is None:
           self.configuration = {'dbname': "inventory"}

    def __init__(self, filename=None):
        '''
        initializes the inventory
        '''
        self.date_creation = datetime.now()
        self.config(filename)

        #
        # TODO: need to pass host, port and other stuff from config file dict to this
        #
        self.db = connect (self.configuration['dbname'])

        self.clusters = []
        self.servers = []
        self.services = []
        self.images = []
        self.stamp()
        pass

    def set (self, elements, attribute, value, namespec=None):
        '''
        sets an attribute of one or multiple matching objects defined by namespec to value.
        
        :param elements: a list of fabric objects
        :param attribute: the attribute to be changed
        :param value: the value to set the attribute to
        :param namespec: the matching condition for the name of the object. 'i[001-003]'. matches the objects with names i001, i002, i003
        '''
        if namespec is None:
            for element in elements:
                element[attribute] = value
                self.stamp()
                element.save(cascade=True)
        else:
            name_list = expand_hostlist(namespec)
            for element in elements:
                if element.name in name_list:
                    element[attribute] = value
                    self.stamp()
                    element.save(cascade=True)


    def create (self, kind, namespec):
        '''
        creates fabric objects of the specified kind and matching the name specification
        :param kind: the kind . see FABRIC_TYPES
        :param namespec: the specifacation for a name list. 'i[001-003]'. creates the objects with names i001, i002, i003
        '''
        elements = []
        names = expand_hostlist(namespec)
        for name in names:
            if kind == "server":
                element = FabricServer(name=name, kind=kind)
            elif kind == "service":
                element = FabricService(name=name, kind=kind)
                log.info("creating {0} {1}".format(name, kind))
            elif kind == "cluster":
                element = FabricCluster(name=name, kind=kind)
                log.info("creating {0} {1}".format(name, kind))
            elif kind == "image":
                element = FabricImage(name=name, kind=kind)
                log.info("creating {0} {1}".format(name, kind))
            else:
                log.error(
                    "kind is not defined, creation of objects failed, kind, nameregex")
                return
            self.stamp()
            element.save(cascade=True)
            elements.append(object)
        return elements

    def create_cluster(self,
                       name,
                       names,
                       ips,
                       management):
        '''
        creates a cluster with the given name specification ip specifications, and the identification of management node.
        
        :param name: name of the cluster
        :param names: the names of the cluster servers. 'i[001-003]'. creates the objects with names i001, i002, i003
        :param ips: the names of the ips for the servers. 'i[001-003].futuregrid.org' creates the ips for the previously defined names
        :param management: the names of the management nodes. 'i[001-002]' sets the nodes i001 and i002 to management nodes. The rest will be set to compute nodes automatically.
        '''

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
            self.stamp()
            server.save(cascade=True)
            servers.append(server)
        cluster = FabricCluster(name=name,
                                cluster=name,
                                definition=names)
        cluster.servers = servers
        self.stamp()
        cluster.save(cascade=True)

        pass

    def get (self, kind, name=None):
        '''
        returns the object with the specified kind and name
        
        :param kind: the kind . see FABRIC_TYPES
        :param name: the name of the object
        '''
        if name is not None:
            if kind == "cluster":
                return FabricCluster.objects(name=name)[0]
            elif kind == "server":
                return FabricServer.objects(name=name)[0]
            elif kind == "service":
                return FabricService.objects(name=name)[0]
            elif kind == "images":
                print "PASSED", name
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

    def names (self, kind):
        '''
        returns the names of object with the specified kind and name
        '''
        elements = self.get(kind=kind)
        names = [element.name for element in elements]
        return names

    def print_cluster (self, name):
        '''
        print some elementary, but not all information of the cluster.
        
        :param name: name of the cluster
        '''
        self.refresh()
        cluster = self.get("cluster", name=name)
        print "%15s:" % "cluster", name
        print "%15s:" % "modified", cluster.date_modified
        #        print "%15s:" % "dbname", self.inventory_name
        print "%15s:" % "cluster", name
        print "%15s:" % "images", cluster.images
        print

        for s in cluster.servers:
            if "manage" in s.tags:
                c = "m"
            elif "compute" in s.tags:
                c = "c"
            else:
                c = " "

            line = " ".join(["%15s:" % s.name, "%-8s" % s.status, "%-15s" % s.ip, c, s.provisioned , ""])
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
        '''
        prints the attributes contained in the object with the given type.
        
        :param kind: the kind of the fabric object
        :param name: the name of the fabric object
        '''
        if kind in FABRIC_TYPES or name is not None:
            element = self.get(kind, name)
            for key in element:
                print "%15s =" % key, element[key]

    def refresh(self, kind=None):
        '''
        the inventory object contains a number of lists to conveniently access all fabric objects by kind. After refresh you can access them through 
        
           inventory = Inventory()
           inventory.refresh()
           
           inventory.servers
           inventory.services
           inventory.clusters
           inventory.images
           
        :param kind:
        '''
        if kind in FABRIC_TYPES or kind is None:
            if kind == "cluster" or kind is None:
                self.clusters = self.get("cluster")

            if kind == "server" or kind is None:
                self.servers = self.get("server")

            if kind == "service" or kind is None:
                self.services = self.get("service")

            if kind == "images" or kind is None:
                self.images = self.get("images")

        else:
            log.error("ERROR: can not find kind: '{0}'".format(kind))
            sys.exit()


    def print_info(self):
        '''
        print some elementary overview information 
        '''
        self.refresh()
        # print "%15s:" % "dbname", self.inventory_name
        print "%15s:" % "clusters", len(self.clusters), "->", ', '.join([c.name for c in self.clusters])
        print "%15s:" % "services", len(self.services)
        print "%15s:" % "servers", len(self.servers)
        print "%15s:" % "images", len(self.images) , "->", ', '.join([c.name for c in self.images])
        print

def main():
    # this example will not work if you have not done a python setup.py install
    # server = FabricServer(name="i")

    # server.tags = ["hallo"]
    # server.save()

    # pprint (server.__dict__)

    inventory = Inventory()

    inventory.create_cluster(name="xindia",
                             names="xi[003-010]",
                             ips="india[003-010].futuregrid.org",
                             management="xi[003,004]")

    servers = FabricServer.objects
    inventory.set(servers, "status", "running", "xi[003-010]")
    inventory.set(servers, "status", "done", "xi[005-007]")

    inventory.print_cluster ("india")


    inventory.print_info()

if __name__ == "__main__":
    main()

# pip install python-hostlist


# mongo>     db.getSiblingDB("admin").runCommand({getCmdLineOpts:1})
# finds path of db

from cloudmesh.util.logger import LOGGER
from datetime import datetime
from hostlist import expand_hostlist
from mongoengine import *
from pprint import pprint
import os
import random
import sys
import time
import yaml

#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)

#

SERVICE_CHOICES = ('openstack',
                   'eucalyptus',
                   'hpc')
     #              'ganglia',
     #              'nagios')

SERVER_CHOICES = ('dynamic', 'static')


class FabricObject(DynamicDocument):

    name = StringField(required=True, unique=True)
    kind = StringField()  # server, service
    cluster = StringField()
    bad = StringField(default="badme")
    subkind = StringField()
                          # server: dynamic, service: openstack, eucalyptus,
                          # hpc
    label = StringField()
    hallo = StringField(required=True)
    status = StringField(default=None)

    
    metadata = ListField(StringField(),default=list)
    group = ListField(StringField(),default=list)
    tags = ListField(StringField(),default=list)

    date_start = DateTimeField()
    date_stop = DateTimeField()
    date_update = DateTimeField()

    date_creation = DateTimeField(default=datetime.now())
    date_modified = DateTimeField(default=datetime.now())

    uptime = LongField(default=0)

    meta = {
        'allow_inheritance': True
    }

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

    def save(self, *args, **kwargs):
        if not self.date_creation:
            self.date_creation = datetime.now()
        self.date_modified = datetime.now()
        return super(FabricObject, self).save(*args, **kwargs)
        # do i need a return?

    @property
    def data(self):
        return self.__dict__["_data"]

    def pprint(self):
        pprint(self.__dict__)

    def set_category(self, which):
        self.category = which
        self.save()
    
class FabricService(FabricObject):
    ip_address = StringField()
    kind = StringField(efault="service")
    subkind = StringField(choices=SERVICE_CHOICES)


class FabricServer(FabricObject):
    ip_address = StringField()
    kind = StringField(default="server")
    subkind = StringField(choices=SERVER_CHOICES, default='static')
    services = ListField(ReferenceField(
        FabricService,
        reverse_delete_rule=CASCADE))
    # the list of pointers to the services hosted on this server

    @property
    def load(self):
        ''' Simulated load on the server '''
        return map(lambda r: random.random() * 10, range(0, 9))


class FabricCluster(FabricObject):
    servers = ListField(ReferenceField(
        FabricServer,
        reverse_delete_rule=CASCADE
    ))
    service_choices = ListField(StringField())


class FabricImage(FabricObject):

    """
    osimage: '/path/to/centos0602v1-2013-06-11.squashfs'
    os: 'centos6'
    extension: 'squashfs'

    partition_scheme: 'mbr'
    method: 'put'
    kernel: 'vmlinuz-2.6.32-279.19.1.el6.x86_64'

    ramdisk: 'initramfs-2.6.32-279.19.1.el6.x86_64.img'
    grub: 'grub'
    rootpass: 'reset'
    """
    kind = StringField(default="image")
    osimage = StringField()
    os = StringField()
    extension = StringField()
    partition_scheme = StringField(default='mbr')
    method = StringField(default='put')
    kernel = StringField()
    ramdisk = StringField()
    grub = StringField(default='grub')
    rootpass = StringField()


class Inventory:

    configuration = {}
    
    def config(self, filename):
        '''
        Reads in a configuration file of the form and eliminates all keys with the None value.
        
        {'inventory': 
          {'name': 'inventory',
           'host': None,
           'port': None,
           'user': None,
           'pass': None,
          } 
        }
        
        Will return 
        
        {'inventory': {'name': 'inventory'}}
        
        :param filename:
        '''
        self.filename = filename
        if os.path.exists(filename):
            f = open(self.filename, "r")
            self.configuration = yaml.safe_load(f)
            f.close()
        # elininate all None attributes
        d = dict((k, v) for (k, v) in self.configuration['inventory'].iteritems() if not v == 'None')
        self.configuration['inventory'] = d
    
    def __init__(self,
                 dbname,
                 host=None,
                 port=None,
                 username=None,
                 password=None):

        self.configuration = {}
        if host:
            self.configuration['host'] = host
        if port:
            self.configuration['port'] = port
        if username:
            self.configuration['username'] = username
        if password:
            self.configuration['password'] = password

        self.db = connect(dbname, **self.configuration)
        return

    def clean(self):
        """removes all services and servers"""
        for kind in self.fabrictype("all").keys():
            log.info("Deleting all {0}".format(kind))
            data = self.fabrictype(kind)
            for element in data:
                element.delete()

    def create_cluster(self, clustername, nameregex, nameformat, startindex, managementnodes, prefix):
        # "delta", "102.202.204.[1-16]", "d-{0:03d}", [1,2], "d"
        # Simulate the Delta cluster
        # Simulate the Delta cluster
        hostnames = self.ip_dict(nameregex, nameformat, startindex)
        for name in hostnames:
            print name
            ip = hostnames[name]
            log.info("create {0} {1}".format(name, ip))
            self.create("server", "dynamic", name)
            self.add_service('%s-openstack' % name, name, 'openstack')
            server = self.find("server", name)
            server.ip_address = ip
            # server['ip_address'] = ip
            server.save()

        self.create("cluster", "dynamic", clustername)
        cluster = self.find("cluster", clustername)
        # cluster.management_node = self.find("server", managementnode)
        # cluster.compute_nodes = filter(
        #    lambda s: s.name[:1] == prefix and s.name != managementnode, self.servers())
        # cluster.service_choices = ('hpc', 'openstack', 'eucalyptus')
        # cluster.()

    def create(self, kind, subkind, nameregex):
        # "india[9-11].futuregrid.org,india[01-02].futuregrid.org"
        names = expand_hostlist(nameregex)
        for name in names:
            if kind == "server":
                object = FabricServer(
                    name=name,
                    kind=kind,
                    subkind=subkind,
                )
            elif kind == "service":
                object = FabricService(
                    name=name,
                    kind=kind,
                    subkind=subkind)
                log.info("creating {0} {1} {2}".format(name, kind, subkind))
            elif kind == "cluster":
                object = FabricCluster(
                    name=name,
                    kind=kind,
                    subkind=subkind)
                log.info("creating {0} {1} {2}".format(name, kind, subkind))
            else:
                log.error(
                    "kind is not defined, creation of objects failed, kind, nameregex")
                return
            object.save(cascade=True)

    def save(self, object=None):
        """saves either a server or service object."""
        if object is not None:
            object.save(cascade=True)
        else:
            for service in self.services:
                self.save(service)
            for server in self.servers:
                self.save(server)

    def pprint(self):
        print "Clusters"
        print 70 * '-'
        for service in self.clusters:
            pprint(service.__dict__)
        print "Servers"
        print 70 * '-'
        for server in self.servers:
            pprint(server.__dict__)
        print
        print "Services"
        print 70 * '-'
        for service in self.services:
            pprint(service.__dict__)
        print "Images"
        print 70 * '-'
        for image in self.images:
            pprint(image.__dict__)

    @property
    def clusters(self):
        return FabricCluster.objects

    @property
    def images(self):
        return FabricImage.objects

    @property
    def servers(self):
        return FabricServer.objects

    @property
    def services(self):
        return FabricService.objects

    def get_one(self, kind, name):
        '''returns the data associated with the object of type kind
        and the given name'''
        s = self.get(kind, name)
        try:
            return s[0]
        except:
            return None

    def fabrictype(self, kind):
        types = {
            'server': self.servers,
            'service': self.services,
            'cluster': self.clusters,
            'image': self.images,
        }
        if kind == "all":
            return types
        if kind in types:
            return types[kind]
        else:
            log.error("Type {0} is not supported".format(type))
            return None

    def get(self, kind, name):
        '''returns the data associated with the object of kind type
        and the given name'''
        s = self.fabrictype(kind)(name=name)
        return s

    def find(self, kind, name):
        s = self.fabrictype(kind)(name=name)[0]
        return s

    def add_category(self, type, name, category):
        '''sets the service of a server'''
        s = self.find(type, name)
        print s.name
        c = s.category
        s.save()
        
    def set_service(self, name, server_name, subkind):
        '''sets the service of a server'''
        s = self.find('server', server_name)
        try:
            service = self.find('service', server_name)
            service.subkind = subkind
        except:
            now = datetime.now()
            service = FabricService(
                name=name,
                subkind=subkind,
                date_start=now,
                date_update=now,
                date_stop=now,
                status="BUILD"
            )
        service.save()
        s.services = [service]
        s.save()

    def add_service(self, name, server, subkind):
        '''sets the service of a server'''
        s = self.servers(name=server)[0]
        try:
            service = self.services(name=server)[0]
            service.subkind = subkind
        except:
            now = datetime.now()
            service = FabricService(
                name=name,
                subkind=subkind,
                date_start=now,
                date_update=now,
                date_stop=now,
                status="BUILD"
            )
        service.save()
        s.services.append(service)
        s.save()

    def exists(self, kind, name):
        '''returns tro if the object of type kind and the given name
        exists'''
        if kind == 'server':
            return self.servers(name=name).count() > 0
        elif kind == 'service':
            return self.services(name=name).count() > 0
        else:
            log.error('wrong kind ' + kind)
        return

    def disconnect(self):
        log.warning("disconnect not yet implemented")

    # static methods

    def ip_name_pair(self, nameregex, format_string, start=1):
        ips = expand_hostlist(nameregex)
        i = start
        names = []
        for ip in ips:
            names.append(format_string.format(i))
            i += 1
        return zip(names, ips)

    def ip_name_dict(self, nameregex, format_string, start=1):
        pairs = self.ip_name_pair(nameregex, format_string, start)
        return [{'name': b, 'ip': a} for b, a in pairs]

    def ip_dict(self, nameregex, format_string, start=1):
        pairs = self.ip_name_pair(nameregex, format_string, start)
        return dict(pairs)

"""
    def dump (self, object):
        print '# ------------------'
        classname = object.__class__.__name__
        values = vars(object)['_data']
        if classname  == 'FabricServer':
           #print each server
            attributes = vars(FabricServer())['_data'].keys()
        elif classname == 'FabricServices':
           #print each service
            attributes = vars(FabricService())['_data'].keys()
        else:
            error ('wrong kind: ' + classname)
            return
        pprint(values)
"""


def main():

    inventory = Inventory('test4')

    inventory.clean()

    now = datetime.now()
    service = FabricService(
        name='india0',
        date_start=now,
        date_update=now,
        date_stop=now
    )

    inventory.save(service)

    server = FabricServer(
        name='india0',
        date_start=now,
        date_update=now,
        date_stop=now,
        services=[service]
    )

    inventory.save(server)
    inventory.pprint()

    x = inventory.get('server', name='india0')[0]
    x.pprint()

    print server.services[0].data

    # server.start()
    # time.sleep(2)
    # server.stop()
    inventory.create(
        "server", "india[9-11].futuregrid.org,india[01-02].futuregrid.org")

    inventory.pprint()

    print "################"
    server = inventory.get_one("server", "india01.futuregrid.org")

    print server.data

    print "################"

    for server in inventory.servers:
        print server.data

    print "################"
    print inventory.exists("server", "india01.futuregrid.org")

    """
        inventory.update("server", "Hallo2")

        server =  inventory.get('server','Hallo2')

        print '##############################'

        inventory.dump(server)
    """

if __name__ == "__main__":
     # main()

     # print ip_name_pair("india[20-25]", "i-", "0000", 1)
     pass

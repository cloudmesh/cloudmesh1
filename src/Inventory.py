# pip install python-hostlist

import logging
from hostlist import expand_hostlist
import time
import sys
from mongoengine import *                           
from datetime import datetime
from pprint import pprint

######################################################################
# SETTING UP A LOGGER
######################################################################

log = logging.getLogger('inventory')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('CM Inventory: [%(levelname)s] %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)

######################################################################

SERVICE_CHOICES = ('openstack',
                   'eucalyptus',
                   'hpc',
                   'ganglia',
                   'nagios')

SERVER_CHOICES = ('dynamic','static')

class FabricObject(Document):
    meta = {
         'allow_inheritance': True
         }
     
    metadata = StringField()
    name = StringField()
    kind = StringField()  # server, service
    subkind = StringField() # server: provisionable, service: openstack, eucalyptus, hpc
    label = StringField()
    status = StringField()
    
    date_start = DateTimeField()
    date_stop = DateTimeField()
    date_update = DateTimeField()

    date_creation = DateTimeField(default=datetime.now())
    date_modified = DateTimeField(default=datetime.now())

    uptime = LongField(default=0)

    def start(self):
        if self.status == "start":
            log.warning("{0} is already started at {1}".format(self.name, self.date_start))
        else:
            self.status = "start"
            self.date_start = datetime.now()
            self.date_stop = None
            self.save(cascade=True)
            log.info("START: {0} {1}".format(self.name, self.date_start))

    def stop(self):
        if self.status == "stop":
            log.warning("{0} is already started at {1}".format(self.name, self.date_start))
        elif self.status == "start":
            self.status = "stop"
            self.date_stop = datetime.now()
            log.info("STOP: {0} {1}".format(self.name, self.date_start))
            # calculate the time difference and add to uptime
            delta =  self.date_stop - self.date_start
            self.uptime = self.uptime + delta.seconds
            self.date_start = None
            self.save(cascade=True)
        else:
            log.warning("{0} is not running to be stopped {1}".format(self.name, self.date_start))

        
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
        pprint (self.__dict__)


class FabricService(FabricObject):              
    ip_address = StringField()
    kind = StringField(default="service")
    subkind = StringField(choices=SERVICE_CHOICES)
    
class FabricServer(FabricObject):              
    ip_address = StringField()
    kind = StringField(default="server")
    subkind = StringField(choices=SERVER_CHOICES, default='static')
    
    services = ListField(ReferenceField(
        FabricService,
        reverse_delete_rule=CASCADE))
    # the list of pointers to the services hosted on this server

class Inventory:

    def __init__ (self,
                  dbname,
                  host=None,
                  port=None,
                  username=None,
                  password=None):

        connectArgs = {}
        if host:
            connectArgs['host'] = host
        if port:
            connectArgs['port'] = port
        if username:
            connectArgs['username'] = username
        if password:
            connectArgs['password'] = password
        
        self.db = connect(dbname, **connectArgs)
        return

    def clean(self):
        """removes all services and servers"""
        for server in self.servers:
            print server.delete()

        for service in self.services:
            print service.delete()

    def create(self, kind, subkind, nameregex):
        #"india[9-11].futuregrid.org,india[01-02].futuregrid.org"
        names = expand_hostlist(nameregex)
        for name in names:
            if kind == "server":
                object = FabricServer(
                    name=name,
                    kind=kind,
                    subkind=subkind)
            elif kind == "service":
                object = FabricService(
                    name=name,
                    kind=kind,
                    subkind=subkind)
                log.info("creating {0} {1} {2}".format(name, kind, subkind))
            else:
                log.error("kind is not defined, creation of objects failed, kind, nameregex")
                return
            object.save(cascade=True)

    def save(self, object=None):
        """saves either a server or service object."""
        if object != None:
            object.save(cascade=True)
        else:
            for service in self.services:
                self.save(service)
            for server in self.servers:
                self.save(server)

            
    def pprint(self):
        print "Servers"
        print 70 * '-'
        for server in self.servers:
            pprint(server.__dict__)
        print
        print "Services"
        print 70 * '-'
        for service in self.services:
            pprint(service.__dict__)

    @property
    def servers(self):
        return FabricServer.objects

    @property
    def services(self):
        return FabricService.objects

    def get_one (self, kind, name):

        '''returns the data associated with the object of type kind
        and the given name'''

        if kind == 'server':
            s = self.servers(name=name)
            return s[0]
        elif kind =='service':
            s = self.services(name=name)
            return s[0]
        else:
            error('wrong kind ' + kind)
        return 

    def get (self, kind, name):
        '''returns the data associated with the object of kind type
        and the given name'''

        if kind == 'server':
            s = self.servers(name=name)
            return s
        elif kind =='service':
            s = self.services(name=name)
            return s
        else:
            error('wrong type ' + kind)
        return 

    def set_service (self, name, server, subkind):
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
        s.services = [service]
        s.save()

    def add_service (self, name, server, subkind):
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


    def exists (self, kind, name):
        '''returns tro if the object of type kind and the given name
        exists'''
        if kind == 'server':
            return self.servers(name=name).count() > 0
        elif kind =='service':
            return self.services(name=name).count() > 0
        else:
            error('wrong kind ' + kind)
        return
    

    
    
    def disconnect(self):
        log.warning("disconnect not yet implemented")


    def ip_name_pair (self, nameregex, format_string, start=1):
        ips = expand_hostlist(nameregex)
        i = start
        names = []
        for ip in ips:
             names.append(format_string.format(i))
             i +=  1 
        return zip(names, ips)

    def ip_name_dict (self, nameregex, format_string, start=1):
        pairs = self.ip_name_pair (nameregex, format_string, start)
        return [{'name':b, 'ip':a} for b,a in pairs]

    def ip_dict (self, nameregex, format_string, start=1):
        pairs = self.ip_name_pair (nameregex, format_string, start)
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

    now =  datetime.now()
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
        services = [service]
        )

    inventory.save(server)
    inventory.pprint()

    x = inventory.get('server', name='india0')[0]
    x.pprint ()

    print server.services[0].data


    #server.start()
    #time.sleep(2)
    #server.stop()
    


    inventory.create("server","india[9-11].futuregrid.org,india[01-02].futuregrid.org")
        
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
     #main()

    print ip_name_pair ("india[20-25]", "i-", "0000", 1)






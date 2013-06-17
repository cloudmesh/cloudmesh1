# pip install python-hostlist

from hostlist import expand_hostlist
import time
import sys
from mongoengine import *                           # To define a schema for a
from datetime import datetime
from pprint import pprint

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
            print "WARNING:", self.name, "is already started at", self.date_start
        else:
            self.status = "start"
            self.date_start = datetime.now()
            self.date_stop = None
            self.save()
            print "START:", self.name, self.date_start

    def stop(self):
        if self.status == "stop":
            print "WARNING:", self.name, "is already stopped at", self.date_start
        elif self.status == "start":
            self.status = "stop"
            self.date_stop = datetime.now()
            print "STOP:", self.name, self.date_start
            # calculate the time difference and add to uptime
            delta =  self.date_stop - self.date_start
            self.uptime = self.uptime + delta.seconds
            self.date_start = None
            self.save()
        else:
            print "WARNING:", self.name, "is not running to be stopped", self.date_start
        
    def save(self, *args, **kwargs):
        if not self.date_creation:
            self.date_creation = datetime.now()
        self.date_modified = datetime.now()
        return super(FabricObject, self).save(*args, **kwargs)

    @property
    def data(self):
        return self.__dict__["_data"]

    def pprint(self):
        pprint (self.__dict__)


class FabricService(FabricObject):              
    ip_address = StringField()
    kind = StringField(default="service")
    
class FabricServer(FabricObject):              
    ip_address = StringField()
    kind = StringField(default="server")

    services = ListField(ReferenceField(FabricService))  # the uniqe names of the services hosted on this server

def error(self,msg):
    print msg

class Inventory:

    def __init__ (self,dbname):
        self.db = connect (dbname)
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
        print names
        for name in names:
            if kind == "server":
                object = FabricServer(name=name, kind=kind, subkind=subkind)
            elif kind == "service":
                object = FabricService(name=name, kind=kind, subkind=subkind)
                print "creating", name, kind, subkind
            else:
                print "ERROR: kind is not defined, creation of objects failed, kind, nameregex"
                return
            object.save()

    def save(self, object):
        """saves either a server or service object."""
        object.save()
        
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
        print "\n>",name
        print "1>", server
        print "2>", subkind
        s = self.servers(name=server)[0]
        try:
            service = self.services(name=server)[0]
            service.subkind = subkind
        except:
            now = datetime.now()
            service = FabricService(
                name=server,
                subkind=subkind,
                date_start=now,
                date_update=now,
                date_stop=now,
                status="BUILD"
                )
        service.save()
        if len(s.data['services']) > 0:
            s.data['services'][0] = service
        else:
            s.data['services'].append(service)
        self.save(s)
        print "OOOO"
        pprint(s.data)
        pprint(s.data['services'][0].data)

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
        print "disconnect not yet implemented"

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
        name='Euca',
        date_start=now,
        date_update=now,
        date_stop=now
    )

    inventory.save(service)
    
    server = FabricServer(
        name='Hallo4',
        date_start=now,
        date_update=now,
        date_stop=now,
        services = [service]
        )

    inventory.save(server)

        

    #server.start()
    #time.sleep(2)
    #server.stop()
    
    inventory.pprint()    

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
    main()





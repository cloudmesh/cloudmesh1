from mongoengine import *                           # To define a schema for a
from datetime import datetime
import pprint


class FabricServer(Document):              
    ip_address = StringField()
    name = StringField(required=True)   # , unique=True)
    kind = ListField(StringField())
    label = ListField(StringField())
    keyword = ListField(StringField())
    time_start = DateTimeField()
    time_stop = DateTimeField()
    time_update = DateTimeField()
    services = ListField(StringField())  # the uniqe names of the services hosted on this server

class FabricService(Document):              
    ip_address = StringField()
    name = StringField(required=True)    # , unique=True)
    kind = ListField(StringField())
    label = ListField(StringField())
    keyword = ListField(StringField())
    time_start = DateTimeField()
    time_stop = DateTimeField()
    time_update = DateTimeField()

def error(self,msg):
    print msg

class Inventory:

    def __init__ (self,dbname):
        connect (dbname)
        return

    def add (self, kind, name, data):
        '''Adds the data defined in the dict data to the object with the defined name. kind is either server or service'''
        return

    def get (self, kind, name):
        '''returns the data associated with the object of type kind and the given name'''
        if kind == 'server':
            s = FabricServer.objects(name=name)
            return s[0]
        elif kind =='service':
            s = FabricService.objects(name=name)
            return s[0]
        else:
            error('wrong kind ' + kind)
        return 

    def exists (self, kind, name):
        '''returns tro if the object of type kind and the given name exists'''
        if kind == 'server':
            return FabricServer.objects(name__exists=name)
        elif kind =='service':
            return FabricService.objects(name__exists=name)
        else:
            error('wrong kind ' + kind)
        return 

    def list (self, kind):
        '''list all object of a specific kind'''
        return

    def listServices (self, name):
        '''list sthe services of a named server'''
        if kind == 'server':
            servers = FabricServer.objects()
            # dump
        elif kind =='service':
            services = FabricService.objects()
            # print
        else:
            error('wrong kind ' + kind)
        return 

    def updateTime (self, name):
        '''updates the time of the last update to now'''
        return

    def dump (self, kind, object):
        print '# ------------------'
        if kind == 'server':
           #print each server
            attributes = vars(FabricServer())['_data'].keys()
            values = vars(object)['_data']
            pprint.pprint(values)
        elif kind == 'services':
           #print each service
            attributes = vars(FabricService())['_data'].keys()
            values = vars(object)['_data']
            pprint.pprint(values)
        else:
            error ('wrong kind')
        return

    def delete(self):
        '''Deletes the current inventory'''
        return
    
    def remove (self, kind, name):
        '''removes the object with the type kind and name from the inventory'''
        return

    def update (self, kind, name, date):
        '''updates the information of the object with the specified data'''
        return

now =  datetime.now()

connect('test1')

server = FabricServer(name='Hallo2', time_start=now,time_update=now,time_stop=now)
server.save()



inventory  = Inventory('test1')

for server in FabricServer.objects:
    inventory.dump ('server',server)


server =  inventory.get('server','Hallo2')

print '##############################'
inventory.dump ('server',server)




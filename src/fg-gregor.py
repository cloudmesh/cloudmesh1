from mongoengine import *                           # To define a schema for a
from datetime import datetime

now =  datetime.now()

class CloudServer(Document):              
    ip_address = StringField()
    name = StringField(required=True)     # , unique=True)
    kind = ListField(StringField())
    label = ListField(StringField())
    keyword = ListField(StringField())
    uid = StringField()
    start_time = DateTimeField()
    stop_time = DateTimeField()


connect('test')

server = CloudServer(name='Hallo1', start_time=now)
server.save()

for server in CloudServer.objects:
    print server.name
    print server.start_time

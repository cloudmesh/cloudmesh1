from mongoengine import *
import datetime
import time
import hashlib
import uuid
from pprint import pprint
#    mongod --noauth --dbpath . --port 27777
from cloudmesh.management.cloudmeshobject import CloudmeshObject
import yaml

connect('cloudmesh', port=27777)

from cloudmesh.management.cloudmeshobject import CloudmeshObject


class Cache(CloudmeshObject):
    id = StringField(primary_key=True)
    value = DictField(required=True)
    cm_kind = "cache"
    start_time = StringField()
    end_time = StringField()


host = "india"
command = "qstat"
entry = Cache(id=host + "_" + command,
              value={"first": "hallo"})

entry.save()

results = Cache.objects()

for result in results:
    print 70 * '-'
    for attribute in result:
        print attribute, ":", result[attribute]

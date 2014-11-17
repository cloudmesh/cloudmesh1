from __future__ import print_function
from mongoengine import *
from cloudmesh.config.cm_config import get_mongo_db, DBConnFactory

get_mongo_db("experiment", DBConnFactory.TYPE_MONGOENGINE)

class ExperimentGroup(Document):
    name = StringField(required=True)
    userid = StringField(required=True)
    description = StringField(max_length=50)

class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)

class GroupItem(Document):
    group_name = ReferenceField(ExperimentGroup, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    meta = {'allow_inheritance': True}

class VM(GroupItem):
    vm_name = StringField()
    vm_id = StringField()
    vm_accessIPv4 = StringField()
    vm_accessIPv6 = StringField()
    vm_created = StringField()
    vm_flavor = StringField()
    vm_metadata = StringField()
    vm_status = StringField()

class IP(GroupItem):
    ip = StringField()
    ip_public = StringField()
    ip_private = StringField()

class VOLUME(GroupItem):
    volume_name = StringField()



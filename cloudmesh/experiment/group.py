from __future__ import print_function
from mongoengine import *
from cloudmesh.config.cm_config import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh_common.logger import LOGGER
from pprint import pprint

log = LOGGER(__file__)

# Anyone who imports this file will have db connection automatically
#get_mongo_db("experiment", DBConnFactory.TYPE_MONGOENGINE)

TYPES_OF_ITEMS_IN_GROUP = ['VM', 'VOLUME']
TYPES_IDENTITY_VALUE = {"VM": "vm_name",
                        "VOLUME": "volume_name"}

class ExperimentGroup(Document):
    name = StringField(required=True)
    userid = StringField(required=True)
    description = StringField(max_length=50)
    tags = ListField(StringField(max_length=30))
    dbname = get_mongo_dbname_from_collection("experiment")
    if dbname:
        meta = {'db_alias': dbname}

class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)
    dbname = get_mongo_dbname_from_collection("experiment")
    if dbname:
        meta = {'db_alias': dbname}
    
class GroupItem(Document):
    group = ReferenceField(ExperimentGroup, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    dbname = get_mongo_dbname_from_collection("experiment")
    if dbname:
        meta = {'allow_inheritance': True, 'db_alias': dbname}
    else:
        meta = {'allow_inheritance': True}
        
class VM(GroupItem):
    vm_name = StringField()
    vm_id = StringField()
    vm_accessIPv4 = StringField()
    vm_accessIPv6 = StringField()
    vm_created = StringField()
    vm_flavor = StringField()
    vm_metadata = DictField()
    vm_status = StringField()


class VOLUME(GroupItem):
    volume_name = StringField()


class GroupManagement(object):
    
    def __init__(self, username):
        self.username = username
        get_mongo_db("experiment", DBConnFactory.TYPE_MONGOENGINE)
        
    def check_type(self, _type):
        if _type.upper() not in TYPES_OF_ITEMS_IN_GROUP:
            raise Exception("item type '{0}' not acceptable, allowed item types in group are: {1}".format(
                                    _type, ", ".join(TYPES_OF_ITEMS_IN_GROUP)))
            
        
    def get_groups(self, groupname=None):
        if groupname:
            return ExperimentGroup.objects.get(userid__exact=self.username, name=groupname)
        else:
            return ExperimentGroup.objects(userid__exact=self.username)
           
    def get_groups_names_list(self):
        groups = self.get_groups()
        res = []
        for group in groups:
            res.append(group.name)
        return res
    
    def create_group(self, groupname):
        groups_names_list = self.get_groups_names_list()
        if groupname in groups_names_list:
            raise Exception("group name '{0}' is used".format(groupname))
        else:
            try:
                ExperimentGroup(name=groupname, userid=self.username).save()
            except:
                raise Exception("failed to create group")
            
    def delete_group(self, groupname):
        group = self.get_groups(groupname=groupname)
        group.delete()
            
    def update_vm_of_group(self, 
                           groupname,
                           vmname,
                           tags=None,
                           comments=None,
                           vm_name=None,
                           vm_id=None,
                           vm_accessIPv4=None,
                           vm_accessIPv6=None,
                           vm_created=None,
                           vm_flavor=None,
                           vm_metadata=None,
                           vm_status=None):
        raise Exception("NOT IMPLEMENTED")
       
        
    def get_item_of_group(self, groupname, _type, value):
        self.check_type(_type)
        group = self.get_groups(groupname=groupname)  
        v = TYPES_IDENTITY_VALUE[_type.upper()]
        temp = {"group": group,
                v: value}
        return globals()[_type.upper()].objects.get(**temp)
          
    
    def add_item_to_group(self, groupname, _type, value):
        self.check_type(_type)
        group = self.get_groups(groupname=groupname)
        
        # check item existence
        temp = None   
        try:
            self.get_item_of_group(groupname,_type,value)
        except Exception as ex:
            temp = type(ex).__name__
            if temp != "DoesNotExist":
                raise ex
        if temp == None:
            raise Exception("item '{0}' of type '{1}' exists in group '{2}'".format(
                                                value, _type, groupname))
        elif temp == "DoesNotExist":
            v = TYPES_IDENTITY_VALUE[_type.upper()]
            a = {"group": group,
                v: value}
            globals()[_type.upper()](**a).save()
            
    def delete_item_of_group(self, groupname, _type, value):
        item = self.get_item_of_group(groupname, _type, value)
        item.delete()
        
    def list_items_of_group(self, groupname, _type=None):
        '''
        returns a dict in which the key is the type and value is a list of items of this type
        if _type is not provided, will return all items in the group
        '''
        group = self.get_groups(groupname=groupname)  
        res = {}
        if _type:
            self.check_type(_type)
            query_res = globals()[_type.upper()].objects(group=group)
            res[_type.upper()] = []
        else:
            query_res = GroupItem.objects(group=group)
            
        for item in query_res:
            cls_name = type(item).__name__
            assert cls_name in TYPES_OF_ITEMS_IN_GROUP
            if cls_name not in res:
                res[cls_name] = []
            temp = getattr(item, TYPES_IDENTITY_VALUE[cls_name])
            res[cls_name].append(temp)
            
        return res
    
    def get_same_items_from_all_groups(self, _type, value):
        '''
        returns all items with same identity value and type from all groups
        '''
        self.check_type(_type)
        v = TYPES_IDENTITY_VALUE[_type.upper()]
        a = {v: value}
        return globals()[_type.upper()].objects(**a)
    

    def add_tag_to_group(self, groupname, tag):
        group = self.get_groups(groupname=groupname)
        tags = group.tags
        if tag not in tags:
            tags.append(tag)
            group.update(set__tags=tags)
          
            

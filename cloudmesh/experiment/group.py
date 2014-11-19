from __future__ import print_function
from mongoengine import *
from cloudmesh.config.cm_config import get_mongo_db, DBConnFactory
from cloudmesh_common.logger import LOGGER
from cloudmesh.cm_mongo import cm_mongo



log = LOGGER(__file__)

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



class GroupManagement(object):
    
    def __init__(self, username):
        self.username = username
        
    def get_groups(self, groupname=None):
        if groupname:
            return ExperimentGroup.objects(userid__exact=self.username, name=groupname)
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
            return False, "group name '{0}' is used".format(groupname)
        else:
            try:
                ExperimentGroup(name=groupname, userid=self.username).save()
            except:
                return False, "failed to create group"
            
    def delete_group(self, groupname):
        group = self.get_groups(groupname=groupname)
        if len(group) == 0:
            return False, "group '{0}' doesn't exist".format(groupname)
        else:
            try:
                group[0].delete()
            except:
                return False, "failed to delete group '{0}'".format(groupname)
            


# -----------------------------------------------------------------------------------------        
def get_group_names_list_by_vms_metadata(username, cloudname, refresh=False):
    '''
    loops through all VMs of a cloud of a user, returns a list of all unique group 
    names accorrding to the metadata
    '''
    mongo = cm_mongo()
    if refresh:
        mongo.activate(cm_user_id=username, names=[cloudname])
        mongo.refresh(cm_user_id=username,
                      names=[cloudname],
                      types=['servers'])
    servers_dict = mongo.servers(
                clouds=[cloudname], cm_user_id=username)[cloudname]
                
    res = []
    for k, v in servers_dict.iteritems():
        if 'cm_group' in v['metadata']:
            temp = v['metadata']['cm_group']
            if temp not in res:
                res.append(temp)
    
    return res
            
            
            
            
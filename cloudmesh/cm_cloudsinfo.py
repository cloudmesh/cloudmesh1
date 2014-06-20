from cloudmesh.config.cm_config import get_mongo_db, cm_config
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh_common.bootstrap_util import path_expand
import sys
from pprint import pprint


class cm_cloudsinfo:
    
    db_clouds = None
    
    def __init__(self):
        self.db_clouds = get_mongo_db("cloudmesh")
        
    def get_clouds(self):
        return self.db_clouds.find({'cm_kind': 'cloud'})
    
    def db_name_map(self, name):
        if name == "cloud":
            return "cm_cloud"
        elif name == "active":
            return "cm_active"
        elif name == "label":
            return "cm_label"
        elif name == "host":
            return "cm_host"
        elif name == "type/version":
            return "cm_type_version"
        elif name == "type":
            return "cm_type"
        elif name == "heading":
            return "cm_heading"
        elif name == "user":
            return "cm_user_id"
        elif name == "credentials":
            return "credentials"
        elif name == "defaults":
            return "default"
    
    
    def set_name(self, cloudname, newname):
        self.db_clouds.update({'cm_kind': 'cloud', 'cm_cloud': cloudname}, {'$set': {'cm_cloud': newname}})

    
    def get_one_cloud(self, cloudname):
        return self.db_clouds.find_one({'cm_kind': 'cloud', 'cm_cloud': cloudname})

    
    def activate(self, cloudname):
        self.db_clouds.update({'cm_kind': 'cloud', 'cm_cloud': cloudname}, {'$set': {'cm_active': True}})

    def deactivate(self, cloudname):
        self.db_clouds.update({'cm_kind': 'cloud', 'cm_cloud': cloudname}, {'$set': {'cm_active': False}})

    

    def add(self, d):
        if d['cm_type'] in ['openstack']:
            if d['credentials']['OS_USERNAME']:
                del d['credentials']['OS_USERNAME']
            if d['credentials']['OS_PASSWORD']:
                del d['credentials']['OS_PASSWORD']
            if d['credentials']['OS_TENANT_NAME']:
                del d['credentials']['OS_TENANT_NAME']
        elif d['cm_type'] in ['ec2', 'aws']:
            if d['credentials']['EC2_ACCESS_KEY']:
                del d['credentials']['EC2_ACCESS_KEY']
            if d['credentials']['EC2_SECRET_KEY']:
                del d['credentials']['EC2_SECRET_KEY']
        elif d['cm_type'] in ['azure']:
            if d['credentials']['subscriptionid']:
                del d['credentials']['subscriptionid']
        self.db_clouds.insert(d)


    def remove(self, cloudname):
        self.db_clouds.remove({'cm_kind': 'cloud', 'cm_cloud': cloudname})
        

 
    
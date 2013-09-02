from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.config.cm_config import cm_config
from cloudmesh.util.util import path_expand
from cloudmesh.config.cm_config import get_mongo_db

import yaml
class Roles:
    
    
    def get_config(self, **kwargs):
        
        if not kwargs.has_key('roles'):#if kwargs['host'] is None:
            self.roles = cm_config_server().get("roles")
    
     
    mongo_host = 'localhost'
    mongo_port = 27017
    mongo_db_name = "cloudmesh"
    mongo_collection = "cloudmesh"
    
    
    def __init__(self):

        collection = "user"  
        self.db_clouds = get_mongo_db(collection)        
        
        self.get_config()
        
        
    def _get_mongo(self):    

        result = self.db_clouds.find({})
        data = {}
        for entry in result:
            id = entry['cm_user_id']
            data[id] = entry
        
        print data
        
        
    def clear(self):
        self.roles = None
    
    def get_roles(self,user):
        pass
    
    def authorized(self,user,role):
        return False
 
    def users(self,role):
        single_users = self.roles[role]['users']
        projects = self.roles[role]['projects']
        result = self.db_clouds.find({'projects.active': { "$in": projects}})
        project_users = []
        for entry in result:
            project_users.append(entry['cm_user_id'])
        s = list(set(single_users + project_users))
        return s

    def get(self,user):
        user_roles = []
        for r in self.roles:
            print "checking", r
            us = self.users(r)
            print "     ", us
            if user in us:
                user_roles.append(r)
        return user_roles
    
    
    
    def __str__(self):
        return str(self.roles)
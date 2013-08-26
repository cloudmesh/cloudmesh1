from config.cm_config import cm_config_server, cm_config
from config.cm_config import  get_mongo_db


import json
from pprint import pprint

class cm_profile (object):
    
    server = None
    config = None
    
    data = None
    
    # initialization
    
    config = None
    
    
    def __init__(self, collection="profile"):
        
        self.data = {}
        self.server = cm_config_server()
        self.config = cm_config()

        self.db_clouds = get_mongo_db(collection)        
        self._get_usernames_from_config()   


    def _get_usernames_from_config(self):
        '''
        gets the various usernames from the clouds, as well as the portal and hpc from the yaml file
        '''
        cm = self.config.get()
        username = {}
        username ["hpc"] = cm["hpc"]["username"]
        username["portal"] = cm["profile"]["username"]  

        for name in cm["clouds"]:
            if cm["clouds"][name]["cm_type"] == "openstack":
               username[name] = cm["clouds"][name]["credentials"]["OS_USERNAME"]
        self.data["username"] = username


    # methods dependent on username 
    
    def _id(self, username):
        '''
        creates a unique name for the profile based on the unique username
        :param username:
        '''
        return "profile-{0}".format(username)
    
    def find_one(self, query):
        '''
        executed the find_one query on the database
        :param query: a regular query
        '''
        return self.db_collection.find_one(query) 
       
    def update(self, username, dict, cloud=None, page=None):
        """updates for the username the dict and if a page is given also includes the page"""
        self.write(username, dict, cloud, page, update=True)

    def save(self, username, dict, cloud=None, page=None):
        """saves for the username the dict and if a page is given also includes the page"""
        self.write(username, dict, cloud, page, update=False)
      
    def write(self, username, dict, cloud=None, page=None, update=False):
        """updates for the username the dict and if a page is given also includes the page. 
            if update is set to True, it jsut works as an update function, use the update method instead."""
        id = self._id(username)
        d = {}  
        if update:
            try:
                d = self.find_one({"cm_id": id})
            except:
                pass  # no element with cm_id
            
        d.update(dict)
        
        self.db_collection.remove({"cm_id": id}, safe=True)
        d.update({"cm_id": id,
                  "cm_username": username})

        if page is not None:
            d.update({"cm_page": page})

        if cloud is not None:
            d.update({"cm_cloud": cloud})

        self.db_collection.insert(d)

    def get(self, username, cloud=None, page=None):
        """returns the profile information for the user"""
        id = self._id(username)
        result = self.find_one({'cm_id' : id})    
        return result
    
    def __str__ (self):
        """prints some provile information for config and server"""
        return json.dumps(self.config, sort_keys=True, indent=4) + \
               json.dumps(self.server, sort_keys=True, indent=4) 
    
    

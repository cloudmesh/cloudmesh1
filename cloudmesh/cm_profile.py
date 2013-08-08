from config.cm_config import cm_config_server, cm_config

import json
from pymongo import MongoClient
from pprint import pprint

class cm_profile (object):
    
    server = None
    config = None
    
    data = None
    
    # initialization
    
    def __init__(self, collection="profile"):
        
        self.data = {}
        self.server = cm_config_server()
        self.config = cm_config()
        
        db_name = self.server.config["mongo"]["db"]
        self.client = MongoClient()    
        self.db = self.client[db_name]          
        self.db_collection = self.db[collection] 
        self._get_usernames_from_config()   


    def _get_usernames_from_config(self):
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
        return "profile-{0}".format(username)
    
    def find_one(self, query):
        return self.db_collection.find_one(query) 
       
    def update(self, username, dict, page=None):
        """updates for the username the dict and if a page is given also includes the page"""
        self.write(username, dict, page=None, update=True)

    def save(self, username, dict, page=None):
        """saves for the username the dict and if a page is given also includes the page"""
        self.write(username, dict, page=None, update=False)
      
    def write(self, username, dict, page=None, update=False):
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

        self.db_collection.insert(d)

    def get(self, username):
        """returns the profile information for the user"""
        id = self._id(username)
        result = self.find_one({'cm_id' : id})    
        return result
    
    def __str__ (self):
        """prints some provile information for config and server"""
        return json.dumps(self.config, sort_keys=True, indent=4) + \
               json.dumps(self.server, sort_keys=True, indent=4) 
    
    

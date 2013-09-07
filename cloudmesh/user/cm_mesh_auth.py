from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.config.cm_config import get_mongo_db
from cloudmesh.util.logger import LOGGER

from pymongo import MongoClient
import pprint

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)

class cm_userauth(object):
    
    def __init__(self):
        self.db_userauth = get_mongo_db("userauth")

    def get(self, username):
        return self.find_one({"cm_id": username, "cm_type": "userauth"})
    

    def set(self, username, d):
        element = dict (d)
        element["cm_id"] = username
        element["cm_type"] = "userauth"
        self.update({"cm_id": username, "cm_type": "userauth"}, element)
    
    
    def update(self, query, values=None):
        '''
        executes a query and updates the results from mongo db.
        :param query:
        '''
        if values is None:
            return self.db_userauth.update(query, upsert=True) 
        else:
            print query
            print values
            return self.db_userauth.update(query, values, upsert=True) 

    
    def insert(self, element):
        self.db_userauth.insert(element)

    def clear(self):
        self.db_userauth.remove({"cm_type" : "userauth"})
        
    def find(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_userauth.find(query) 
    
    def find_one(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_userauth.find_one(query) 
    


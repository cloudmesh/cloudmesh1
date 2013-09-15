from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.config.cm_config import get_mongo_db
from cloudmesh.util.logger import LOGGER


from pymongo import MongoClient
import pprint

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)

class cm_launcher_db(object):

    def __init__(self):
        self.cm_type = "launcher"
        self.db = get_mongo_db(self.cm_type)

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
            return self.db.update(query, upsert=True)
        else:
           # print "query: ",query
           # print "values: ",values
            return self.db.update(query, {"$set":values}, upsert=True)


    def insert(self, element):
        self.db.insert(element)

    def clear(self):
        self.db.drop()


    def find(self, query=None):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        if query == None:
            return self.db.find()
        return self.db.find(query)

    def find_one(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db.find_one(query)



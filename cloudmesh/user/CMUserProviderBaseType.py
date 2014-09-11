from cloudmesh.config.cm_config import cm_config_server, get_mongo_db
from cloudmesh_common.logger import LOGGER
import pymongo


# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)


class CMUserProviderBaseType(object):

    providers = {}

    client = None
    db_clouds = None

#    config = None

    def __init__(self, collection="user"):
        """initializes the cloudmesh mongo db. The name of the collection os passed."""
        self.db_clouds = get_mongo_db(collection)

    def find(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_clouds.find(query)

    def find_one(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_clouds.find_one(query)

    def add(self, id, dict):
        '''
        adds a user with the given id to the users database. The attributes are specified in the dict.

        :param id: the unique id of the user
        :param dict: the attributes of the user
        '''
        # print "IDIDID", id
        # print "DICTDICT", dict
        result = {}
        result['cm_user_id'] = id
        result.update(dict)
        self.db_clouds.insert(result)
        # result[element]['cm_user_id'] = id
        # self.db_clouds.insert(result[element])

    def updates(self, id, dict):
        '''
        updates the attributes specified in the dict for a given user with the id

        :param id: the unique id of the user
        :param dict: the attributes of the use
        '''
        # print "DICT in updates():", dict
        data = self.find_one({'cm_user_id': id})
        # print "EXISTING data in updates():", data
        if data is None:
            data = {}
            data.update(dict)
        # print "data after update in updates():", data
        self.remove(id)
        self.add(id, dict)

    def remove(self, id):
        '''
        removes the used with the given id

        :param id: the unique id of the user
        '''
        self.db_clouds.remove({"cm_user_id": id}, safe=True)

    def clear(self):
        '''
        empties th user database
        '''
        log.error("to be implemented")

    def refresh(self):
        '''
        refreshes the userdatabase from the user provider
        '''
        log.error("to be implemented")

    def register(self, name, type, params):
        '''
        registers a provider with som parameters specified in the dict params

        :param name: the name of the provider
        :param type: the type of the provider, overwrites a possibly given type in params
        :param params: a dictionary describing wht needs to be poassed to the service that provides user information
        '''
        log.error("to be implemented")

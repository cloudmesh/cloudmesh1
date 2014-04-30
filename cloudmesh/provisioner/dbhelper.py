from cloudmesh.config.cm_config import get_mongo_db
from cloudmesh.util.logger import LOGGER
#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)

class DBHelper:
    def __init__(self, coll_name="inventory"):
        self.coll_name = coll_name
        self.db_client = get_mongo_db(coll_name)
        
    def find(self, query_elem):
        """
        Thin Wrap of the mongo find command.
        return: {"result": True|False, "data": []} 
        result is False if error occured,
        result is True means query success. the "data" contains the query result. 
        empty "data" array means no document match the query
        """
        result = True
        data = None
        try:
            result_cursor = self.db_client.find(query_elem)
            if not result_cursor:
                result = False
            else:
                data = result_cursor[:]
        except:
            result = False
        return {"result": result, "data": data}
        
    def find_one(self, query_elem):
        result = True
        data = None
        try:
            data = self.db_client.find_one(query_elem)
        except:
            result = False
        return {"result": result, "data": data}
        
    def insert(self, elem):
        result = True
        data = None
        try:
            data = self.db_client.insert(elem)
        except:
            result = False
        return {"result": result, "data": data}
    
    def update(self, query_elem, update_elem, flag_upsert=True, flag_multi=True):
        result = True
        data = None
        try:
            data = self.db_client.update(query_elem, update_elem, 
                                         upsert=flag_upsert, multi=flag_multi)
        except:
            result = False
        return {"result": result, "data": data}
        
    def remove(self, query_elem, flag_multi=True):
        result = True
        data = None
        try:
            data = self.db_client.remove(query_elem, multi=flag_multi)
        except:
            result = False
        return {"result": result, "data": data}
        
    def atom_update(self, query_elem, update_elem, flag_upsert=True, flag_new=True):
        result = True
        data = None
        try:
            data = self.db_client.find_and_modify(query_elem,
                                                update=update_elem, upsert=flag_upsert, new=flag_new)
        except:
            result = False
        return {"result": result, "data": data}
        

from __future__ import print_function
from cloudmesh.config.cm_config import get_mongo_db
from cloudmesh_common.logger import LOGGER
from bson.objectid import ObjectId
#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)


class DBHelper:

    def __init__(self, coll_name="inventory"):
        """Construction
        :param string coll_name: the collection name
        """
        self.coll_name = coll_name
        self.db_client = get_mongo_db(coll_name)

    def find(self, query_elem):
        """
        Thin Wrap of the mongo find command.
        :param dict query_elem: the query dict, if you want to use "_id" in query_elem, you SHOULD call :py:func:`convert_str_to_objectid` to get the ObjectId for the "_id"
        :return: result is a dict with the formation {"result": True, "data": []} or {"result":False, "data":None}
        result is False if error occured,
        result is True means query success. the "data" contains the query result. empty "data" array means no document match the query
        If you want to use ObjectId attribute in data, you SHOULD call :py:func:`convert_objectid_to_str` to get a string of objectid.
        """
        result = True
        data = None
        try:
            result_cursor = self.db_client.find(query_elem)
            if not result_cursor:
                result = False
            else:
                data = list(result_cursor)
        except:
            result = False
        return {"result": result, "data": data}

    def find_one(self, query_elem):
        """
        Thin Wrap of the mongo find_one command.
        :param dict query_elem: the query dict, if you want to use "_id" in query_elem, you SHOULD call :py:func:`convert_str_to_objectid` to get the ObjectId for the "_id"
        :return: result is a dict with the formation {"result": True, "data": {}} or {"result":False, "data":None}
        result is False if error occured,
        result is True means query success. the "data" contains the query result. empty "data" array means no document match the query
        If you want to use ObjectId attribute in data, you SHOULD call :py:func:`convert_objectid_to_str` to get a string of objectid.
        """
        result = True
        data = None
        try:
            data = self.db_client.find_one(query_elem)
        except:
            result = False
        return {"result": result, "data": data}

    def insert(self, elem):
        """insert an element to mongodb
        :param dict elem: the element that will be inserted into mongodb, it can alse be the list of element, [elem]
        :return: a result dict with the formation {"result":True, "data": ObjectId('ididid')} or {"result":False, "data": None} if insert failed
        If the parameter elem is a list of element, then the data attribute in result value also be a list of ObjectId.
        """
        result = True
        data = None
        try:
            data = self.db_client.insert(elem)
        except:
            result = False
        return {"result": result, "data": data}

    def update(self, query_elem, update_elem, flag_upsert=True, flag_multi=True):
        """update document(s)
        :param dict query_elem: the query dict, if you want to use "_id" in query_elem, you SHOULD call :py:func:`convert_str_to_objectid` to get the ObjectId for the "_id"
        :param dict update_elem: the update dict, try to use mongodb operatate modifier
        :param boolean flag_upsert: a flag whether to insert document if there is NO document matching query_elem
        :param boolean flag_multi: a flag whether update all the document or just the first one matching query_elem
        :return: a result dict with the formation {"result":True, "data":{'updatedExisting': True|False, 'connectionId': 17, 'ok': 1.0, 'err': None, 'n': 10}}, the n in data attribute means how many document are updated from mongodb,
        if operation error occured, the result result will be {"result":False, "data":None}
        """
        result = True
        data = None
        try:
            data = self.db_client.update(query_elem, update_elem,
                                         upsert=flag_upsert, multi=flag_multi)
        except:
            result = False
        return {"result": result, "data": data}

    def remove(self, query_elem, flag_multi=True):
        """remove document(s)
        :param dict query_elem: the query dict, if you want to use "_id" in query_elem, you SHOULD call :py:func:`convert_str_to_objectid` to get the ObjectId for the "_id"
        :param boolean flag_multi: a flag whether remove all the document or just the first one matching query_elem
        :return: a result dict with the formation {"result":True, "data":{'connectionId': 17, 'ok': 1.0, 'err': None, 'n': 10}}, the n in data attribute means how many document are removed from mongodb,
        if operation error occured, the result result will be {"result":False, "data":None}
        """
        result = True
        data = None
        try:
            data = self.db_client.remove(query_elem, multi=flag_multi)
        except:
            result = False
        return {"result": result, "data": data}

    def atom_update(self, query_elem, update_elem, flag_upsert=True, flag_new=True):
        """atom update one document
        :param dict query_elem: the query dict, if you want to use "_id" in query_elem, you SHOULD call :py:func:`convert_str_to_objectid` to get the ObjectId for the "_id"
        :param dict update_elem: the update dict, try to use mongodb operatate modifier
        :param boolean flag_upsert: a flag whether to insert document if there is NO document matching query_elem
        :param boolean flag_new: a flag whether the result is new document after upate or old document before update
        :return: a result dict with the formation {"result":True, "data":{}}
        if operation error occured, the result result will be {"result":False, "data":None}
        """
        result = True
        data = None
        try:
            data = self.db_client.find_and_modify(query_elem,
                                                  update=update_elem, upsert=flag_upsert, new=flag_new)
        except:
            result = False
        return {"result": result, "data": data}

    def convert_objectid_to_str(self, oid):
        """Helper fucntion, convert ObjectId to String
        :param ObjectId oid: a object of ObjectId
        :return: the string represent of the object oid if oid is an ObjectId, otherwise result is None
        :rtype: string
        """
        return str(oid) if type(oid) == ObjectId else None

    def convert_str_to_objectid(self, sid):
        """Helper fucntion, convert string id to ObjectId object
        :param string sid: the string value of an ObjectId
        :return: the valid ObjectId if sid is valid
        :rtype: ObjectId
        """
        return ObjectId(sid) if sid else None

if __name__ == "__main__":
    dbc = DBHelper()
    obj_id = dbc.convert_str_to_objectid(None)
    query_elem = {"_id": obj_id}
    result = dbc.find(query_elem)
    print("find result is: ", result)
    result = dbc.find_one(query_elem)
    print("find_one result is: ", result)
    insert_elem = [{"cm_kind": "baremetal", "cm_id": "chen_test_insert", "data": {"test": "data", }},
                   {"cm_kind": "baremetal", "cm_id": "chen_test_insert",
                       "data": {"test": "data2", }},
                   {"cm_kind": "baremetal", "cm_id": "chen_test_insert",
                       "data": {"test": "data3", }}
                   ]
    result = dbc.insert(insert_elem)
    print("insert result is: ", result)
    insert_elem = {"cm_kind": "baremetal",
                   "cm_id": "chen_test_insert", "data": {"test": "data2", }}
    result = dbc.insert(insert_elem)
    print("insert result is: ", result)
    insert_elem = {"cm_kind": "baremetal",
                   "cm_id": "chen_test_insert", "data": {"test": "data3", }}
    result = dbc.insert(insert_elem)
    print("insert result is: ", result)

    query_elem = {"cm_id": "chen_test_insert"}
    update_elem = {"$set": {"value3": "my value3"}}
    result = dbc.atom_update(query_elem, update_elem, flag_new=False)
    print("update result is: ", result)
    #query_elem = {"cm_id": "chen_test_insert"}
    #result = dbc.remove(query_elem)
    # print "remove result is: ", result

from __future__ import print_function
from cloudmesh_common.logger import LOGGER
from cloudmesh.config.cm_config import get_mongo_db
from datetime import datetime
#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)


class BaremetalDB:

    """
      Manage the baremetal data in database.
      The data structure of top control document in Mongodb is:
        {
            "cm_kind" : "baremetal",
            "cm_type" : "bm_inventory",
            "bm_type" : "inventory_summary",
            "data" : {
                "gravel" : {
                    "idle_list" : [
                        "gravel02", "gravel03"
                    ]
                },
                "india" : {
                    "idle_list" : [
                        "i080",
                        "i079"
                    ],
                    "used_list" : [
                        "i072",
                        "i073",
                        "i074",
                        "i078"
                    ]
                }
            }
        }
        The data structure of used client document in Mongodb is:
        {
            "cm_kind" : "baremetal",
            "cm_type" : "bm_inventory",
            "bm_type" : "inventory_clients",
            "bm_style" : "cobbler",
            "client_id": "i078",
            "user_id": "your_id",
            "client_status" : {
                "status" : "unknown",     # "unknown", "deploy", "poweron", "poweroff"
                "deploy" : {
                    "result" : "unknown",   # "unknown", "success", "failure"
                    "date" : ""
                },
                "poweron" : {
                    "result" : "unknown",
                    "date" : ""
                },
                "poweroff" : {
                    "result" : "unknown",
                    "date" : ""
                }
            },
        }
        The data structure of user request baremetal document in Mongodb is:
        {
            "cm_kind" : "baremetal",
            "cm_type" : "bm_inventory",
            "bm_type" : "user_request",
            "request_date": "YYYYMMDD",
            "request_sn": "nnn",
            "user_id": "your_id",
            "status" : "unknown",      # "unknown", "pending", "refused", "approved", "part-approved"
            "request_content" : {
                "number": number,
                "date": {"from": "YYYYMMDD",
                         "to": "YYYYMMDD",
                        }
            },
        }
    """

    def __init__(self):
        self.coll_name = "inventory"
        self.cm_kind = "baremetal"
        self.cm_type = "bm_{0}".format(self.coll_name)
        self.bm_type = "inventory_summary"
        self.db_client = self.connect_db(self.coll_name)

    def connect_db(self, coll_name):
        return get_mongo_db(coll_name)

    def init_base_document_structure(self):
        elem = {"cm_kind": "baremetal",
                "cm_type": "bm_inventory",
                "bm_type": "inventory_summary",
                }
        flag_insert = True
        result = self.do_find(elem)
        print(result)
        if result["result"]:
            if result["data"] and len(result["data"]) > 0:
                flag_insert = False
        if flag_insert:
            elem["data"] = {}
            result = self.do_insert(elem)
        return result["result"]

    def get_default_query(self):
        return {"cm_type": self.cm_type,
                "cm_kind": self.cm_kind,
                "bm_type": self.bm_type
                }

    def get_full_query(self, query_elem):
        elem = self.get_default_query()
        if query_elem:
            elem.update(query_elem)
        return elem

    def do_find(self, query_elem):
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
            result_cursor = self.db_client.find(
                self.get_full_query(query_elem))
            if not result_cursor:
                result = False
            else:
                data = list(result_cursor)
        except:
            result = False
        return {"result": result, "data": data}

    def do_find_one(self, query_elem):
        result = True
        data = None
        try:
            data = self.db_client.find_one(self.get_full_query(query_elem))
        except:
            result = False
        return {"result": result, "data": data}

    def do_insert(self, elem):
        result = True
        data = None
        try:
            data = self.db_client.insert(elem)
        except:
            result = False
        return {"result": result, "data": data}

    def do_update(self, query_elem, update_elem, flag_upsert=True, flag_multi=True):
        result = True
        data = None
        try:
            data = self.db_client.update(self.get_full_query(query_elem), update_elem,
                                         upsert=flag_upsert, multi=flag_multi)
        except:
            result = False
        return {"result": result, "data": data}

    def do_remove(self, query_elem, flag_multi=True):
        result = True
        data = None
        try:
            data = self.db_client.remove(self.get_full_query(query_elem),
                                         multi=flag_multi)
        except:
            result = False
        return {"result": result, "data": data}

    def do_atom_update(self, query_elem, update_elem, flag_upsert=True, flag_new=True):
        result = True
        data = None
        try:
            data = self.db_client.find_and_modify(self.get_full_query(query_elem),
                                                  update=update_elem, upsert=flag_upsert, new=flag_new)
        except:
            result = False
        return {"result": result, "data": data}

    def get_baremetal_computers(self, cluster=None):
        result = None
        find_result = self.do_find_one({})
        if find_result["result"]:
            data = find_result["data"]
            if cluster:  # a specific cluster
                result = data["data"].get(cluster, {cluster: {}})
            else:
                result = data["data"]
        return result

    def append_baremetal_computers(self, dict_computer):
        return self.add_remove_baremetal_computers(dict_computer)

    def remove_baremetal_computers(self, dict_computer):
        return self.add_remove_baremetal_computers(dict_computer, False)

    def add_remove_baremetal_computers(self, dict_computer, flag_add=True):
        """
          param dict_computer: {"gravel": ["01", "02"],
                                "india": ["", ""],
                               }
        """
        update_elem = {}
        array_operator = "${0}".format("each" if flag_add else "in")
        for cluster in dict_computer:
            update_elem["data.{0}.idle_list".format(cluster)] = {
                array_operator: dict_computer[cluster]}
        update_data = self.do_atom_update(
            {}, {"${0}".format("addToSet" if flag_add else "pull"): update_elem})
        return update_data["result"]

    def update_baremetal_computers(self, dict_computer, flag_to_used=True):
        """
          param flag_to_used: True means change bm computer status from `idle` to `used`,
                              False means change from `used` to `idle`
        """
        pull_elem = {}
        push_elem = {}
        pull_list_name = "{0}_list".format("idle" if flag_to_used else "used")
        push_list_name = "{0}_list".format("used" if flag_to_used else "idle")
        for cluster in dict_computer:
            pull_elem["data.{0}.{1}".format(cluster, pull_list_name)] = {
                "$in": dict_computer[cluster]}
            push_elem["data.{0}.{1}".format(cluster, push_list_name)] = {
                "$each": dict_computer[cluster]}
        update_data = self.do_atom_update(
            {}, {"$pull": pull_elem, "$addToSet": push_elem})
        return update_data["result"]

    def assign_baremetal_to_user(self, dict_computer, user_id):
        query_elem = {
            "bm_type": "inventory_clients",
        }
        update_elem = {
            "bm_style": "unknown",
                        "user_id": user_id,
                        "client_status": {
                            "status": "unknown",
                            "deploy": {
                                "result": "unknown",
                                "date": ""
                            },
                            "poweron": {
                                "result": "unknown",
                                "date": ""
                            },
                            "poweroff": {
                                "result": "unknown",
                                "date": ""
                            }
                        }
        }
        result = True
        for cluster in dict_computer:
            for client_id in dict_computer[cluster]:
                query_elem["client_id"] = client_id
                update_data = self.do_atom_update(
                    query_elem, {"$set": update_elem})
                result = update_data["result"]
                if not result:
                    break
            if not result:
                break
        if result:
            result = self.update_baremetal_computers(dict_computer)
        return result

    def withdraw_baremetal_from_user(self, dict_computer, user_id=None):
        query_elem = {
            "bm_type": "inventory_clients",
        }
        if user_id:
            query_elem["user_id"] = user_id
        result = True
        for cluster in dict_computer:
            for client_id in dict_computer[cluster]:
                query_elem["client_id"] = client_id
                remove_data = self.do_remove(query_elem)
                result = remove_data["result"]
                if not result:
                    break
            if not result:
                break
        if result:
            result = self.update_baremetal_computers(dict_computer, False)
        return result

    def get_user_baremetal_computers(self, user_id):
        query_elem = {
            "bm_type": "inventory_clients",
            "user_id": user_id,
        }
        find_data = self.do_find(query_elem)
        return find_data["data"] if find_data["result"] else None

    def get_baremetal_computer_status(self, computer_id):
        """
           return a value in three status: "unknown", "idle", "used"
        """
        result = "unknown"
        data = self.get_baremetal_computers()
        if data:
            for status in data:
                for cluster in data[status]:
                    if computer_id in data[status][cluster]:
                        result = status
                        break
                if result == status:  # find
                    break
        return result

    def get_baremetal_computer_detail(self, computer_id):
        query_elem = {
            "bm_type": "inventory_clients",
            "client_id": computer_id,
        }
        find_data = self.do_find_one(query_elem)
        return find_data["data"] if find_data["result"] else None

    def get_baremetal_computers(self):
        find_data = self.do_find_one({})
        if not find_data["result"]:
            return None
        result = {"idle": {}, "used": {}}
        query_result = find_data["data"]
        for cluster in query_result["data"]:
            idle_list = query_result["data"][cluster].get("idle_list", [])
            if len(idle_list):
                result["idle"][cluster] = idle_list
            used_list = query_result["data"][cluster].get("used_list", [])
            if len(used_list):
                result["used"][cluster] = used_list
        return result

    def get_user_request_types(self):
        return ["pending", "refused", "approved", "part-approved"]

    def get_user_requests(self, user_id, status=None):
        query_elem = {"bm_type": "user_request", "user_id": user_id, }
        if status and status in self.get_user_request_types():
            query_elem["status"] = status
        find_data = self.do_find(query_elem)
        return find_data["data"] if find_data["result"] else None

    def insert_user_request(self, user_id, content):
        insert_elem = {"status": "unknown", "request_content": content}
        today = datetime.now()
        request_date = ""

    def update_user_request(self, user_id, request_date, request_sn, status):
        result = False
        if status in self.get_user_request_types():
            query_elem = {
                "user_id": user_id, "request_date": request_date, "request_sn": request_sn}
            update_data = self.do_atom_update(
                query_elem, {"$set": {"status": status}}, False, flag_new)
            result = update_data["result"]
        return result
# test
if __name__ == "__main__":
    bmdb = BaremetalDB()
    """
    dict_computers = {"gravel": ["g03", ],
                      "india": ["i02", ]
                      }
    result = bmdb.update_baremetal_computers(dict_computers, False)
    print "append bm result is: ", result
    result = bmdb.get_baremetal_computers()
    """
    """
    unexist_elem = {"chen": "chen"}
    result = bmdb.do_find_one(unexist_elem)
    """
    result = bmdb.init_base_document_structure()
    print(result)
    #result = bmdb.assign_baremetal_to_user(dict_computers, "testXXX")

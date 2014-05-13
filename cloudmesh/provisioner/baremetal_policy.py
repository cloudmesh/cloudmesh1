from dbhelper import DBHelper
from hostlist import expand_hostlist
from types import *
from copy import deepcopy
from cloudmesh.util.logger import LOGGER
#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)

class BaremetalPolicy:
    """Baremetal Policy. Get/Add/Delete user/group policy
    FIXME/TODO: It will add **permission access** that only admin can operate on poilicy later
    the formation of policy is 
    {"_id" : "53727f1c93f9d73e90520090",
    "name" : "user1,user2,user3",
    "policy_type" : "user", # or "group"
    "policy" : "i[101-103]",
    "cm_kind" : "baremetal",
    "cm_type" : "policy_inventory"
    }
    """
    def __init__(self):
        """Construction fucntion
        """
        self.db_client = DBHelper()
        
    def add_user_policy(self, user, policy):
        """add a policy for an user.
        :param string user: a username
        :param string policy: one piece of policy, means user can access which baremetal servers, e.g. "i[001-004]"
        :return: UUID means add policy success, otherwise None for failed 
        """
        return self.add_ug_policy("user", user, policy)
    
    def add_group_policy(self, group, policy):
        """add a policy for a group.
        :param string group: a group/project name
        :param string policy: one piece of policy, means this group/project can access which baremetal servers, e.g. "i[001-004]"
        :return: UUID means add policy success, otherwise None for failed
        """
        return self.add_ug_policy("group", group, policy)
    
    def add_ug_policy(self, type, name, policy):
        """add a policy for a specify *type*
        :param string type: the type of policy, currently supports **user** and **group**
        :param string name: the name in each type
        :param string policy: one piece of policy
        :return: UUID means add policy success, otherwise None for failed
        :rtype: string
        """
        add_elem = {"policy_type": type, "name": name, "policy": policy, }
        full_elem = self.get_full_query(add_elem)
        result = self.db_client.insert(full_elem)
        return None if not result["result"] else self.db_client.convert_objectid_to_str(result["data"])
    
    def remove_policy(self, uuid):
        """remove a policy based on uuid.
        :param string uuid: an uuid of the removed policy
        :return: True means remove policy success, otherwise False 
        """
        object_uuid = self.db_client.convert_str_to_objectid(uuid)
        elem = {"_id": object_uuid, }
        result = self.db_client.remove(elem)
        return result["result"]
    
    def get_policy_based_user(self, user):
        """get all the policies for a user
        :param string user: a username
        :return: a list of policy with the formation ['policy1', 'policy2']
        """
        policys = self.get_all_user_policy()
        if user == "all":
            return policys
        users = user.split(",")
        data = []
        for puser in policys:
            pusers = puser.split(",")
            common_users = [u for u in pusers if u in users]
            if common_users:
                data.extend(policys[puser])
        return data
    
    def get_policy_based_group(self, group):
        """get all the policies for a group/project
        :param string user: a group/project
        :return: a list of policy with the formation ['policy1', 'policy2']
        """
        policys = self.get_all_group_policy()
        if group == "all":
            return policys
        groups = expand_hostlist(group)
        data = []
        for pgroup in policys:
            pgroups = expand_hostlist(pgroup)
            common_groups = [u for u in pgroups if u in groups]
            if common_groups:
                data.extend(policys[pgroup])
        return data
    
    def get_all_user_policy(self):
        """get all the policies for all user
        :return: a dict of user and policy with the formation {"user1":['policy1', 'policy2'], "user2": [],}
        """
        return self.get_all_policy()["users"]
    
    def get_all_group_policy(self):
        """get all the policies for all group/project
        :return: a dict of group/project and policy with the formation {"group1":['policy1', 'policy2'], "group2": [],}
        """
        return self.get_all_policy()["groups"]
    
    def get_all_policy(self):
        """get all the policies for all users and group/project
        :return: a dict of group/project and policy with the formation {"users": {"user1": [], "user2": []}, "groups":{"group1":['policy1', 'policy2'], "group2": [],}}
        """
        policys = self._get_policy()
        if not policys:
            return None
        data = {"users": {}, "groups": {}}
        for policy in policys:
            name = policy["name"]
            type = policy["policy_type"]
            if type == "user":
                if name in data["users"]:
                    data["users"][name].append(policy)
                else:
                    data["users"][name] = [policy]
            elif type == "group":
                if name in data["groups"]:
                    data["groups"][name].append(policy)
                else:
                    data["groups"][name] = [policy]
        return data
    
    
    def _get_policy(self):
        """get all the records of policy
        :return: an ordered list of policy or None if failed
        """
        result = self.db_client.find(self.get_full_query())
        if result["result"]:
            records = result["data"]
            for record in records:
                record["_id"] = self.db_client.convert_objectid_to_str(record["_id"])
            return sorted(records, key=lambda x: x["_id"])
        return None
    
    def get_default_query(self):
        return {"cm_kind": "baremetal", "cm_type": "policy_inventory", }
    
    def get_full_query(self, query_elem=None):
        elem = self.get_default_query()
        if query_elem:
            elem.update(query_elem)
        return elem
    
    
if __name__ == "__main__":
    bmp = BaremetalPolicy()
    #result = bmp.add_user_policy("chen,heng", "i[001-003]")
    #result = bmp.add_user_policy("chen,fugang,heng", "i[101-103]")
    #result = bmp.get_all_policy()
    #result = bmp.get_policy_based_user("fugang")
    result = bmp.get_policy_based_user("gregor")
    print "result is: ", result
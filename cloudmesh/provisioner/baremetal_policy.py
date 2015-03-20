from __future__ import print_function
from dbhelper import DBHelper
from hostlist import expand_hostlist, collect_hostlist
from types import *
from copy import deepcopy
from cloudmesh_base.logger import LOGGER
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

    def get_policy_based_user_or_its_projects(self, user, projects):
        """get the merged policy based on the username and his/her related projects
        :param string user: only one valid username
        :param list projects: a list of project
        :return: a policy with hostlist string, or None if non-exist policy for user and its projects
        """
        user_policy = self.get_policy_based_user(user)
        group_policy = self.get_policy_based_group(collect_hostlist(projects))
        if user_policy or group_policy:
            if user_policy:
                valid_policy = user_policy
                if group_policy:
                    valid_policy.update(group_policy)
            else:
                valid_policy = group_policy
        else:
            return None
        all_policys = []
        for name in valid_policy:
            all_policys.extend(expand_hostlist(valid_policy[name]))
        return collect_hostlist(list(set(all_policys)))

    def get_policy_based_user(self, user):
        """get all the policies for a user
        :param string user: a username with hostlist formation
        :return: a dict of user and policy with the formation {"name1": "hostlist", "name2": "hostlist2"}
        """
        policys = self.get_all_user_policy()
        return self.merge_policy_based_ug(policys) if user == "all" else self.merge_policy_based_ug(policys, True, user)

    def get_policy_based_group(self, group):
        """get all the policies for a group/project
        :param string group: a group/project with hostlist formation
        :return: a dict of group and policy with the formation {"name1": "hostlist", "name2": "hostlist2"}
        """
        policys = self.get_all_group_policy()
        return self.merge_policy_based_ug(policys, False) if group == "all" else self.merge_policy_based_ug(policys, False, group)

    def merge_policy_based_ug(self, policys, flag_user=True, name=None):
        """merge policy based the name of user/group
        :param dict policys: all the possible policys for users/groups
        :param boolean flag_user: True means user, False means group
        :param string name: the name of one or more user/group, None means all user/groups
        :return: a dict of user/group and policy with the formation {"name1": "hostlist", "name2": "hostlist2"}
        """
        if policys:
            data = {}
            names = expand_hostlist(name) if name else None
            for puser in policys:
                users = expand_hostlist(puser)
                common_users = [
                    u for u in users if u in names] if names else users
                hosts = []
                for policy in policys[puser]:
                    hosts.extend(expand_hostlist(policy["policy"]))
                for user in common_users:
                    if user in data:
                        data[user].extend(hosts)
                    else:
                        data[user] = deepcopy(hosts)
            for user in data:
                data[user] = collect_hostlist(data[user])
            # flip data, combine duplicate values
            flipped_data = {}
            for user in data:
                if data[user] in flipped_data:
                    flipped_data[data[user]].append(user)
                else:
                    flipped_data[data[user]] = [user]
            # try to merge user with same hosts
            data = {}
            for value in flipped_data:
                data[collect_hostlist(flipped_data[value])] = value
            return data if data else None
        return None

    def get_all_user_policy(self, flag_merge=False):
        """get all the policies for all user
        :param boolean flag_merge: True meanse merge all possible user and policy into string
        :return: flag_merge is False, result is a dict of user and policy with the formation {"user1":['policy1', 'policy2'], "user2": [],}
        flag_merge is True, result is a dict of user/group and policy with the formation {"name1": "hostlist", "name2": "hostlist2"}
        """
        all_policys = self.get_all_policy()
        if all_policys:
            policys = all_policys.get("users", None)
            return policys if not flag_merge else self.merge_policy_based_ug(policys)
        return None

    def get_all_group_policy(self, flag_merge=False):
        """get all the policies for all group/project
        :param boolean flag_merge: True meanse merge all possible user and policy into string
        :return: flag_merge is False, result is a dict of group/project and policy with the formation {"group1":['policy1', 'policy2'], "group2": [],}
        flag_merge is True, result is a dict of user/group and policy with the formation {"name1": "hostlist", "name2": "hostlist2"}
        """
        all_policys = self.get_all_policy()
        if all_policys:
            policys = all_policys.get("groups", None)
            return policys if not flag_merge else self.merge_policy_based_ug(policys, False)
        return None

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
                record["_id"] = self.db_client.convert_objectid_to_str(
                    record["_id"])
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
    # result = bmp.add_user_policy("chen,heng", "i[001-003]")
    # result = bmp.add_user_policy("chen,fugang,heng", "i[101-103]")
    # result = bmp.get_all_policy()
    # result = bmp.get_policy_based_user("fugang")
    # result = bmp.get_policy_based_user("gregor")
    # result = bmp.add_group_policy("fg[1-3]", "i[111-113]")
    result = bmp.get_all_group_policy(True)
    print("result is: ", result)

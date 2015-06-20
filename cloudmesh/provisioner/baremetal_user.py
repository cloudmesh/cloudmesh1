from __future__ import print_function
from dbhelper import DBHelper
from cloudmesh_base.hostlist import Parameter
from types import *
from copy import deepcopy
from cloudmesh_base.logger import LOGGER
#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)


class BaremetalUser:

    """Baremetal computer user. Manage user in owners of cobbler objects.
    """

    def __init__(self, default="admin"):
        """Init function of class BaremetalUser
        :param string default: the default user added in cobbler owners if it is not None, otherwise, no default user will be added
        """
        self.default_user = default
        self.group_flag = "_grp__"
        self.seperator = ","

    def add_user_to_owners(self, user, owner_str):
        """shortcut for add user to owners.
        """
        return self.edit_user_in_owners(user, owner_str, "users", "add")

    def remove_user_from_owners(self, user, owner_str):
        """shortcut for remove user from owners.
        """
        return self.edit_user_in_owners(user, owner_str, "users", "remove")

    def add_group_to_owners(self, user, owner_str):
        """shortcut for add user to owners.
        """
        return self.edit_user_in_owners(user, owner_str, "groups", "add")

    def remove_group_from_owners(self, user, owner_str):
        """shortcut for remove user from owners.
        """
        return self.edit_user_in_owners(user, owner_str, "groups", "remove")

    def edit_user_in_owners(self, user, owner_str, item, action):
        """add/remove user from owners. The example of user: "abc", "abc,def,ccc", ["abc", "def", "ccc"]
        :param user: the user will be add/removed to/from the owners. It can be a single/combined user string, list of users
        :type user: string or list
        :param string owner_str: the owner string
        :param string item: a value in ["users", "groups"]
        :param string action: a value in ["add", "remove", ]
        :return: the processed owner string
        """
        owners = self.parse_user_string(owner_str)
        owner_users = owners[item] if owners[item] else []
        type_user = type(user)
        users = None
        if type_user in [StringType, UnicodeType]:
            users = self.get_valid_list(user.split(self.seperator))
        elif type_user in [ListType]:
            users = self.get_valid_list(user)
        if users:
            for user in users:
                if action == "add":  # add users
                    if user not in owner_users:
                        owner_users.append(user)
                elif action == "remove":  # remove users
                    if user in owner_users:
                        owner_users.remove(user)
        if item == "users":
            return self.merge_user_string(owner_users, owners["groups"])
        else:
            return self.merge_user_string(owners["users"], owner_users)

    def user_exist_in_owners(self, user, owner_str):
        """shortcut to check whether a user exist in the owners
        """
        return self.ug_exist_in_owners(user, owner_str, "users")

    def group_exist_in_owners(self, user, owner_str):
        """shortcut to check whether a user exist in the owners
        """
        return self.ug_exist_in_owners(user, owner_str, "groups")

    def ug_exist_in_owners(self, user, owner_str, item):
        """user/group exist in owners or not.
        :param string user: user name or group name, It can ONLY be a single string, The example of user: "abc"
        :param string owner_str: the owner string
        :param string item: a value in ["users", "groups"]
        :return: True means user exist in groups, otherwise False
        """
        owners = self.parse_user_string(owner_str)
        owner_users = owners[item] if owners[item] else []
        return user in owner_users

    def parse_user_string(self, user_str):
        """parse a list of user from user_str string
        :param string user_str: the combined user string, including group information
        :return: a dict of users and groups with the formation {"users": users, "groups":groups}, both of users and groups are list
        """
        users = None
        groups = None
        if user_str:
            names = self.get_valid_list(user_str.split(self.seperator))
            users = [
                name for name in names if not name.startswith(self.group_flag)]
            flag_len = len(self.group_flag)
            groups = [name[flag_len:]
                      for name in names if name.startswith(self.group_flag)]
        return {"users": users, "groups": groups}

    def merge_user_string(self, users=None, groups=None):
        """merge users and groups into one combined user string
        :param list users: a list of users
        :param list groups: a list of groups
        :return: a combined user string
        """
        user_str = self.merge_user(users)
        group_str = self.merge_group(groups)
        return self.seperator.join([user_str, group_str]) if group_str else user_str

    def merge_user(self, users=None):
        """merge a list of user into one user string.
        :param list users: a list of users with the formation ["user1", "user2",]
        :return: a user string "admin,user1,user2" in which user is sperated by **seperator**
        """
        users = self.get_valid_list(users)
        if users and len(users) > 0:
            temp_users = self.seperator.join(users)
            return temp_users if self.default_user in temp_users else self.seperator.join([self.default_user, temp_users])
        return self.default_user

    def merge_group(self, groups=None):
        """merge group to a string
        :param list groups: a list of group with the formation ["group1", "group2"]
        :return: a group string "_grp__group1,_grp__group2" in which group is prefix by a flag and each group is seperated by **seperator**
        """
        groups = self.get_valid_list(groups)
        if groups and len(groups) > 0:
            return self.seperator.join(["{0}{1}".format(self.group_flag, g) for g in groups])
        return None

    def get_valid_list(self, names):
        """get a valid list by removing the empty element and get rid of the whitespace in the start and end of each element
        """
        return [name.strip() for name in names if name.strip()] if names else None


if __name__ == "__main__":
    bmu = BaremetalUser()
    """
    users = ['a', 'admin', 'd', 'b',]#[]#None
    result = bmu.merge_user(users)
    """
    """
    user_str = ","#""#None
    result = bmu.parse_user(user_str)
    """
    """
    groups = ["  ", " a ", "b"]#None
    result = bmu.merge_group(groups)
    """
    users = ["a", "b", "c"]
    groups = ["ga", "gb"]
    owner_str = bmu.merge_user_string(users, groups)
    result = bmu.add_user_to_owners("1", owner_str)
    owner_str = result
    result = bmu.add_group_to_owners("g2 ", owner_str)
    owner_str = result
    result = bmu.remove_group_from_owners("gba", owner_str)
    result = bmu.group_exist_in_owners("ga", owner_str)
    print("result is:{0}".format(result))

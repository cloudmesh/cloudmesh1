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
    """
    def __init__(self):
        """Construction fucntion
        """
        self.db_client = DBHelper()
        
    def add_user_policy(self, user, policy):
        """add a policy for an user.
        :param string user: a username
        :param string policy: one piece of policy, means user can access which baremetal servers, e.g. "i[001-004]"
        :return: True means add policy success, otherwise False 
        """
        # TODO later...
        return True
    
    def add_group_policy(self, group, policy):
        """add a policy for a group.
        :param string group: a group/project name
        :param string policy: one piece of policy, means this group/project can access which baremetal servers, e.g. "i[001-004]"
        :return: True means add policy success, otherwise False 
        """
        # TODO later...
        return True
    
    def remove_user_policy(self, user, policy):
        """remove a policy for an user.
        :param string user: a username
        :param string policy: one piece of policy, means user will NOT access which baremetal servers, e.g. "i[001-004]"
        :return: True means add policy success, otherwise False 
        """
        # TODO later...
        return True
    
    def remove_group_policy(self, user, policy):
        """remove a policy for an group/project.
        :param string user: a group/project
        :param string policy: one piece of policy, means group/project will NOT access which baremetal servers, e.g. "i[001-004]"
        :return: True means add policy success, otherwise False 
        """
        # TODO later...
        return True
    
    def get_user_policy(self, user):
        """get all the policies for a user
        :param string user: a username
        :return: a list of policy with the formation ['policy1', 'policy2']
        """
        return []
    
    def get_group_policy(self, group):
        """get all the policies for a group/project
        :param string user: a group/project
        :return: a list of policy with the formation ['policy1', 'policy2']
        """
        return []
    
    def get_all_user_policy(self):
        """get all the policies for all user
        :return: a dict of user and policy with the formation {"user1":['policy1', 'policy2'], "user2": [],}
        """
        return {}
    
    def get_all_group_policy(self):
        """get all the policies for all group/project
        :return: a dict of group/project and policy with the formation {"group1":['policy1', 'policy2'], "group2": [],}
        """
        return {}
    
    def get_all_policy(self):
        """get all the policies for all users and group/project
        :return: a dict of group/project and policy with the formation {"users": {"user1": [], "user2": []}, "groups":{"group1":['policy1', 'policy2'], "group2": [],}}
        """
        return {}
    
if __name__ == "__main__":
    bmp = BaremetalPolicy()
    result = bmp.get_all_policy()
    print "all policy is: ", bmp
# -*- coding: utf-8 -*-
"""
    cloudmesh.user.cm_user
    ~~~~~~~~~~~~~~~~~~~~~~

    cm_user provides user information from the ldap and the cloud like openstack
    through mongodb. fab mongo.cloud command initialize mongo database and pour
    the information into the mongodb. Once the mongodb for cloudmesh has the
    user information, cm_user retrieves the user data from the mongodb
    instead of directly accessing the ldap and OpenStack Keystone. cm_user_id is
    the unique identification in ldap and cloud.

"""
from cloudmesh.config.cm_config import cm_config_server, get_mongo_db
from cloudmesh.util.logger import LOGGER
import traceback

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)

class cm_user(object):
    """cm_user provides user information including the ldap's and the clouds'.
    The ldap has a user profile such as a first name, last name and active
    project ids. In OpenStack Keystone, it has cloud-related information such as
    a tenant id, user id, cloud version, cloud type and location.
    """

    config_server = None

    def __init__(self):
        self.config_server = cm_config_server()
        self.connect_db()

    def connect_db(self):
        """ Connect to the mongo db."""

        ldap_collection = 'user'
        cloud_collection = 'cloudmesh'
        defaults_collection = 'defaults'
        passwd_collection = 'password'

        self.db_clouds = get_mongo_db(cloud_collection)
        self.db_users = get_mongo_db(ldap_collection)
        self.db_defaults = get_mongo_db(defaults_collection)
        self.userdb_passwd = get_mongo_db(passwd_collection)


    def info(self, portal_id, cloud_names=[]):
        """Return the user information with a given portal id.

        :param portal_id: the unique portal id to retrieve
        :type portal_id: str
        :param cloud_names: the list of cloud names to search, e.g.
        sierra_openstack_grizzly
        :type cloud_names: list
        :returns: dict

        """
        ldap_info = self.db_users.find({"cm_user_id": portal_id})
        cloud_info = self.db_clouds.find({"name": portal_id, "cm_kind": "users"})
        userinfo = {}
        # username is unique in ldap
        if ldap_info.count() > 0:
            ldap_user = ldap_info[0]
            del ldap_user['_id']
            userinfo["profile"] = ldap_user
            #
            # repositionning kesya nd projects
            #

            userinfo["keys"] = {'keylist': ldap_user['keys']}

            userinfo["projects"] = ldap_user['projects']
            del userinfo['profile']['keys']
            del userinfo['profile']['projects']

            userinfo['portalname'] = portal_id

        userinfo['clouds'] = {}
        for arec in cloud_info:
            del arec['_id']
            if len(cloud_names) > 0:
                if arec['cm_cloud'] in cloud_names:
                    userinfo['clouds'][arec['cm_cloud']] = arec
            else:
                userinfo['clouds'][arec['cm_cloud']] = arec
        userinfo['defaults'] = self.get_defaults(portal_id)
        #
        # update project names
        #
        projects = userinfo["projects"]
        projects = self.update_users_project_names(projects)

        return userinfo



    def update_users_project_names(self, projects):

        def correct_project_names(projects):
            tmp = [ "fg" + str(x) for x in projects]
            print "YYYYYY", tmp
            if tmp is None:
                #
                #  BUG HACK must be empty list
                #
                tmp = ['fg0']
            return tmp

        # projects = usersinfo[portal_id]["profile"]["projects"]
        try:
            projects["active"] = correct_project_names(projects["active"])
        except Exception, e:
            print e
            pass
        try:
            projects["completed"] = correct_project_names(projects["completed"])
        except:
            pass
        return projects

    def list_users(self, cloud_names=[]):
        """Return all user information with a given cloud.

        :param cloud_names: the cloud name
        :type cloud_names: list
        
        """
        ldap_info = self.db_users.find()
        usersinfo = {}
        for ldap_user in ldap_info:
            # e.g. ldap_user = {u'cm_user_id': u'abc', u'lastname': u'abc'
            # , u'_id': ObjectId('abc'), u'projects':
            # {u'active': []}, u'firstname': u'bbc'}
            portal_id = ldap_user['cm_user_id']
            usersinfo[portal_id] = {}

            userinfo = usersinfo[portal_id]

            userinfo['portalname'] = portal_id
            userinfo['profile'] = ldap_user
            #
            # repositioning
            #
            userinfo["keys"] = {'keylist': ldap_user['keys']}

            userinfo["projects"] = ldap_user['projects']
            del userinfo['profile']['keys']
            del userinfo['profile']['projects']

            #
            # correct projects
            #
            projects = userinfo["projects"]
            projects = self.update_users_project_names(projects)

        cloud_info = self.db_clouds.find({"cm_kind": "users"})
        for cloud_user in cloud_info:
            portal_id = cloud_user['name']
            try:
                usersinfo[portal_id]
            except KeyError:
                print portal_id + " doesn't exist in the ldap, skip to search"
                continue

            try:
                usersinfo[portal_id]['clouds']
            except KeyError:
                usersinfo[portal_id]['clouds'] = {}

            if cloud_names:
                if cloud_user['cm_cloud'] in cloud_names:
                    usersinfo[portal_id]['clouds'][cloud_user['cm_cloud']] = \
                    cloud_user
            else:
                usersinfo[portal_id]['clouds'][cloud_user['cm_cloud']] = \
                cloud_user

        return usersinfo

    def __getitem__(self, key):
        return self.info(key)

    def get_name(self, portal_id):
        """Return a user name in a tuple. (firstname, lastname)
        
        :param portal_id: the unique portal id
        :type portal_id: str
        :returns: tuple

        """
        ldap_data = self.db_users.find({"cm_user_id": portal_id})
        if ldap_data.count() > 0:
            ldap_info = ldap_data[0]
            (first_name, last_name) = (ldap_info['firstname'], ldap_info['lastname'])

            return (first_name, last_name)

    def set_defaults(self, username, d):
        """ Sets the defaults for a user """
        if type(d) is dict:
            self.db_defaults.update({'cm_user_id': username},
                                    {'$set': {'defaults': d}})
        else:
            raise TypeError, 'defaults value must be a dict'

    def set_default_attribute(self, username, attribute, value):
        """will set a variable in mongo
            ["defaults"][attribute]
        """
        d = self.get_defaults(username)
        d[attribute] = value
        self.set_defaults(username, d)

    def get_defaults(self, username):
        """returns the defaults for the user"""
        user = self.db_defaults.find({'cm_user_id': username})
        print "****** ", user['defaults'] if 'defaults' in user else "no defaults for {0}".format(username)
        return user['defaults'] if 'defaults' in user else {}


    def set_password(self, username, password, cloud):
        """Store a user password for the cloud

        :param username: OS_USERNAME or cm_user_id
        :type username: str
        :param password: OS_PASSWORD
        :type password: str
        :param cloud: the cloud name e.g. sierra_openstack_grizzly
        :type cloud: str

        """
        self.userdb_passwd.update({"username": username, "cloud": cloud }, \
                                  {"username":username, "password":password, \
                                   "cloud": cloud}, upsert=True)

    def get_password(self, username, cloud):
        """Return a user password for the cloud

        :param username: OS_USERNAME
        :type username: str
        :param cloud: the cloud name e.g. sierra_openstack_grizzly
        :type cloud:str

        """
        passwd = self.userdb_passwd.find({"username": username, "cloud":cloud})
        try:
            return passwd[0]
        except:
            return None

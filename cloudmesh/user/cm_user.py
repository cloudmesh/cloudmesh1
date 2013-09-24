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
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.util.logger import LOGGER
from pymongo import MongoClient

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

    def __init__(self):
        self.connect_db()
        self.connect_userdb()

    def connect_db(self):
        """ Connect to the mongo db."""
        db_name = cm_config_server().get("mongo.db")
        client = MongoClient()
        db = client[db_name]
        ldap_collection = 'user'
        cloud_collection = 'cloudmesh'
        defaults_collection = 'defaults'
        self.db_clouds = db[cloud_collection]
        self.db_users = db[ldap_collection]
        self.db_defaults = db[defaults_collection]

    def connect_userdb(self):
        try:
            self._connect_userdb()
        except:
            print
            print "The below lines should be existed in cloudmesh_server.yaml"
            print "----------------------"
            print "mongo_user:\n" + \
                    "    db: cm_user\n" + \
                    "    host: hostname\n" + \
                    "    port: portnumber\n" + \
                    "    username: admin\n" + \
                    "    password: passwd\n" + \
                    "    path: ~/.futuregrid/mongodb_user\n" + \
                    "    collections:\n" + \
                    "        cm_password:\n" + \
                    "            db: cm_user"
            print "---------------------"


    def _connect_userdb(self):
        """ Connect to the mongo user db."""
        # This will be enabled with ssl
        db_name = cm_config_server().get("mongo_user.db")
        host = cm_config_server().get("mongo_user.host")
        port = cm_config_server().get("mongo_user.port")
        username = cm_config_server().get("mongo_user.username")
        password = cm_config_server().get("mongo_user.password")
        client = MongoClient(host=host, port=port)
        db = client[db_name]
        passwd_collection = 'cm_password'
        self.userdb_passwd = db[passwd_collection]
        db.authenticate(username, password)

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
        userinfo['clouds'] = {}
        for arec in cloud_info:
            del arec['_id']
            if len(cloud_names) > 0:
                if arec['cm_cloud'] in cloud_names:
                    userinfo['clouds'][arec['cm_cloud']] = arec
            else:
                userinfo['clouds'][arec['cm_cloud']] = arec
        userinfo['defaults'] = self.get_defaults(portal_id)
        return userinfo

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
            usersinfo[portal_id]['profile'] = ldap_user
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
            self.db_defaults.update({'cm_user_id': username}, {'$set': {'defaults': d}})
        else:
            raise TypeError, 'defaults value must be a dict'

    def get_defaults(self, username):
        """returns the defaults for the user"""
        user = self.db_defaults.findOne({'cm_user_id': username})
        return user['defaults'] when 'defaults' in user else {}


    def set_password(self, username, password, cloud):
        """Store a user password for the cloud

        :param username: OS_USERNAME or cm_user_id
        :type username: str
        :param password: OS_PASSWORD
        :type password: str
        :param cloud: the cloud name e.g. sierra_openstack_grizzly
        :type cloud: str

        """
        self.userdb_passwd.insert({"username":username, "password":password,
                                   "cloud": cloud})

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

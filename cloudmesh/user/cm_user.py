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
from cloudmesh_install import config_file
from cloudmesh.config.cm_config import cm_config_server, get_mongo_db, cm_config
from cloudmesh.util.encryptdata import encrypt, decrypt
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.util import deprecated
from cloudmesh_install.util import path_expand
from cloudmesh.user.cm_template import cm_template
from cloudmesh.user.cm_userLDAP import cm_userLDAP, get_ldap_user_from_yaml
from cloudmesh.cm_mongo import cm_mongo
import traceback
from pprint import pprint
from passlib.hash import sha256_crypt

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

    def __init__(self, from_yaml=False):
        self.from_yaml = from_yaml
        self.config_server = cm_config_server()
        self.password_key = self.config_server.get(
            "cloudmesh.server.mongo.collections.password.key")
        self.with_ldap = cm_config_server().get(
            "cloudmesh.server.ldap.with_ldap")
        self.connect_db()

    def authenticate(self, userId, password):
        if not self.with_ldap:
            # return True
            passhash = self.get_credential(userId,
                            'cm_password_local',
                            'cm_password_local')['password']
            return sha256_crypt.verify(password, passhash)
        try:
            idp = cm_userLDAP()
            idp.connect("fg-ldap", "ldap")
            return idp.authenticate(userId, password)
        except Exception, e:
            log.error("{0}".format(e))
            return False

    def generate_yaml(self, id, basename):
        '''
        Generates the content for a yaml file based on the passed parameters.

        :param id: The username for which we want to create the yaml file
        :type id: String
        :param basename: The base name of the yaml file in the etc directory.
                         Allowed values are 'me' and 'cloudmesh'
        :type basename: String
        '''

        """id = username"""
        """basename = me, cloudmesh"""

        log.info("generate {1} yaml {0}".format(id, basename))
        result = self.info(id)
        result['password'] = self.get_credentials(id)

        etc_filename = config_file("/etc/{0}.yaml".format(basename))

        t = cm_template(etc_filename)
        out = t.replace(kind='dict', values=result)

        return out

    def connect_db(self):
        """ Connect to the mongo db."""

        if not self.from_yaml:

            ldap_collection = 'user'
            cloud_collection = 'cloudmesh'
            defaults_collection = 'defaults'
            passwd_collection = 'password'

            self.db_clouds = get_mongo_db(cloud_collection)
            self.db_users = get_mongo_db(ldap_collection)
            self.db_defaults = get_mongo_db(defaults_collection)
            self.userdb_passwd = get_mongo_db(passwd_collection)

    def info(self, portal_id, cloud_names=[]):
        """Return the: the list of cloud names to search, e.g.
        sierra
        :type cloud_names: list
        :returns: dict

        """

        if self.from_yaml:
            return get_ldap_user_from_yaml()

        else:

            ldap_info = self.db_users.find({"cm_user_id": portal_id})
            cloud_info = self.db_clouds.find(
                {"name": portal_id, "cm_kind": "users"})
            userinfo = {}
            # username is unique in ldap
            if ldap_info.count() > 0:
                ldap_user = ldap_info[0]
                del ldap_user['_id']
                userinfo["profile"] = ldap_user
                #
                # repositionning keys and projects
                #

                try:
                    userinfo["keys"] = {}
                    userinfo["keys"]["keylist"] = ldap_user['keys']
                except:
                    userinfo["keys"]["keylist"] = {}

                try:
                    userinfo["projects"] = ldap_user['projects']
                except:
                    userinfo["projects"] = {'active': [], 'completed': []}

                del userinfo['profile']['keys']
                del userinfo['profile']['projects']

                userinfo['portalname'] = portal_id
                userinfo['cm_user_id'] = portal_id

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

            try:
                projects = userinfo["projects"]
                projects = self.update_users_project_names(projects)
            except:
                pass

            return userinfo

    cloud_names = cm_config().cloudnames()
    default_security_group = cm_config().get("cloudmesh.security.default")
    # default_cloud = 'sierra'
    default_cloud = None

    def init_defaults(self, username):
        # ONLY for debug
        # added by HC on Nov. 11, 2013 to test LDAP and user.mongo
        # BEGIN debug
        # log.debug("cm_user_init_defaults, I was called.........")
        # END debug

        user = self.info(username)

        defaults = self.get_defaults(username)
        defaults['cm_user_id'] = username
        if 'prefix' not in defaults:
            defaults['prefix'] = user['cm_user_id']
        if 'index' not in defaults:
            defaults['index'] = 1

        # DO NOT set default cloud any more
        if 'cloud' not in defaults:
            if self.default_cloud in self.cloud_names:
                defaults['cloud'] = self.default_cloud
            # elif len(self.cloud_names) > 0:
            #    defaults['cloud'] = self.cloud_names[0]

        if 'key' not in defaults:
            keylist = user['keys']['keylist']
            if len(keylist) > 0:
                defaults['key'] = keylist.keys()[0]

        if 'project' not in defaults:
            projectlist = user['projects']['active']
            if len(projectlist) > 0:
                defaults['project'] = projectlist[0]

        if 'activeclouds' not in defaults:
            if 'cloud' in defaults:
                defaults['activeclouds'] = [defaults['cloud']]
            else:
                defaults['activeclouds'] = []

        if 'registered_clouds' not in defaults:
            if 'activeclouds' in defaults:
                defaults['registered_clouds'] = defaults['activeclouds']
            else:
                defaults['registered_clouds'] = []

        cm = cm_mongo()

        #
        # set default images for active clouds
        #

        if 'images' not in defaults:
            defaults['images'] = {}
        for cloud in defaults['activeclouds']:
            if cloud not in defaults['images']:
                default_image = "none"
                try:
                    default_image = cm.images([cloud])[cloud].keys()[0]
                except:
                    pass
                defaults['images'][cloud] = default_image

        #
        # set default flavors for active clouds
        #
        if 'flavors' not in defaults:
            defaults['flavors'] = {}
        for cloud in defaults['activeclouds']:
            if cloud not in defaults['flavors']:
                default_flavor = "none"
                try:
                    default_flavor = cm.flavors([cloud])[cloud].keys()[0]
                except:
                    pass
                defaults['flavors'][cloud] = default_flavor

        #
        # set default page status (Accordion open/close) for active clouds
        # added by HC, Nov. 8, 2013
        # to fix the bug 'UndefinedError: no attribute pagestatus' found by HL on Nov. 7, 2013
        #
        str_pagestatus = 'pagestatus'
        if str_pagestatus not in defaults:
            defaults[str_pagestatus] = {}
        for cloud in defaults['activeclouds']:
            if cloud not in defaults[str_pagestatus]:
                defaults[str_pagestatus][cloud] = "false"

        if 'securitygroup' not in defaults:
            defaults['securitygroup'] = self.default_security_group

        if 'group' not in defaults:
            defaults['group'] = None

        self.update_defaults(username, defaults)

    def update_users_project_names(self, projects):

        if "active" not in projects.keys():
            projects["active"] = []

        if "completed" not in projects.keys():
            projects["active"] = []

        return projects

    def list_users(self, cloud_names=[]):
        """Return all user information with a given cloud.

        :param cloud_names: the cloud name
        :type cloud_names: list

        """
        if self.from_yaml:
            log.critical("NOT IMPLEMENTED")
        else:

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

    @deprecated
    def get_name(self, portal_id):
        """Return a user name in a tuple. (firstname, lastname)

        :param portal_id: the unique portal id
        :type portal_id: str
        :returns: tuple

        """
        (firstname, lastname) = (None, None)
        ldap_data = self.db_users.find({"cm_user_id": portal_id})
        if ldap_data.count() > 0:
            ldap_info = ldap_data[0]
            (first_name, last_name) = (
                ldap_info['firstname'], ldap_info['lastname'])

        return (first_name, last_name)

    def update_defaults(self, username, d):
        """ Sets the defaults for a user """
        stored_d = self.get_defaults(username)
        for attribute in d:
            stored_d[attribute] = d[attribute]
        self.set_defaults(username, stored_d)

    def set_defaults(self, username, d):
        """ Sets the defaults for a user """
        if type(d) is dict:
            self.db_defaults.update({'cm_user_id': username}, d, upsert=True)

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
        user = self.db_defaults.find_one({'cm_user_id': username})

        if user is None:
            user = {}
        return user

    def set_credential(self, username, cloud, credential, cred_type='cloud'):
        """credential is a dict"""
        safe_credential = {}
        if cred_type in ('cloud', 'cm_password_local'):
            for cred in credential:
                safe_credential[cred] = encrypt(
                    credential[cred], self.password_key)
            self.userdb_passwd.update({"cm_user_id": username, "%s" % cred_type: cloud},
                                      {"cm_user_id": username, "credential": safe_credential,
                                       "%s" % cred_type: cloud}, upsert=True)

    def get_credential(self, username, cloud, cred_type='cloud'):
        if cred_type in ('cloud', 'cm_password_local'):
            try:
                safe_credential = self.userdb_passwd.find_one(
                    {"cm_user_id": username, "%s" % cred_type: cloud})["credential"]

                for cred in safe_credential:
                    t = safe_credential[cred]

                    n = decrypt(t, self.password_key)

                    safe_credential[cred] = n

                return safe_credential
            except:
                return None

    def get_credentials(self, username):
        """Return all user passwords in the form of a dict, keyed by cloud name"""
        credentials = self.userdb_passwd.find({"cm_user_id": username})
        d = {}
        """ bug multiple times same cloud ? """
        for c in credentials:
            cloud = c["cloud"]
            d[cloud] = {}
            d[cloud]["credential"] = self.get_credential(username, cloud)
        return d

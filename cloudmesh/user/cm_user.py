from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.util.logger import LOGGER

from pymongo import MongoClient

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)

class cm_user(object):
    
    def __init__(self):
        db_name = cm_config_server().get("mongo.db")
        client = MongoClient()
        db = client[db_name]
        ldapcollection = 'user'
        cloudcollection = 'cloudmesh'
        self.db_clouds = db[cloudcollection]
        self.db_users = db[ldapcollection]
        
    def info(self, portalname, cloudnames = []):
        ldapret = self.db_users.find({"cm_user_id": portalname})
        cloudret = self.db_clouds.find({"name": portalname, "cm_kind": "users"})
        userinfo = {}
        # username is unique in ldap
        if ldapret.count() > 0:
            ldapuser = ldapret[0]
            del ldapuser['_id']
            userinfo["profile"] = ldapuser
        userinfo['clouds'] = {}
        for arec in cloudret:
            del arec['_id']
            if len(cloudnames) > 0:
                if arec['cm_cloud'] in cloudnames:
                    userinfo['clouds'][arec['cm_cloud']] = arec
            else:
                userinfo['clouds'][arec['cm_cloud']] = arec
        return userinfo

    def __getitem__(self,key):
        return self.info(key)

    def get_name(self, portalname):
        ldapret = self.db_users.find({"cm_user_id": portalname})
        (firstname, lastname) = (ldapret['firstname'], ldapret['lastname'])

        return (firstname, lastname)


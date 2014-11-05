from __future__ import print_function
from cloudmesh_install import config_file
from CMUserProviderBaseType import CMUserProviderBaseType
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh_common.logger import LOGGER
from pprint import pprint
import ldap
import sys

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)


def get_ldap_user_from_yaml():
    me = ConfigDict(filename=config_file("/me.yaml"))
    d = {}
    for element in ["firstname",
                    "lastname",
                    "email",
                    "phone",
                    "address"]:
        d[element] = me.get("profile.{0}".format(element))
    d["cm_user_id"] = me.get("portalname")
    d["gidNumber"] = 0
    d["uidNumber"] = 0

    if "gidNumber" in me.keys():
        d["gidNumber"] = me.get("gidNumber")

    if "uidNumber" in me.keys():
        d["uidNumber"] = me.get("uidNumber")

    d["projects"] = me.get("projects")

    #
    # copy the keys
    #
    d['keys'] = me.get("keys.keylist")
    return d


class cm_userLDAP (CMUserProviderBaseType):

    providers = {}
    host = None
    cert = None

    def get_config(self, **kwargs):

        if 'host' not in kwargs:  
            self.host = cm_config_server().get(
                "cloudmesh.server.ldap.hostname")

        if 'ldapcert' not in kwargs:  
            self.cert = cm_config_server().get("cloudmesh.server.ldap.cert")

    def authenticate(self, userId, password, **kwargs):
        ret = False

        # bug pass **kwargs
        self.get_config()

        # print "'" + userId + "':'" + authProvider + "':'" + authCred + "'"

        # print adminuser, adminpass
        basedn = "ou=People,dc=futuregrid,dc=org"
        userdn = "uid={0},{1}".format(userId, basedn)
        # print userdn
        ldapconn = ldap.initialize("ldap://{0}".format(self.host))
        log.info("Initializing the LDAP connection to server: " + self.host)
        try:
            ldapconn.start_tls_s()
            log.info("tls started...")
            ldapconn.bind_s(userdn, password)
            ret = True
        except ldap.INVALID_CREDENTIALS:
            log.info("Your username or password is incorrect. Cannot bind.")
            ret = False
        except ldap.LDAPError:
            log.info(
                "User '" + userId + "' failed to authenticate due to LDAP error. The user may not exist." + str(sys.exc_info()))
            ret = False
        except:
            ret = False
            log.info(
                "User '" + userId + "' failed to authenticate due to possible password encryption error." + str(sys.exc_info()))
        finally:
            log.info("Unbinding from the LDAP.")
            ldapconn.unbind()
        return ret

    def __init__(self, collection="user"):
        super(cm_userLDAP, self).__init__()
        self.ldapconn = None

    def refresh_one(self, user_cn):
        '''
        Refresh the user database from the user provider for one user
        '''
        self._refresh(user_cn)
        data = self.get(user_cn)
        self.updates(user_cn, data)

    def refresh(self):
        '''
        Refresh the user database from the user provider
        '''
        self._refresh()
        users = self.list()
        for user in users:
            data = self.get(user)
            self.updates(user, data)

    def connect(self, name, type, **kwargs):
        '''
        Register a provider with som parameters specified in the dict params

        :param name: the name of the provider
        :param type: the type of the provider, overwrites a possibly given type in params
        :param params: a dictionary describing wht needs to be poassed to the service that provides user information
        '''
        # kwargs host=None, ldapcert=None)
        provider = {'type': type,
                    'name': name}
        for k, v in kwargs.iteritems():
            provider[k] = v

        if 'host' not in kwargs:  
            self.host = cm_config_server().get(
                "cloudmesh.server.ldap.hostname")

        if 'ldapcert' not in kwargs:  
            self.cert = cm_config_server().get("cloudmesh.server.ldap.cert")

        ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, self.cert)
        # BUG IN FINAL VERSION MAKE SURE WE CHECK
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

        self.ldapconn = ldap.initialize("ldap://" + self.host)
        self.ldapconn.start_tls_s()
        self.ldapconn.bind_s('', '')
        self.users = {}

    def disconnect(self):
        if self.ldapconn:
            self.ldapconn.unbind()

    def __del__(self):
        self.disconnect()

    def get(self, username):
        '''
        Return the dict associated with the username
        :param username:
        '''
        return self.users[username]

    def list(self, username=None):
        '''
        Return a list with all usernames
        '''
        if username:
            if username in self.users.keys():
                return [username]
            else:
                return []
        else:
            return self.users.keys()

    def _refresh(self, user_cn=None):
        self._getUsers(user_cn)
        self._getProjects(user_cn)
        return self.users

    def _getUsers(self, user_cn=None):
        ldap_filter = "(objectclass=inetorgperson)"
        if user_cn:
            ldap_filter = "(&{0}(cn={1}))".format(ldap_filter, user_cn)
        # print "LDAP query..."
        try:
            # ldap constant
            ldapbasedn = "dc=futuregrid,dc=org"
            ldapscope = ldap.SCOPE_SUBTREE
            ldapfilter = ldap_filter
            # info to be retrieved from ldap
            ldapattribs = ['uid',
                           'uidNumber',
                           'gidNumber',
                           'mail',
                           'givenName',
                           'sn',
                           'telephoneNumber',
                           'address',
                           'sshPublicKey']

            # retrieve all ldap users
            ldapresults = list(
                self.ldapconn.search_s(ldapbasedn, ldapscope, ldapfilter, ldapattribs))
            for ldapresult in ldapresults:
                # print ldapresult[1]
                # a result may not have 'mail' attribute, but valid account
                # must have
                if 'mail' in ldapresult[1]:
                    ldapmail = ldapresult[1]['mail'][0]
                    ldapuid = ldapresult[1]['uid'][0]
                    ldapuidNumber = ldapresult[1]['uidNumber'][0]
                    ldapgidNumber = ldapresult[1]['gidNumber'][0]
                    firstname = ldapresult[1]['givenName'][0]
                    lastname = ldapresult[1]['sn'][0]
                    phone = ldapresult[1]['telephoneNumber'][
                        0] if 'telephoneNumber' in ldapresult[1] else None
                    address = 'TBD'  # not currently in LDAP

                    keys = {}
                    if 'sshPublicKey' in ldapresult[1]:
                        for sshkey in ldapresult[1]['sshPublicKey']:
                            if sshkey.strip():
                                (keytype, key, nickname) = (
                                    sshkey.strip().split(None, 2) + [''])[0:3]
                                keys[
                                    nickname.translate(None, '.$')] = "key %s" % sshkey

                    self.users[ldapuid] = {"firstname": firstname,
                                           "lastname": lastname,
                                           "uidNumber": ldapuidNumber,
                                           "gidNumber": ldapgidNumber,
                                           "phone": phone,
                                           "email": ldapmail,
                                           "address": address,
                                           "projects": {"active": [], "completed": []},
                                           "keys": keys}
        except:
            print("WRONG" + str(sys.exc_info()))

    def _getProjects(self, user_cn=None):
        ldap_filter = "(&(objectclass=posixGroup)(cn=fg*))"
        if user_cn:
            ldap_filter = "(&(objectclass=posixGroup)(cn=fg*)(memberUid={0}))".format(
                user_cn)
        try:
            ldapbasedn = "dc=futuregrid,dc=org"
            ldapscope = ldap.SCOPE_SUBTREE
            ldapfilter = "(&(objectclass=posixGroup)(cn=fg*))"
            ldapattribs = ['cn', 'memberUid']
            ldapresults = list(
                self.ldapconn.search_s(ldapbasedn, ldapscope, ldapfilter, ldapattribs))
            for ldapresult in ldapresults:
                if 'cn' in ldapresult[1]:
                    cn = ldapresult[1]['cn'][0]
                    # projid = cn
                    if 'memberUid' in ldapresult[1]:
                        for auid in ldapresult[1]['memberUid']:
                            if auid in self.users:
                                if self.users[auid]["projects"]["active"] is not None:
                                    self.users[auid]["projects"][
                                        "active"].append(cn)
                                else:
                                    self.users[auid]["projects"][
                                        "active"] = [cn]
        except:
            print("WRONG" + str(sys.exc_info()))

    def _get_user_from_yaml(self, username):
        me = ConfigDict(config_file("/me.yaml"))

        print(me)


def main():
    idp = cm_userLDAP(CMUserProviderBaseType)

    idp.connect("fg-ldap", "ldap")
    idp.refresh()
    users = idp.list()

    from pprint import pprint

    pprint(users)

    pprint(idp.users)

    # idp._get_user_from_yaml(None)

if __name__ == "__main__":
    main()

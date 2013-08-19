from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.util.logger import LOGGER
from CMUserProviderBaseType import CMUserProviderBaseType
import ldap

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER('cm_user')



class cm_userLDAP (CMUserProviderBaseType):
    
    providers = {}
    host = None
    cert = None
    
    def get_config(self, **kwargs):
        
        if not kwargs.has_key('host'):#if kwargs['host'] is None:
            self.host = cm_config_server().config["ldap"]["hostname"]
    
        if not kwargs.has_key('ldapcert'):#if kwargs['ldapcert'] is None:
            self.cert = cm_config_server().config["ldap"]["cert"]
            
            
    def authenticate(self, userId, password, **kwargs):
        ret = False
                
        # bug pass **kwargs
        self.get_config()
        
        
        # print "'" + userId + "':'" + authProvider + "':'" + authCred + "'"
        
        #print adminuser, adminpass
        userdn = "uid=" + userId + ",ou=People,dc=futuregrid,dc=org"
        #print userdn
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
            log.info("User '" + userId + "' failed to authenticate due to LDAP error. The user may not exist."+ str(sys.exc_info()))
            ret = False
        except:
            ret = False
            log.info("User '" + userId + "' failed to authenticate due to possible password encryption error."+str(sys.exc_info()))
        finally:
            log.info("Unbinding from the LDAP.")
            ldapconn.unbind()
        return ret
    
    def __init__(self, collection="user"):
        super( cm_userLDAP, self ).__init__()

    def refresh(self):
        '''
        refreshes the userdatabase from the user provider
        '''
        self._refresh()
        users = self.list()
        for user in users:
            data = self.get(user)
            self.updates(user, data)  

    def connect(self, name, type, **kwargs):
        '''
        registers a provider with som parameters specified in the dict params
        
        :param name: the name of the provider
        :param type: the type of the provider, overwrites a possibly given type in params
        :param params: a dictionary describing wht needs to be poassed to the service that provides user information
        '''
        #kwargs host=None, ldapcert=None)
        provider = {'type': type, 
                    'name': name}
        for k,v in kwargs.iteritems():
            provider[k] = v
        
        if not kwargs.has_key('host'):#if kwargs['host'] is None:
            self.host = cm_config_server().config["ldap"]["hostname"]
    
        if not kwargs.has_key('ldapcert'):#if kwargs['ldapcert'] is None:
            self.cert = cm_config_server().config["ldap"]["cert"]
            
        ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, self.cert)
        self.ldapconn = ldap.initialize("ldap://" + self.host)
        self.ldapconn.start_tls_s()
        self.ldapconn.bind_s('', '')
        self.users = {}

    def disconnect(self):
        self.ldapconn.unbind()
    
    def __del__(self):
        self.disconnect()

        
    def get(self,username):
        '''
        returns the dict associated with the username
        :param username:
        '''
        return self.users[username]
                
    def list(self):
        '''
        returns a list with all usernames
        '''
        return self.users.keys()

    def _refresh(self):
        self._getUsers()
        self._getProjects()
        return self.users
            
    def _getUsers(self):
        #print "LDAP query..."
        try:
            # ldap constant
            ldapbasedn = "dc=futuregrid,dc=org"
            ldapscope = ldap.SCOPE_SUBTREE
            ldapfilter = "(objectclass=inetorgperson)"
            # info to be retrieved from ldap
            ldapattribs = ['uid', 'uidNumber', 'mail', 'givenName', 'sn']

            # retrieve all ldap users
            ldapresults = list(self.ldapconn.search_s(ldapbasedn, ldapscope, ldapfilter, ldapattribs))
            for ldapresult in ldapresults:
                #print ldapresult[1]
                # a result may not have 'mail' attribute, but valid account must have
                if ldapresult[1].has_key('mail'):
                    ldapmail = ldapresult[1]['mail'][0]
                    ldapuid = ldapresult[1]['uid'][0]
                    firstname = ldapresult[1]['givenName'][0]
                    lastname = ldapresult[1]['sn'][0]
                self.users[ldapuid] = {"firstname":firstname, "lastname":lastname, "projects":{"active":[]} }
        except:
            print "WRONG" + str(sys.exc_info())

    def _getProjects(self):
        try:
            ldapbasedn = "dc=futuregrid,dc=org"
            ldapscope = ldap.SCOPE_SUBTREE
            ldapfilter = "(&(objectclass=posixGroup)(cn=fg*))"
            ldapattribs = ['cn', 'memberUid']
            ldapresults = list(self.ldapconn.search_s(ldapbasedn, ldapscope, ldapfilter, ldapattribs))
            for ldapresult in ldapresults:
                if ldapresult[1].has_key('cn'):
                    cn = ldapresult[1]['cn'][0]
                    projid = cn[2:]
                    if ldapresult[1].has_key('memberUid'):
                        for auid in ldapresult[1]['memberUid']:
                            if self.users.has_key(auid):
                                if self.users[auid]["projects"]["active"] is not None:
                                    self.users[auid]["projects"]["active"].append(int(projid))
                                else:
                                    self.users[auid]["projects"]["active"] = [int(projid)]
        except:
            print "WRONG" + str(sys.exc_info())

  

def main():
    idp = cm_userLDAP (CMUserProviderBaseType)
    idp.connect("fg-ldap","ldap")
    idp.refresh()
    users = idp.list()

    from pprint import pprint
    
    pprint(users)
    
    pprint(idp.users)
    
    

if __name__ == "__main__":
    main()
        
        
            
        
        
        
        

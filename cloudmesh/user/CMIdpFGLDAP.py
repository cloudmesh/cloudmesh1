#!/usr/bin/env python

__author__ = 'Fugang Wang'
__version__ = '0.1'

import sys
import os
import ldap

class CMIdpFGLDAP(object):
    
    def __init__(self, host=None, ldapcert=None):
        if host is None:
            self.host = CMIdpFGLDAP.LDAPHOST
        if ldapcert is None:
            self.cert = CMIdpFGLDAP.LDAPCERTPATH
        ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, self.cert)
        self.ldapconn = ldap.initialize("ldap://" + self.host)
        self.ldapconn.start_tls_s()
        self.ldapconn.bind_s('', '')
        self.users = {}

    def __del__(self):
        self.ldapconn.unbind()

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

    def _getProjs(self):
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

    def getUsersProjs(self):
        self._getUsers()
        self._getProjs()
        return self.users

def main():
    idp = CMIdpFGLDAP()
    users = idp.getUsersProjs()


if __name__ == "__main__":
    main()
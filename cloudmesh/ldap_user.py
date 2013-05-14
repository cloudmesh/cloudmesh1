import ldap

class ldap_user:
    """ Provides a class for getting the user/project
    data that will come from LDAP. """

    # put these in a config file?
    LDAP_HOST = 'im3r.idp.iu.futuregrid.org'
    LDAP_PERSONBASE = 'ou=People,dc=futuregrid,dc=org'
    LDAP_PROJECTBASE = 'ou=Groups,dc=futuregrid,dc=org'

    def __init__(self, username):
        self._username = username
        self._data = None

    def _load_data(self):
        # specify ca cert (make sure TLS_CACERTDIR is defined in
        # /etc/openldap/ldap.conf, or optionally set LDAPTLS_CACERTDIR
        # in environment)
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)

        # connect
        ldapconn = ldap.initialize('ldap://%s' % self.LDAP_HOST)

        # start tls connection and bind
        ldapconn.start_tls_s()
        ldapconn.simple_bind_s()

        # Get profile and project data from LDAP
        self._data = {}

        search_result_person = ldapconn.search_s(self.LDAP_PERSONBASE, ldap.SCOPE_SUBTREE, '(cn=%s)' % self.username)
        self._data['person'] = search_result_person[0][1] if search_result_person is not None else None

        self._data['projects'] = ldapconn.search_s(self.LDAP_PROJECTBASE, ldap.SCOPE_SUBTREE, '(&(memberUid=%s)(cn=fg*))' % self.username, ['cn'])


    @property
    def username(self):
        return self._username

    @property
    def data(self):
        if self._data is None:
            self._load_data()
        return self._data

    @property
    def uid(self):
        return self.data['person']['uidNumber'][0] if 'uidNumber' in self.data['person'] else None

    @property
    def gid(self):
        return self.data['person']['gidNumber'][0] if 'gidNumber' in self.data['person'] else None

    @property
    def firstname(self):
        return self.data['person']['givenName'][0] if 'givenName' in self.data['person'] else None

    @property
    def lastname(self):
        return self.data['person']['sn'][0] if 'sn' in self.data['person'] else None

    @property
    def phone(self):
        return self.data['person']['telephoneNumber'][0] if 'telephoneNumber' in self.data['person'] else None

    @property
    def email(self):
        return self.data['person']['mail'][0] if 'mail' in self.data['person'] else None

    @property
    def address(self):
        return self.data['person']['homePostalAddress'] if 'homePostalAddress' in self.data['person'] else None

    @property
    def keys(self):
        keys = {}
        if 'sshPublicKey' in self.data['person']:
            for sshkey in self.data['person']['sshPublicKey']:
                (keytype, key, nickname) = sshkey.split()
                keys[nickname] = "key %s" % sshkey
            return keys
        else:
            return None

    @property
    def activeclouds(self):
        """Not yet implemented"""
        return ['sierra-openstack-grizzly']

    @property
    def defaultcloud(self):
        """Not yet implemented"""
        return 'sierra-openstack-grizzly'

    @property
    def activeprojects(self):
        """List of active projects"""
        if self.data['projects']:
            projects = []
            for project in self.data['projects']:
                (projectDN, projectAttrs) = project
                projectCN = projectAttrs['cn'][0]
                projects.append("%s" % projectCN)
        return projects

    @property
    def completedprojects(self):
        """Not yet implemented"""
        return []

    @property
    def defaultproject(self):
        """The user's default project (currently just the first active project)"""
        return self.activeprojects[0]


if __name__ == "__main__":
    luser = ldap_user('astreib')
    print "Username: %s" % luser.username
    print "Uid: %s" % luser.uid
    print "Gid: %s" % luser.gid
    print "First Name: %s" % luser.firstname
    print "Last Name: %s" % luser.lastname
    print "Keys: %s" % luser.keys
    print "Phone: %s" % luser.phone
    print "Email: %s" % luser.email
    print "Address: %s" % luser.address
    print "Projects - Active: %s" % luser.activeprojects
    print "Projects - Completed: %s" % luser.completedprojects
    print "Projects - Default: %s" % luser.defaultproject
    print "Active Clouds: %s" % luser.activeclouds
    print "Default Cloud: %s" % luser.defaultcloud

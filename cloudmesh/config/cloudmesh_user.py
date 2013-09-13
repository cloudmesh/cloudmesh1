from cloudmesh.user import cm_user

class cloudmesh_user:
    """ Provides a class for getting the user/project data"""

    def __init__(self, username):
        self._username = username
        self._data = None

    def _load_data(self):
        # Get profile and project data from LDAP
        cmu = cm_user.cm_user()
        self._data = cmu.info(self.username)

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
        return self.data['uidNumber']

    @property
    def gid(self):
        return self.data['gidNumber']

    @property
    def firstname(self):
        return self.data['firstname']

    @property
    def lastname(self):
        return self.data['lastname']

    @property
    def phone(self):
        return self.data['phone'] or 'n/a'

    @property
    def email(self):
        return self.data['email']

    @property
    def address(self):
        # This is currently not in LDAP; also needs to split address
        # lines into a list, not sure how ldap will represent this so
        # it is not yet done.
        # return self.data['person']['homePostalAddress'] if
        # 'homePostalAddress' in self.data['person'] else None
        return self.data['address'] or 'n/a'

    @property
    def keys(self):
        self.data['keys']

    @property
    def activeclouds(self):
        """Not yet implemented"""
        return ['sierra_openstack_grizzly']

    @property
    def defaultcloud(self):
        """Not yet implemented"""
        return 'sierra_openstack_grizzly'

    @property
    def activeprojects(self):
        """List of active projects"""
        if self.data['projects']:
            projects = []
            for project in self.data['projects']['active']:
                projects.append("fg-%s" % project)
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
    luser = cloudmesh_user('astreib')
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

class Client(object):
    """ Provides a mock class for testing.  Represents the keystone client. """
    mockusername = 'foo'
    mocktenants = ['foo']

    class mock_object(object):
        def __init__(self, **kwds):
            self.__dict__.update(kwds)

    class mock_users(object):
        def __init__(self, users):
            self.users = users
        def create(self, name, password, email):
            pass
        def update_password(self, user, password):
            pass
        def list(self):
            return self.users

    class mock_roles(object):
        def __init__(self, roles):
            self.roles = roles
        def add_user_role(self, user, role, tenant):
            pass
        def list(self):
            return self.roles

    class mock_tenants(object):
        def __init__(self, tenants):
            self.tenants = tenants
        def list(self):
            return self.tenants

    def __init__(self, username, password, tenant_name, auth_url, cacert):
        self.user = Client.mock_object(name=self.mockusername)
        self.role = Client.mock_object(name='_member_')
        self.tenantlist = []
        for t in self.mocktenants:
            self.tenantlist.append(Client.mock_object(name=t))

    @property
    def users(self):
        return self.mock_users([self.user])

    @property
    def roles(self):
        return self.mock_roles([self.role])

    @property
    def tenants(self):
        return self.mock_tenants(self.tenantlist)

if __name__ == "__main__":
    muser = Client('foo', 'foo', 'foo', 'foo', 'foo')
    print muser.users.list()[0].name
    print muser.roles.list()[0].name
    print muser.tenants.list()[0].name

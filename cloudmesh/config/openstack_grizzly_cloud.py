from __future__ import print_function
import sys


from cloudmesh.config.cloudmesh_cloud import cloudmesh_cloud

try:
    from keystoneclient.v2_0 import client
except:
    print("ERROR: keystoneclient is not installed")
    print("       Please see http://docs.openstack.org/developer/python-keystoneclient/")
    sys.exit(1)


class openstack_grizzly_cloud(cloudmesh_cloud):
    _client = client.Client

    def __init__(self, username, email, defaultproj, projectlist, cloudname, cloudcreds, cloudadmincreds=None):
        self._keystone = None
        self._keystone_admin = None
        cloudmesh_cloud.__init__(
            self, username, email, defaultproj, projectlist, cloudname, cloudcreds, cloudadmincreds)

    @property
    def keystone_admin(self):
        if self._keystone_admin is None:
            self._keystone_admin = self._keystone_client(as_admin=True)
        return self._keystone_admin

    @property
    def keystone(self):
        if self._keystone is None:
            self._keystone = self._keystone_client(as_admin=False)
        return self._keystone

    def _keystone_client(self, as_admin=False):
        if self._keystone is None:
            if as_admin:
                # Create/connect to keystone as administrator
                cloud_creds = self.admin_credentials
            else:
                # Create/connect to keystone as user
                cloud_creds = self.credentials
            client_creds = {'username': cloud_creds['OS_USERNAME'],
                            'password': cloud_creds['OS_PASSWORD'],
                            'tenant_name': cloud_creds['OS_TENANT_NAME'],
                            'auth_url': cloud_creds['OS_AUTH_URL'],
                            'cacert': cloud_creds['OS_CACERT']}
            try:
                self._keystone = self._client(**client_creds)
            except (client.exceptions.AuthorizationFailure,
                    client.exceptions.Unauthorized) as authz_err:
                print(('\n'.join(
                    ["Error: %s" % authz_err,
                     "Hint: check cloud configuration data; problems can occur if you",
                     "changed your password outside of cloudmesh.  If you need an",
                     "administrative password reset, email help@futuregrid.org."]
                )
                ), file=sys.stderr)
                sys.exit(1)
        return self._keystone

    def get_user_by_name(self, name):
        user = [u for u in self.keystone_admin.users.list() if u.name == name]
        return user[0] if len(user) == 1 else None

    def get_role_by_name(self, name):
        role = [r for r in self.keystone_admin.roles.list() if r.name == name]
        return role[0] if len(role) == 1 else None

    def get_tenant_by_name(self, name):
        tenant = [
            t for t in self.keystone_admin.tenants.list() if t.name == name]
        return tenant[0] if len(tenant) == 1 else None

    def initialize_cloud_user(self):
        creds = {}
        defaults = {}
        password = self.newpass()

        creds['OS_USERNAME'] = self.username
        creds['OS_PASSWORD'] = password
        defaults['project'] = self.defaultproject

        # Create user or reset password (we cannot retrieve existing password)
        user = self.get_user_by_name(self.username)
        if user is None:
            user = self.keystone_admin.users.create(
                self.username, password, self.email)
        else:
            self.keystone_admin.users.update_password(user, password)

        # Create membership role for user in each tenant
        member_role = self.get_role_by_name('_member_')
        os_tenants = []
        for tname in self.projects:
            tenant = self.get_tenant_by_name(tname)
            if tenant is None:
                tenant = self.keystone_admin.tenants.create(tname)
            user_roles = self.keystone_admin.roles.roles_for_user(user, tenant)
            if not filter(lambda r: r.id == member_role.id, user_roles):
                self.keystone_admin.roles.add_user_role(
                    user, member_role, tenant)
            os_tenants.append(tname)
        creds['FG_OS_TENANTS'] = ','.join(os_tenants)
        creds['OS_TENANT_NAME'] = self.defaultproject
        self.credentials = creds

    def change_own_password(self, oldpass, newpass):
        if cloudmesh_cloud.change_own_password(self, oldpass, newpass):
            self.keystone.users.update_own_password(oldpass, newpass)
            self.credentials['OS_PASSWORD'] = newpass
            print("Changed password for user %s in %s." % (self.username, self.cloudname))

    def get_own_password(self):
        return self.credentials['OS_PASSWORD']

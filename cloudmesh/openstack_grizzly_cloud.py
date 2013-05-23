import sys
import yaml
from cloudmesh_cloud import cloudmesh_cloud

try:
    from keystoneclient.v2_0 import client
except:
    print "ERROR: keystoneclient is not installed"
    print "       Please see http://docs.openstack.org/developer/python-keystoneclient/"
    sys.exit(1)

class openstack_grizzly_cloud(cloudmesh_cloud):
    _client = client.Client

    def __init__(self, profiledata, defaultproj, projectlist, cloudname):
        self._credentials = None
        self._keystone = None
        cloudmesh_cloud.__init__(self, profiledata, defaultproj, projectlist, cloudname)

    @property
    def keystone(self):
        if self._keystone is None:
            # Create/connect to keystone
            cm_admin = self.admin_data['cm_admin']
            try:
                self._keystone = self._client(
                    username=cm_admin['OS_USERNAME'],
                    password=cm_admin['OS_PASSWORD'],
                    tenant_name=cm_admin['OS_TENANT_NAME'],
                    auth_url=cm_admin['OS_AUTH_URL'],
                    cacert=cm_admin['OS_CACERT']
                    )
            except client.exceptions.AuthorizationFailure as authz_err:
                print "%s\nHint: check configuration in %s" % (authz_err, self.CLOUD_DEFNS)
                sys.exit(1)
        return self._keystone

    def get_user_by_name(self, name):
        user = [u for u in self.keystone.users.list() if u.name == name]
        return user[0] if len(user) == 1 else None

    def get_role_by_name(self, name):
        role = [r for r in self.keystone.roles.list() if r.name == name]
        return role[0] if len(role) == 1 else None

    def get_tenant_by_name(self, name):
        tenant = [t for t in self.keystone.tenants.list() if t.name == name]
        return tenant[0] if len(tenant) == 1 else None

    def initialize_cloud_user(self):
        creds = self.credentials
        defaults = self.clouddefaults
        password = self.newpass()

        creds['OS_USERNAME'] = self.username
        creds['OS_PASSWORD'] = password
        defaults['project'] = self.defaultproject

        # Create user or reset password (we cannot retrieve existing password)
        user = self.get_user_by_name(self.username)
        if user is None:
            user = self.keystone.users.create(self.username, password, self.email)
        else:
            self.keystone.users.update_password(user, password)

        # Create membership role for user in each tenant
        member_role = self.get_role_by_name('_member_')
        os_tenants = []
        for tname in self.projects:
            tenant = self.get_tenant_by_name(tname)
            if tenant is None:
                tenant = self.keystone.tenants.create(tname)
            user_roles = self.keystone.roles.roles_for_user(user, tenant)
            if not filter(lambda r: r.id == member_role.id, user_roles):
                self.keystone.roles.add_user_role(user, member_role, tenant)
            os_tenants.append(tname)
        creds['FG_OS_TENANTS'] = os_tenants
        creds['OS_TENANT_NAME'] = self.defaultproject

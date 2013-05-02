import yaml
from cloudmesh_cloud import cloudmesh_cloud
from keystoneclient.v2_0 import client   # http://docs.openstack.org/developer/python-keystoneclient/


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
            self._keystone = self._client(
                username=cm_admin['OS_USERNAME'],
                password=cm_admin['OS_PASSWORD'],
                tenant_name=cm_admin['OS_TENANT_NAME'],
                auth_url=cm_admin['OS_AUTH_URL'],
                cacert=cm_admin['OS_CACERT']
                )
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

    def initialize_cloud_user(self, create_user=False):
        creds = self.credentials
        defaults = self.clouddefaults
        password = self.newpass()

        creds['OS_USERNAME'] = self.username
        creds['OS_PASSWORD'] = password
        defaults['project'] = self.defaultproject

        # Create user or reset password (we cannot retrieve existing password)
        if create_user:
            user = self.keystone.users.create(self.username, password, self.email)
        else:
            user = self.get_user_by_name(self.username)
            self.keystone.users.update_password(user, password)

        # Create membership role for user in each tenant
        member_role = self.get_role_by_name('_member_')
        for tname in self.projects:
            tenant = self.get_tenant_by_name(tname)
            self.keystone.roles.add_user_role(user, member_role, tenant)
            os_tenant = '%s_OS_TENANT_NAME' % tname.replace('-', '').upper()
            creds[os_tenant] = tname
        creds['OS_TENANT_NAME'] = '$%s_OS_TENANT_NAME' % self.defaultproject.replace('-', '').upper()


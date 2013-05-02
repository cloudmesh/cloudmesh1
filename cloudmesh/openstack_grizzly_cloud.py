import yaml
from cloudmesh_cloud import cloudmesh_cloud
from keystoneclient.v2_0 import client

class openstack_grizzly(cloudmesh_cloud):

    def __init__(self, username, tennant, resourcename):
        self._tennant = tennant
        cloudmesh_cloud.__init__(self, username, '%s-openstack-grizzly' % resourcename)

    @property
    def tennant(self):
        return self._tennant

    @property
    def credentials(self):
        creds = self.data['credentials']
        creds['OS_USERNAME'] = self.username
        creds['OS_PASSWORD'] = None
        creds['OS_TENANT_NAME'] = self.tennant
        return creds

if __name__ == "__main__":
    lcloud = openstack_grizzly('astreib', 'fg82', 'sierra')
    print "Username: %s" % lcloud.username
    print "Cloudname: %s" % lcloud.cloudname
    print "Data: %s" % lcloud.data
    print "Credentials: %s" % lcloud.credentials



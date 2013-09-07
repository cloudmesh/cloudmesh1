from cloudmesh.config.openstack_essex_cloud import openstack_essex_cloud
from cloudmesh.config.openstack_grizzly_cloud import openstack_grizzly_cloud

class cloudmesh_cloud_handler(object):
    cloud_handlers = {
        ('openstack', 'grizzly'): openstack_grizzly_cloud,
        ('openstack', 'essex'): openstack_essex_cloud,
        # etc
    }

    def __new__(__class, cloudname):
        # assume cloudnames are like:
        #   host-cloudtype-cloudversion, e.g. sierra_openstack_grizzly
        (cloudtype, cloudversion) = cloudname.split('-')[1:]
        return cloudmesh_cloud_handler.cloud_handlers[(cloudtype, cloudversion)]

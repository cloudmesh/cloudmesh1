from cloudmesh.config.openstack_essex_cloud import openstack_essex_cloud
from cloudmesh.config.openstack_grizzly_cloud import openstack_grizzly_cloud

class cloudmesh_cloud_handler(object):
    cloud_handlers = {
        ('sierra-openstack-grizzly'): openstack_grizzly_cloud,
        ('india-openstack-essex'): openstack_essex_cloud,
        # etc
    }

    def __new__(__class, cloudname):
        return cloudmesh_cloud_handler.cloud_handlers[cloudname]

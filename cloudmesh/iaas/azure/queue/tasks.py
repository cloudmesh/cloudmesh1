from __future__ import absolute_import
from celery import current_task
from celery.utils.log import get_task_logger
from cloudmesh.iaas.azure.queue.celery import celery
from cloudmesh.iaas.azure.cm_compute import azure as windows_azure
#
#logger = get_task_logger(__name__)
#

@celery.task(track_started=True)
def vm_create(name, flavor_name, image_id, security_groups=None, key_name=None,
              meta={}, userdata=None):
    '''
    create a vm instance in the background by celery task queue

    Description:
        creates an object of windows azure class from cloudmesh.iaas.azure.cm_compute

    '''
    obj = windows_azure()
    obj.vm_create(name, flavor_name, image_id ,security_groups, key_name, meta,
                  userdata)

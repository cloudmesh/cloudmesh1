from __future__ import absolute_import
from celery import current_task
from celery.utils.log import get_task_logger
from cloudmesh.iaas.azure.queue.celery import celery_azure_queue
from cloudmesh.iaas.azure.cm_compute import azure as windows_azure
from cloudmesh.cm_mongo import cm_mongo
#
# logger = get_task_logger(__name__)
#


@celery_azure_queue.task(track_started=True)
def vm_create(name, flavor_name, image_id, security_groups=None, key_name=None,
              meta={}, userdata=None):
    '''
    create a vm instance in the background by celery task queue

    Description:
        creates an object of windows azure class from cloudmesh.iaas.azure.cm_compute

    '''
    obj = windows_azure()
    obj.vm_create(name, flavor_name, image_id, security_groups, key_name, meta,
                  userdata)


@celery_azure_queue.task(track_started=True)
def refresh(cm_user_id=None, names=None, types=None):

    if isinstance(names, str):
        names = [names]
    if isinstance(types, str):
        types = [types]

    clouds = cm_mongo()
    clouds.activate(cm_user_id=cm_user_id)
    clouds.refresh(cm_user_id=cm_user_id, names=names, types=types)

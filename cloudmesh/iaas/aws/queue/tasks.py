from __future__ import absolute_import
from celery import current_task
from celery.utils.log import get_task_logger
from cloudmesh.iaas.aws.queue.celery import celery_aws_queue
from cloudmesh.iaas.aws.cm_compute import aws as amazon_ec2
from cloudmesh.cm_mongo import cm_mongo

#
# logger = get_task_logger(__name__)
#


@celery_aws_queue.task(track_started=True)
def refresh(cm_user_id=None, names=None, types=None):

    if isinstance(names, str):
        names = [names]
    if isinstance(types, str):
        types = [types]

    clouds = cm_mongo()
    clouds.activate(cm_user_id=cm_user_id)
    clouds.refresh(cm_user_id=cm_user_id, names=names, types=types)

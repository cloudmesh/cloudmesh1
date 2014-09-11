from __future__ import absolute_import
from celery import current_task
from cloudmesh.provisioner.queue.celery import celery_provisiner_queue
from cloudmesh.provisioner.provisioner import ProvisionerSimulator as Provider

import sys
import os

from celery.utils.log import get_task_logger

import time

logger = get_task_logger(__name__)

provisioner = Provider()


@celery_provisiner_queue.task(track_started=True)
def provision(host, image):
    '''
    provisions on a specific host the image specified
    :param host:
    :param image:
    '''
    provisioner.provision([host], image)


@celery_provisiner_queue.task
def info():
    logger.info('executing info')
    request = current_task.request
    print('Executing task id %r, args: %r kwargs: %r' % (
        request.id, request.args, request.kwargs))
    time.sleep(5)
    return "info world"

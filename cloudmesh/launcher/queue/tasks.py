from __future__ import absolute_import
from celery import current_task
from cloudmesh.launcher.queue.celery import celery_launcher_queue
from cloudmesh.launcher.cm_launcher import SimulatorLauncher as Launcher

import sys
import os

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

launcher = Launcher()


@celery_launcher_queue.task(track_started=True)
def task_launch(task_dict):
    '''
    Launches the recipies on the server as per the task_dict. The task dict should the following properties
    name: name of the server
    recipies: a list of tuples where the first element of the tuple would be name of recipie and second would be the type
    host: information about the host
    '''
    print "task recieved"
    launcher.run(task_dict)

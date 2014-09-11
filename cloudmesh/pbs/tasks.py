from __future__ import absolute_import
from celery import current_task
from cloudmesh.pbs.celery import celery_pbs_queue
from cloudmesh.config.cm_config import cm_config
from cloudmesh.pbs.pbs_mongo import pbs_mongo
import datetime

import sys
import os
import time

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@celery_pbs_queue.task(track_started=True)
# checks the mongodb for last qstat refresh and if it is
def refresh_qstat(hosts):
    '''
    Launches the recipies on the server as per the task_dict. The task dict should the following properties
    name: name of the server
    recipies: a list of tuples where the first element of the tuple would be name of recipie and second would be the type
    host: information about the host
    '''
    max_time_diff_allowed = 30  # indicates 30 seconds of time difference allowed between old and new values
    config = cm_config()
    user = config["cloudmesh"]["hpc"]["username"]
    pbs = pbs_mongo()
    error = ""
    print "task recieved"
    for host in hosts:
        time = datetime.datetime.now()
        datetime.datetime.now()
        data = pbs.get_qstat(host)
        perform_refresh = False
        jobcount = data.count()
        if jobcount > 0:
            last_refresh = data[0]["cm_refresh"]
            time_diff = time - last_refresh
            if time_diff.seconds > max_time_diff_allowed:
                perform_refresh = True
        else:
            perform_refresh = True
        if perform_refresh:
            print "Beginning refresh for {0}".format(host)
            pbs.activate(host, user)
            try:
                d = pbs.refresh_qstat(host)
            except Exception, e:
                error += "error {0} {1}".format(str(host), str(e))
        else:
            print "No refresh needed for {0}".format(host)
    return error

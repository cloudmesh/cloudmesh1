from __future__ import absolute_import
from celery import current_task
from cloudmesh.rack.queue.celery import celery
from cloudmesh.temperature.cm_temperature import cm_temperature as Temperature

import sys
import os

from celery.utils.log import get_task_logger

import time

log = get_task_logger(__name__)

ipmi_temp = Temperature()


@celery.task(track_started=True)
def temperature(host, unit):
    '''
    get the temperature of 'host' with the help of ipmi API
    '''
    result = None
    tdict = ipmi_temp.get_ipmi_temperature(host)
    if any(tdict):
        result = ipmi_temp.parse_max_temp(tdict, unit)
        # log.debug("host [{0}] temperature: {1}".format(host, result))
        # write the result to mongo DB
        # TODO ...
        # TODO, use celery async event
    else:
        log.error("host [{0}] is NOT reachable with ipmitool".format(host))

    # only for debug, return the result directly
    return result

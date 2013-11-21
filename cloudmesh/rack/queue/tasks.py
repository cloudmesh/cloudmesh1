from __future__ import absolute_import
from celery import current_task
from cloudmesh.rack.queue.celery import celery

from cloudmesh.temperature.cm_temperature import cm_temperature as Temperature
from cloudmesh.rack.rack_data import rack_data

import sys
import os

from celery.utils.log import get_task_logger

import time

log = get_task_logger(__name__)


@celery.task(track_started=True)
def temperature(host_name, rack_name, unit):
    '''
    get the temperature of 'host_name' with the help of ipmi API
    '''
    log.debug("temperature_task recieved")
    ipmi_temp = Temperature()
    tdict = ipmi_temp.get_ipmi_temperature(host_name)
    rack_inventory = rack_data()
    rack_inventory.server_refresh_update_temperature(rack_name, host_name, tdict)
    
    """
    result = None
    tdict = ipmi_temp.get_ipmi_temperature(host_name)
    if tdict is not None:
        result = ipmi_temp.parse_max_temp(tdict, unit)
        # log.debug("host [{0}] temperature: {1}".format(host, result))
        # write the result to mongo DB
        # TODO ...
        # TODO, use celery async event
    else:
        log.error("host [{0}] is NOT reachable with ipmitool".format(host))

    # only for debug, return the result directly
    return result
    """

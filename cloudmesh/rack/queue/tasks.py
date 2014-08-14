from __future__ import absolute_import
from celery import current_task
from cloudmesh.rack.queue.celery import celery_rack_queue_tasks

from cloudmesh.temperature.cm_temperature import cm_temperature as Temperature
from cloudmesh.rack.rack_data import RackData
from cloudmesh.rack.rack_work import RackWork

import sys
import os

from celery.utils.log import get_task_logger

import time

log = get_task_logger(__name__)


@celery_rack_queue_tasks.task(track_started=True)
def temperature(host_name, rack_name, unit):
    '''
    get the temperature of 'host_name' with the help of ipmi API
    '''
    log.debug("temperature_task recieved")
    ipmi_temp = Temperature()
    tdict = ipmi_temp.get_ipmi_temperature(host_name)
    rackdata = RackData()
    rackdata.server_refresh_update_temperature(rack_name, host_name, tdict)


@celery_rack_queue_tasks.task(track_started=True)
def pbs_service(rack_name):
    '''
    get all server type with the help of PBS
    '''
    log.debug("pbs_service_task recieved")
    rack_work = RackWork()
    tdict = rack_work.pbs_service(rack_name)
    rackdata = RackData()
    rackdata.server_refresh_update_service(rack_name, tdict)

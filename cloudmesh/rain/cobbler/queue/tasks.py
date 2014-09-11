from __future__ import absolute_import
from celery import current_task
from cloudmesh.rain.cobbler.queue.celery import celery_rain_queue

from cloudmesh.rain.cobbler.cobbler_rest_api import CobblerRestAPI

from celery.utils.log import get_task_logger

log = get_task_logger(__name__)


@celery_rain_queue.task(track_started=True)
def deploy_system(name):
    '''Deploy baremetal computer whose name is **name**
    :param string name: the unique name of baremetal computer
    '''
    log.debug("deploy_system_task recieved, host is {0}".format(name))
    rest_api = CobblerRestAPI()
    result = rest_api.deploy_cobbler_system(name)
    log.info("deploy_system, deploy command result is: {0}".format(result))


@celery_rain_queue.task(track_started=True)
def power_system(name, flag_on):
    '''Power ON/OFF baremetal computer whose name is **name**
    :param string name: the unique name of baremetal computer
    :param boolean flag_on: True means power ON, False means OFF
    '''
    log.debug("power_system_task recieved, host is {0}, flag is: {1}".format(
        name, "ON" if flag_on else "OFF"))
    rest_api = CobblerRestAPI()
    result = rest_api.power_cobbler_system(name, flag_on)
    log.info("power_system, power command result is: {0}".format(result))

"""
async task, get cluster temperature,
value of "-1" means cannot connect to server or get temperature
"""

from sh import ssh
from celery import Celery

from cloudmesh.temperature.cm_temperature import cm_temperature as Temperature
from cloudmesh.rack.rack_data import rack_data

import sys
import os

from celery.utils.log import get_task_logger

import time

log = get_task_logger(__name__)

ipmi_temp = Temperature()


celery_rack_queue = Celery(
    'cloudmesh.rack.tasks', backend='amqp', broker='amqp://guest@localhost//')


@celery_rack_queue.task
def temperature(host_name, rack_name, unit):
    '''
    get the temperature of 'host_name' with the help of ipmi API
    '''
    tdict = ipmi_temp.get_ipmi_temperature(host_name)
    rack_inventory = rack_data()
    rack_inventory.server_refresh_update_temperature(
        rack_name, host_name, tdict)


@celery_rack_queue.task
def task_sensors(dict_idip):
    dict_data = {}
    for cluster in dict_idip.keys():
        dict_data[cluster] = {}
        for uid in dict_idip[cluster].keys():
            ip = cluster[uid]
            dict_data[cluster][uid]["ip"] = ip
            # fetch uid-ip server's temperature
            report = ssh("-o ConnectTimeout=1", "-o ConnectionAttempts=1",
                         "user", ip,
                         "sensors"
                         )
            temp = parseCpuTemperature(report)
            dict_data[cluster][uid]["temp"] = temp[0]

    # write current temperature data to mongo db

    # get the highest cpu temperature throught parseing the output of 'sensors'
    # return is a list including 2 elems, [36.0, C] or [36.0, F]
    # C or F is the unit name of temperature
    def parseCpuTemperature(self, values):
        lines = values.split("\n")
        cpu_lines = [x for x in lines if x.find("(high") > -1]
        tunit = "C"
        tmax = -1
        for line in cpu_lines:
            # position of degree sign
            pos_degree = line.find(u"\xb0")
            # position of +
            pos_plus = line.find(u"+")
            tnum = float(line[pos_plus + 1:pos_degree])
            tunit = line[pos_degree + 1:pos_degree + 2]
            if tnum > tmax:
                tmax = tnum

        return [tmax, tunit]

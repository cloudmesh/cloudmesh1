from flask import Blueprint
from flask import render_template, request, redirect
from cloudmesh.pbs.pbs import PBS
from cloudmesh.config.cm_config import cm_config
import cloudmesh
from flask.ext.login import login_required
from datetime import datetime

from cloudmesh_base.logger import LOGGER

log = LOGGER(__file__)

status_module = Blueprint('status_module', __name__)

#
# ROUTE: status
#


@status_module.route('/status')
@login_required
def display_status():

    msg = ""
    status = ""

    values = {
        'india': {'jobs': 0, 'users': 0},
        'bravo': {'jobs': 0, 'users': 0},
        'echo': {'jobs': 0, 'users': 0},
        'delta': {'jobs': 0, 'users': 0},
    }

    config = cm_config()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    user = config.get("cloudmesh.hpc.username")

    services = {}
    qinfo = {}
    qstat = {}
    qstat_uniq_users = {}

    for host in ['india.futuregrid.org',
                 ]:
        pbs = PBS(user, host)
        services[host] = pbs.service_distribution()
        qinfo[host] = pbs.qinfo()
        qstat[host] = pbs.qstat()
        qstat_uniq_users[host] = pbs.get_uniq_users()

    machines = services.keys()

    # print "FFF", machines

    #
    # collecting all atttributes
    #
    all_attributes = set()

    for machine in machines:
        attributes = set(list(services[machine].keys()))
        print "P", attributes
        all_attributes.update(attributes)

        # print "XXX", all_attributes

    spider_services = {'machines': machines,
                       'categories': list(all_attributes),
                       'data': {}}

    #
    # seeting all attributes to 0
    #

    for machine in machines:
        ser = []
        i = 0
        for attribute in all_attributes:
            try:
                ser.append(services[machine][attribute])
            except:
                ser.append(0)
            i = i + 1
        spider_services['data'][machine] = ser

    # print "SSS", spider_services

    # Users and Jobs
    total_jobs = {}
    unique_users = {}
    for machine in machines:
        for qserver in qinfo[machine]:
            total_jobs[qserver] = 0
            unique_users[qserver] = 0
            try:
                hostname = qserver.split('.')[0]
            except:
                hostname = ""
            for qname in qinfo[machine][qserver]:
                total_jobs[
                    qserver] += qinfo[machine][qserver][qname]['total_jobs']
                try:
                    unique_users[
                        qserver] += len(qstat_uniq_users[machine][qserver])
                except KeyError:
                    pass
            values[hostname]['jobs'] = total_jobs[qserver]
            values[hostname]['users'] = unique_users[qserver]

    return render_template('status/status.html',
                           services=spider_services,
                           values=values,
                           status=status,
                           show=msg)

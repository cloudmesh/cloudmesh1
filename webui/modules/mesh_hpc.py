from flask import Blueprint
from flask import render_template, request, redirect
from cloudmesh.config.cm_config import cm_config
from cloudmesh.cm_mongo import cm_mongo
from datetime import datetime
from cloudmesh.util.util import address_string
from pprint import pprint
from ast import literal_eval
from cloudmesh.pbs.pbs_mongo import pbs_mongo
from cloudmesh.util.util import cond_decorator
from flask.ext.login import login_required
import cloudmesh
from cloudmesh.pbs import tasks
from cloudmesh.config.ConfigDict import ConfigDict


from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

mesh_hpc_module = Blueprint('mesh_hpc_module', __name__)


# ============================================================
# ROUTE: /mesh/qstat
# ============================================================

@mesh_hpc_module.route('/mesh/refresh/qstat')
@mesh_hpc_module.route('/mesh/refresh/qstat/<host>')
@login_required
def display_mongo_qstat_refresh(host=None):
    celery_config = ConfigDict(filename="~/.futuregrid/cloudmesh_celery.yaml")
    log.info ("qstat refresh request {0}".format(host))
    timeout = 15;
    config = cm_config()
    user = config["cloudmesh"]["hpc"]["username"]
    pbs = pbs_mongo()
    if host is None:
        hosts = ["india.futuregrid.org",
                 "sierra.futuregrid.org",
                 "hotel.futuregrid.org",
                 "alamo.futuregrid.org"]
    else:
        hosts = [host]
    error = ""
    queue = celery_config = celery_config.get("cloudmesh.workers.qstat.queue")
    res = tasks.refresh_qstat.apply_async(queue=queue, priority=0, args=[hosts])
    try:
        error = res.get(timeout=timeout)
    except :
            return render_template('error.html',
                           error="Time out",
                           type="Some error in qstat",
                           msg="")
    if error != "":
        return render_template('error.html',
                               error=error,
                               type="Some error in qstat",
                               msg="")
    return redirect('mesh/qstat')


@mesh_hpc_module.route('/mesh/qstat/')
@login_required
def display_mongo_qstat_new():
    time_now = datetime.now()

    address_string = ""
    error = ""
    config = cm_config()
    user = config["cloudmesh"]["hpc"]["username"]

    pbs = pbs_mongo()
    hosts = ["india.futuregrid.org",
             "sierra.futuregrid.org",
             "hotel.futuregrid.org",
             "alamo.futuregrid.org"]
#    for host in hosts:
#        pbs.activate(host,user)


    data = {}
    jobcount = {}
    timer = {}
    for host in hosts:
        try:
            data[host] = pbs.get_qstat(host)
        except:
            error += "get_qstat({0})".format(host)
        try:
            jobcount[host] = data[host].count()
        except:
            error += "jobcount {0}".format(host)

        if jobcount[host] > 0:
            timer[host] = data[host][0]["cm_refresh"]
            # pprint(data[host][0])
        else:
            timer[host] = datetime.now()

    attributes = {"pbs":
                  [
                        [ "Queue" , "queue"],
                        # [ "Server" , "server"],
                        [ "State" , "job_state"],
                        [ "Name" , "Job_Name"],
                        [ "Owner" , "Job_Owner"],
                        [ "NCpus" , "Resource_List", "ncpus"],
                        [ "Walltime" , "Resource_List", "walltime"],
                        [ "Nodes" , "Resource_List", "nodes"],
                        [ "Nodect" , "Resource_List", "nodect"],
                        # [ "ctime", "ctime"],
                        [ "mtime", "mtime"],
                        [ "qtime", "qtime"],
                        [ "Used Cpu Time", "resources_used", 'cput'],
                        [ "Used Mem ", "resources_used", 'mem'],
                        [ "Used VMem ", "resources_used", 'vmem'],
                        [ "Used Cpu Walltime", "resources_used", 'walltime']
                  ],
                  }
    """
    for host in hosts:
        pprint (host)
        for server in data[host]:
            print "S", server
            for attribute in server:
                print attribute, server[attribute]
    """

    return render_template('mesh/hpc/mesh_qstat.html',
                           hosts=hosts,
                           jobcount=jobcount,
                           timer=timer,
                           address_string=address_string,
                           attributes=attributes,
                           updated=time_now,
                           qstat=data,
                           error=error,
                           config=config)




@mesh_hpc_module.route('/mesh/refresh/qinfo')
@mesh_hpc_module.route('/mesh/refresh/qinfo/<host>')
@login_required
def display_mongo_qinfo_refresh(host=None):
    log.info ("qinfo refresh request {0}".format(host))
    timeout = 15;
    config = cm_config()
    user = config["cloudmesh"]["hpc"]["username"]

    if host is None:
        hosts = ["india.futuregrid.org",
                 "sierra.futuregrid.org",
                 "hotel.futuregrid.org",
                 "alamo.futuregrid.org"]
    elif host in ['bravo.futuregrid.org',
                  'echo.futuregrid.org',
                  'delta.futuregrid.org']:
        hosts = ['india.futuregrid.org']
    else:
        hosts = [host]
    error = ""
    pbs = pbs_mongo()
    for h in hosts:
        pbs.activate(h, user)
        res = pbs.refresh_qinfo(h)

    return redirect('mesh/qinfo')



@mesh_hpc_module.route('/mesh/qinfo/')
@login_required
def display_mongo_qinfo():
    time_now = datetime.now()

    address_string = ""
    error = ""
    config = cm_config()
    user = config["cloudmesh"]["hpc"]["username"]

    pbs = pbs_mongo()
    hosts = ["india.futuregrid.org",
             "echo.futuregrid.org",
             "delta.futuregrid.org",
             "bravo.futuregrid.org",
             "sierra.futuregrid.org",
             "hotel.futuregrid.org",
             "alamo.futuregrid.org"]
#    for host in hosts:
#        pbs.activate(host,user)


    data = {}
    jobcount = {}
    timer = {}
    for host in hosts:
        timer[host] = datetime.now()
        try:
            data[host] = pbs.get_qinfo(host)
        except:
            log.error("get_qinfo {0}".format(host))
            error += "get_qinfo({0})".format(host)
        try:
            jobcount[host] = data[host].count()
            if jobcount[host] > 0:
                timer[host] = data[host][0]["cm_refresh"]
                # pprint(data[host][0])
            else:
                timer[host] = datetime.now()

        except:
            error += "jobcount {0}".format(host)


    attributes = {"pbs":
                  [
                        [ "Queue" , "queue"],
                        # [ "Server" , "server"],
                        [ "State" , "started"],
                        [ "Type" , "queue_type"],
                        [ "Walltime" , "resources_default_walltime"],
                        [ "Total" , "total_jobs"],
                        [ "Exiting" , "state_count", "Exiting"],
                        [ "Held" , "state_count", "Held"],
                        [ "Queued", "state_count", "Queued"],
                        [ "Running", "state_count", "Running"],
                        [ "Transit" , "state_count", "Transit"],
                        [ "Waiting" , "state_count", "Waiting"],
                  ],
                  }
    """
    for host in hosts:
        pprint (host)
        for server in data[host]:
            print "S", server
            for attribute in server:
                print attribute, server[attribute]
    """

    return render_template('mesh/hpc/mesh_qinfo.html',
                           hosts=hosts,
                           jobcount=jobcount,
                           timer=timer,
                           address_string=address_string,
                           attributes=attributes,
                           updated=time_now,
                           qinfo=data,
                           error=error,
                           config=config)


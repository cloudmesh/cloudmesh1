from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.config.cm_config import cm_config
from cloudmesh.pbs import tasks
from cloudmesh.pbs.pbs_mongo import pbs_mongo
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.util import address_string, cond_decorator
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, flash
from flask.ext.login import login_required
from pprint import pprint
import cloudmesh
from flask.ext.principal import Permission, RoleNeed
import traceback
from cloudmesh_install import config_file

log = LOGGER(__file__)

admin_permission = Permission(RoleNeed('admin'))

mesh_hpc_module = Blueprint('mesh_hpc_module', __name__)


# ============================================================
# ROUTE: /mesh/qstat
# ============================================================

error = ""

@mesh_hpc_module.route('/mesh/hpc/login')
@login_required
def hpc_login():
    return render_template('/mesh/hpc/login.html')


@mesh_hpc_module.route('/mesh/refresh/qstat')
@mesh_hpc_module.route('/mesh/refresh/qstat/<host>')
@login_required
def display_mongo_qstat_refresh(host=None):
    celery_config = ConfigDict(filename=config_file("/cloudmesh_celery.yaml"))
    log.info ("qstat refresh request {0}".format(host))

    # timeout = 15;

    config = cm_config()
    user = config["cloudmesh"]["hpc"]["username"]


    if host is None:
        hosts = ["india.futuregrid.org",
                 "lima.futuregrid.org",
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

    try:
        pbs = pbs_mongo()

        # queue = celery_config = celery_config.get("cloudmesh.workers.qstat.queue")
        # res = tasks.refresh_qstat.apply_async(queue=queue, priority=0, args=[hosts])
        for host in hosts:

            pbs.activate(host, user)
            log.info("refresh qstat: {0} {1}".format(host, user))
            pbs.refresh_qstat(host)

    #    error = res.get(timeout=timeout)
    except Exception, e:

        print traceback.format_exc()
        error = "{0}".format(e)
        log.error(error)

        category = "qstat-{0}".format(host)
        flash(error, category=str(category))

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
             "echo.futuregrid.org",
             "delta.futuregrid.org",
             "bravo.futuregrid.org",
             "sierra.futuregrid.org",
             "hotel.futuregrid.org",
             "lima.futuregrid.org",
             "alamo.futuregrid.org"]
    #hosts = ["india.futuregrid.org",
    #         "lima.futuregrid.org",
    #         "sierra.futuregrid.org",
    #         "hotel.futuregrid.org",
    #         "alamo.futuregrid.org"]

    #    for host in hosts:
    #        pbs.activate(host,user)


    data = {}
    jobcount = {}
    timer = {}
    for host in hosts:
        timer[host] = datetime.now()        
        try:
            data[host] = pbs.get_qstat(host)
        except:
            log.error("get_qstat {0}".format(host))
            error += "get_qstat({0})".format(host)
        try:
            jobcount[host] = data[host].count()
        except:
            error += "jobcount {0}".format(host)
            log.error("jobcount {0}".format(host))
            
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
                 "lima.futuregrid.org",
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

    try:
        pbs = pbs_mongo()

        
        for host in hosts:
            pbs.activate(host, user)
            res = pbs.refresh_qinfo(host)
    except Exception, e:

        print traceback.format_exc()
        error = "{0}".format(e)
        log.error(error)

        category = "qinfo-{0}".format(host)
        flash(error, category=str(category))

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
             "lima.futuregrid.org",
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


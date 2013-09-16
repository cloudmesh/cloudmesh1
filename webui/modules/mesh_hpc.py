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
mesh_hpc_module = Blueprint('mesh_hpc_module', __name__)

# ============================================================
# ROUTE: /mesh/qstat
# ============================================================

@mesh_hpc_module.route('/mesh/refresh/qstat')
@mesh_hpc_module.route('/mesh/refresh/qstat/<host>')
@cond_decorator(cloudmesh.with_login, login_required)
def display_mongo_qstat_refresh(host=None):
    print "recieved refresh request ===========", host
    timeout = 300;
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
    res = tasks.refresh_qstat.apply_async(queue="questat", priority=0, args=[hosts])
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
@cond_decorator(cloudmesh.with_login, login_required)
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
            print"101010101010101001010101001"
            # print data[host]
        except:
            error += "get_qstat({0})".format(host)
        try:

            print "DDD", host, data[host].count()
            jobcount[host] = data[host].count()
        except:
            error += "jobcount {0}".format(host)

        if jobcount[host] > 0:
            timer[host] = data[host][0]["cm_refresh"]
            print timer
            print "TTTTT"
            pprint(data[host][0])
            # timer[host] = datetime.now()
        else:
            timer[host] = datetime.now()
        # print "TIMER", timer
    attributes = {"pbs":
                  [
                        [ "Queue" , "queue"],
                        [ "Server" , "server"],
                        [ "State" , "job_state"],
                        [ "Name" , "Job_Name"],
                        [ "Owner" , "Job_Owner"],
                        [ "NCpus" , "Resource_List", "ncpus"],
                        [ "Walltime" , "Resource_List", "walltime"],
                        [ "Nodes" , "Resource_List", "nodes"],
                        [ "Nodect" , "Resource_List", "nodect"],
                        [ "Walltime" , "Resource_List", "walltime"],
                        [ "ctime", "ctime"],
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

    return render_template('qstat_mesh.html',
                           hosts=hosts,
                           jobcount=jobcount,
                           timer=timer,
                           address_string=address_string,
                           attributes=attributes,
                           updated=time_now,
                           qstat=data,
                           error=error,
                           config=config)

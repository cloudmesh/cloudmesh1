from cloudmesh_task.tasks import cm_ssh
from cloudmesh_task.parallel import Parallel, Sequential
from cloudmesh.util.stopwatch import StopWatch
from cloudmesh_common.util import banner
from pprint import pprint

hosts = ["hotel.futuregrid.org",
        "india.futuregrid.org",
         "sierra.futuregrid.org",
         "alamo.futuregrid.org"]


task = {}

watch = StopWatch()
"""


banner("SEQUENTIAL")

watch.start("sequential")
#for host in hosts:
#    print host
#    task[host] = cm_ssh(username="gvonlasz",
#                          host=host,
#                          command="qstat")
result = Sequential(hosts, cm_ssh, username="gvonlasz", command="qstat")
watch.stop("sequential")

for host in hosts:
    banner(host)
    if result[host]["error"]:
        pprint (result[host]["error"])
    print result[host]["output"]
"""
    
banner("ASYNCHRONOUS")
task = {}

watch.start("parallel")
#for host in hosts:
#    print host
#    task[host] = cm_ssh.delay(username="gvonlasz",
#                                host=host,
#                                command="qstat")

task = Parallel(hosts, cm_ssh, username="gvonlasz", command="qstat")
print "gather results"
banner("PRINT")
watch.stop("parallel")

for host in hosts:
    banner(host)
    print task[host]["result"]

for timer in ["parallel", "sequential"]:
    print timer, watch.get(timer), "s"



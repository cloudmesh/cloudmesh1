from cloudmesh_task.tasks import cm_ssh
from cloudmesh_task.parallel import Parallel, Sequential
from cloudmesh.util.stopwatch import StopWatch
from cloudmesh_common.util import banner
from pprint import pprint
from cloudmesh.config.cm_config import cm_config


username = cm_config().get("cloudmesh.hpc.username")
print "USERNAME:", username

hosts = []

hosts.append("india.futuregrid.org")
hosts.append("hotel.futuregrid.org")
hosts.append("sierra.futuregrid.org")
hosts.append("alamo.futuregrid.org")        

task = {}

watch = StopWatch()

f = Sequential
for execute in [Sequential, Parallel]:

    name = execute.__name__

    banner(name)
    watch.start(name)

    result = execute(hosts, cm_ssh, username=username, command="qstat")

    watch.stop(name)

    pprint(result)
    
    banner("PRINT")        
    for host in result:
        print result[host]["output"]
    

for timer in watch.keys():
    print timer, watch.get(timer), "s"



"""    
######################################################################
banner("SEQUENTIAL")
######################################################################

watch.start("sequential")
#for host in hosts:
#    print host
#    task[host] = cm_ssh(username=username,
#                          host=host,
#                          command="qstat")
result = Sequential(hosts, cm_ssh, username=username, command="qstat")

pprint(result)
watch.stop("sequential")


######################################################################    
banner("ASYNCHRONOUS")
######################################################################
task = {}

watch.start("parallel")
#for host in hosts:
#    print host
#    task[host] = cm_ssh.delay(username=username,
#                                host=host,
#                                command="qstat")

result = Parallel(hosts, cm_ssh, username=username, command="qstat")
print "gather results"
watch.stop("parallel")

"""

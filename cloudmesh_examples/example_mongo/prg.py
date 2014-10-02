from cloudmesh_task.tasks import cm_ssh
from cloudmesh_task.parallel import Parallel, Sequential
from cloudmesh.util.stopwatch import StopWatch
from cloudmesh import banner
from pprint import pprint
from cloudmesh.config.cm_config import cm_config
from cloudmesh.config.ConfigDict import ConfigDict
import sys

config = ConfigDict(
    filename="~/.cloudmesh/cloudmesh_hpc.yaml")["cloudmesh"]["hpc"]

print config


#hosts = []
# hosts.append("localhost")
# hosts.append("bigred2.uits.iu.edu")
# hosts.append("india.futuregrid.org")

def get_credentials(hosts):
    credential = {}
    for host in hosts:
        credential[host] = config[host]['username']
    return credential


hosts = config.keys()

credentials = get_credentials(hosts)


task = {}

watch = StopWatch()


for execute in [Sequential, Parallel]:
    # for execute in [Sequential]:
    # for execute in [Parallel]:

    name = execute.__name__

    banner(name)
    watch.start(name)

    result = execute(credentials, cm_ssh, command="qstat")

    watch.stop(name)

    pprint(result)

    banner("PRINT")
    for host in result:
        print result[host]["output"]


for timer in watch.keys():
    print timer, watch.get(timer), "s"

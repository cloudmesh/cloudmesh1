from __future__ import with_statement
import fabric
from fabric.api import task, local, hide, settings
import clean
import mq
import time
import hostlist
from pprint import pprint
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh_common.util import banner
from cloudmesh.provisioner.queue.celery import celery_provisiner_queue as p_queue
from cloudmesh.launcher.queue.celery import celery_launcher_queue as l_queue
from cloudmesh.pbs.celery import celery_pbs_queue as pbs_queue
from celery import Celery
from cloudmesh_install import config_file
from cloudmesh_common.util import PROGRESS
from cloudmesh.config.cm_config import cm_config_server 

progress_queue = PROGRESS('Cloudmesh Queue Services', 13)

__all__ = ['start', 'stop', 'list', 'clean', 'gui',
           'monitor', 'kill', 'ls', 'lspbs', 'flower_server']

celery_config = ConfigDict(
    filename=config_file("/cloudmesh_celery.yaml"), kind="worker")
workers = celery_config.get("cloudmesh.workers")

debug = True
try:
    debug = cm_config_server().get("cloudmesh.server.debug")
except:
    pass

fabric.state.output.debug  = debug
fabric.state.output.running  = debug
fabric.state.output.status  = debug
fabric.state.output.stdout  = True
fabric.state.output.stderr  = debug
fabric.state.output.warnings  = debug
fabric.state.output.aborts  = debug
fabric.state.output.user  = debug

"""
for worker in workers:
    workers[worker] = {"app":"cloudmesh.launcher{0}.queue",
                       "hostlist":hostlist.expand_hostlist("l[1-{0}]".format(workers[worker])),
                      "queue": worker}
"""
# no_workers_launcher =
for worker in workers:
    workers[worker]["hostlist"] = hostlist.expand_hostlist(
        "{0}[1-{1}]".format(workers[worker]["id"], workers[worker]["count"]))

# launcher_workers = {"app":"cloudmesh.launcher.queue",
#                     "hostlist":hostlist.expand_hostlist("l[1-{0}]".format(workers["launcher"]["count"])),
#                     "queue":"launcher"}
#
# provisioner_workers = {"app":"cloudmesh.provisioner.queue",
#                        "hostlist":hostlist.expand_hostlist("p[1-2]"),
#                        "queue":"provisioner"}
#
# questat_workers = {"app":"cloudmesh.pbs",
#                    "hostlist":['q1'],
#                    "queue":"questat",
#                    "concurrency":1}


@task
def kill():
    stop()
    with settings(warn_only=True):
        with hide('output', 'running', 'warnings'):
            local("killall mongod")
            local("killall python")


@task
def flower_server():
    """start the flower celery gui"""
    flower_port = 5556

#    try:
#        with settings(warn_only=True):
#            with hide('output', 'running', 'warnings'):
#                local("ps auxww | grep 'flower' | awk '{print $2}' | xargs kill -9")
#    except:
#        print "no flower running"

    try:
        with settings(warn_only=True):
            local("flower --port={0} &".format(flower_port))
        time.sleep(1)
    except:
        print "could not start flower"


@task
def flower_gui():
    """start the flower celery gui"""
    # server_config = cm_config_server()
    # port = cm_config_server().get("cloudmesh.server.webui.port")
    # host = cm_config_server().get("cloudmesh.server.webui.host")

    # local("open http://{0}:{1}".format(host, port))

    flower_port = 5556
    flower_host = "localhost"
    local("open http://{0}:{1}".format(flower_host, flower_port))


@task
def gui():
    """start the flower celery gui"""
    flower_server()
    flower_gui()


@task
def monitor():
    """provide some information about celery"""
    local("celery worker -l info -Q celery")


def celery_command(command, app, workers, queue, concurrency=None):
    """execute the celery command on the application and workers specified"""
    progress_queue.next()
    worker_str = " ".join(workers)
    exec_string = "celery multi {0} {1} -A {2} -l info -Q {3}".format(
        command, worker_str, app, queue)
    # directories for log and pid file
    celery_dir = "celery"
    local("mkdir -p %s" % celery_dir)
    exec_string += " --pidfile=\"{0}/%n.pid\" ".format(celery_dir)
    exec_string += " --logfile=\"{0}/%n.log\" ".format(celery_dir)
    if concurrency is not None:
        exec_string += " --concurrency={0}".format(concurrency)
    local(exec_string, capture=not debug)
    # print "celery multi {0} {1} -A {2} -l info".format(command, worker_str,
    # app)


@task
def start(view=None):
    """start the celery server

    :param: if view is set to any value start also rabit and attach
            to it so we can see the log
    """
    #pprint (fabric.state.output)
    with settings(warn_only=True):
        stop()
        time.sleep(2)
        progress_queue.next()
        mq.start()
        progress_queue.next()
        time.sleep(2)
        progress_queue.next()

        for worker in workers:
            progress_queue.next()
            concurrency = None
            if "concurrency" in workers[worker]:
                concurrency = workers[worker]["concurrency"]
            # print worker, ":   ", str(workers[worker])
            celery_command("start", workers[worker]["app"],
                           workers[worker]["hostlist"], workers[
                               worker]["queue"],
                           concurrency=concurrency)

    if view is None:
        progress_queue.next()
        time.sleep(2)
        print
        # local("celery worker --app={0} -l info".format(app))
        # local("celery worker -l info".format(app))


@task
def stop():
    """stop the workers"""
    for worker in workers:
        celery_command("stop", workers[worker]["app"], workers[
                       worker]["hostlist"], workers[worker]["queue"])
    mq.stop()
    clean()


@task
def clean():
    """stop celery and clean up"""
    with settings(warn_only=True):
        with hide('output', 'running', 'warnings'):
            local("ps auxww | "
                  "grep 'celery worker' | "
                  "awk '{print $2}' | "
                  "xargs kill -9")

        local("rm -f celeryd@*")


@task
def list():
    """list the workers"""
    with hide('output', 'running'):
        result = local(
            "ps auxww | grep 'celery worker' ", capture=True).split("\n")
    for line in result:
        if "grep" not in line:
            print line


@task
def ls():
    print p_queue

    banner("Dict")
    pprint(p_queue.__dict__)

    i = p_queue.control.inspect()
    c = p_queue.control
    banner("Active Queues")
    pprint(i.active_queues())
    banner("Registered")
    pprint(i.registered())
    banner("Active")
    pprint(i.active())
    banner("Scheduled")
    pprint(i.scheduled())
    banner("Reserved")
    pprint(i.reserved())
    # banner("Revoked")
    # pprint (i.resoked())
    banner("Stats")
    pprint(i.stats())

    banner("Ping")
    pprint(c.ping(timeout=0.5))


@task
def lspbs():
    print pbs_queue

    banner("Dict")
    pprint(pbs_queue.__dict__)

    i = pbs_queue.control.inspect()
    c = pbs_queue.control
    banner("Active Queues")
    pprint(i.active_queues())
    banner("Registered")
    pprint(i.registered())
    banner("Active")
    pprint(i.active())
    banner("Scheduled")
    pprint(i.scheduled())
    banner("Reserved")
    pprint(i.reserved())
    # banner("Revoked")
    # pprint (i.resoked())
    banner("Stats")
    pprint(i.stats())

    banner("Ping")
    pprint(c.ping(timeout=0.5))


@task
def lsl():
    print pbs_queue

    banner("Dict")
    pprint(l_queue.__dict__)

    i = l_queue.control.inspect()
    c = l_queue.control
    banner("Active Queues")
    pprint(i.active_queues())
    banner("Registered")
    pprint(i.registered())
    banner("Active")
    pprint(i.active())
    banner("Scheduled")
    pprint(i.scheduled())
    banner("Reserved")
    pprint(i.reserved())
    # banner("Revoked")
    # pprint (i.resoked())
    banner("Stats")
    pprint(i.stats())

    banner("Ping")
    pprint(c.ping(timeout=0.5))

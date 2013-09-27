from __future__ import with_statement
from fabric.api import task, local, execute, hide, settings
import clean
import mq
import time
import hostlist
from pprint import pprint

from cloudmesh.util.util import banner
from cloudmesh.provisioner.queue.celery import celery as p_queue
from celery import Celery

__all__ = ['start', 'stop', 'list', 'clean', 'gui', 'monitor', 'kill', 'ls']

# app="cloudmesh.provisioner.queue"


workers = {"launcher": {"count": "2"},
           "provisioner": {"count":"2"},
           "qstat": {"count": "1", "councurrency": 1}
           }

"""
for worker in workers:
    workers[worker] = {"app":"cloudmesh.launcher{0}.queue", 
                    "hostlist":hostlist.expand_hostlist("l[1-{0}]".format(workers[worker])), 
                    "queue": worker}


"""

# no_workers_launcher =


launcher_workers = {"app":"cloudmesh.launcher.queue",
                    "hostlist":hostlist.expand_hostlist("l[1-{0}]".format(workers["launcher"]["count"])),
                    "queue":"launcher"}

provisioner_workers = {"app":"cloudmesh.provisioner.queue",
                       "hostlist":hostlist.expand_hostlist("p[1-2]"),
                       "queue":"provisioner"}

questat_workers = {"app":"cloudmesh.pbs",
                   "hostlist":['q1'],
                   "queue":"questat",
                   "concurrency":1}

worker_list = [provisioner_workers, launcher_workers, questat_workers];
@task
def kill():
    stop()
    with settings(warn_only=True):
        with hide('output', 'running', 'warnings'):
            local("killall mongod")
            local("killall python")

@task
def gui():
    """start the flower celery gui"""
    local("celery flower &")
    time.sleep(1)
    local("open http://localhost:5555")

@task
def ls():
    print p_queue

    banner("Dict")
    pprint (p_queue.__dict__)

    i = p_queue.control.inspect()
    c = p_queue.control
    banner("Active Queues")
    print i.active_queues()
    banner("Registered")
    print i.registered()
    banner("Active")
    print i.active()
    banner("Scheduled")
    print i.scheduled()
    banner("Reserved")
    print i.reserved()

    banner("Ping")
    print c.ping(timeout=0.5)


@task
def monitor():
    """provide some information about celery"""
    local("celery worker -l info -Q celery")

def celery_command(command, app, workers, queue, concurrency=None):
    """execute the celery command on the application and workers specified"""

    worker_str = " ".join(workers)
    exec_string = "celery multi {0} {1} -A {2} -l info -Q {3}".format(command, worker_str, app, queue)
    if concurrency != None:
        exec_string += " --concurrency={0}".format(concurrency)
    local(exec_string)
    # print "celery multi {0} {1} -A {2} -l info".format(command, worker_str, app)

@task
def start(view=None):
    """start the celery server
    :param: if view is set to any value start also rabit and attach to it so we can see the log
    """
    with settings(warn_only=True):
        stop()
        time.sleep(2)
        mq.start()
        time.sleep(2)

        for worker in worker_list:
            concurrency = None;
            if "concurrency" in worker:
                concurrency = worker["concurrency"]
            celery_command("start", worker["app"],
                           worker["hostlist"], worker["queue"],
                           concurrency=concurrency)

    if view is None:
        time.sleep(2)
        # local("celery worker --app={0} -l info".format(app))
        # local("celery worker -l info".format(app))
@task
def stop():
    """stop the workers"""
    for worker in worker_list:
        celery_command("stop", worker["app"], worker["hostlist"], worker["queue"])
    mq.stop()
    clean()

@task
def clean():
    """stop celery and clean up"""
    with settings(warn_only=True):
        with hide('output', 'running', 'warnings'):
            local("ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9")

        local("rm -f celeryd@*")


@task
def list():
    """list the workers"""
    with hide('output', 'running'):
        result = local("ps auxww | grep 'celery worker' ", capture=True).split("\n")
    for line in result:
        if "grep" not in line:
            print line


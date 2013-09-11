from __future__ import with_statement
from fabric.api import task, local, execute, hide,settings
import clean
import mq
import time
import hostlist
__all__ = ['start', 'stop', 'list', 'clean','gui','monitor', 'kill']

app="cloudmesh.provisioner.queue"

launcher_workers = {"app":"cloudmesh.launcher.queue", "hostlist":hostlist.expand_hostlist("l[1-2]")}
provisioner_workers = {"app":"cloudmesh.provisioner.queue", "hostlist":hostlist.expand_hostlist("p[1-2]")}

@task
def kill():
    stop()
    with settings(warn_only=True):
        with hide('output','running','warnings'):  
            local("killall mongod")
            local("killall python")

@task
def gui():
    """start the flower celery gui"""
    local("celery flower &")
    time.sleep(1)
    local("open http://localhost:5555")

@task
def monitor():
    """provide some information about celery"""
    local("celery worker -l info -Q celery")

def celery_command(command, app, workers):
    """execute the celery command on the application and workers specified"""

    worker_str = " ".join(workers)
    local("celery multi {0} {1} -A {2} -l info".format(command, worker_str, app))
    print "celery multi {0} {1} -A {2} -l info".format(command, worker_str, app)
    
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
        celery_command("start", launcher_workers["app"], launcher_workers["hostlist"])
        celery_command("start", provisioner_workers["app"], provisioner_workers["hostlist"])
    if view is None:
        time.sleep(2)
        #local("celery worker --app={0} -l info".format(app))
        local("celery worker -l info".format(app))
@task
def stop():
    """stop the workers"""

    celery_command("stop", launcher_workers["app"], launcher_workers["hostlist"])
    celery_command("stop", provisioner_workers["app"], provisioner_workers["hostlist"])
    mq.stop()
    clean()

@task
def clean():
    """stop celery and clean up"""
    with settings(warn_only=True):
        with hide('output','running','warnings'):  
            local("ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9")
        
        local("rm -f celeryd@*")

    
@task
def list():
    """list the workers"""
    with hide('output','running'):
        result = local("ps auxww | grep 'celery worker' ", capture=True).split("\n")
    for line in result:
        if "grep" not in line:
            print line


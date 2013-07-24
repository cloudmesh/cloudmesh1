from __future__ import with_statement
from fabric.api import task, local, execute, hide,settings
import clean
import mq
import time
import hostlist
__all__ = ['start', 'stop', 'list', 'clean','gui','monitor']

app="cloudmesh.provisioner.queue"

workers = hostlist.expand_hostlist("w[1-2]")

@task
def gui():
    """start the flower celery gui"""
    local("celery flower")
    time.sleep(1)
    local("open http://localhost:5555")

@task
def monitor():
    """provide some information about celery"""
    local("celery worker -l info -Q celery")

def celery_command(command, app, workers):
    """execute the celery command on the application and workers specified"""
    local("celery multi {0} {1} -A {2} -l info".format(command, workers, app))
    
@task
def start(view=None):
    """start the celery server
    :param: if view is set to any value start also rabit and attach to it so we can see the log
    """
    if view is None:
        # if rabit is not running 
        mq.start()
        celery_command("start", app, workers)
    else:
        local("celery worker --app={0} -l info".format(app))
@task
def stop():
    """stop the workers"""
    celery_command("stop", app, workers)
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


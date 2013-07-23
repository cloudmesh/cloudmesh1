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
    local("celery flower")
    time.sleep(1)
    local("open http://localhost:5555")

@task
def monitor():
    local("celery worker -l info -Q celery")

def celery_command(command, app, workers):
    local("celery multi {0} {1} -A {2} -l info".format(command, workers, app))
    
@task
def start(view=None):
    if view is None:
        # if rabit is not running 
        mq.start()
        celery_command("start", app, workers)
    else:
        local("celery worker --app={0} -l info".format(app))
@task
def stop():
    celery_command("stop", app, workers)
    mq.stop()
    clean()

@task
def clean():
    with settings(warn_only=True):
        with hide('output','running','warnings'):  
            local("ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9")
        
    local("rm -f celeryd@*")

    
@task
def list():
    with hide('output','running'):
        result = local("ps auxww | grep 'celery worker' ", capture=True).split("\n")
    for line in result:
        if "grep" not in line:
            print line


from fabric.api import task, local, execute
import clean
import mq

__all__ = ['start', 'stop', 'list']


workers = 'w1 w2'



def celery_command(command, app, workers):
    local("celery multi {0} {1} -A {2} -l info".format(command, workers, app))
    
@task
def start():
    # if rabit is not running 
    #  mq.start()
    celery_command("start", "queue", workers)
    
@task
def stop():
    celery_command("stop", "queue", workers)


@task
def clean():
    local("ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9")

    
@task
def list():
    result = local("ps auxww | grep 'celery worker' ", capture=True).split("\n")
    for line in result:
        if "grep" not in line:
            print line




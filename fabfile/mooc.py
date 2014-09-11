from fabric.api import task, local, execute, hide, settings
from fabric.contrib.console import confirm


@task
def start():
    local("fab server.start:server=mooc,mooc")


def stop():
    local("fab server.stop")

from fabric.api import task, local


@task
def start():
    local("fab server.start:server=mooc,mooc")


def stop():
    local("fab server.stop")

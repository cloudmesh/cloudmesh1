from fabric.api import task, local


@task
def random():
    """creting random users and projects"""
    local("python cloudmesh/management/generate.py")


@task
def mongo():
    local("make -f cloudmesh/management/Makefile mongo")

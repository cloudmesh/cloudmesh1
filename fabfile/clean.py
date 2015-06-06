from fabric.api import task, local
from cloudmesh_admin.Clean import Clean


@task
def dir():
    """clean the dirs"""
    Clean.dir()


@task
def cmd3():
    Clean.cmd3()


@task
def all():
    """clean the dis and uninstall cloudmesh"""
    Clean.all()



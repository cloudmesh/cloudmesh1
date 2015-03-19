from fabric.api import task, local
from cloudmesh_base.util import banner
from cloudmesh_base.locations import config_file
import server

import os


@task
def dir():
    """clean the dirs"""
    banner("STOPPING SERVER")
    server.stop()
    banner("CLEAN DIR")
    local("rm -rf *.egg")
    local('find . -name "*~" -exec rm {} \;  ')
    local('find . -name "*.pyc" -exec rm {} \;  ')
    local("rm -rf build dist *.egg-info *~ #*")
    # local("cd docs; make clean")
    local("rm -rf *.egg-info")
    local("rm -f celeryd@*")
    local("rm -f *.dump")


@task
def cmd3():
    banner("CLEAN CMD3")
    local("rm -rf {0}".format(config_file("/cmd3local")))


@task
def all():
    """clean the dis and uninstall cloudmesh"""
    dir()
    cmd3()
    banner("CLEAN PREVIOUS CLOUDMESH INSTALLS")
    delete_package("cloudmesh")
    delete_package("cloudmesh_cmd3")
    delete_package("cloudmesh_common")
    delete_package("cloudmesh_install")


def delete_package(name):
    banner("CLEAN PREVIOUS {0} INSTALLS".format(name))
    r = int(local("pip freeze |fgrep {0} | wc -l".format(name), capture=True))
    while r > 0:
        local('echo "y" | pip uninstall {0}'.format(name))
        r = int(
            local("pip freeze |fgrep {0} | wc -l".format(name), capture=True))

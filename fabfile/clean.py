from fabric.api import task, local
from cloudmesh_common.util import banner
from cloudmesh_install import config_file

@task
def dir():
    """clean the dirs"""
    banner("CLEAN DIR")
    local("rm -rf *.egg")
    local('find . -name "*~" -exec rm {} \;  ')
    local('find . -name "*.pyc" -exec rm {} \;  ')
    local("rm -rf build doc/build dist *.egg-info *~ #*")
    local("cd doc; make clean")
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
    r = int(local("pip freeze |fgrep cloudmesh | wc -l", capture=True))
    while r > 0:
        local('echo "y\n" | pip uninstall cloudmesh')
        r = int(local("pip freeze |fgrep cloudmesh | wc -l", capture=True))

from fabric.api import task, local
from cloudmesh_base.util import banner
from cloudmesh_base.locations import config_file
import os
from cloudmesh_base.Shell import Shell


@task
def dir():
    """clean the dirs"""
    banner ("clean the directory")
    commands='''
        find . -name \"#*\" -exec rm {} \\;
        find . -name \"*~\" -exec rm {} \\;
        find . -name \"*.pyc\" -exec rm {} \\;
    '''.split("\n")
    for command in commands:
        command = command.strip()
        if command != "":
            print "Executing:", command
            os.system(command)
    Shell.rm("-rf", "build", "dist", "*.egg-info")
    Shell.rm("-rf", "docs/build", "dist", "*.egg-info")
    Shell.rm("-f", "celeryd@*")
    Shell.rm("-f", "*.dump")
    Shell.rm("-f", "*.egg")


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
    delete_package("cmd3")
    delete_package("cloudmesh_base")


def delete_package(name):
    try:
        banner("CLEAN PREVIOUS {0} INSTALLS".format(name))
        r = int(local("pip freeze |fgrep {0} | wc -l".format(name), capture=True))
        while r > 0:
            local('echo "y" | pip uninstall {0}'.format(name))
            r = int(
                local("pip freeze |fgrep {0} | wc -l".format(name), capture=True))
    except:
        print "ERROR: uninstalling", name
from fabric.api import task, local
from cloudmesh_base.util import banner
from cloudmesh_base.locations import config_file


def kill(server="server", debug=True):
    """kills all server processes """
    with settings(warn_only=True):
        execute_command("STOP MONGO", "fab mongo.stop", debug=debug)
        result = local(
            'ps -ax | fgrep "python {0}.py" | fgrep -v fgrep'.format(server), capture=True).split("\n")
        for line in result:
            if line is not '':
                pid = line.split(" ")[0]
                local("kill -9 {0}".format(pid))
                # local("fab queue.stop")
@task
def dir():
    """clean the dirs"""
    banner("STOPPING SERVER")
    kill()
    banner("CLEAN DIR")
    local("rm -rf *.egg")
    local('find . -name "*~" -exec rm {} \;  ')
    local('find . -name "*.pyc" -exec rm {} \;  ')
    local("rm -rf build dist *.egg-info *~ #*")
    # local("cd docs; make clean")
    local("rm -rf *.egg-info")
    local("rm -f celeryd@*")
    local("rm -f *.dump")
    sys.exit()


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

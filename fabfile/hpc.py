from fabric.api import task, local
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh_install import config_file


@task
def touch(username=None):
    """clean the dirs"""
    if username is None:
        # bug for some reason the get method does not work
        # useranme = ConfigDict(filename=config_file("/cloudmesh.yaml")).get("cloudmesh.hpc.username")
        username = ConfigDict(
            filename=config_file("/cloudmesh.yaml"))["cloudmesh"]["hpc"]["username"]
        print "Username: ", username
    for host in ["india", "sierra", "alamo", "hotel", "foxtrot"]:
        local("ssh %s@%s.futuregrid.org hostname -a" % (username, host))


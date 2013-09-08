from fabric.api import task, local
from cloudmesh.config.ConfigDict import ConfigDict

def get_server_config():   
    return ConfigDict(filename="~/.futuregrid/cloudmesh_server.yaml")

def get_user_config():   
    return ConfigDict(filename="~/.futuregrid/cloudmesh.yaml")

@task
def open(user,host,port):
    """clean the dirs"""
    local("ssh -L {2}:{1}:{2} {0}@{1}".format(user,host,port))

@task
def ldap(host=None):
    config = get_user_config()
    user = config.get("cloudmesh.hpc.username")
    open(user, host, 636)
    
@task
def flask():
    config = get_user_config()
    user = config.get("cloudmesh.hpc.username")
    open(user,"cloudmesh.futuregrid.org",5000)
    
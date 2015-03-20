from fabric.api import task, local, settings, hide
from cloudmesh_base.ConfigDict import ConfigDict
from cloudmesh.config.cm_config import cm_config_server
from sh import kill
from sh import sudo
from cloudmesh_base.locations import config_file


def get_server_config():
    return ConfigDict(filename=config_file("/cloudmesh_server.yaml"))


def get_user_config():
    return ConfigDict(filename=config_file("/cloudmesh.yaml"))


@task
def open(user, host, port, proxyhost, proxyuser, sudo=True):
    """clean the dirs"""
    if sudo:
        local(
            "sudo ssh -L {2}:{1}:{2} {4}@{3}".format(user, host, port, proxyhost, proxyuser))
    else:
        local(
            "ssh -L {2}:{1}:{2} {4}@{3}".format(user, host, port, proxyhost, proxyuser))


@task
def ldap(host=None):
    config_server = get_server_config()
    config_user = get_user_config()
    user = config_user.get("cloudmesh.hpc.username")
    ldaphost = config_server.get("cloudmesh.server.ldap.hostname")
    ldapproxyhost = config_server.get("cloudmesh.server.ldap.proxyldap")
    proxyuser = config_server.get("cloudmesh.server.ldap.proxyuser")
    proxyhost = config_server.get("cloudmesh.server.ldap.proxyhost")
    port = 389

    command = "sudo ssh -f -N -L {1}:{0}:{1} {2}@{3}".format(
        ldapproxyhost, port, proxyuser, proxyhost)

    print "STARTING LDAP TUNNEL"
    print "   ", command

    local(command)


@task
def kill():
    with settings(warn_only=True):
        with hide('output', 'running', 'warnings'):
            procs = local(
                'ps -j -ax -u root -o pid | fgrep ssh | fgrep 389', capture=True).split("\n")

    if procs != ['']:

        for proc in procs:
            columns = proc.split()
            pid = columns[1]
            print "Killing", proc
            sudo.kill("-9", "{0}".format(pid))
        print "SUCCESS. tunnel killed"
    else:
        print "WARNING: no tunnel were running"


@task
def flask():
    config = get_user_config()
    user = config.get("cloudmesh.hpc.username")
    server_config = cm_config_server()
    port = cm_config_server().get("cloudmesh.server.webui.port")
    host = cm_config_server().get("cloudmesh.server.webui.host")

    open(user, host, port)

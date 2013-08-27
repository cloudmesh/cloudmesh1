from fabric.api import task, local, settings
from pprint import pprint
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh.user.cm_userLDAP import cm_userLDAP
from cloudmesh.pbs.pbs_mongo import pbs_mongo

import sys

@task
def start():
    path = cm_config_server().get()["mongo"]["path"]
    port = cm_config_server().get()["mongo"]["port"]
    local("mkdir -p {0}".format(path))
    local("mongod --fork --dbpath {0} --port {1}".format(path, port))

@task
def stop():
    # for some reason shutdown does not work
    # local("mongod --shutdown")
    with settings(warn_only=True):
        pid = local("ps -ax |fgrep mongo | fgrep '??'", capture=True).split(" ")[0]
        local ("kill -9 {0}".format(pid))

@task
def clean():
    local("make clean")
    result = local('echo "show dbs" | mongo --quiet ', capture=True).splitlines()
    for line in result:
        name = line.split()[0]
        local('mongo {0} --eval "db.dropDatabase();"'.format(name))

@task
def vms_find():
    c = cm_mongo()
    c.activate()
    pprint (c.servers())
    
@task
def cloud():
    clean()
    c = cm_mongo()
    c.activate()
    c.refresh(types=['users', 'servers', 'images', 'flavors'])
    ldap()
    fg()

@task
def simple():
    clean()
    c = cm_mongo()
    c.activate()
    c.refresh(types=['servers', 'images', 'flavors'])
    fg()
    
@task
def users():
    c = cm_mongo()
    c.activate()
    c.refresh(types=['users'])
    
    
@task
def ldap():
    idp = cm_userLDAP ()
    idp.connect("fg-ldap", "ldap")
    idp.refresh()

    users = idp.list()

    print ("Fetching {0} Users from LDAP".format(len(users)))
    

@task
def fg():
    """create a simple testbed"""
    start()
    local("python setup.py install")
    local("python webui/fg.py")    

@task
def pbs(host, type):
    pbs = pbs_mongo()
    
    # get hpc user

    config = cm_config()
    user = config.config["cloudmesh"]["hpc"]["username"]

    
    pbs.activate(host, user)

    print "ACTIVE PBS HOSTS", pbs.hosts
    
    if host is None:
        hosts = pbs.hosts
    else:
        hosts = [host]
        
    if type is None:
        types = ['qstat', 'nodes']
    else:
        types = [type]
    
    d = []
    
    for host in hosts:
        for type in types:
            if type in  ["qstat", "queue", "q"]:
                d = pbs.get_pbsnodes(host)    
            elif type in ["nodes"]:
                d = pbs.refresh_pbsnodes(host)
    
    for e in d:
        print "PBS -->"
        pprint(e) 


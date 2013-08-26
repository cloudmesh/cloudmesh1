from fabric.api import task, local
from pprint import pprint
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from cloudmesh.user.cm_userLDAP import cm_userLDAP
from cloudmesh.pbs.pbs_mongo import pbs_mongo

@task
def start():
    local("mkdir -p ./mongodb/")
    local("mongod --dbpath ./mongodb/ --port 27017")

@task
def stop():
    local("mongod --shutdown")

@task
def clean():
    local("make clean")
    local('mongo cloudmesh --eval "db.dropDatabase();"')
    local('mongo inventory --eval "db.dropDatabase();"')
    local('mongo test --eval "db.dropDatabase();"')

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
    c.refresh(types=['users','servers','images','flavors'])
    ldap()
    fg()

@task
def simple():
    clean()
    c = cm_mongo()
    c.activate()
    c.refresh(types=['servers','images','flavors'])
    fg()
    
@task
def users():
    c = cm_mongo()
    c.activate()
    c.refresh(types=['users'])
    
    
@task
def ldap():
    idp = cm_userLDAP ()
    idp.connect("fg-ldap","ldap")
    idp.refresh()

    users = idp.list()

    print ("Fetching {0} Users from LDAP".format(len(users)))
    

@task
def fg():
    """create a simple testbed"""
    local("mongod &")
    local("python setup.py install")
    local("python webui/fg.py")    

@task
def pbs(host,type):
    pbs = pbs_mongo()
    
    #get hpc user

    config = cm_config()
    user = config.config["cloudmesh"]["hpc"]["username"]

    
    pbs.activate(host,user)

    print "ACTIVE PBS HOSTS", pbs.hosts
    
    if host is None:
        hosts = pbs.hosts
    else:
        hosts = [host]
        
    if type is None:
        types =['qstat', 'nodes']
    else:
        types = [type]
    
    d = []
    
    for host in hosts:
        for type in types:
            if type in  ["qstat", "queue","q"]:
                d = pbs.get_pbsnodes(host)    
            elif type in ["nodes"]:
                d = pbs.refresh_pbsnodes(host)
    
    for e in d:
        print "PBS -->"
        pprint(e) 


from fabric.api import task, local
from pprint import pprint
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.user.cm_userLDAP import cm_userLDAP

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


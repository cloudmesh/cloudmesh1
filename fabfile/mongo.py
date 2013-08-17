from fabric.api import task, local
from pprint import pprint
from cloudmesh.cm_mongo import cm_mongo
    
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

@task
def vms_find():
    c = cm_mongo()
    c.activate()
    pprint (c.servers())
    
@task
def vms_refresh():
    c = cm_mongo()
    c.activate()
    c.refresh(types=['users','servers','images','flavors'])
    
@task
def users():
    c = cm_mongo()
    c.activate()
    c.refresh(types=['users'])
    
    

from fabric.api import task, local
from pprint import pprint
from cloudmesh.cloudmesh_mongo import cloudmesh_mongo
    
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
    c = cloudmesh_mongo()
    c.activate()
    pprint (c.servers())
    
@task
def vms_refresh():
    c = cloudmesh_mongo()
    c.activate()
    c.refresh(types=['servers','images','flavors'])
    
    

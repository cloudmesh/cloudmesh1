from fabric.api import local

def start():
    local("mkdir -p ./mongodb/")
    local("mongod --dbpath ./mongodb/ --port 27017")

def stop():
    local("mongod --shutdown")

def clean():
    local("make clean")

    

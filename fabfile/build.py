from fabric.api import task, local
import clean

@task
def req():
    """install the requirements"""
    local("pip install -r requirements.txt")

@task
def sdist():
    """create the sdist""" 
    clean.all()
    local("python setup.py sdist --format=bztar,zip")

@task
def install(): 
    """install cloudmesh"""
    local("python setup.py install")



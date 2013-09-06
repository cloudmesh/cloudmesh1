from fabric.api import task, local, execute
import clean

__all__ = ['req', 'sdist', 'install']

@task
def req():
    """install the requirements"""
    local("pip install -r requirements.txt")

@task
def sdist():
    """create the sdist""" 
    execute(clean.all)
    local("python setup.py sdist --format=bztar,zip")

@task
def install(): 
    """install cloudmesh"""
    local("pip install -r requirements.txt")
    local("python setup.py install")



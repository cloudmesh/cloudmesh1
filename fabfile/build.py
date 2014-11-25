import fabric
from fabric.api import task, local, execute
import clean
import os

__all__ = ['fast', 'sdist', 'install', 'sphinx']
    
def cursor_on():
    """If one uses progress in python the cursor may disapear if the
    progress is not properly finished. THis command will create a fake
    progresspar forcing the finish. it can be used in for example any
    fabfile so that at the end the progress is finsihed. However if
    the command does not properly quit it will not work. as this
    command may not be reached."""

    os.system("python bin/cursor_on.py")

@task
def sdist():
    """create the sdist"""
    fabric.state.output.stdout = True
    clean.all()
    local("python setup.py sdist --format=bztar,zip")
    cursor_on()

@task
def fast():
    """install cloudmesh"""
    fabric.state.output.stdout = True
    local("python setup.py install")
    cursor_on()
        
@task
def install():
    """install cloudmesh"""
    fabric.state.output.stdout = True
    local("./install requirements")
    local("python setup.py install")
    cursor_on()
    
@task
def sphinx():
    fabric.state.output.stdout = True
    local("rm -rf  /tmp/sphinx-contrib")
    local("cd /tmp; hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/")
    local("cd /tmp/sphinx-contrib/autorun/; python setup.py install")
    cursor_on()

import fabric
from fabric.api import task, local, execute
import clean

__all__ = ['fast', 'sdist', 'install', 'sphinx']


@task
def sdist():
    """create the sdist"""
    fabric.state.output.stdout = True
    execute(clean.all)
    local("python setup.py sdist --format=bztar,zip")


@task
def fast():
    """install cloudmesh"""
    fabric.state.output.stdout = True
    local("python setup.py install")


@task
def install():
    """install cloudmesh"""
    fabric.state.output.stdout = True
    local("./install requirements")
    local("python setup.py install")


@task
def sphinx():
    fabric.state.output.stdout = True
    local("rm -rf  /tmp/sphinx-contrib")
    local("cd /tmp; hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/")
    local("cd /tmp/sphinx-contrib/autorun/; python setup.py install")

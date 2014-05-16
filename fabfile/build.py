from fabric.api import task, local, execute
import clean

__all__ = ['sdist', 'install', 'sphinx']

@task
def sdist():
    """create the sdist"""
    execute(clean.all)
    local("python setup.py sdist --format=bztar,zip")

@task
def install():
    """install cloudmesh"""
    local("./install requirements.txt")
    local("python setup.py install")

@task
def sphinx():
    local("rm -rf  /tmp/sphinx-contrib")
    local("cd /tmp; hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/")
    local("cd /tmp/sphinx-contrib/autorun/; python setup.py install")

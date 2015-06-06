import fabric
from fabric.api import task, local
from cloudmesh_admin.Clean import Clean
import os

__all__ = ['fast', 'sdist', 'install', 'sphinx']


class Dist(object):

    @classmethod
    def sdist(cls):
        """create the sdist"""
        fabric.state.output.stdout = True
        Clean.all()
        os.system("python setup.py sdist --format=bztar,zip")

    @classmethod
    def fast(cls):
        """install cloudmesh"""
        fabric.state.output.stdout = True
        os.system("python setup.py install")

    @classmethod
    def install(cls):
        """install cloudmesh"""
        fabric.state.output.stdout = True
        #TODO replace with function call
        os.system("./install requirements")
        os.system("python setup.py install")

    def sphinx(cls):
        "install sphinx contrib"
        # TODO check if needed
        fabric.state.output.stdout = True
        os.system("rm -rf  /tmp/sphinx-contrib")
        os.system("cd /tmp; hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/")
        os.system("cd /tmp/sphinx-contrib/autorun/; python setup.py install")


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
    Dist.sdist()
    cursor_on()


@task
def fast():
    """install cloudmesh"""
    Dist.fast()
    cursor_on()


@task
def install():
    """install cloudmesh"""
    Dist.install()
    cursor_on()


@task
def sphinx():
    Dist.sphinx()
    cursor_on()

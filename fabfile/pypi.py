from fabric.api import task, local
import build

__all__ = ['upload', 'register']


@task
def upload():
    """upload the dist to pypi"""
    build.sdist()
    local("python setup.py sdist upload")


@task
def register():
    """register with pypi. Needs only to be done once."""
    local("python setup.py register")

from fabric.api import task, local
import sys

browser = "firefox"

if sys.platform == 'darwin':
    browser = "open"

@task
def view():
    """view the documentation in a browser"""
    local("{browser} doc/build/html/index.html".format(browser=browser))

@task
def html():
    """build the doc locally and view"""
    local("cd doc; make html")
    view()


@task
def gh():
    """deploy the documentation on gh-pages"""
    local("git checkout gh-pages")
    local("make pages")

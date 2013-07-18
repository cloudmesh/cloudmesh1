from fabric.api import task, local
import sys

browser = "firefox"

if sys.platform == 'darwin':
    browser = "open"

@task
def html():
    """build the doc locally and view"""
    local("cd doc; make html")
    local("{browser} doc/build/html/index.html".format(browser=browser))

@task
def gh():
    """deploy the documentation on gh-pages"""
    local("git checkout gh-pages")
    local("make pages")

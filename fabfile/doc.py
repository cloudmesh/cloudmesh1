from fabric.api import task, local

@task
def build():
    """build the doc locally and view"""
    local("cd doc; make html")
    local("open doc/build/html/index.html")

@task
def gh():
    """deploy the documentation on gh-pages"""
    local("git checkout gh-pages")
    local("make pages")

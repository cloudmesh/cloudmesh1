from fabric.api import task, local

@task
def dir():
    """clean the dirs"""
    local("rm -rf *.egg")
    local('find . -name "*~" -exec rm {} \;  ')
    local('find . -name "*.pyc" -exec rm {} \;  ')
    local("rm -rf build doc/build dist *.egg-info *~ #*")
    local("cd doc; make clean")
    local("rm -rf *.egg-info")
    local("rm -f celeryd@*")
    local("rm -f *.dump")

@task
def all():
    """clean the dis and uninstall cloudmesh"""
    dir()
    r = int(local("pip freeze |fgrep cloudmesh | wc -l", capture=True))
    while r > 0:
        local('echo "y\n" | pip uninstall cloudmesh')
        r = int(local("pip freeze |fgrep cloudmesh | wc -l", capture=True))

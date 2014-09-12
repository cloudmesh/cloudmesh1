from fabric.api import task, local


@task
def stat():
    """create statistics for pep8"""
    local(
        "pep8 --statistics --filename *.py */*.py */*/*.py */*/*/*.py */*/*/*/*.py */*/*/*/*/*.py")


@task
def auto():
    """run autopep8 on all python files"""
    local("autopep8 -i */*.py")
    local("autopep8 -i */*/*.py")
    local("autopep8 -i */*/*/*.py")
    local("autopep8 -i */*/*/*/*.py")
    local("autopep8 -i */*/*/*/*/*.py")
    local("autopep8 -i */*/*/*/*/*/*.py")


@task
def install():
    """install pep8, autopep8, pylint"""
    local("pip install autopep8 --upgrade")
    local("pip install pep8 --upgrade")
    local("pip install pylint --upgrade")
    local("pip install pyflakes --upgrade")

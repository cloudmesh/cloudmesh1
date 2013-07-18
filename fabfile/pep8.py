from fabric.api import task, local

@task
def stat():
	local("pep8 --statistics --filename *.py */*.py */*/*.py */*/*/*.py */*/*/*/*.py */*/*/*/*/*.py")
	
@task
def auto():
	local("autopep8 -i */*.py")
	local("autopep8 -i */*/*.py")
	local("autopep8 -i */*/*/*.py")
	local("autopep8 -i */*/*/*/*.py")
	local("autopep8 -i */*/*/*/*/*.py")
	local("autopep8 -i */*/*/*/*/*/*.py")

@task
def install():
    local("pip install autopep8 --upgrade")
    local("pip install pep8 --upgrade")
    local("pip install pylint --upgrade")
    local("pip install pyflakes --opgrade")



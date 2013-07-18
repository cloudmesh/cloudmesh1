from fabric.api import task, local

@task
def stats():
	local("pep8 --statistics --filename *.py */*.py */*/*.py */*/*/*.py */*/*/*/*.py */*/*/*/*/*.py")




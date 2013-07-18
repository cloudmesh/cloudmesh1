from fabric.api import task, local

@task
def req():
	local("pip install -r requirements.txt")

@task
def dist():
	local("make -f Makefile pip")

@task
def sdist(): 
    #clean.all()
	local("python setup.py sdist --format=bztar,zip")

@task
def install(): 
	local("python setup.py install")



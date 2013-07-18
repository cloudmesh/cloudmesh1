from fabric.api import task, local


@task
def upload():
	local("make -f Makefile pip")
	#local("python setup.py register")
	local("python setup.py sdist upload")

@task
def register():
	local("python setup.py register")



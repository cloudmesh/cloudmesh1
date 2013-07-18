from fabric.api import task, local

@task
def push():
	local("git commit -a ")
	local("git push")

@task
def pull():
	local("git pull ")

@task
def gregor():
	local('git config --global user.name "Gregor von Laszewski"')
	local('git config --global user.email laszewski@gmail.com')

    


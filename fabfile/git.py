from fabric.api import task, local

@task
def push():
    """git push"""
    local("git commit -a ")
    local("git push")

@task
def pull():
    """git pull"""
    local("git pull ")

@task
def gregor():
    """git config of name and email for gregor"""
    local('git config --global user.name "Gregor von Laszewski"')
    local('git config --global user.email laszewski@gmail.com')

    


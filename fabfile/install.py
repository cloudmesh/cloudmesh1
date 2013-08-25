from fabric.api import task, local

@task
def deploy():
    """deploys the system on ubuntu"""
    # download()
    ubuntu()
    install()

@task
def download():
    '''downloads cloudmesh'''
    local("git clone git@github.com:cloudmesh/cloudmesh.git")

@task
def install():
    local("pip install -r Requirements.txt")
    local("pip setup.py install")

@task
def ubuntu():
    '''prepares an ubuntu system and installs all 
    needed packages before we install cloudmesch'''
    packages = ["git", 
    	        "curl", 
		"python-virtualenv", 
		"python-dev", 
		"libldap2-dev", 
		"libsasl2-dev", 
		"ldap-user",
        "mongodb-10gen",
        "rabbitmq-server"]
    for package in packages:
    	local ("sudo apt-get install {0}".format(package)) 


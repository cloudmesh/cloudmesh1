from fabric.api import task, local
import sys
import platform

def is_ubuntu():
    return platform.dist()[0] == 'Ubuntu'

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


def install_mongodb():
    if is_ubuntu():
        local('sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10')
        local(
              'sudo sh -c "echo \'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen\' > /etc/apt/sources.list.d/10gen.list"')
        local('sudo apt-get update')
        local('sudo apt-get install mongodb-10gen')
    elif sys.platform == "darwin":
        local('ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"')
        local('brew update')
        local('brew install mongodb')


def install_package(package):
    if is_ubuntu():
        local ("sudo apt-get install {0}".format(package)) 
    elif sys.platform == "darwin":
        print "Not yet supported"
        sys.exit()
    elif sys.platform == "win32":
        print "Windows is not supported"
        print "Use Linux instead"
        sys.exit()

@task 
def install_packages(packages):
    for package in packages:
        install_package (package) 

@task
def ubntu():
    '''prepares an system and installs all 
    needed packages before we install cloudmesch'''
    
    install_packages(["git", 
                      "curl", 
                      "python-virtualenv", 
                      "python-dev", 
                      "libldap2-dev", 
                      "libsasl2-dev", 
                      "ldap-user"])
    install_mongodb()
    install_packages(["rabbitmq-server"])






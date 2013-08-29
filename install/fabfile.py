from fabric.api import task, local
import sys
import platform
import os

def is_ubuntu():
    """test sif the platform is ubuntu"""
    return platform.dist()[0] == 'Ubuntu'

def is_centos():
    """test if the platform is centos"""
    (centos, version, release) = platform.dist()
    if centos == "centos" and version != "6.4":
        print "Warning: centos %s is not tested" % version
    return centos == "centos"

@task
def deploy():
    """deploys the system on supported distributions"""
    # download()
    (major, minor, micro, releaselevel, serial) = sys.version_info
    if major != 2 or (major == 2 and minor < 7):
        print "Your version of python is not supported.  Please install python 2.7 for cloudmesh"
        sys.exit()
    if not hasattr(sys, 'real_prefix'):
        print "You do not appear to be in a vitualenv.  Please create and/or activate a virtualenv for cloudmesh installation"
        sys.exit()
    if is_ubuntu():
        ubuntu()
    elif is_centos():
        centos()
    else:
        print "OS distribution not supported; please see documatation for manual installation instructions."
        sys.exit()

    #install()

@task
def download():
    '''downloads cloudmesh'''
    local("git clone git@github.com:cloudmesh/cloudmesh.git")

@task
def install():
    local("cd ..; pip install -r requirements.txt")
    local("cd ..; python setup.py install")


def install_mongodb():
    if is_ubuntu():
        install_packages(["mongodb"])
    elif is_centos():
        install_packages(["mongodb", "mongodb-server"])
    elif sys.platform == "darwin":
        local('ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"')
        local('brew update')
        local('brew install mongodb')


def install_package(package):
    if is_ubuntu():
        local ("sudo apt-get -y install {0}".format(package)) 
    if is_centos():
        local("sudo yum -y install {0}".format(package))
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
def ubuntu():
    '''prepares an system and installs all 
    needed packages before we install cloudmesch'''
    
    install_packages(["git", 
                      "curl", 
                      "python-virtualenv", 
                      "python-dev", 
                      "libldap2-dev", 
                      "libsasl2-dev"])
    install_mongodb()
    install_packages(["rabbitmq-server"])
    install()

def centos():
    install_packages (["git", "wget", "gcc", "make", "readline-devel", "zlib-devel", "openssl-devel", "openldap-devel", "bzip2-devel"])
    install_mongodb()
    install_packages(["rabbitmq-server"])
    local('sudo sh -c "chkconfig rabbitmq-server on && service rabbitmq-server start"')
    install()

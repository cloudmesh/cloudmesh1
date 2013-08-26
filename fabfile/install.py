from fabric.api import task, local
import sys
import platform
import os

def is_ubuntu():
    return platform.dist()[0] == 'Ubuntu'

def is_centos():
    (centos, version, release) = platform.dist()
    if version != "6.4":
        print "Warning: centos %s is not tested" % version
    return centos == "centos"

@task
def deploy():
    """deploys the system on supported distributions"""
    # download()
    if is_ubuntu():
        ubuntu()
    elif is_centos():
        centos()
    else:
        print "OS distribution not supported; please see documatation for manual installation instructions."
        sys.exit()

    install()

@task
def download():
    '''downloads cloudmesh'''
    local("git clone git@github.com:cloudmesh/cloudmesh.git")

@task
def install():
    local("virtualenv --no-site-packages ~/.cloudmesh_v")
    local("source ~/.cloudmesh_v/bin/activate && pip install -r requirements.txt && pip setup.py install")


def install_mongodb():
    if is_ubuntu():

        local('sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10')
        local(
              'sudo sh -c "echo \'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen\' > /etc/apt/sources.list.d/10gen.list"')
        local('sudo apt-get update')
        local('sudo apt-get install mongodb-10gen')
    elif is_centos():
        local("sh -c \"echo '[10gen]\nname=10gen Repository\nbaseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64\ngpgcheck=0\nenabled=1' >/etc/yum.repos.d/10gen\"")
        install_packages(["mongo-10gen", "mongo-10gen-server"])
    elif sys.platform == "darwin":
        local('ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"')
        local('brew update')
        local('brew install mongodb')


def install_package(package):
    if is_ubuntu():
        local ("sudo apt-get install {0}".format(package)) 
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

def centos():
    install_packages ["git", "openldap-devel", "bzip2-devel", "rabbitmq-server"])
    local('sudo sh -c "chkconfig rabbitmq-server on && service rabbitmq-server start"')
    if not os.path.exists("/opt/python"):
        local('sudo mkdir -p /opt/python')
        local('sh -c "cd /tmp && wget http://www.python.org/ftp/python/2.7.5/Python-2.7.5.tgz && tar xzf python/2.7.5/Python-2.7.5.tgz && ./configure --prefix=/opt/python && make && sudo make install')
        local('sh -c "cd /tmp && curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gz && tar xfz virtualenv-1.10.1.tar.gz && virtualenv-1.10.1.tar.gz && sudo python setup.py install"')
        print "Add /opt/python/bin to your PATH"
    else:
        print "Could not install python, /opt/python already exists"
        sys.exit()

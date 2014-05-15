#!/usr/bin/env python
from cloudmesh_install import config_file
import glob
import shutil
import sys
import stat
sys.path.append("..")
sys.path.append(".")

from jinja2.runtime import Undefined
from jinja2 import Environment, meta
import json
import yaml
from string import Template
from collections import OrderedDict

import os
import platform
from cloudmesh_common.util import banner, path_expand, backup_name
from util import is_ubuntu, is_centos, is_osx
from cloudmesh_common.util import yn_choice


######################################################################
# STOP IF PYTHON VERSION IS NOT 2.7.x
######################################################################
(major, minor, micro, releaselevel, serial) = sys.version_info
if major != 2 or (major == 2 and minor < 7):
        print "Your version of python is not supported.  Please install python 2.7 for cloudmesh"
        sys.exit()

# BUG we need to ignore this in centos and install python 2.7


if not hasattr(sys, 'real_prefix'):
    print "ERROR: You are runing this script not inside a virtual machine"
    sys.exit()

    
try:
    from fabric.api import local,task 
except:
    os.system("pip install fabric")
    from fabric.api import local, task

try:
    from docopt import docopt
except:
    os.system("pip install docopt")
    from docopt import docopt

class IgnoreUndefined(Undefined):
    def __int__(self):
        return "None"

def install_command(args):
    """
    Usage:
        install -h | --help
        install --version
        install cloudmesh
        install delete_yaml    
        install query
        install new    
        install vagrant
    
    """
    arguments = docopt(install_command.__doc__,args)

    if arguments["cloudmesh"]:
        deploy()

    elif arguments["new"]:

        new_cloudmesh_yaml()
        
    elif arguments["delete_yaml"]:

        answer = yn_choice("THIS COMMAND IS REAL DANGEROUS AND WILL DELETE ALL YOUR YAML FILE. Proceed", default='y')

        if answer:
            print "You fool we just deleted your yaml files"
            cp("etc/*.yaml", "~/.futuregrid/")
        else:
            print "puuh you interrupted"
            pass
        
    elif arguments["system"]:
        
        banner("Installing Ubuntu System Requirements")

        if is_ubuntu():
            ubuntu()
        elif is_osx():
            osx()
        elif is_centos():
            centos()


    elif arguments["query"]:

        import platform
        print "System:    ", platform.system()
        #print "Uname:     ", platform.uname()                                          print "Machine:   ", platform.machine()                        
        print "Processor: ", platform.processor()                
        print "Platform:  ", platform.platform()        
        print "Python:    ", platform.python_version()
        print "Virtualenv:", hasattr(sys, 'real_prefix')
    elif arguments["vagrant"]:
        vagrant()

def new_cloudmesh_yaml():

    # create ~/.futuregrid dir
    #

    dir = config_file("")

    # Make sure we do not clobber existing non-empty yaml files.
    # (installation may create empty yaml files to avoid errors)
    if os.path.exists(dir):
        for f in glob.glob(dir + "/*.yaml"):
            if (os.path.getsize(f) > 0):
                print "ERROR: the (nonempty) yaml file '{0}' already exists.".format(f)
                print "       The 'new' command will not overwrite files."
                sys.exit(1)
    else:
        os.makedirs(dir, stat.S_IRWXU )

    filename_tmp = dir + '/cloudmesh-new.yaml'
    cloudmesh_out = dir + '/cloudmesh.yaml'
    filename_bak = cloudmesh_out

    cloudmesh_template = "etc/cloudmesh.yaml"
    filename_values = dir + "/me.yaml"

    # copy the yaml files

    def cp_urw(file_from, file_to):
        print "copy {0} -> {1}".format(file_from, file_to)
        shutil.copy(file_from, file_to)
        os.chmod(file_to, stat.S_IRWXU)
        
    
    def file_from_template(file_template, file_out, values):
        content = open(file_template, 'r').read()
        env = Environment(undefined=IgnoreUndefined)
        template = env.from_string(content)
        result = template.render(values)
        out_file=open(file_out, 'w+')
        out_file.write(result)
        out_file.close()


    for file_from in glob.glob("etc/*.yaml"):
        file_to = dir + "/" + file_from.replace("etc/","")
        cp_urw(file_from, file_to)
    cp_urw(dir + "/me-none.yaml", dir + "/me.yaml")

    # me_values = "etc/me-none.yaml"
    # me_template = "etc/me-all.yaml"
    me_file = dir + "/me.yaml"

    try:
        # do simple yaml load
        
        result = open(me_file, 'r').read()
        values = yaml.safe_load(Template(result).substitute(os.environ))
        #values = yaml.safe_load(Template(result).substitute(os.environ))
        #print json.dumps(values, indent=4)
        
    except Exception, e:
        print "ERROR: There is an error in the yaml file", e
        sys.exit(1)

    for cloud in values['clouds']:
        values['clouds'][cloud]['default'] = {}            
        values['clouds'][cloud]['default']['image'] = None
        values['clouds'][cloud]['default']['flavor'] = None            

    file_from_template(cloudmesh_template, cloudmesh_out, values)

    print "# Created: {0}".format(me_file)
    banner(c="-")
            

    #sys.exit()
    #
    #format = "yaml"
    #if format in ["json"]:
    #    result =  json.dumps(values, indent=4)    
    #elif format in ["yaml", "yml"]:
    #    result = yaml.dump(values, default_flow_style=False)
    #banner("done", c="-")


    
    #print "# Template: {0}".format(filename_template)
    #print "# Values  : {0}".format(filename_values)
    #print "# Backup : {0}".format(filename_bak)            
    
    
def deploy():
    """deploys the system on supported distributions"""
    # download()

    print "version_info", sys.version_info
    print "sys.prefix", sys.prefix

    if is_ubuntu():
        ubuntu()
    elif is_centos():
        centos()
    elif is_osx():
        osx()
    else:
        print "OS distribution not supported; please see documatation for manual installation instructions."
        sys.exit()

    # install()


def download():
    '''downloads cloudmesh'''
    local("git clone git@github.com:cloudmesh/cloudmesh.git")


def install():
    sphinx_updates()
    local("pip install -r requirements.txt")
    local("python setup.py install")


def install_mongodb():
    local("fab mongo.install")

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


def install_packages(packages):
    for package in packages:
        install_package (package)


def ubuntu():
    '''prepares an system and installs all 
    needed packages before we install cloudmesch'''

    local ("sudo apt-get update")
    install_packages(["python-dev", 
                      "git",
                      "mercurial",
                      "curl",
                      "libldap2-dev",
                      "libsasl2-dev",
                      "libpng-dev",
                      "mongodb-server"])    
    install_packages(["rabbitmq-server"])
    install()
    # install_mongodb()

    # important that mongo_db installation be done only after all we
    # install all needed python packages(as per requiremnts.txt)

def centos():
    install_packages (["git",
                       "mercurial",
                       "wget",
                       "gcc",
                       "make",
                       "readline-devel",
                       "zlib-devel",
                       "openssl-devel",
                       "openldap-devel",
                       "bzip2-devel",
                       "python-matplotlib",
                       "libpng-devel"])
    
    install_packages(["rabbitmq-server"])
    local('sudo sh -c "chkconfig rabbitmq-server on && service rabbitmq-server start"')
    install()
    # install_mongodb() 

def osx():
    
    local("export CFLAGS=-Qunused-arguments")
    local("export CPPFLAGS=-Qunused-arguments")
    local('brew install wget')
    local('brew install mercurial')
    local('brew install freetype')
    local('brew install libpng')
    try:
        import numpy
        print "numpy already installed"
    except:
        local('pip install numpy')
    try:
        import matplotlib
        print "matplotlib already installed"
    except:
        local ('LDFLAGS="-L/usr/local/opt/freetype/lib -L/usr/local/opt/libpng/lib" CPPFLAGS="-I/usr/local/opt/freetype/include -I/usr/local/opt/libpng/include -I/usr/local/opt/freetype/include/freetype2" pip install matplotlib')

        # local('pip install matplotlib')
    
    install()
    # install_mongodb()

def sphinx_updates():
    local('rm -rf /tmp/install-cloudmesh')
    local('mkdir -p /tmp/install-cloudmesh')
    local('cd /tmp/install-cloudmesh; hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/')
    local('~/ENV/bicd /tmp/install-cloudmesh/sphinx-contrib/autorun; python setup.py install')

        
def vagrant():
    local("rm -rf /tmp/vagrant")
    local("mkdir -p /tmp/vagrant")
    local("cd /tmp/vagrant; git clone git@github.com:cloudmesh/cloudmesh.git")
    local("cd /tmp/vagrant; vagrant init ubuntu-14.04-server-amd64")
    local("cd /tmp/vagrant; vagrant up")
    local("cd /tmp/vagrant; vagrant ssh")
             
if __name__ == '__main__':
    install_command(sys.argv)


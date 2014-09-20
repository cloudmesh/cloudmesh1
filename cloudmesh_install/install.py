#!/usr/bin/env python
from __future__ import with_statement
import glob
import shutil
import sys
import stat
import getpass
import os

try:
    import yaml
except:
    print "WARNING: yaml not yet installed"

try:
    from jinja2.runtime import Undefined
    from jinja2 import Environment
except:
    print "WARNING: jinja2 not yet installed"

from string import Template

from cloudmesh_install.util import banner
from cloudmesh_install.util import is_ubuntu, is_centos, is_osx
from cloudmesh_install.util import yn_choice
from cloudmesh_install import config_file_prefix, config_file

######################################################################
# STOP IF PYTHON VERSION IS NOT 2.7.5
######################################################################
(major, minor, micro, releaselevel, serial) = sys.version_info
if major != 2 or (major == 2 and minor < 7):
    print "ERROR: Your version of python is not supported."
    print "       Please install python 2.7 for cloudmesh."
    sys.exit()

# BUG we need to ignore this in centos and install python 2.7


if not hasattr(sys, 'real_prefix'):
    print "ERROR: You are not running this script inside a virtualenv."
    sys.exit()


try:
    from fabric.api import local
except:
    os.system("pip install fabric")
    from fabric.api import local

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
        install system
        install query
        install new [--force]
        install vagrant
        install enable admin [--username=<username>]

    """
    # This is a debuging message
    # print "IIIII<" + args + ">"

    arguments = docopt(install_command.__doc__, args)

    print arguments

    if arguments["cloudmesh"]:
        deploy()

    elif arguments["new"]:

        force = arguments["--force"] 
        new_cloudmesh_yaml(force)

    elif arguments["delete_yaml"]:

        answer = yn_choice(
            "THIS COMMAND IS REAL DANGEROUS AND WILL DELETE ALL YOUR YAML FILE. Proceed", default='y')

        if answer:
            # TODO: cp is not imported, defined
            print("You fool we just deleted your yaml files")
            cp("etc/*.yaml", config_file_prefix())
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
        # print "Uname:     ", platform.uname()
        print "Machine:   ", platform.machine()
        print "Processor: ", platform.processor()
        print "Platform:  ", platform.platform()
        print "Python:    ", platform.python_version()
        print "Virtualenv:", hasattr(sys, 'real_prefix')

    elif arguments["vagrant"]:
        vagrant()

    elif arguments["enable"] and arguments["admin"]:
        enable_admin_page(arguments['--username'])


def new_cloudmesh_yaml(force=False):
    """ Generate yaml files from the templates in etc directory
        if yaml files exist, this function won't perform.

        - check existance
        - create ~/CONFIG e.g. .cloudmesh
        - copy templates from etc/ to $HOME/.cloudmesh
    """

    dirname = config_file("")

    # Make sure we do not clobber existing non-empty yaml files.
    # (installation may create empty yaml files to avoid errors)
    if os.path.exists(dirname):
        for f in glob.glob(dirname + "/*.yaml"):
            if os.path.getsize(f) > 0:
                print "ERROR: the (nonempty) yaml file '{0}' already exists.".format(f)
                if not force:
                    print "       The 'new' command will not overwrite files."
                    sys.exit(1)
                else:
                    print "WARNING: we are overwriting the yaml files"
    else:
        os.makedirs(dirname, stat.S_IRWXU)

    filename_tmp = dirname + '/cloudmesh-new.yaml'
    cloudmesh_out = dirname + '/cloudmesh.yaml'
    filename_bak = cloudmesh_out

    cloudmesh_template = "etc/cloudmesh.yaml"
    filename_values = dirname + "/me.yaml"

    # copy the yaml files

    def cp_urw(file_from, file_to):
        print "copy {0} -> {1}".format(file_from, file_to)
        shutil.copy(file_from, file_to)
        os.chmod(file_to, stat.S_IRWXU)

    # Copy yaml files from etc directoy to the destination
    for file_from in glob.glob("etc/*.yaml"):
        file_to = dirname + "/" + file_from.replace("etc/", "")
        cp_urw(file_from, file_to)

    # Copy me-none.yaml to me.yaml which is filled with TBD
    cp_urw(dirname + "/me-none.yaml", dirname + "/me.yaml")

    # me_values = "etc/me-none.yaml"
    # me_template = "etc/me-all.yaml"
    me_file = dirname + "/me.yaml"

    try:
        # do simple yaml load

        result = open(me_file, 'r').read()
        values = yaml.safe_load(Template(result).substitute(os.environ))
        # values = yaml.safe_load(Template(result).substitute(os.environ))
        # print json.dumps(values, indent=4)

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

    # sys.exit()
    #
    # format = "yaml"
    # if format in ["json"]:
    #    result =  json.dumps(values, indent=4)
    # elif format in ["yaml", "yml"]:
    #    result = yaml.dump(values, default_flow_style=False)
    # banner("done", c="-")

    # print "# Template: {0}".format(filename_template)
    # print "# Values  : {0}".format(filename_values)
    # print "# Backup : {0}".format(filename_bak)


def file_from_template(file_template, file_out, values):
    content = open(file_template, 'r').read()
    env = Environment(undefined=IgnoreUndefined)
    template = env.from_string(content)
    result = template.render(values)
    out_file = open(file_out, 'w+')
    out_file.write(result)
    out_file.close()


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
        print "ERROR: OS distribution not supported"
        print "       please see documatation for manual"
        print "       installation instructions."
        sys.exit()

    # install()


def download():
    '''downloads cloudmesh'''
    local("git clone git@github.com:cloudmesh/cloudmesh.git")


def install():
    sphinx_updates()
    banner("cloudmesh python install")
    local("python setup.py install")


def install_mongodb():
    local("fab mongo.install")


def install_package(package):
    """installes the package.
    :param package: lthe package name
    """

    if is_ubuntu():
        local("sudo apt-get -y install {0}".format(package))
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
    """installes the packages in the list.
    :param packages: list of package names
    """
    for package in packages:
        install_package(package)


def ubuntu():
    '''prepares an system and installs all
    needed packages before we install cloudmesh'''

    # Note: package installations (apt-get install) are now done in
    # bin/prepare-ubuntu.sh

    install()
    # install_mongodb()

    # important that mongo_db installation be done only after all we
    # install all needed python packages(as per requiremnts.txt)


def centos():
    install_packages(["git",
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
    local(
        'sudo sh -c "chkconfig rabbitmq-server on && service rabbitmq-server start"')
    install()
    # install_mongodb()


def safe_install(what):
    try:
        local(what)
    except:
        print "WARNING: could not install:", what


def osx():

    local("export CFLAGS=-Qunused-arguments")
    local("export CPPFLAGS=-Qunused-arguments")

    safe_install('brew install wget')
    safe_install('brew install mercurial')
    safe_install('brew install freetype')
    safe_install('brew install libpng')

    try:
        import numpy
        print "numpy already installed"
    except:
        safe_install('pip install numpy')
    try:
        import matplotlib
        print "matplotlib already installed"
    except:
        try:
            local(
                'LDFLAGS="-L/usr/local/opt/freetype/lib -L/usr/local/opt/libpng/lib" CPPFLAGS="-I/usr/local/opt/freetype/include -I/usr/local/opt/libpng/include -I/usr/local/opt/freetype/include/freetype2" pip install matplotlib')
        except:
            print "WARNING: installing matplot lib"
        # local('pip install matplotlib')
    safe_install('brew install mongodb')
        
    install()
    # 


def sphinx_updates():
    # *mktemp -d* should be applied to get a unique directory name to a user
    # who runs this function.
    # Otherwise, if there are ohter users who run this command as well,
    # permission conflict will occur when it trys to write or delete
    # the directory
    # TODO: the use of mktemp was wrong as we need to pass a template

    banner("install sphinx autorun", c="-")
    user = getpass.getuser()
    dirname = local(
        "mktemp -d /tmp/{0}_cloudmesh.XXXXX".format(user), capture=True)
    dirname = dirname + "/install-cloudmesh"
    local('rm -rf %s' % dirname)
    local('mkdir -p %s' % dirname)
    local('cd %s; hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/' %
          dirname)
    local('cd %s/sphinx-contrib/autorun; python setup.py install' %
          dirname)
    banner("insall autorun ok")


def vagrant():
    # applied mktemp like sphinx_updates
    dirname = local("mktemp -d", capture=True)
    dirname = dirname + "/vagrant"
    local("rm -rf %s" % dirname)
    local("mkdir -p %s" % dirname)
    local("cd %s; git clone git@github.com:cloudmesh/cloudmesh.git" % dirname)
    local("cd %s; vagrant init ubuntu-14.04-server-amd64" % dirname)
    local("cd %s; vagrant up" % dirname)
    local("cd %s; vagrant ssh" % dirname)


def enable_admin_page(userid):
    if not userid:
        userid = _get_username_from_profile()

    _set_username_to_admin(userid)


def _set_username_to_admin(userid):
    server_yaml = _get_value_from_yaml("/cloudmesh_server.yaml", [])

    updated_yaml = server_yaml
    updated_yaml['cloudmesh']['server']['roles']['admin']['users'] = [userid]

    _set_value_to_yaml("/cloudmesh_server.yaml", updated_yaml)


def _get_bak_filename(filename, postfix=0):
    import os.path
    bak_name = os.path.abspath(filename) + ".bak" + "." + str(postfix)
    if os.path.isfile(bak_name):
        return _get_bak_filename(filename, postfix + 1)
    return bak_name


def _make_a_backup(filename):
    dest = _get_bak_filename(filename)
    shutil.copyfile(filename, dest)
    return dest


def _set_value_to_yaml(filepath, data):

    dir = config_file("")
    cm_file = dir + filepath

    # make a backup
    bak = _make_a_backup(cm_file)
    print "[%s] backup made" % bak

    # Write yaml
    with open(cm_file, 'w') as outfile:
        outfile.write(yaml.dump(data, default_flow_style=False))
        print "[%s] updated" % cm_file


def _get_username_from_profile():
    return _get_value_from_yaml("/cloudmesh.yaml",
                                ['cloudmesh', 'profile', 'username'])


def _lookup(data, keys):
    try:
        if keys:
            if keys[0] in data:
                return _lookup(data[keys[0]], keys[1:])
    except:
        return data
    return data


def _get_value_from_yaml(filepath, column_keys):
    dir = config_file("")
    cm_file = dir + filepath

    try:
        result = open(cm_file, 'r').read()
        values = yaml.safe_load(Template(result).substitute(os.environ))
    except Exception, e:
        print "ERROR: There is an error in the yaml file", e
        sys.exit(1)

    return _lookup(values, column_keys)

if __name__ == '__main__':
    install_command(sys.argv)

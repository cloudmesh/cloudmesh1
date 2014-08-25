#!/usr/bin/env python
from __future__ import with_statement

from os.path import expanduser
from cloudmesh_install import config_file
import glob
import shutil
import sys
import stat
import getpass

from jinja2.runtime import Undefined
from jinja2 import Environment
import yaml
from string import Template

import os
from cloudmesh_common.util import banner
from util import is_ubuntu, is_centos, is_osx
from cloudmesh_common.util import yn_choice
from ConfigParser import SafeConfigParser
from paramiko import SSHClient, AutoAddPolicy, BadHostKeyException, AuthenticationException, SSHException
from cloudmesh_install import config_file, config_file_prefix

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


        
rc_file_locations = {
    'india': {
        'hostname': 'india.futuregrid.org',
        'source': '.futuregrid/openstack_havana/novarc',
        'dest': "~/.cloudmesh/clouds/india",
        },
    'sierra': {
        'hostname': 'sierra.futuregrid.org',
        'source': '.futuregrid/novarc',
        'dest': "~/.cloudmesh/clouds/sierra",
        }
    }


def download_rc_files(userid):

    for hostname in rc_file_locations:
        host = rc_file_locations[hostname]
        host["userid"] = userid
        host["dest"]= expanduser(host["dest"])
        
        print "fetching from ", host["hostname"], host

        print "creade dir"
        
        os.system ("mkdir -p %(dest)s" % host)

        copy_cmd = "scp -o StricthostKeyChecking=no %(userid)s@%(hostname)s:%(source)s %(dest)s" % host        
        print "    <-", copy_cmd
        print "    ",
        result = None
        try:
            from sh import scp
            result = scp("-o","StrictHostKeyChecking=no", "%(userid)s@%(hostname)s:%(source)s" % host, "%(dest)s" % host)
            print "ok", result
        except Exception, e:
            print "failed", result, e


def install_command(args):
    """
    Usage:
        install -h | --help
        install --version
        install cloudmesh
        install delete_yaml
        install system
        install query
        install new
        install apply_credentials
        install vagrant
        install rc fetch [--username=<username>] [--outdir=<outdir>]
        install rc fill
        install rc login [--username=<username>]

    """
    arguments = docopt(install_command.__doc__, args)

    if arguments["cloudmesh"]:
        deploy()

    elif arguments["new"]:

        new_cloudmesh_yaml()

    elif arguments["delete_yaml"]:

        answer = yn_choice(
            "THIS COMMAND IS REAL DANGEROUS AND WILL DELETE ALL YOUR YAML FILE. Proceed", default='y')

        if answer:
            print "You fool we just deleted your yaml files"
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

    elif arguments["rc"] and arguments["fetch"]:
        fetchrc(arguments["--username"], arguments["--outdir"])

    elif arguments["rc"] and arguments["fill"]:
        apply_credentials_to_yaml_file()

    elif arguments["rc"] and arguments["login"]:
        verify_ssh_login(arguments["--username"])


def new_cloudmesh_yaml():
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
                print "       The 'new' command will not overwrite files."
                sys.exit(1)
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


def apply_credentials_to_yaml_file():
    """
    rc_dir_location = {}
    # (hostname, loaction of dir on remote host, location of dir on localhost)
    rc_dir_location["india_openstack_havana"] = ("india.futuregird.org", "?", "?")
    rc_dir_location["sierra_openstack_grizzly"] = ("sierra.futuregrid.org", "?", "?")

    for label in rc_dir_location
        (host,dir) = rc_rdilocation(label)
        get rc file form the host and dir and copy to install_dir

    me_dict = read current me.yaml



    for label in rc_dir_location
        (host,dir) = rc_rdilocation(label)

        if label does not exist make it and also add the credentials for it,
            fill out initially with TBD

        if openstack:
           put values from local dir into dict

        elif eucalyptus:
           put values from local dir into dict

    return me dict
    """

    class Readrcfile(object):

        """ Read novarc, eucarc and store variables
            with configparser
            reference:
            http://stackoverflow.com/questions/2819696/parsing-properties-file-in-python/2819788#2819788
        """

        def __init__(self, fp):
            self.fp = fp
            self.head = '[rcfile]\n'

        def readline(self):
            if self.head:
                try:
                    return self.head
                finally:
                    self.head = None
            else:
                return self.fp.readline().replace("export ", "")

    def get_variables(fpath):
        section_title = "rcfile"
        read_values = ["OS_TENANT_NAME", "OS_USERNAME", "OS_PASSWORD"]  # case-sensitive
        result = {}

        cp = SafeConfigParser()
        try:
            cp.readfp(Readrcfile(open(fpath)))
            # cp.items(section_title)
            for read_value in read_values:
                tmp = cp.get(section_title, read_value)
                if tmp.startswith("$"):
                    tmp = cp.get(section_title, tmp[1:])  # without $ sign
                result[read_value] = tmp
            return result

        except:
            print "ERROR: Failed to read rc files. Please check you have valid \
                    rcfiles in %s." % fpath
            print sys.exc_info()
            sys.exit(1)

    # #######################################################
    # MISSING PART IS HERE
    # WE HAVE TO FILL THE me.yaml FILE WITH A REAL VALUE HERE
    # #######################################################

    # me-all.yaml is correct one instead me-none.yaml
    # to fill variables with template
    # -----------------------------------------------

    dir = config_file("")
    me_file = dir + "/me.yaml"

    try:
        result = open(me_file, 'r').read()
        values = yaml.safe_load(Template(result).substitute(os.environ))
    except Exception, e:
        print "ERROR: There is an error in the yaml file", e
        sys.exit(1)

    # rcfile location
    rcfile_path = dir + "/clouds/"
    new_values = {}
    for filepath in glob.glob(rcfile_path + "/*/*rc"):
        filename = os.path.basename(filepath)
        cloud_name = os.path.basename(
            os.path.normpath(filepath.replace(filename, "")))
        new_values[cloud_name] = get_variables(filepath)
        print "[%s] loaded" % filepath

    for cloud in values['clouds']:
        values['clouds'][cloud]['default'] = {}
        # Fill in credentials with real values
        # This does not update me.yaml file. This will be done soon.
        try:
            for k, v in new_values[cloud].iteritems():
                values['clouds'][cloud]['credential'][k] = new_values[cloud][k]
        except:
            pass

    cloudmesh_out = dir + '/cloudmesh.yaml'

    # file_from_template
    # ------------------
    # This is only for replacing variables in Jinja2 template.

    # For example, {{clouds.openstack.credential}} is going to be replaced with
    # values['clouds']['openstack']['credential']

    # file_from_template(cloudmesh_out, cloudmesh_out, values)

    # replace TBD in yaml
    # -------------------
    # 'cm-init fill' might do same thing
    #
    # In case yaml file contains TBD values, this logic replaces it with real
    # values
    # Similar to file_from_template but replace with TBD
    try:
        result = open(cloudmesh_out, 'r').read()
        data = yaml.safe_load(Template(result).substitute(os.environ))
    except Exception, e:
        print "ERROR: There is an error in the yaml file", e
        sys.exit(1)

    # Update yaml if a value is TBD
    # -----------------------------
    # 'cm-init fill' might do same thing
    for cloud_name, value in new_values.iteritems():
        clouds_in_yaml = data['cloudmesh']['clouds']
        if cloud_name in clouds_in_yaml:
            credentials = clouds_in_yaml[cloud_name]['credentials']
            for k, v in value.items():
                if k in credentials and credentials[k] == "TBD":
                    credentials[k] = v

    # replacing default project and username
    data['cloudmesh']['hpc']['username'] = new_values[cloud_name]['OS_USERNAME']
    data['cloudmesh']['projects']['default'] = \
    new_values[cloud_name]['OS_TENANT_NAME']
    # active projects can be multiple values
    # it should be a list to stack unique project ids
    # TBD
    data['cloudmesh']['projects']['active'] = \
    [new_values[cloud_name]['OS_TENANT_NAME']]

    # Write yaml
    with open(cloudmesh_out, 'w') as outfile:
        outfile.write(yaml.dump(data, default_flow_style=False))
        print "[%s] updated" % cloudmesh_out


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
        print "Warning: could not install:", what


    
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
            print "Warning: installing matplot lib"
        # local('pip install matplotlib')

    install()
    # install_mongodb()


def sphinx_updates():
    # *mktemp -d* should be applied to get a unique directory name to a user
    # who runs this function.
    # Otherwise, if there are ohter users who run this command as well,
    # permission conflict will occur when it trys to write or delete
    # the directory
    # TODO: the use of mktemp was wrong as we need to pass a template

    banner("install sphinx autorun", c="-")
    user = getpass.getuser()
    dirname = local("mktemp -d /tmp/{0}_cloudmesh.XXXXX".format(user), capture=True)
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


def fetchrc(userid=None, outdir=None):

    banner("download rcfiles (novarc, eucarc, etc) from IaaS platforms")

    print ""
    # Task 1. list portal user id

    '''
    try:
        from cloudmesh.config.ConfigDict import ConfigDict
    except Exception, e:
        print "ERROR: your have not yet configured cloudmesh completely. "
        print "       Have you called"
        print
        print "          ./install cloudmesh"
        print
        sys.exit(1)

    dir = config_file("")

    config = ConfigDict(dir + "/me.yaml")
    userid = config["portalname"]
    '''

    if not userid:
        userid = getpass.getuser()
        userid = raw_input("Please enter your portal user id [default: %s]: " %
                           userid) or userid

    # Task 2. list hostnames to get access. In Futuregrid, india, sierra are
    # mandatory hosts to be included.
    # TEMPORARY
    host_ids = ["india_openstack_havana", "sierra_openstack_grizzly"]

    # user input is disabled
    # host_ids = raw_input("Please enter host identifications [default: %s]: "
    #                     % ", ".join(host_ids)) or host_ids

    if isinstance(host_ids, str):
        host_ids = map(lambda x: x.strip(), host_ids.split(","))

    domain_name = ".futuregrid.org"
    hostnames = map(lambda x: x.split("_")[0] + domain_name, host_ids)

    key_path = "~/.ssh/id_rsa"
    # private key path is disabled
    # key_path = raw_input("Please enter a path of the ssh private key to" + \
    #                     " login the hosts [default: %s]: " % key_path) or \
    #                    key_path

    try:

        download_rc_files(userid)
        
        """
        # cmd = "fab rcfile.download:userid='%s',host_ids='%s',key_path='%s'" \
        cmd = "fab -H %s -u %s -i %s rcfile.download:'%s','%s'" \
            % (",".join(hostnames), userid, key_path,
               "\,".join(host_ids), outdir)
        print "CMD", cmd
        os.system(cmd)
        """
        
    except:
        print sys.exc_info()
        sys.exit(1)




def verify_ssh_login(userid):
    client = SSHClient()
    client.load_system_host_keys()
    # client.set_missing_host_key_policy(WarningPolicy)
    client.set_missing_host_key_policy(AutoAddPolicy())

    # TEST ONLY
    hosts = ["india.futuregrid.org", "sierra.futuregrid.org"]
    key = os.path.expanduser(os.path.join("~", ".ssh", "id_rsa"))
    print "[key: %s]" % key

    if not userid:
        userid = getpass.getuser()

    for host in hosts:
        try:
            client.connect(host, username=userid, key_filename=key)
            client.close()
            print "[%s] succeeded with %s." % (host, userid)
        except (BadHostKeyException, AuthenticationException, SSHException) as e:
            # print sys.exc_info()
            print ("[%s] %s with %s. Please check your ssh setup (e.g. key " +
                   "files, id, known_hosts)") % (host, e, userid)

if __name__ == '__main__':
    install_command(sys.argv)

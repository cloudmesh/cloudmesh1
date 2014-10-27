#! /usr/bin/env python
from __future__ import print_function
from cloudmesh_install import config_file
from pprint import pprint
import getpass
import yaml
from docopt import docopt
from cloudmesh.config.cm_config import cm_config
import sys
import os
import stat
# from cloudmesh_user import cloudmesh_user
from sh import scp
from getpass import getpass
from cloudmesh import yn_choice
from cloudmesh import path_expand
from cloudmesh import banner
from cloudmesh.user.cm_user import cm_user
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh_install import config_file
from cloudmesh_install import config_file_prefix

debug = True


def DEBUG(label, var):
    if debug:
        print(70 * "-")
        print(label)
        print(70 * " ")
        print(str(var))
        print(70 * "-")


def cm_manage():
    """Usage:
      cm-manage config projects list
      cm-manage config projects
      cm-manage config [-f FILE] [-o OUT] [-p PROJECT] cloud NAME [-]
      cm-manage config dump [--format=(yaml|dict)]
      cm-manage config init [-o OUT] [-u USER]
      cm-manage config list
      cm-manage config password NAME
      cm-manage config show passwords
      cm-manage config fetch [-u USER] [-r HOST]
      cm-manage --version
      cm-manage --help

    Arguments:
      NAME                 name of the cloud

    Options:
      -h --help            show this help message and exit

      -v --version         show version and exit

      -f NAME --file=NAME  the Name of the cloud to be specified,
                           if ? a selection is presented

      -o OUT --out=OUT     writes the result in the specifide file

      -p PROJECT --project=PROJECT   selects a project (e.g. for eucalyptus
                                     which has project-specific environments)

      -u USER --user=USER  the user (login) name

      -r HOST --remote=HOST  the host machine on which the yaml file is
                             located in the CONFIG directory
                             [default: india.futuregrid.org]

      -d  --debug          debug

      -                    this option is a - at the end of the command.
                           If data is written to a file it is also put out to stdout

    Description:

       Command to generate rc files from our cloudmesh configuration files.

        This program generates form a YAML file containing the login
        information for a cloud an rc file that can be used to later source
        it.

    Example:
        we assume the yaml file has an entry india-openstack::

        cm-manage config -o novarc india-openstack
        source novarc

      This will create a novarc file and than you can source it::

         cm-manage config ? -

      Presents a selction of cloud choices and writes the choice into a
      file called CONFIG/novarc


    """

    default_path = config_file_prefix + '/novarc'
    arguments = docopt(cm_manage.__doc__)

    DEBUG("arguments", arguments)

    home = os.environ['HOME']

    # DEBUG("home", home)

    #
    # This secion deals with handeling "cm config" related commands

    ######################################################################
    is_config = arguments['config'] != None

    if is_config:

        # DEBUG('Arguments', arguments)

        file = arguments['--file']
        try:
            config = cm_config(file)
            # DEBUG("config", config)
        except IOError:
            print("{0}: Configuration file '{1}' not found".format("CM ERROR", file))
            sys.exit(1)
        except (yaml.scanner.ScannerError, yaml.parser.ParserError) as yamlerror:
            print("{0}: YAML error: {1}, in configuration file '{2}'".format("CM ERROR", yamlerror, file))
            sys.exit(1)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            sys.exit(1)

        name = arguments['NAME']

        #
        # NOT TESTED
        #

        if arguments['fetch'] or name == 'fetch':

            DEBUG('Arguments', arguments)

            # get user
            var = {}
            var['user'] = arguments['--user']
            var['host'] = arguments['--remote']
            #
            # BUG should be
            #
            var['file'] = config_file_prefix() + "/cloudmesh.yaml"
            if var['user'] is None:
                var['user'] = getpass.getuser()

            from_location = "%(user)s@%(host)s:%(file)s" % var
            to_location = config_file("/%(file)s" % var)

            if os.path.isfile(to_location):
                print("WARNING: The file %s exists" % to_location)
                if not yn_choice("Would you like to replace the file", default='y'):
                    sys.exit(1)

            print(from_location)
            print(to_location)

            print("Copy cloudmesh file from %s to %s" % (from_location, to_location))

            result = scp(from_location, to_location)

            print(result)

            sys.exit(0)

        #
        # ok
        #
        # if (arguments['projects'] and arguments['list']) :
        if arguments['projects'] and arguments['list']:

            projects = config.get('cloudmesh.projects')
            print(yaml.dump(projects, default_flow_style=False, indent=4))
            sys.exit(0)

        #
        # OK, needs setting
        #

        if arguments['projects']:

            projects = config.projects('active')

            print("Please select from the following:")
            print("0 - Cancel")
            selected = False
            choices = []
            while not selected:
                counter = 1
                for name in projects:
                    print(counter, "-" "%20s" % name)
                    choices.append(name)
                    counter += 1
                print("Please select:")
                input = int(sys.stdin.readline())
                if input == 0:
                    print("Selection terminated")
                    sys.exit(0)
                selected = (input > 0) and (input < counter)
            print("Selected: ", input)
            name = choices[input - 1]
            print(name)

            print("ERROR: THIS JUST SELECTS A PROJECT ID BUT DOES NOT SET IT")
            sys.exit(0)

        if arguments['init'] or name == 'init':
            output = arguments['--out']
            username = arguments['--user'] or os.getenv('USER')

            location = path_expand(output)
            new_yaml_file = open(location, 'w+')

            user_yaml = cm_user().generate_yaml(username, 'cloudmesh')
            print(yaml.dump(
                user_yaml, default_flow_style=False), file=new_yaml_file)
            new_yaml_file.close()
            print("Written new yaml file in " + location)
            sys.exit(0)

        #
        # OK
        #

        if arguments['list'] or name == 'list':
            for name in config.cloudnames():
                if 'cm_type' in config.cloud(name):
                    print(name, "(%s)" % config.cloud(name)['cm_type'])
            sys.exit(0)

        #
        # NOT TESTED
        #
        if arguments['password']:
            oldpass = getpass("Current password: ")
            newpass1 = getpass("New password: ")
            newpass2 = getpass("New password (again): ")

            # TODO: some kind of password strength checking?
            if newpass1 == newpass2:
                config.change_own_password(name, oldpass, newpass1)
            else:
                print("New passwords did not match; password not changed.")

            sys.exit(0)

        #
        # OK, but does not display the username
        #
        if arguments['show'] or name == 'show' and arguments['passwords']:
            warning = "Your passwords will appear on the screen. Continue?"
            if yn_choice(warning, 'n'):

                me = ConfigDict(filename=config_file("/me.yaml"))
                banner("PASSWORDS")
                for name in me['password']:
                    print("{0}: {1}".format(name, me['password'][name]))

            sys.exit(0)

        #
        # OK
        #
        if arguments['dump'] or name == 'dump':
            format = arguments['--format']
            if format == 'yaml':
                d = dict(config)
                print(yaml.dump(d, default_flow_style=False))
            elif format == 'dict' or format is None:
                print(config)
            sys.exit(0)

        #
        # NOT TESTED
        #
        if name in ['?', 'x']:
            if file is None:
                arguments['--out'] = "%s/%s" % (home, default_path)
            print("Please select from the following:")
            print("0 - Cancel")
            selected = False
            choices = []
            while not selected:
                counter = 1
                for name in config.cloudnames():
                    if 'cm_type' in config.cloud(name):
                        print("{0} - {1:<30} ({2})".format(counter, name, config.cloud(name)['cm_type']))
                        choices.append(name)
                        counter += 1
                print("Please select:")
                input = int(sys.stdin.readline())
                if input == 0:
                    print("Selection terminated")
                    sys.exit(0)
                selected = (input > 0) and (input < counter)
            print("Selected: ", input)
            name = choices[input - 1]

        output = arguments['--out']

        #
        # OK
        #
        if name is not None:
            cloud = config.cloud(name)
            if not cloud:
                print("%s: The cloud '%s' is not defined." % ("CM ERROR", name))
                print("Try instead:")
                for keyname in config.cloudnames():
                    print("    ", keyname)
                sys.exit(1)

            if cloud['cm_type'] == 'eucalyptus':
                if arguments['--project']:
                    project = arguments['--project']
                    if not project in cloud:
                        print("No such project %s defined in cloud %s." % (project, name))
                        sys.exit(1)
                else:
                    project = config.cloud_default(
                        name, 'project') or config.projects('default')
                    if not project in cloud:
                        print("Default project %s not defined in cloud %s." % (project, name))
                        sys.exit(1)
                rc_func = lambda name: config.rc_euca(name, project)
            else:
                rc_func = config.rc

            result = rc_func(name)

            #
            # OK
            #
            if arguments["-"]:
                print(result)
            else:
                if output is None:
                    arguments['--out'] = "%s/%s" % (home, default_path)
                    output = arguments['--out']
                out = False
                if yn_choice("Would you like to review the information", default="y"):
                    banner("WARNING: FIle will be written to " + output)
                    print(result)
                    print(banner(""))
                try:
                    # First we try to open the file assuming it doesn't exist
                    out = os.open(
                        output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, stat.S_IRUSR | stat.S_IWUSR)
                except OSError as oserr:
                    # If file exists, offer to replace it
                    if oserr.errno == 17:
                        delete = raw_input(
                            "'%s' exists; Overwrite it [N|y]? " % output)
                        if delete.strip().lower() == 'y':
                            out = os.open(output, os.O_TRUNC | os.O_WRONLY)
                if out:
                    os.write(out, result)
                    os.close(out)

    #
    # END "cm config" related commands
    #

if __name__ == '__main__':
    cm_manage(sys.argv)

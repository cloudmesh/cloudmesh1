#! /usr/bin/env python
"""cm-manage config
------------
Command to generate rc files from our cloudmesh configuration files.

Usage:
  cm-manage config projects (list|?)
  cm-manage config [-f FILE] [-o OUT] [-p PROJECT] NAME [-]
  cm-manage config dump [--format=(yaml|dict)]
  cm-manage config init [-o OUT] [-u USER]
  cm-manage config list
  cm-manage config fetch [-u USER] [-r HOST] 
  cm-manage --version
  cm-manage --help

This program generates form a YAML file containing the login
information for a cloud an rc file that can be used to later source
it.

Example:
  we assume the yaml file has an entry india-openstack

    cm-manage config -o novarc india-openstack
    source novarc

  This will create a novarc file and than you can source it.


     cm-manage config ? -

   Presents a selction of cloud choices and writes the choice into a
   file called ~/.futuregrid/novarc

Arguments:
  NAME name of the cloud

Options:
  -h --help            show this help message and exit

  -v --version         show version and exit

  -f NAME --file=NAME  the Name of the cloud to be specified, if ? a selection is presented

  -o OUT --out=OUT     writes the result in the specifide file

  -p PROJECT --project=PROJECT   selects a project (e.g. for eucalyptus which has project-specific environments)

  -u USER --user=USER  the user (login) name

  -r HOST --remote=HOST  the host machine on which the yaml file is located in the ~/.futuregrid directory [default: sierra.futuregrid.org]

  -d  --debug          debug

  -                    this option is a - at the end of the command. If data is written to a file it is also put out to stdout

"""
import getpass
import yaml
from docopt import docopt
from cm_config import cm_config
import sys
import os
import stat
from ldap_user import ldap_user
from openstack_grizzly_cloud import openstack_grizzly_cloud
from sh import scp

##### For testing
# import mock_keystone

debug = True

def DEBUG(label, var):
    if debug:
        print 70 * "-"
        print label 
        print 70 * " "
        print str(var)
        print 70 * "-"

#
# http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
#
def yn_choice(message, default='y'):
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = raw_input("%s (%s) " % (message, choices))
    values = ('y', 'yes', '') if default == 'y' else ('y', 'yes')
    return True if choice.strip().lower() in values else False

def main():
    default_path = '.futuregrid/novarc'
    arguments = docopt(__doc__, version='0.8')

    DEBUG("arguments", arguments)
    
    home = os.environ['HOME']

    DEBUG("home", home)
    

    ######################################################################
    # This secion deals with handeling "cm config" related commands
    ######################################################################
    is_config =  arguments['config'] != None




    if is_config:

        DEBUG('Arguments', arguments)

        file = arguments['--file']
        try:
            config = cm_config(file)
            DEBUG("config", config)
        except IOError:
            print "%s: Configuration file '%s' not found" % ("CM ERROR", file)
            sys.exit(1)
        except (yaml.scanner.ScannerError, yaml.parser.ParserError) as yamlerror:
            print "%s: YAML error: %s, in configuration file '%s'" % ("CM ERROR", yamlerror, file)
            sys.exit(1)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            sys.exit(1)

        name = arguments['NAME']
        
        if arguments['fetch'] or name == 'fetch':
            
            DEBUG('Arguments', arguments)


            # get user
            var = {}
            var['user'] = arguments['--user']
            var['host'] = arguments['--remote']
            var['file'] = ".futuregrid/cloudmesh.yaml"
            if var['user'] == None:
                var['user'] = getpass.getuser()

            from_location = "%(user)s@%(host)s:%(file)s" % var
            to_location = os.path.expanduser("~/%(file)s" % var)


            if os.path.isfile(to_location):
                print "WARNING: The file %s exists" % to_location
                if not yn_choice("Would you like to replace the file", default='y'):
                    sys.exit(1)

            print from_location
            print to_location

            print "Copy cloudmesh file from %s to %s" %  (from_location, to_location)

            result = scp(from_location, to_location)

            print result

            sys.exit(0)


        if arguments['projects'] and arguments['list']:

            projects = config.data['cloudmesh']['projects']
            print yaml.dump(projects, default_flow_style=False, indent=4)
            sys.exit(0)

        if arguments['projects'] and arguments['?']:

            projects = config.data['cloudmesh']['projects']['active']

            print "Please select from the following:"
            print "0 - Cancel"
            selected = False
            choices = []
            while not selected:
                counter = 1
                for name in projects:
                    print counter, "-" "%20s" % name 
                    choices.append(name)
                    counter += 1
                print "Please select:"
                input = int(sys.stdin.readline())
                if input == 0:
                    print "Selection terminated"
                    sys.exit(0)
                selected = (input > 0) and (input < counter)
            print "Selected: ", input
            name = choices[input-1]
            print name

            sys.exit(0)

        if arguments['init'] or name == 'init':
            output = arguments['--out']
            username = arguments['--user'] or os.getenv('USER')
            config.userdata_handler = ldap_user
            config.cloudcreds_handler = openstack_grizzly_cloud
            ########### for testing #############################################################
            # config.cloudcreds_handler._client = mock_keystone.Client
            # config.cloudcreds_handler._client.mockusername = username
            # config.cloudcreds_handler._client.mocktenants = config.data['cloudmesh']['active']
            #####################################################################################
            config.initialize(username)
            try:
                config.write(output)
            except OSError as oserr:
                if oserr.errno == 17:
                    print "'%s' exists, please rename or remove it and try again." % oserr.filename
            sys.exit(0)

        if arguments['list'] or name == 'list':
            for name in config.keys():
                if 'cm_type' in config.data['cloudmesh']['clouds'][name]:
                    print name, "(%s)" % config.data['cloudmesh']['clouds'][name]['cm_type']
            sys.exit(0)

        if arguments['dump'] or name =='dump':
            format = arguments['--format']
            if format == 'yaml':
                print yaml.dump(config, default_flow_style=False, indent=4)
            elif format == 'dict' or format ==None:
                print config
            sys.exit(0)

        if name == '?':
            if file == None:
                arguments['--out'] = "%s/%s" % (home, default_path)
            print "Please select from the following:"
            print "0 - Cancel"
            selected = False
            choices = []
            while not selected:
                counter = 1
                for name in config.keys():
                    if 'cm_type' in config.data['cloudmesh']['clouds'][name]:
                        print counter, "-" "%20s" % name, "(%s)" % config.data['cloudmesh']['clouds'][name]['cm_type']
                        choices.append(name)
                        counter += 1
                print "Please select:"
                input = int(sys.stdin.readline())
                if input == 0:
                    print "Selection terminated"
                    sys.exit(0)
                selected = (input > 0) and (input < counter)
            print "Selected: ", input
            name = choices[input-1]

        output = arguments['--out']

        if name != None:
            cloud = config.cloud(name)
            if not cloud:
                print "%s: The cloud '%s' is not defined." % ("CM ERROR", name)
                print "Try instead:"
                for keyname in config.keys():
                    print "    ", keyname
                sys.exit(1)

            if cloud['cm_type'] == 'eucalyptus':
                if arguments['--project']:
                    project = arguments['--project']
                    if not project in cloud:
                        print "No such project %s defined in cloud %s." % (project, name)
                        sys.exit(1)
                else:
                    project = config.cloud_default(name, 'project') or config.projects('default')
                    if not project in cloud:
                        print "Default project %s not defined in cloud %s." % (project, name)
                        sys.exit(1)
                rc_func = lambda name: config.rc_euca(name, project)
            else:
                rc_func = config.rc

            result = rc_func(name)

            if arguments["-"]:
                print result
            else:
                if output == None:
                    arguments['--out'] = "%s/%s" % (home, default_path)
                    output = arguments['--out']
                out = False
                try:
                    # First we try to open the file assuming it doesn't exist
                    out = os.open(output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, stat.S_IRUSR | stat.S_IWUSR)
                except OSError as oserr:
                    # If file exists, offer to replace it
                    if oserr.errno == 17:
                        delete = raw_input("'%s' exists; Overwrite it [N|y]? " % output)
                        if delete.strip().lower() == 'y':
                            out = os.open(output, os.O_TRUNC | os.O_WRONLY)
                if out:
                    os.write(out,result)
                    os.close(out)

    ######################################################################
    # END "cm config" related commands
    ######################################################################

if __name__ == '__main__':
    main()

#! /usr/bin/env python
"""cm-rc config
------------
Command to generate rc files from our cloudmesh configuration files.

Usage:
  cm-rc config projects (list|?)
  cm-rc config [-f FILE] [-o OUT] NAME [-]
  cm-rc config dump [--format=(yaml|dict)]
  cm-rc config list
  cm-rc --version
  cm-rc --help

This program generates form a YAML file containing the login
information for a cloud an rc file that can be used to later source
it.

Example:
  we assume the yaml file has an entry india-openstack

    cm-rc config -o novarc india-openstack
    source novarc

  This will create a novarc file and than you can source it.


     cm-rc config ? -

   Presents a selction of cloud choices and writes the choice into a
   file called ~/.futuregrid/novarc

Arguments:
  NAME name of the cloud

Options:
  -h --help            show this help message and exit

  -v --version         show version and exit

  -f NAME --file=NAME  the Name of the cloud to be specified, if ? a selection is presented

  -o OUT --out=OUT     writes the result in the specifide file

  -d  --debug          debug

  -                    this option is a - at the end of the command. If data is written to a file it is also put out to stdout

"""
import yaml
from docopt import docopt
from cm_config import cm_config
import sys
import os

debug = False

def DEBUG(label, var):
    if debug:
        print 70 * "-"
        print label 
        print 70 * " "
        print str(var)
        print 70 * "-"

if __name__ == '__main__':

    default_path = '.futuregrid/novarc'
    arguments = docopt(__doc__, version='1.0.1')

    DEBUG("arguments", arguments)
    
    home = os.environ['HOME']

    DEBUG("home", home)
    

    ######################################################################
    # This secion deals with handeling "cm config" related commands
    ######################################################################
    is_config = arguments['config'] != None

    if is_config:

        print arguments

        file = arguments['--file']
        try:
            config = cm_config(file)
            DEBUG("config", config)
        except:
            print "%s: Configureation file '%s' not found" % ("CM ERROR", file)
            sys.exit(1)

        name = arguments['NAME']


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

        if arguments['list'] or name == 'list':
            for name in config.keys():
                if 'cm_type' in config.data['cloudmesh'][name]:
                    print name, "(%s)" % config.data['cloudmesh'][name]['cm_type']
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
                    if 'cm_type' in config.data['cloudmesh'][name]:
                        print counter, "-" "%20s" % name, "(%s)" % config.data['cloudmesh'][name]['cm_type']
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
            try:
                result = config.rc(name)
            except:
                print "%s: The cloud '%s' can not befound" % ("CM ERROR", name)
                print "Try instead"
                for name in config.keys():
                    if 'cm_type' in config.data['cloudmesh'][name]:
                        print "    ", name

                sys.exit(1)

            if arguments["-"]:
                print result
            else:

                if output == None:
                    arguments['--out'] = "%s/%s" % (home, default_path)
                    output = arguments['--out']
                out = open(output, "w")
                out.write(result)
                out.close()
                os.system("cat " + str(output))

    ######################################################################
    # END "cm config" related commands
    ######################################################################

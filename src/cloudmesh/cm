#! /usr/bin/env python
"""Command to generate rc files from our cloudmesh configuration files.

Usage:
  cm config [-f FILE] [-o OUT] NAME [-]
  cm config list
  cm --version
  cm --help

This program generates form a YAML file containing the login
information for a cloud an rc file that can be used to later source
it. 

Example:
  we assume the yaml file has an entry india-openstack

    cm config -o novarc india-openstack
    source novarc

  This will create a novarc file and than you can source it.


     cm config ? -

   Presents a selction of cloud choices and writes the choice into a
   file called ~/.futuregrid/novarc

Arguments:
  NAME name of the cloud

Options:
  -h --help            show this help message and exit
  -v --version         show version and exit
  -f NAME --file=NAME  the Name of the cloud to be specified, if ? a selection is presented
  -o OUT --out=OUT     writes the result in the specifide file
  -                    if data is written to a file it is also put out to stdout
    
"""
from docopt import docopt
from  cm_config import cm_config
import sys
import os

if __name__ == '__main__':

    default_path = '.futuregrid/novarc'
    arguments = docopt(__doc__, version='1.0.0rc2')

    is_config = arguments['config'] != None

    if is_config:
        file = arguments['--file']
        try:
            config = cm_config(file)
        except:
            print "%s: Configureation file '%s' not found" % ("CM ERROR", file)
            sys.exit(1)


        name = arguments['NAME']
        if name=='list':
            for name in config.keys():
                print name
            sys.exit(0)
        
        if name=='?':
            if file == None:
                home = os.environ['HOME']
                arguments['--out'] = "%s/%s" % (home,default_path)
            print "Please select from the following:"
            print "0 - Cancel"
            selected = False
            choices = []
            while not selected:
                counter = 1
                for name in config.keys():
                    print counter, "-", name
                    choices.append(name)
                    counter += 1
                print "Please select:" 
                input = int(sys.stdin.readline())
                if input == 0:
                    print "Selection terminated"
                    sys.exit(0)
                selected = ( input > 0 ) and ( input < counter )
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
                    print "    ", name
            
                sys.exit(1)
                
            if output == None:
                print result
            else:
                out = open (output, "w+" )
                out.write(result)
                out.close()

        if arguments["-"]:
            filename = arguments['--out']
            os.system ("cat " + filename)


        out.close()
    


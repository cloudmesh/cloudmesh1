#! /usr/bin/env python
"""
Usage:
    cm-image -h | --help
    cm-image --version
    cm-image info
    cm-image build OS
    cm-image register OS

    
Arguments:
    OS        the OS you can find with cm-image list
    GUI       yes or no
    
Options:
    --format=FORMAT        Format of the output json, cfg. [default:json]
    --gui                  switch on the gui

"""

from docopt import docopt
import hostlist
from cloudmesh.util.util import path_expand, banner
import os
import sh


#definitions = ["~/veewee", "$CLOUDMESH/images/veewee"]
definitions = ["$CLOUDMESH/images/veewee"]

def not_implemented():
    print "ERROR: not yet implemented"


def cm_image_command(arguments):

    print(arguments)

    """
    cm-image admin on HOSTS
    cm-image admin off HOSTS
    """

    path = path_expand(definitions[0])
    
    if arguments["info"]:

        banner("info")
        
        for definition in definitions:
            try:
                path = path_expand(definition)
                if os.path.exists(path):
                    os.system("cd '%s' ; veewee vbox list" % path)
                else:
                    print "WARNING: path", path, "does not exist"
            except KeyError, key:
                print 'WARNING: no environment variable called', key, 'found'
                
    elif arguments["build"]:

        banner("build")        
        system_name = arguments["OS"]

        print "System:", system_name
        print "Path:  ", path
        print "Gui:   ", arguments['gui']
        if arguments['gui']:
            gui = ""
        else:
            gui = '--nogui'
        os.system("cd '%s' ; veewee vbox build '%s' --force %s" % (path, system_name, gui))
        # due to some bug the following does not work
        # os.system("veewee vbox build %s --workdir='%s' --force" % (path, system_name))        

    elif arguments["register"]:

        banner("register")
        system_name = arguments["OS"]
        print system_name, path

        banner("export iamge", c="-")
        os.system("cd '%s' ; veewee vbox export '%s'" % (path, system_name))

        banner("add iamge", c="-")
        os.system("cd '%s' ; vagrant box add '%s' '%s.box'" % (path, system_name, system_name))

if __name__ == '__main__':
    arguments = docopt(__doc__)

    cm_image_command(arguments)
    

    

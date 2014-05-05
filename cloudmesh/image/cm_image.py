#! /usr/bin/env python
"""
Usage:
    cm-image -h | --help
    cm-image --version
    cm-image info
    cm-image create OS

    
Arguments:
    OS        the OS you can find with cm-image list
    
Options:
    --format=FORMAT        Format of the output json, cfg. [default:json]


"""

from docopt import docopt
import hostlist
from cloudmesh.util.util import path_expand
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

        for definition in definitions:
            try:
                path = path_expand(definition)
                if os.path.exists(path):
                    os.system("cd '%s' ; veewee vbox list" % path)
                else:
                    print "WARNING: path", path, "does not exist"
            except KeyError, key:
                print 'WARNING: no environment variable called', key, 'found'
                
        

    if arguments["create"]:

        system_name = arguments["OS"]
        print system_name, path
        os.system("cd '%s' ; veewee vbox build '%s' --force" % (path, system_name))
        # due to some bug the following does not work
        # os.system("veewee vbox build %s --workdir='%s' --force" % (path, system_name))        


if __name__ == '__main__':
    arguments = docopt(__doc__)

    cm_image_command(arguments)
    

    

#! /usr/bin/env python
"""
Usage:
    cm-image -h | --help
    cm-image version
    cm-image [--kind=KIND] info
    cm-image [--kind=KIND] [--gui] build OS
    cm-image [--kind=KIND] register OS

    
Arguments:
    OS        the OS you can find with cm-image list
    GUI       yes or no
    
Options:
    --gui                  switch on the gui. [default: False]
    --kind=KIND            the Kind of the image to be created. [default: vbox]
    
"""

from docopt import docopt
import hostlist
from cloudmesh import path_expand, banner
import os
import sh
import cloudmesh


#definitions = ["~/veewee", "$CLOUDMESH/images/veewee"]
definitions = ["$CLOUDMESH/images/veewee"]


def not_implemented():
    print "ERROR: not yet implemented"


def cm_image_command(arguments):
    """
    cm-image admin on HOSTS
    cm-image admin off HOSTS
    """

    path = path_expand(definitions[0])

    if arguments["version"]:

        print cloudmesh.__version__

    elif arguments["info"]:

        banner("info")

        banner("System", c='-')
        print "Kind:   ", arguments['--kind']
        print "Path:   ", path
        print "Version:", cloudmesh.__version__
        banner("List of templates", c='-')
        system_name = None

        for definition in definitions:
            try:
                path = path_expand(definition)
                if os.path.exists(path):
                    os.system("cd '%s' ; veewee vbox list" % path)
                else:
                    print "WARNING: path", path, "does not exist"
            except KeyError, key:
                print 'WARNING: no environment variable called', key, 'found'

        print
        print "To build one, please use one of the"
        print
        print "    cm-image build OS"
        print
        print "Next you need to register the image"
        print
        print "    cm-image register OS"
        print
        print "where OS is one of the labels listed above."
        print

    elif arguments["build"]:

        banner("build")
        system_name = arguments["OS"]

        if arguments['--gui']:
            gui = ""
        else:
            gui = '--nogui'

        if arguments['--kind'] == "vbox":

            os.system("cd '%s' ; veewee vbox build '%s' --force %s" %
                      (path, system_name, gui))
            # due to some bug the following does not work
            # os.system("veewee vbox build %s --workdir='%s' --force" % (path,
            # system_name)
        else:
            print "ERROR: wrong options"

    elif arguments["register"]:

        banner("register")
        system_name = arguments["OS"]
        print system_name, path

        banner("export iamge", c="-")

        if arguments['--kind'] is 'vbox':
            os.system("cd '%s' ; veewee vbox export '%s'" %
                      (path, system_name))

            banner("add iamge", c="-")
            os.system("cd '%s' ; vagrant box add '%s' '%s.box'" %
                      (path, system_name, system_name))


def main():
    arguments = docopt(__doc__)
    cm_image_command(arguments)

if __name__ == '__main__':
    main()

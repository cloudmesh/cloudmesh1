#! /usr/bin/env python
import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cloudmesh.util.util import path_expand
from cloudmesh.user.cm_template import cm_template
from cloudmesh.util.util import yn_choice
from sh import less
import os

from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

def init_shell_command(arguments):
    """
    Usage:
           init [force] generate yaml
           init [force] generate me
           init [force] generate none
           init [force] generate FILENAME
           init list [-f FILENAME]

    Initializes cloudmesh from a yaml file

    Arguments:
       generate   generates a yaml file
       yaml       specifies if a yaml file is used for generation
                  the file is located at ~/.futuregrid/me.yaml
       me         same as yaml

       none       specifies if a yaml file is used for generation
                  the file is located at ~/.futuregrid/etc/none.yaml
       force      force mode does not ask. This may be dangerous as it
                  overwrites the ~/.futuregrid/cloudmesh.yaml file
       FILENAME   The filename to be generated or from which to read
                  information

    Options:

       -v       verbose mode

    Description:

      init list [-f FILENAME]
         Lists the available clouds in the configuration yaml file.

    """
    # log.info(arguments)
    # print "<", args, ">"
    if arguments["list"]:
        print "HALLO"

        filename = arguments['FILENAME']
        if filename is None:
            filename = path_expand('~/.futuregrid/cloudmesh.yaml')
        config = cm_config(filename)

        print config

    if arguments["generate"]:
        new_yaml = path_expand('~/.futuregrid/cloudmesh-new.yaml')
        print "1aaaaaa"
        old_yaml = path_expand('~/.futuregrid/cloudmesh.yaml')
        print "2aaaaaa"
        etc_filename = path_expand("~/.futuregrid/etc/cloudmesh.yaml")
        print "3aaaaaa"

        if arguments["generate"] and (arguments["me"] or arguments["yaml"]):
            print "4aaaaaa"
            me_filename = path_expand("~/.futuregrid/me.yaml")
            print "5aaaaaa"

        elif (args.strip() in ["generate none"]):
            me_filename = path_expand("~/.futuregrid/etc/none.yaml")
        elif arguments["FILENAME"] is not None:
            me_filename = path_expand(arguments["FILENAME"])
        # print me_filename
        # print etc_filename
        print "b"
        t = cm_template(etc_filename)
        print "c"
        t.generate(me_filename, new_yaml)
        print "d"

        if not arguments["force"]:
            if yn_choice("Review the new yaml file", default='n'):
                os.system("less -E {0}".format(new_yaml))
        if arguments["force"]:
            os.system("mv {0} {1}".format(new_yaml, old_yaml))
        elif yn_choice("Move the new yaml file to {0}"
                       .format(old_yaml), default='y'):
            os.system("mv {0} {1}".format(new_yaml, old_yaml))
        return

def init_shell_main():
    arguments = docopt(init_shell_command.__doc__)
    init_shell_command(arguments)

if __name__ == '__main__':
    init_shell_main()

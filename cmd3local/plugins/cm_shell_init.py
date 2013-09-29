import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
from cloudmesh.util.util import path_expand

from cloudmesh.user.cm_template import cm_template
from cloudmesh.util.util import yn_choice
from sh import less
import os


from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_init:

    """opt_example class"""

    def activate_cm_shell_init(self):
        pass

    @command
    def do_init(self, args, arguments):
        """
        Usage:
               init [force] generate yaml
               init [force] generate me
               init [force] generate none
               init [force] generate FILENAME
               
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

        Options:
           
           -v       verbose mode

        """
        # log.info(arguments)
        # print "<", args, ">"

        if arguments["generate"]:

            new_yaml = path_expand('~/.futuregrid/cloudmesh-new.yaml')
            old_yaml = path_expand('~/.futuregrid/cloudmesh.yaml')
            etc_filename = path_expand("~/.futuregrid/etc/cloudmesh.yaml")

            if arguments["generate"] and (arguments["me"] or arguments["yaml"]):
                me_filename = path_expand("~/.futuregrid/me.yaml")

            elif (args.strip() in ["generate none"]):
                me_filename = path_expand("~/.futuregrid/etc/none.yaml")

            elif arguments["FILENAME"] is not None:
                me_filename = path_expand(arguments["FILENAME"])

            # print me_filename
            # print etc_filename

            t = cm_template(etc_filename)
            t.generate(me_filename, new_yaml)

            if not arguments["force"]:
                if yn_choice("Review the new yaml file", default='n'):
                    os.system ("less -E {0}".format(new_yaml))
            if arguments["force"]:
                os.system ("mv {0} {1}".format(new_yaml, old_yaml))
            elif yn_choice("Move the new yaml file to {0}".format(old_yaml), default='y'):
                os.system ("mv {0} {1}".format(new_yaml, old_yaml))

            return






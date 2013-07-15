import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command

from cloudmesh.util.logger import LOGGER

log = LOGGER('project shell')

class cm_shell_project:

    """opt_example class"""

    def activate_cm_shell_project(self):
        pass

    @command
    def do_project(self, args, arguments):
        """
        Usage:
               project info [NAME]
               project members
               project default NAME
               
        Manages the project

        Arguments:

          NAME           The name of a service or server


        Options:

           -v       verbose mode

        """
        log.info(arguments)



        if arguments["default"] and arguments["NAME"]:
            log.info ("delete the project")
            return
        
        if arguments["info"] and arguments["NAME"]:
            log.info ("project info for the NAMED one")
            return

        if arguments["info"] and arguments["NAME"] is None:
            log.info ("project info for all")
            return

        if arguments["members"]:
            log.info ("list the project members")
            return


        
        

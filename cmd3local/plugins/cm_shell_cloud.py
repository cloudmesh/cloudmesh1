import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command

from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_cloud:

    """opt_example class"""

    def activate_cm_shell_cloud(self):
        pass

    @command
    def do_cloud(self, args, arguments):
        """
        Usage:
               cloud
               cloud set
               cloud NAME
               cloud info [NAME]
               cloud on NAME
               cloud off NAME

               
        Manages the cloud

        Arguments:

          NAME           The name of a service or server


        Options:

           -v       verbose mode

        """
        log.info(arguments)
        print "<", args, ">"

        if arguments["set"] or args is None:
            log.info ("set the cloud")
            return

        if arguments["on"] and arguments["NAME"]:
            log.info ("activatethe cloud")
            return

        if arguments["off"] and arguments["NAME"]:
            log.info ("activatethe cloud")
            return
        
        if arguments["info"] and arguments["NAME"]:
            log.info ("cloud info")
            return

        if arguments["create"] and arguments["NAME"]:
            log.info ("cloud info")
            return


        
        

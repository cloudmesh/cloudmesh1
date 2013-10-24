import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
import cloudmesh

from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_list:

    """opt_example class"""

    def activate_cm_shell_list(self):
        pass

    @command
    def do_list(self, args, arguments):
        """
        Usage:
               list
               list flavors 
               list servers
               list images
               
        Options:

           -v       verbose mode

        """
        log.info(args)

        log.info(arguments)


        if arguments["flavors"]:
            log.info ("list flavors")
            return


        if arguments["servers"]:
            log.info ("list servers")
            return


        if arguments["images "]:
            log.info ("list images s")
            return

    @command
    def do_count(self, args, arguments):
        """
        Usage: count
               count flavors 
               count servers
               count images
               
        Options:

           -v       verbose mode

        """
        log.info(args)

        log.info(arguments)


        if arguments["flavors"]:
            log.info ("count flavors")
            return


        if arguments["servers"]:
            log.info ("count servers")
            return


        if arguments["images "]:
            log.info ("list images s")
            return

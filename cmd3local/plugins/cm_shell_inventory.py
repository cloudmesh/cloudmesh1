import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command

from cloudmesh.util.logger import LOGGER

log = LOGGER('inventory shell')

class cm_shell_inventory:

    """opt_example class"""

    def activate_cm_shell_inventory(self):
        pass

    @command
    def do_inventory(self, args, arguments):
        """
        Usage:
               inventory clean
               inventory create server [dynamic] DESCRIPTION
               inventory create service [dynamic] DESCRIPTION
               inventory test me DESCRIPTION
               inventory exists server NAME
               inventory exists service NAME
               inventory print
               inventory info
               inventory info server NAME
               inventory info service NAME
               
        Manages the inventory

        Arguments:

          DESCRIPTION    The hostlist "india[9-11].futuregrid.org,india[01-02].futuregrid.org"

          NAME           The name of a service or server


        Options:
           --clean       cleans the inventory
           --server      define servers

           -v       verbose mode

        """
        log.info(arguments)


        if arguments["clean"]:
            log.info ("clean the inventory")
            return

        if arguments["print"]:
            log.info ("print the inventory")
            return

        if arguments["info"] and not arguments["server"] and not arguments["service"]:
            log.info ("print the inventory")
            return
        

        if arguments["info"] and arguments["server"]:
            name = arguments["NAME"]
            log.info ("info for servers" + name)
            return

        if arguments["info"] and arguments["service"]:
            name = arguments["NAME"]
            log.info ("info for service" + name)
            return


        if arguments["create"] and arguments["server"]:
            hostlist = arguments["DESCRIPTION"]
            log.info ("create servers" + hostlist)
            return

        if arguments["create"] and arguments["service"]:
            hostlist = arguments["DESCRIPTION"]
            log.info ("create services" + hostlist)
            return


        if arguments["exists"] and arguments["server"]:
            name = arguments["NAME"]
            log.info ("exists servers" + name)
            return

        if arguments["exists"] and arguments["service"]:
            name = arguments["NAME"]
            log.info ("exists service" + name)
            return

        
        

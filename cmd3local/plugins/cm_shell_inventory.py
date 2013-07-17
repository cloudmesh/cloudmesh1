import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command

from cloudmesh.util.logger import LOGGER
from cloudmesh.inventory.resources import Inventory

log = LOGGER('inventory shell')

class cm_shell_inventory:

    """opt_example class"""

    
    def activate_cm_shell_inventory(self):
        self.inventory_name = "test"
        
        self.inventory = Inventory(self.inventory_name)
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
               inventory
               inventory print
               inventory info
               inventory server NAME
               inventory service NAME
               
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
        log.info(args)

        if args == "":
            log.info ("print inventory")


        if arguments["clean"]:
            log.info ("clean the inventory")
            return

        if arguments["print"]:
            log.info ("print the inventory")
            self.inventory.pprint()
            return

        if arguments["info"]:
            log.info ("info for servers")
            print
            print "Inventory Information"
            print "---------------------"
            print
            print "%15s:" % "name", self.inventory_name
            print "%15s:" % "clusters", len(self.inventory.clusters), "->", ', '.join([c.name for c in self.inventory.clusters])
            print "%15s:" % "services", len(self.inventory.services)
            print "%15s:" % "servers", len(self.inventory.servers)
            print "%15s:" % "images", len(self.inventory.images) , "->", ', '.join([c.name for c in self.inventory.images])
            print
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

        
        

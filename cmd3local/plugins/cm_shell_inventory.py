import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
from pprint import pprint

from cloudmesh.util.logger import LOGGER
from cloudmesh.inventory.inventory import Inventory
from mongoengine import *

log = LOGGER(__file__)

class cm_shell_inventory:

    """opt_example class"""


    def info_cm_shell_inventory(self):
        print "%20s =" % "DBNAME", self.inventory_name
        
    def activate_cm_shell_inventory(self):
        self.inventory_name = "test"
        db = connect (self.inventory_name)
        
        self.inventory = Inventory()
        pass

    @command
    def do_inventory(self, args, arguments):
        """
        Usage:
               inventory clean
               inventory create image DESCRIPTION             
               inventory create server [dynamic] DESCRIPTION  
               inventory create service [dynamic] DESCRIPTION 
               inventory exists server NAME                   
               inventory exists service NAME                  
               inventory                   
               inventory print        
               inventory info [CLUSTER] [SERVER] [v]     
               inventory server NAME  
               inventory service NAME 
               
        Manages the inventory

            clean       cleans the inventory
            server      define servers

        Arguments:

          DESCRIPTION    The hostlist "india[9-11].futuregrid.org,india[01-02].futuregrid.org"

          NAME           The name of a service or server


        Options:

           v       verbose mode

        """
        if arguments["v"]:
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
            print
            print "Inventory Information"
            print "---------------------"
            print
            if not (arguments["CLUSTER"] or arguments["SERVER"]):

                print self.inventory.print_info()
                print

            if arguments["CLUSTER"] and not arguments["SERVER"]:

                name = arguments["CLUSTER"]

                self.inventory.print_cluster(name)
                
            return

        for kind in ["server","service","image"]:
            if arguments["info"] and arguments[kind]:
                name = arguments["NAME"]
                kind = arguments[kind]
                self.inventory.print_kind(serv, name)
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
            if self.inventory.exists("server", name):
                print "true"
            else:
                print "false"
            return

        if arguments["exists"] and arguments["service"]:
            name = arguments["NAME"]
            if self.inventory.exists("service", name):
                print "true"
            else:
                print "false"
            return

        
        

import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
from pprint import pprint

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

                print "%15s:" % "dbname", self.inventory_name
                print "%15s:" % "clusters", len(self.inventory.clusters), "->", ', '.join([c.name for c in self.inventory.clusters])
                print "%15s:" % "services", len(self.inventory.services)
                print "%15s:" % "servers", len(self.inventory.servers)
                print "%15s:" % "images", len(self.inventory.images) , "->", ', '.join([c.name for c in self.inventory.images])
                print

            if arguments["CLUSTER"] and not arguments["SERVER"]:

                name = arguments["CLUSTER"]
                print "%15s:" % "dbname", self.inventory_name
                print "%15s:" % "cluster", name
                print

                cluster=self.inventory.find("cluster", name)
                m = cluster.management_node
                line = " ".join(["%15s:" % m.name, "%8s" % m.status, m.ip_address,  "M", ""])
                service_line = ', '.join([service.subkind for service in m["services"]])
                service_line = service_line.replace("openstack", "o")
                line += service_line
                print line
                
                servers = cluster.compute_nodes
                for s in servers:
                    line = " ".join(["%15s:" % s.name, "%8s" % s.status, s.ip_address,  "M",""])
                    service_line = ', '.join([str(service.subkind) for service in s["services"]])
                    service_line = service_line.replace("openstack", "o")
                    line += service_line
                    print line
                print

                print "%15s:" % "Legend"
                print "%15s ="% "M", "Management"
                print "%15s ="% "S", "Server"
                print "%15s ="% "o", "OpenStack"
                print "%15s ="% "e", "OpenStack"
                print "%15s ="% "h", "HPC"
                
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

        
        

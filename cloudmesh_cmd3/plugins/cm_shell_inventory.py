from __future__ import print_function
from cmd3.shell import command
from pprint import pprint
from cloudmesh.inventory import Inventory
from cloudmesh_common.logger import LOGGER
log = LOGGER(__file__)


class cm_shell_inventory:

    """opt_example class"""

    inventory_connection = False
    inventory_name = None

    def info_cm_shell_inventory(self):
        print("%20s =" % "inventory_name", self.inventory_name)
        print("%20s =" % "inventory_connection", self.inventory_connection)

    def _connect_to_inventory(self):
        """connects to the inventory and prints an error if not successfull"""
        self.inventory_name = "test"
        try:
            # TODO: port number is missing
            # TODO: should be imported from cloudmesh_server.yaml
            # db = connect(self.inventory_name)
            self.inventory = Inventory()
        except:
            self.Inventory = None
            raise Exception("ERROR: connection to inventory failed")

    def activate_cm_shell_inventory(self):
        self.register_command_topic('cloud', 'inventory')
        try:
            self._connect_to_inventory()
        except Exception, e:
            print(e)
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
               inventory info [--cluster=CLUSTER] [--server=SERVER]
               inventory list [--cluster=CLUSTER] [--server=SERVER]
               inventory server NAME
               inventory service NAME

        Manages the inventory

            clean       cleans the inventory
            server      define servers

        Arguments:

          DESCRIPTION    The hostlist"i[009-011],i[001-002]"

          NAME           The name of a service or server


        Options:

           v       verbose mode

        """
        # if arguments["v"]:
        log.info(arguments)
        log.info(args)

        if args == "":
            log.info("print inventory")

        if arguments["clean"]:
            log.info("clean the inventory")
            return

        if arguments["print"]:
            try:
                self._coonnect_to_inventory(self)
                log.info("print the inventory")
                try:
                    r = self.inventory.find({})
                    for e in r:
                        pprint(e)
                except:
                    raise Exception("Error: problem searching the inventory")

            except Exception, e:
                print(e)

            return

        if arguments["info"]:
            print()
            print("Inventory Information")
            print("---------------------")
            print()
            if not (arguments["--cluster"] or arguments["--server"]):

                print(self.inventory.info())
                print()

            if arguments["--cluster"] and not arguments["--server"]:

                name = arguments["--cluster"]

                r = self.inventory.cluster(name)
                pprint(r)

            return

        for kind in ["server", "service", "image"]:
            if arguments["info"] and arguments[kind]:
                name = arguments["NAME"]
                kind = arguments[kind]
                self.inventory.print_kind(serv, name)
                return

        if arguments["create"] and arguments["server"]:
            hostlist = arguments["DESCRIPTION"]
            log.info("create servers" + hostlist)
            return

        if arguments["create"] and arguments["service"]:
            hostlist = arguments["DESCRIPTION"]
            log.info("create services" + hostlist)
            return

        if arguments["exists"] and arguments["server"]:
            name = arguments["NAME"]
            if self.inventory.exists("server", name):
                print("true")
            else:
                print("false")
            return

        if arguments["exists"] and arguments["service"]:
            name = arguments["NAME"]
            if self.inventory.exists("service", name):
                print("true")
            else:
                print("false")
            return

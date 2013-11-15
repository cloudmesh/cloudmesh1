import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
from cloudmesh.user.cm_user import cm_user
from cloudmesh.cm_mongo import cm_mongo
from pprint import pprint
from prettytable import PrettyTable
from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_vm:

    """opt_example class"""

    def activate_cm_shell_vm(self):
        pass

    @command
    def do_vm(self, args, arguments):
        """
        Usage:
               vm clean
               vm delete NAME
               vm create [NAME]
               vm info [NAME]
               vm cloud NAME
               vm image NAME
               vm flavour NAME
               vm index NAME
               vm count N
               vm list

        Manages the vm

        Arguments:

          NAME           The name of a service or server
          N              The number of VMs to be started


        Options:

           -v       verbose mode

        """
        log.info(arguments)

        if arguments["clean"]:
            log.info ("clean the vm")
            return

        if arguments["delete"] and arguments["NAME"]:
            log.info ("delete the vm")
            return

        if arguments["info"] and arguments["NAME"]:
            log.info ("vm info")
            return

        if arguments["create"] and arguments["NAME"]:
            log.info ("vm info")
            return

        if arguments["list"]:
            c = cm_mongo()
            c.activate(cm_user_id="psjoshi")
            clouds = c.servers(cm_user_id="psjoshi")
            vmList = clouds["sierra_openstack_grizzly"]
            x = PrettyTable()
            x.field_names = (["name", "status", "flavor", "id", "user_id"])
            for key, vm in vmList.items():
                x.add_row([vm['name'], vm['status'], vm['flavor'], vm['id'], vm['user_id']])
            print x

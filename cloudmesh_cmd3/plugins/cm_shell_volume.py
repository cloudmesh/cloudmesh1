import os
import sys
from cmd3.shell import command
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.tables import row_table

log = LOGGER(__file__)

class cm_shell_volume:

    """opt_example class"""

    def activate_cm_shell_volume(self):
        self.register_command_topic('cloud','volume')
        pass

    @command
    def do_volume(self, args, arguments):
        """
        Usage:
            volume list
            volume create
            volume delete VOLUMEID
            volume attach SERVER VOLUMEID
            volume help

        volume management

        Arguments:
            help    Prints the nova manual
            list          
          
        Options:

           -v       verbose mode

        """
        # log.info(arguments)

        if arguments["help"]:
            return
        else:
            print arguments
            return


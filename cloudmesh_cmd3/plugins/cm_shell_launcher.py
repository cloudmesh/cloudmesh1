import os
import sys
from cmd3.shell import command
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.tables import row_table

log = LOGGER(__file__)

class cm_shell_launcher:

    """opt_example class"""

    def activate_cm_shell_launcher(self):
        self.register_command_topic('cloud','launcher')
        pass

    @command
    def do_launcher(self, args, arguments):
        """
        Usage:
            launcher start COOKBOOK
            launcher stop LAUNCHER_ID
            launcher list
            launcher cookbooks list
            launcher import FILEPATH
            launcher export FILEPATH
            launcher help

        An orchestration tool with Chef Cookbooks

        Arguments:

          COOKBOOK       Name of a cookbook
          LAUNCHER_ID    ID of a launcher
          FILEPATH       Filepath
          help           Prints this message
          
        Options:

           -v       verbose mode

        """
        log.info(arguments)

        if arguments["help"]:

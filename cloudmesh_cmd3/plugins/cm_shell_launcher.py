import os
import sys
from cmd3.shell import command
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.tables import row_table
from cmd3.console import Console
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh_install.util import path_expand
from pprint import pprint

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
            launcher import [FILEPATH] [--force]
            launcher export FILEPATH
            launcher help | -h

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

        if arguments["help"] or arguments["-h"]:
            print self.do_launcher.__doc__
        
        elif arguments['import']:
            filepath = "~/.cloudmesh/cloudmesh_launcher.yaml"
            if arguments['FILEPATH']:
                filepath = arguments['FILEPATH']
            try:
                filename = path_expand(filepath)
                fileconfig = ConfigDict(filename=filename)
            except:
                Console.error(
                    "error while loading '{0}', please check".format(filepath))
                return
            try:
                recipis_dict = fileconfig.get("cloudmesh", "launcher", "recipies")
            except:
                Console.error("error while loading recipies from the file")
                
        

from __future__ import print_function
from cmd3.shell import command
from cloudmesh.config.cm_config import cm_config
from cloudmesh_base.logger import LOGGER
from cmd3.console import Console

log = LOGGER(__file__)

class cm_shell_color:

    def activate_cm_shell_yaml(self):
        self.cm_config = cm_config()
        Console.color = self.cm_config.get("cloudmesh.shell.color")
        # BUG: this is not a cloud command but a regular cm command
        # In fact this command should probably moved to cmd3
        # self.register_command_topic('cloud', 'color')
        #

    @command
    def do_color(self, args, arguments):
        """
        ::
        
          Usage:
              color on
              color off
              color

              Turns the shell color printing on or off

          Description:

              color on   switched the color on

              color off  switches the color off

              color      without parameters prints a test to display
                         the various colored mesages. It is intended
                         as a test to see if your terminal supports
                         colors.

        """
        if arguments['on']:
            key = "cloudmesh.shell.color"
            value = True
            self.cm_config._update(key, value)
            self.cm_config.write(format="yaml")
            Console.color = True
            print ("color on.")
        elif arguments['off']:
            key = "cloudmesh.shell.color"
            value = False
            self.cm_config._update(key, value)
            self.cm_config.write(format="yaml")
            Console.color = False
            print ("color off.")
        else:
            print("Color:", Console.color)
            Console.warning("Warning")
            Console.error("Error")
            Console.info("Info")
            Console.msg("Msg")
            Console.ok("Success")

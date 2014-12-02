from __future__ import print_function
from cmd3.shell import command
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_debug:

    def activate_cm_shell_debug(self):
        self.register_command_topic('cloud', 'debug')

    @command
    def do_debug(self, args, arguments):
        """
        Usage:
            debug on
            debug off

            Turns the debug log level on and off.
        """

        self.cm_config_server = cm_config_server()

        if arguments['on']:
            key = "cloudmesh.server.loglevel"
            value = "DEBUG"
            self.cm_config_server._update(key, value)
            self.cm_config_server.write(format="yaml")
            print ("Debug mode is on.")
        elif arguments['off']:
            key = "cloudmesh.server.loglevel"
            value = "ERROR"
            self.cm_config_server._update(key, value)
            self.cm_config_server.write(format="yaml")
            print ("Debug mode is off.")

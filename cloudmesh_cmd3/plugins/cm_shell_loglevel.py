from __future__ import print_function
from cmd3.shell import command
from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_loglevel:

    def activate_cm_shell_loglevel(self):
        self.cm_config = cm_config()
        self.cm_config_server = cm_config_server()
        self.register_command_topic('cloud', 'loglevel')

    @command
    def do_loglevel(self, args, arguments):
        """
        Usage:
            loglevel
            loglevel error
            loglevel warning
            loglevel debug
            loglevel info
            loglevel critical

            Shows current log level or changes it.
        """
        key = "cloudmesh.server.loglevel"
        if arguments['debug']:
            value = "DEBUG"
        elif arguments['error']:
            value = "ERROR"
        elif arguments['warning']:
            value = "WARNING"
        elif arguments['info']:
            value = "INFO"
        elif arguments['critical']:
            value = "CRITICAL"
        else:
            print(self.cm_config_server.get(key))
            return

        self.cm_config_server._update(key, value)
        self.cm_config_server.write(format="yaml")
        log.info("{0} mode is set.".format(value))

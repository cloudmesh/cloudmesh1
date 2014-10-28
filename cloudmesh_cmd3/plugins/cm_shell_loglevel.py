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
            loglevel critical
            loglevel error
            loglevel warning
            loglevel info
            loglevel debug

            Shows current log level or changes it.
            
            loglevel - shows current log level
            critical - shows log message in critical level
            error    - shows log message in error level including critical
            warning  - shows log message in warning level including error
            info     - shows log message in info level including warning
            debug    - shows log message in debug level including info
            
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
            loglevel = self.cm_config_server.get(key)
            print ("Log level: {0}".format(loglevel))
            return

        self.cm_config_server._update(key, value)
        self.cm_config_server.write(format="yaml")
        print ("Log level: {0} is set".format(value))

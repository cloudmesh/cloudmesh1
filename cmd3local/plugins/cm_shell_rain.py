import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import function_command
from cloudmesh.cobbler.cobbler_rain import rain_command

from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)


class cm_shell_rain:

    """The command handler for rain"""

    def activate_cm_shell_rain(self):
        pass

    @function_command(rain_command)
    def do_rain(self, args, arguments):
        log.info(arguments)
        log.info(args)

        rain_command(arguments)
        pass

import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command

from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_rain:

    """The command handler for rain"""

    def activate_cm_shell_rain(self):
        pass

    @command
    def do_rain(self, args, arguments):
        """
        Usage:
            rain -h | --help
            rain --version
        """

        log.info(arguments)
        log.info(args)

        print "==========="
        print arguments
        print "==========="
        print args


        if arguments["info"]:
            log.info ("rain info")
            return





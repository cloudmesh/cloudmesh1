import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
from cloudmesh.util.util import path_expand
from cloudmesh.config.cm_init import init_command

from cloudmesh.user.cm_template import cm_template
from cloudmesh.util.util import yn_choice
from sh import less
import os


from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)


class cm_shell_init:

    """opt_example class"""

    def activate_cm_shell_init(self):
        pass

    @function_command(init_command)
    def do_init(self, args, arguments):
        log.info(arguments)
        log.info(args)

        init_command(arguments)
        pass

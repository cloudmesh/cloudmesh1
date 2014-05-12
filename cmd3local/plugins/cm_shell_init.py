import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import function_command
from cloudmesh.util.util import path_expand
from cloudmesh.config.cm_init import init_shell_command

from cloudmesh.user.cm_template import cm_template
from cloudmesh.util.util import yn_choice
from sh import less
import os


from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)


class cm_shell_init:

    """opt_example class"""

    
    def activate_cm_shell_init(self):
        self.register_command_topic('cloud','init')
        pass

    @function_command(init_shell_command)
    def do_init(self, args, arguments):
        init_shell_command(arguments)
        pass

#    def __init__(self):
#        pass
#
#if __name__ == '__main__':
#    command = cm_shell_init()
#    command.do_init("")

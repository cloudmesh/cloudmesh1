from __future__ import print_function
from pprint import pprint
from cmd3.console import Console
from cmd3.shell import command

class cm_shell_vm0:

    def activate_cm_shell_vm0(self):
        self.register_command_topic('cloud', 'vm0')

    @command
    def do_vm0(self, args, arguments):
        """
        NOT IMPLEMENTED
        """
        pass

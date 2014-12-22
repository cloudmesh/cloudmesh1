from cmd3.shell import function_command
from cloudmesh.user.cm_default import shell_command_default
# BUG: shell_command_default is a shell commnd and should be in the shell directory

class cm_shell_default:

    def activate_cm_shell_default(self):
        self.register_command_topic('cloud', 'default')

    @function_command(shell_command_default)
    def do_default(self, args, arguments):
        shell_command_default(arguments)

from cmd3.shell import function_command
from cloudmesh.user.cm_defaults import shell_command_defaults

class cm_shell_defaults:
    
    def activate_cm_shell_defaults(self):
        self.register_command_topic('cloud','defaults')

    @function_command(shell_command_defaults)
    def do_defaults(self, args, arguments):
    
        shell_command_defaults(arguments)
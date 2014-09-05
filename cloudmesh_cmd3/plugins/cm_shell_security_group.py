from cmd3.shell import function_command
from cloudmesh.iaas.cm_security_group import shell_command_security_group


class cm_shell_security_group:

    def activate_cm_shell_security_group(self):
        self.register_command_topic('cloud', 'security_group')

    @function_command(shell_command_security_group)
    def do_security_group(self, args, arguments):

        shell_command_security_group(arguments)

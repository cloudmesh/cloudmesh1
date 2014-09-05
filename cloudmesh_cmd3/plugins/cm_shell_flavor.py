from cmd3.shell import function_command
from cloudmesh.iaas.cm_flavor import shell_command_flavor


class cm_shell_flavor:

    def activate_cm_shell_flavor(self):
        self.register_command_topic('cloud', 'flavor')

    @function_command(shell_command_flavor)
    def do_flavor(self, args, arguments):

        # args is not needed?
        shell_command_flavor(arguments)

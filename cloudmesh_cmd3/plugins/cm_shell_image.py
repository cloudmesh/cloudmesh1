from cmd3.shell import function_command
from cloudmesh.shell.cm_image import shell_command_image


class cm_shell_image:

    def activate_cm_shell_image(self):
        self.register_command_topic('cloud', 'image')

    @function_command(shell_command_image)
    def do_image(self, args, arguments):

        shell_command_image(arguments)

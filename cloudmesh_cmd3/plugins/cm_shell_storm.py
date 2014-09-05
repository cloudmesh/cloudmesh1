from cmd3.shell import function_command
from cloudmesh.shell.cm_storm import shell_command_storm


class cm_shell_storm:

    def activate_cm_shell_storm(self):
        self.register_command_topic('cloud', 'storm')
        pass

    @function_command(shell_command_storm)
    def do_storm(self, args, arguments):
        shell_command_storm(arguments)
        pass

#    def __storm__(self):
#        pass
#
# if __name__ == '__main__':
#    command = cm_storm()
#    command.do_storm("")

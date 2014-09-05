from cmd3.shell import function_command
from cloudmesh.shell.cm_user import shell_command_user


class cm_shell_user:

    def activate_cm_shell_user(self):
        self.register_command_topic('cloud', 'user')
        pass

    @function_command(shell_command_user)
    def do_user(self, args, arguments):
        shell_command_user(arguments)
        pass

#    def __user__(self):
#        pass
#
# if __name__ == '__main__':
#    command = cm_shell_user()
#    command.do_user("")

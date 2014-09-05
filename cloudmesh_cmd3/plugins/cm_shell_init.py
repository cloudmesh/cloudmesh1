from cmd3.shell import function_command
from cloudmesh.config.cm_init import init_shell_command


class cm_shell_init:

    def activate_cm_shell_init(self):
        self.register_command_topic('cloud', 'init')
        pass

    @function_command(init_shell_command)
    def do_init(self, args, arguments):
        init_shell_command(arguments)
        pass

#    def __init__(self):
#        pass
#
# if __name__ == '__main__':
#    command = cm_shell_init()
#    command.do_init("")

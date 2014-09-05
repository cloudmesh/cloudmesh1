from cmd3.shell import function_command
from cloudmesh.shell.cm_experiment_group import shell_command_experiment_group


class cm_shell_group:

    def activate_cm_shell_group(self):
        self.register_command_topic('cloud', 'group')
        pass

    @function_command(shell_command_experiment_group)
    def do_group(self, args, arguments):
        shell_command_experiment_group(arguments)
        pass

if __name__ == '__main__':
    command = cm_shell_experiment_group()
    command.do_group("")

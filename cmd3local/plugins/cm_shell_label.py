from cmd3.shell import function_command
from cloudmesh.shell.cm_label import shell_command_label

class cm_shell_label:
    
    def activate_cm_shell_label(self):
        # self.register_command_topic('cloud','label')
        pass

    @function_command(shell_command_label)
    def do_label(self, args, arguments):
        shell_command_label(arguments)
        pass

#    def __label__(self):
#        pass
#
#if __name__ == '__main__':
#    command = cm_label()
#    command.do_label("")

from cmd3.shell import function_command
from cloudmesh.shell.cm_open_web import shell_command_open_web

class cm_shell_web:
    
    def activate_cm_shell_web(self):
        self.register_command_topic('gui','web')
        pass

    @function_command(shell_command_open_web)
    def do_web(self, args, arguments):
        shell_command_open_web(arguments)
        pass

if __name__ == '__main__':
    command = cm_shell_web()
    command.do_web("")

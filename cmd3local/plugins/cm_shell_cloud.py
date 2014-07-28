from cmd3.shell import function_command
from cloudmesh.iaas.cm_list import shell_command_cloud

class cm_shell_list:
    
    def activate_cm_shell_list(self):
        self.register_command_topic('cloud','cloud')

    @function_command(shell_command_list)
    def do_list(self, args, arguments):
    
        shell_command_cloud(arguments)
from cmd3.shell import function_command
from cloudmesh.iaas.cm_cloud import shell_command_cloud

class cm_shell_cloud:
    
    def activate_cm_shell_cloud(self):
        self.register_command_topic('cloud','cloud')

    @function_command(shell_command_cloud)
    def do_cloud(self, args, arguments):
    
        shell_command_cloud(arguments)
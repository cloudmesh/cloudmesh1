from cmd3.shell import function_command
from cloudmesh.iaas.cm_vm import shell_command_vm

class cm_shell_vm:
    
    def activate_cm_shell_vm(self):
        self.register_command_topic('cloud','vm')

    @function_command(shell_command_vm)
    def do_vm(self, args, arguments):
	
        shell_command_vm(arguments)

from cmd3.shell import function_command
from cloudmesh.metric.cm_metric import shell_command_metric

class cm_shell_metric:
    
    def activate_cm_shell_metric(self):
        self.register_command_topic('cloud','metric')

    @function_command(shell_command_metric)
    def do_metric(self, args, arguments):
	
	# args is not needed?
        shell_command_metric(arguments)

from cmd3.shell import function_command
from cloudmesh.metric.cm_metric import shell_command_metric
<<<<<<< HEAD
from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)
=======
>>>>>>> 17434a15ae4b02dccd3a3d095ff46842e7388be1

class cm_shell_metric:
    
    def activate_cm_shell_metric(self):
        self.register_command_topic('cloud','metric')

    @function_command(shell_command_metric)
    def do_metric(self, args, arguments):
<<<<<<< HEAD
        shell_command_metric(arguments)
        pass

#    def __metric__(self):
#        pass
#
#if __name__ == '__main__':
#    command = cm_shell_metric()
#    command.do_metric("")


=======
        #log.info(arguments)
        #log.info(args)
	
	# args is not needed?
        shell_command_metric(arguments)
>>>>>>> 17434a15ae4b02dccd3a3d095ff46842e7388be1

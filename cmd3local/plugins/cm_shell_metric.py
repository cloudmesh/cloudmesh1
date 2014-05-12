from cmd3.shell import function_command
from cloudmesh.metric.cm_metric import metric_command
from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_metric:

    """Command handler for metric"""

    def activate_cm_shell_metric(self):
        self.register_command_topic('cloud','metric')
        pass

    @function_command(cm_metric_command)
    def do_metric(self, args, arguments):
        log.info(arguments)
        log.info(args)
	
	# args is not needed?
        metric_command(arguments)
        pass

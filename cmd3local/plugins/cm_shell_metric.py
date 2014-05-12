from cmd3.shell import function_command
from cloudmesh.metric.cm_metric import shell_command_metric
from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_metric:
    
    def activate_cm_shell_metric(self):
        self.register_command_topic('cloud','metric')
        pass

    @function_command(shell_command_metric)
    def do_metric(self, args, arguments):
        shell_command_metric(arguments)
        pass

#    def __metric__(self):
#        pass
#
#if __name__ == '__main__':
#    command = cm_shell_metric()
#    command.do_metric("")



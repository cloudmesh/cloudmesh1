
import cloudmesh
from cmd3.shell import function_command

from cloudmesh.metric.cm_metric import cm_metric_command

from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)


class cm_shell_metric:

    """cm_shell_metric class"""

    def activate_cm_shell_metric(self):
        pass

    @function_command(cm_metric_command)
    def do_metric(self, args, arguments):
        log.info(arguments)
        log.info(args)

        cm_metric_command(arguments)
        pass

from cmd3.shell import command
from cloudmesh_common.logger import LOGGER
from pprint import pprint
from cloudmesh.config.cm_config import DBConnFactory

log = LOGGER(__file__)

class cm_shell_status:

    def activate_cm_shell_status(self):
        self.register_command_topic('cloud', 'status')

    @command
    def do_status(self, args, arguments):
        """
        Usage:
            status mongo

            Shows system status
        """
        if arguments['status'] and arguments['mongo']:
            status = DBConnFactory.getconn("admin")
            pprint (status)

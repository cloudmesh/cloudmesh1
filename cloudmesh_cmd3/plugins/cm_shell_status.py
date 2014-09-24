from cmd3.shell import command
from cloudmesh_common.logger import LOGGER
from pprint import pprint
from cloudmesh.cm_mongo import cm_mongo_status
from cloudmesh_common.tables import two_column_table

log = LOGGER(__file__)

class cm_shell_status:

    def activate_cm_shell_status(self):
        self.register_command_topic('cloud', 'status')

    @command
    def do_status(self, args, arguments):
        """
        Usage:
            status mongo [--format=FORMAT]

            Shows system status
        """
        if arguments['mongo']:
            stat = cm_mongo_status()
            func = getattr(self, "_print_" + str(arguments['--format']))
            func(stat.serverStatus())

    def _print_None(self, data):
        self._print_table(data)

    def _print_json(self, data):
        pprint (data)
      
    def _print_table(self, data):
        print two_column_table(data)

from __future__ import print_function
from cmd3.shell import command
from cloudmesh_common.logger import LOGGER
from pprint import pprint
from cloudmesh.cm_mongo import cm_mongo_status
# from cloudmesh_common.tables import two_column_table

log = LOGGER(__file__)


class cm_shell_status:

    def activate_cm_shell_status(self):
        self.register_command_topic('cloud', 'status')

    @command
    def do_status(self, args, arguments):
        """
        Usage:
            status mongo
            status celery
            status celery ping
            status celery stats
            status rabbitmq

            Shows system status
        """
        # TODO: temp design

        if arguments['mongo']:
            stat = cm_mongo_status()
            pprint(stat.serverStatus())
            # func = getattr(self, "_print_" + str(arguments['--format']))
            # func(stat.serverStatus())

        elif arguments['celery'] and arguments['ping']:

            import celery
            res = celery.current_app.control.inspect().ping()
            print(res)

        elif arguments['celery'] and arguments['stats']:

            import celery
            res = celery.current_app.control.inspect().stats()
            pprint (res)

        elif arguments['celery']:

            # from subprocess import call
            # call(['celery','inspect','ping'])

            import celery
            res = celery.current_app.control.inspect().ping()
            pprint(res)

            # if arguments['--simple'] or arguments['-s']:
            #     res = celery.current_app.control.inspect().ping()
            # else:
            #     res = celery.current_app.control.inspect().stats()
            # func = getattr(self, "_print_" + str(arguments['--format']))

            # func(res)

        elif arguments['rabbitmq']:
            from subprocess import call            
            call(['sudo', 'rabbitmqctl', 'status'])

    '''
    def _print_None(self, data):
        self._print_table(data)

    def _print_json(self, data):
        pprint (data)

    def _print_table(self, data):
        print two_column_table(data)
    '''

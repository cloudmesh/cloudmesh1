import os
import sys
from cmd3.shell import command
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.tables import row_table
from cmd3.console import Console
from pprint import pprint
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config

log = LOGGER(__file__)

class cm_shell_stack:

    """opt_example class"""
    cm_mongo = cm_mongo()
    cm_config = cm_config()

    def activate_cm_shell_stack(self):
        self.register_command_topic('cloud','stack')
        pass

    @command
    def do_stack(self, args, arguments):
        """
        Usage:
            stack start NAME [--template=TEMPLATE] [--param=PARAM]
            stack stop STACK_ID
            stack list
            stack help | -h

        An orchestration tool (OpenStack Heat)

        Arguments:

          STACK_ID       ID of a stack
          help           Prints this message
          
        Options:

           -v       verbose mode

        """
        log.info(arguments)

        if arguments["help"] or arguments["-h"]:
            print self.do_stack.__doc__
        elif arguments['start'] and arguments['NAME']:
            def_cloud = self.cm_config.get_default(attribute='cloud')
            userid = self.cm_config.username()
            t_url = arguments['--template']
            param = arguments['--param']
            s_name = arguments['NAME']
            self.cm_mongo.activate(userid)
            res = self.cm_mongo.stack_create(cloud=def_cloud, cm_user_id=userid,
                                             servername=s_name,
                                             template_url=t_url, parameters=param)
            print res
            return res

        elif arguments['list']:
            userid = self.cm_config.username()
            d = self.cm_mongo.stacks(cm_user_id=userid)
            '''
            Default             | Value
            |
            +---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
            | cm_cloud_type       | openstack
            |
            | description         | Deploy big data MOOC Cloudmesh with IPython
            notebook I590
            |
            | links               | [{u'href':
                u'http://149.165.146.57:8004/v1/3e6eaf1d913a48f694a7bc0fbb027507/stacks/hrlee/05c1b262-59e4-41d6-895f-d620db451c9a',
                u'rel': u'self'}] |
                | stack_status_reason | Stack create completed successfully
                |
                | stack_name          | hrlee
                |
                | creation_time       | 2014-10-07T23:00:26Z
                |
                | cm_type_version     | havana
                |
                | updated_time        | 2014-10-07T23:04:02Z
                |
                | cm_id               | india-t_stacks-hrlee
                |
                | cm_refresh          | 2014-10-16T23-43-33Z
                |
                | cm_cloud            | india
                |
                | cm_user_id          | hrlee
                |
                | stack_status        | CREATE_COMPLETE
                |
                | cm_kind             | t_stacks
                |
                | _id                 | 5440906503a123799785cc5d
                |
                | cm_type             | openstack
                |
                | id                  | 05c1b262-59e4-41d6-895f-d620db451c9a
                |
                +---------------------+
            '''
            table = []
            def_row = { 'host-cloud-type': None,
                     'description': None,
                     'stack_name': None,
                     'creation_time': None,
                     'stack_status': None,
                     'id': None }

            pprint (d)
            #print row_table(d, order=None) #, labels=["Variable", "Value"])

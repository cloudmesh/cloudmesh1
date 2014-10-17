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
            stack start 
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
        elif arguments['list']:
            userid = self.cm_config.username()
            d = self.cm_mongo.stacks(cm_user_id=userid)
            pprint (d)
            #print row_table(d, order=None) #, labels=["Variable", "Value"])

# import os
from __future__ import print_function
import sys
from cloudmesh_common.logger import LOGGER
from cloudmesh.config.cm_config import cm_config
from cloudmesh.user.cm_user import cm_user
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh_common.tables import row_table

from cmd3.console import Console
from cmd3.shell import command
import json
from pprint import pprint

log = LOGGER(__file__)

class cm_shell_quota:

    """opt_example class"""
    _id = "usage"  # id for usage in cm_mongo

    def activate_cm_shell_quota(self):
        self.register_command_topic('cloud', 'quota')

    def get_cloud_name(self, cm_user_id):
        """Returns a default cloud name if exists
        """
        try:
            return self.cm_user.get_defaults(cm_user_id)['cloud']
        except KeyError:
            Console.error('Please set a default cloud.')
            return None

    @command
    def do_quota(self, args, arguments):
        """
        Usage:
            quota [CLOUD] [--format=json]
            quota help | -h

        quota limit on a current project (tenant)

        Arguments:
          
          CLOUD          Cloud name to see the usage
          help           Prints this message

        Options:

           -v       verbose mode

        """
        pprint(arguments)
        
        self.cm_mongo = cm_mongo()
        self.cm_config = cm_config()
        self.cm_user = cm_user()

        if arguments["help"] or arguments["-h"]:
            print (self.do_quota.__doc__)
        else:
            userid = self.cm_config.username()
            self.cm_mongo.activate(userid)

            cloudid = arguments["CLOUD"]
            if cloudid is None:
                cloudid = self.get_cloud_name(userid)
            # if an id is still not found print error
            if cloudid is None:
                Console.error('Please set a default cloud.')
                return
            
            quota = self.cm_mongo.quota(cloudid, userid)
            if arguments["--format"] is None:
                print(row_table(quota, order=None, labels=["Variable", "Value"]))
            elif 'json' in arguments["--format"]:
                print(json.dumps(quota, indent=4))
            else:
                Console.error('Quota is not supported.')
            return quota

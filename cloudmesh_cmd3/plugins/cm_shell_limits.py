# import os
from __future__ import print_function

from cloudmesh_base.logger import LOGGER
from cloudmesh.config.cm_config import cm_config
from cloudmesh.user.cm_user import cm_user
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh_common.tables import row_table

from cmd3.console import Console
from cmd3.shell import command
import json

log = LOGGER(__file__)


class cm_shell_limits:

    """opt_example class"""
    _id = "limits"  # id for usage in cm_mongo

    def activate_cm_shell_limits(self):
        self.register_command_topic('cloud', 'usage')

    def get_cloud_name(self, cm_user_id):
        """Returns a default cloud name if exists
        """
        try:
            return self.cm_user.get_defaults(cm_user_id)['cloud']
        except KeyError:
            log.error('set a default cloud with openstack. "stack" works on'
                      ' openstack platform only')
            return None

    @command
    def do_limits(self, args, arguments):
        """
        ::
        
          Usage:
              limits [CLOUD] [--format=json]
              limits help | -h

          Current usage data with limits on a selected project (tenant)

          Arguments:

            CLOUD          Cloud name to see the usage
            help           Prints this message

          Options:

             -v       verbose mode

        """
        self.cm_mongo = cm_mongo()
        self.cm_config = cm_config()
        self.cm_user = cm_user()

        if arguments["help"] or arguments["-h"]:
            print (self.do_limits.__doc__)
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

            usage_with_limits = self.cm_mongo.usage_with_limits(cloudid,
                                                                userid)

            if arguments["--format"] is None:
                print(row_table(usage_with_limits,
                                order=None,
                                labels=[
                                    "Limits",
                                    "(Used/Max)"
                                    ]))

            elif 'json' in arguments["--format"]:
                print(json.dumps(usage_with_limits, indent=4))
            else:
                Console.error('Quota is not supported.')

            return usage_with_limits

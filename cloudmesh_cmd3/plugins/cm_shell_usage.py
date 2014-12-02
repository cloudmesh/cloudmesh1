# import os
from __future__ import print_function
import sys
from cloudmesh_common.logger import LOGGER
from cloudmesh.config.cm_config import cm_config
from cloudmesh.user.cm_user import cm_user
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh_common.tables import row_table

from cmd3.shell import command

log = LOGGER(__file__)

class cm_shell_usage:

    """opt_example class"""
    _id = "usage"  # id for usage in cm_mongo

    def activate_cm_shell_usage(self):
        self.register_command_topic('cloud', 'usage')
        pass

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
    def do_usage(self, args, arguments):
        """
        Usage:
            usage [CLOUD] [--start=START] [--end=END]
            usage help | -h

        Usage data on a current project (tenant)

        Arguments:
          
          CLOUD          Cloud name to see the usage
          START          start date of usage (YYYY-MM-DD)
          END            end date of usage (YYYY-MM-DD)
          help           Prints this message

        Options:

           -v       verbose mode

        """
        self.cm_mongo = cm_mongo()
        self.cm_config = cm_config()
        self.cm_user = cm_user()

        if arguments["help"] or arguments["-h"]:
            print (self.do_usage.__doc__)
        else:
            userid = self.cm_config.username()
            def_cloud = self.get_cloud_name(userid)
            self.cm_mongo.activate(userid)
            usage = self.cm_mongo.usage(def_cloud, userid)
            # server usages need to be supressed.
            # e.g. {u'hours': 24.00000006388889, u'uptime': 1960234,
            # u'started_at': u'2014-10-07T23:03:57.000000', u'ended_at': None,
            # u'name': u'hrlee-server-2zuvke4wujud', u'tenant_id':
            # u'3e6eaf1d913a48f694a7bc0fbb027507', u'instance_id':
            # u'2c9d24e0-7453-4f83-84b7-f8c0254a574f', u'state':
            # u'active', u'memory_mb': 2048, u'vcpus': 1, u'flavor':
            # u'm1.small', u'local_gb': 20} 
            try:
                usage['server_usages'] = str(len(usage['server_usages'])) + " vms"
            except:
                pass

            print(row_table(usage, order=None, labels=["Variable", "Value"]))

            return usage

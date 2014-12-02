from __future__ import print_function
import os
import sys
from cmd3.shell import command
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.tables import row_table
from cmd3.console import Console
from pprint import pprint
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from cloudmesh.user.cm_user import cm_user
from cloudmesh.util.shellutil import shell_commands_dict_output

log = LOGGER(__file__)

class cm_shell_stack:

    """opt_example class"""
    name = "stack"
    _id = "t_stacks"

    def activate_cm_shell_stack(self):
        self.register_command_topic('cloud','stack')
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
    def do_stack(self, args, arguments):
        """
        Usage:
            stack start NAME [--template=TEMPLATE] [--param=PARAM]
            stack stop NAME
            stack show NAME
            stack list [--refresh] [--column=COLUMN] [--format=FORMAT]
            stack help | -h

        An orchestration tool (OpenStack Heat)

        Arguments:

          NAME           stack name
          help           Prints this message
          
        Options:

           -v       verbose mode

        """
        self.cm_mongo = cm_mongo()
        self.cm_config = cm_config()
        self.cm_user = cm_user()

        log.info(arguments)

        if arguments["help"] or arguments["-h"]:
            print(self.do_stack.__doc__)
        elif arguments['show'] and arguments['NAME']:
            print ("NOT IMPLEMENTED")
            return
        elif arguments['start'] and arguments['NAME']:
            userid = self.cm_config.username()
            def_cloud = self.get_cloud_name(userid)
            t_url = arguments['--template']
            param = arguments['--param']
            s_name = arguments['NAME']
            self.cm_mongo.activate(userid)
            res = self.cm_mongo.stack_create(cloud=def_cloud, cm_user_id=userid,
                                             servername=s_name,
                                             template_url=t_url,
                                             parameters=param)
            print(res)
            return res

        elif arguments['stop'] and arguments['NAME']:
            userid = self.cm_config.username()
            def_cloud = self.get_cloud_name(userid)
            s_name = arguments['NAME']
            self.cm_mongo.activate(userid)
            res = self.cm_mongo.stack_delete(cloud=def_cloud, cm_user_id=userid,
                                       server=s_name)

            return res

        elif arguments['list']:
            userid = self.cm_config.username()
            if arguments['--refresh']:
                self.cm_mongo.activate(userid)
                self.cm_mongo.refresh(cm_user_id=userid, types=[self._id])
            d = self.cm_mongo.stacks(cm_user_id=userid)
            
            columns = None
            if arguments['--column']:
                if arguments['--column'] != "all":
                    columns = [x.strip() for x in arguments['--column'].split(',')]
            else:
                columns = ['stack_name','description', 'stack_status',
                       'creation_time', 'cm_cloud']
                
            if arguments['--format']:
                if arguments['--format'] not in ['table', 'json', 'csv']:
                    Console.error("please select printing format among table, json and csv")
                    return
                else:
                    p_format = arguments['--format']
            else:
                p_format = None
            
            for k, v in d.iteritems():
                for k0, v0 in v.iteritems():
                    if '_id' in v0:
                        del v0['_id']
                
                shell_commands_dict_output(userid,
                                           v,
                                           print_format=p_format,
                                           firstheader="stack_id",
                                           header=columns)

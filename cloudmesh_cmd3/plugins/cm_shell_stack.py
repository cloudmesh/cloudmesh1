import os
import sys
from cmd3.shell import command
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.tables import row_table
from cmd3.console import Console
from pprint import pprint
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from cloudmesh.util.shellutil import shell_commands_dict_output

log = LOGGER(__file__)

class cm_shell_stack:

    """opt_example class"""
    name = "stack"
    _id = "t_stacks"
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
            stack stop NAME
            stack list [--refresh] [--column=COLUMN] [--format=FORMAT]
            stack help | -h

        An orchestration tool (OpenStack Heat)

        Arguments:

          NAME           stack name
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
                                             template_url=t_url,
                                             parameters=param)
            print res
            return res

        elif arguments['stop'] and arguments['NAME']:
            def_cloud = self.cm_config.get_default(attribute='cloud')
            userid = self.cm_config.username()
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
            columns = ['stack_name','description', 'stack_status',
                       'creation_time', 'cm_cloud']
            if arguments['--column'] and arguments['--column'] != "all":
                columns = [x.strip() for x in arguments['--column'].split(',')]
                
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
                
                shell_commands_dict_output(v,
                                           print_format=p_format,
                                           firstheader="stack_id",
                                           header=columns)

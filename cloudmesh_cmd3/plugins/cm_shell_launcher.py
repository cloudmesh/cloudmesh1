import os
import sys
from pprint import pprint
from cloudmesh_install.util import path_expand
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.tables import row_table
from cloudmesh_common.util import get_rand_string
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.config.cm_config import cm_config
from cloudmesh.user.cm_user import cm_user
from cloudmesh.cm_mongo import cm_mongo
from cmd3.shell import command
from cmd3.console import Console

log = LOGGER(__file__)

class cm_shell_launcher:

    """opt_example class"""

    def activate_cm_shell_launcher(self):
        self.register_command_topic('cloud','launcher')
        pass

    @command
    def do_launcher(self, args, arguments):
        """
        Usage:
            launcher start COOKBOOK
            launcher stop LAUNCHER_ID
            launcher list
            launcher cookbooks list
            launcher import [FILEPATH] [--force]
            launcher export FILEPATH
            launcher help | -h

        An orchestration tool with Chef Cookbooks

        Arguments:

          COOKBOOK       Name of a cookbook
          LAUNCHER_ID    ID of a launcher
          FILEPATH       Filepath
          help           Prints this message
          
        Options:

           -v       verbose mode

        """
        log.info(arguments)
        self.cm_mongo = cm_mongo()
        self.cm_config = cm_config()
        self.user = cm_user()

        if arguments["help"] or arguments["-h"]:
            print self.do_launcher.__doc__

        elif arguments['list'] and arguments['cookbooks']:
            print "big_data_mooc"
            print "..."

        elif arguments['start'] and arguments['COOKBOOK']:
            def_cloud = self.cm_config.get_default(attribute='cloud')
            userid = self.cm_config.username()
            self.cm_mongo.activate(userid)
            keyname = self.user.get_defaults(userid)['key']
            s_name = "launcher-{0}-{1}".format(userid, get_rand_string())
            cookbook = arguments['COOKBOOK']
            passwdHash = "123"
            t_url = \
            "https://raw.githubusercontent.com/cloudmesh/cloudmesh/dev/heat-templates/centos6/launcher/launcher.yaml"
            param = {'KeyName': keyname,
                     'Cookbook': cookbook,
                     'PasswdHash': passwdHash}
            log.debug(def_cloud, userid, s_name, t_url, param)
            res = self.cm_mongo.stack_create(cloud=def_cloud, cm_user_id=userid,
                                             servername=s_name,
                                             template_url=t_url,
                                             parameters=param)
            log.debug(res)
            return res

        elif arguments['import']:
            filepath = "~/.cloudmesh/cloudmesh_launcher.yaml"
            if arguments['FILEPATH']:
                filepath = arguments['FILEPATH']
            try:
                filename = path_expand(filepath)
                fileconfig = ConfigDict(filename=filename)
            except:
                Console.error(
                    "error while loading '{0}', please check".format(filepath))
                return
            try:
                recipis_dict = fileconfig.get("cloudmesh", "launcher", "recipies")
            except:
                Console.error("error while loading recipies from the file")
                
        

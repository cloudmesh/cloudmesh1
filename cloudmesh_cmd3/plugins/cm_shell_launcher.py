import os
import sys
import traceback
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
from cloudmesh.util.shellutil import shell_commands_dict_output
from cloudmesh.util.config import ordered_dump
from cloudmesh_common.util import dict_uni_to_ascii

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
            launcher cookbook list [--column=COLUMN] [--format=FORMAT]
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
         
        elif arguments['list'] and arguments['cookbook']:
            userid = self.cm_config.username()
            launchers = self.cm_mongo.launcher_get(userid)
            
            
            if launchers.count() == 0:
                Console.warning("no launcher in database, please import launcher first"
                                "(launcher import [FILEPATH] [--force])")
            else:
                d = {}
                for launcher in launchers:
                    d[launcher['cm_launcher']] = launcher
                    if "_id" in d[launcher['cm_launcher']]:
                        del d[launcher['cm_launcher']]['_id']
                    
            columns = None
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
                
            shell_commands_dict_output(d,
                                       print_format=p_format,
                                       firstheader="launcher",
                                       header=columns
                                       #vertical_table=True
                                       )

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
                recipes_dict = fileconfig.get("cloudmesh", "launcher", "recipies")
            except:
                Console.error("error while loading recipies from the file")
                
            #print recipes_dict
            userid = self.cm_config.username()
            launcher_names = []
            launchers = self.cm_mongo.launcher_get(userid)
            for launcher in launchers:
                launcher_names.append(launcher['cm_launcher'].encode("ascii"))
            
            for key in recipes_dict:
                if key in launcher_names:
                    if arguments['--force']:
                        self.cm_mongo.launcher_remove(userid, key)
                        self.cm_mongo.launcher_import(
                            recipes_dict[key], key, userid)
                        print "launcher '{0}' overwritten.".format(key)
                    else:
                        print "ERROR: launcher '{0}' exists in database, please remove it from database first, or enable '--force' when add".format(key)
                else:
                    self.cm_mongo.launcher_import(
                        recipes_dict[key], key, userid)
                    print "launcher '{0}' added.".format(key)
              
                    
        elif arguments['export']:
            userid = self.cm_config.username()
            launchers = self.cm_mongo.launcher_get(userid)
            
            
            if launchers.count() == 0:
                Console.warning("no launcher in database, please import launcher first"
                                "(launcher import [FILEPATH] [--force])")
            else:
                d = {}
                for launcher in launchers:
                    key = launcher['cm_launcher']
                    d[key] = launcher
                    if "_id" in d[key]:
                        del d[key]['_id']
                    if "cm_launcher" in d[key]:
                        del d[key]['cm_launcher']
                    if "cm_kind" in d[key]:
                        del d[key]['cm_kind']
                    if "cm_user_id" in d[key]:
                        del d[key]['cm_user_id']
                        
                d = dict_uni_to_ascii(d)
                
                pprint(d)
                
                print "exporting to {0}...".format(arguments['FILEPATH'])
                
                try:
                    filename = path_expand(arguments['FILEPATH'])
                    stream = file(filename, 'w')
                    ordered_dump(d, stream=stream)
                    Console.ok("done")
                except Exception, err:
                    Console.error("failed exporting to {0}".format(arguments['FILEPATH']))
                    print traceback.format_exc()
                    print sys.exc_info()[0]
                        
                    
        

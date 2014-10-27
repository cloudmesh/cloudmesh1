# import os
from __future__ import print_function
import sys
import traceback
from pprint import pprint
from cloudmesh_install.util import path_expand
from cloudmesh_common.logger import LOGGER
# from cloudmesh_common.tables import row_table
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
from cloudmesh_install import config_file

log = LOGGER(__file__)


class cm_shell_launcher:

    """opt_example class"""
    _id = "t_stacks"  # id for stack in cm_mongo

    def activate_cm_shell_launcher(self):
        self.register_command_topic('cloud', 'launcher')
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
    def do_launcher(self, args, arguments):
        """
        Usage:
            launcher start MENU
            launcher stop STACK_NAME
            launcher list
            launcher menu [--column=COLUMN] [--format=FORMAT]
            launcher import [FILEPATH] [--force]
            launcher export FILEPATH
            launcher help | -h

        An orchestration tool with Chef Cookbooks

        Arguments:

          MENU           Name of a cookbook
          STACK_NAME     Name of a launcher
          FILEPATH       Filepath
          COLUMN         column name to display
          FORMAT         display format (json, table)
          help           Prints this message

        Options:

           -v       verbose mode

        """
        log.info(arguments)
        self.cm_mongo = cm_mongo()
        self.cm_config = cm_config()
        self.user = cm_user()

        if arguments["help"] or arguments["-h"]:
            print (self.do_launcher.__doc__)

        elif arguments['menu']:
            userid = self.cm_config.username()
            launchers = self.cm_mongo.launcher_get(userid)

            if launchers.count() == 0:
                Console.warning("no launcher in database, please import launcher first"
                                "(launcher import [FILEPATH] [--force])")
                return
            else:
                d = {}
                for launcher in launchers:
                    d[launcher['cm_launcher']] = launcher
                    if "_id" in d[launcher['cm_launcher']]:
                        del d[launcher['cm_launcher']]['_id']

            columns = None
            if arguments['--column']:
                if arguments['--column'] != "all":
                    columns = [x.strip() for x in arguments['--column'].split(',')]
            else:
                columns = ['name', 'description']

            if arguments['--format']:
                if arguments['--format'] not in ['table', 'json', 'csv']:
                    Console.error("please select printing format ",
                                  "among table, json and csv")
                    return
                else:
                    p_format = arguments['--format']
            else:
                p_format = None

            shell_commands_dict_output(d,
                                       print_format=p_format,
                                       firstheader="launcher",
                                       header=columns
                                       # vertical_table=True
                                       )

        elif arguments['list']:
            userid = self.cm_config.username()
            self.cm_mongo.activate(userid)
            self.cm_mongo.refresh(cm_user_id=userid, types=[self._id])
            stacks = self.cm_mongo.stacks(cm_user_id=userid)
            launchers = self.filter_launcher(
                stacks,
                {"search": "contain",
                 "key": "stack_name",
                 "value": "launcher"}
                )
            log.debug(launchers)

            d = {}
            for k0, v0 in launchers.iteritems():
                for k1, v1 in launchers[k0].iteritems():
                    d[v1['id']] = v1
            columns = ['stack_name', 'description', 'stack_status',
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

            shell_commands_dict_output(d,
                                       print_format=p_format,
                                       firstheader="launcher_id",
                                       header=columns
                                       # vertical_table=True
                                       )

        elif arguments['start'] and arguments['MENU']:
            userid = self.cm_config.username()
            def_cloud = self.get_cloud_name(userid)
            self.cm_mongo.activate(userid)
            keyname = self.user.get_defaults(userid)['key']
            cookbook = arguments['MENU']
            s_name = "launcher-{0}-{1}-{2}".format(userid, cookbook, get_rand_string())
            dummy = "123456789"  # doing nothing. just for test
            t_url = "https://raw.githubusercontent.com/cloudmesh/cloudmesh/dev/heat-templates/centos6/launcher/launcher.yaml"
            param = {'KeyName': keyname,
                     'Cookbook': cookbook,
                     'dummy': dummy}
            log.debug(def_cloud, userid, s_name, t_url, param)
            res = self.cm_mongo.stack_create(cloud=def_cloud, cm_user_id=userid,
                                             servername=s_name,
                                             template_url=t_url,
                                             parameters=param)
            log.debug(res)
            if 'error' in res:
                print (res['error']['message'])
            return res

        elif arguments['stop'] and arguments['STACK_NAME']:
            userid = self.cm_config.username()
            def_cloud = self.get_cloud_name(userid)
            s_id = arguments['STACK_NAME']
            self.cm_mongo.activate(userid)
            res = self.cm_mongo.stack_delete(cloud=def_cloud,
                                             cm_user_id=userid,
                                             server=s_id)
            log.debug(res)
            return res

        elif arguments['import']:
            filepath = config_file("/cloudmesh_launcher.yaml")

            if arguments['FILEPATH']:
                filepath = arguments['FILEPATH']
            try:
                filename = path_expand(filepath)
                fileconfig = ConfigDict(filename=filename)
            except Exception, err:
                Console.error(
                    "error while loading '{0}', please check".format(filepath))
                print (traceback.format_exc())
                print (sys.exc_info()[0])
                return
            try:
                recipes_dict = fileconfig.get("cloudmesh", "launcher", "recipies")
            except:
                Console.error("error while loading recipies from the file")

            # print recipes_dict
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
                        print ("launcher '{0}' overwritten.".format(key))
                    else:
                        print ("ERROR: launcher '{0}' exists, "
                               "please remove it first, or use "
                               "'--force' when adding".format(key))
                else:
                    self.cm_mongo.launcher_import(
                        recipes_dict[key], key, userid)
                    print ("launcher '{0}' added.".format(key))

        elif arguments['export']:
            userid = self.cm_config.username()
            launchers = self.cm_mongo.launcher_get(userid)

            if launchers.count() == 0:
                Console.warning(
                    "no launcher in database, "
                    "please import launcher first"
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

                d = {"meta": {"yaml_version": "2.1",
                              "kind": "launcher"},
                     "cloudmesh": {"launcher": {"recipies": d}}}

                pprint(d)

                print ("exporting to {0}...".format(arguments['FILEPATH']))

                try:
                    filename = path_expand(arguments['FILEPATH'])
                    stream = file(filename, 'w')
                    ordered_dump(d, stream=stream)
                    Console.ok("done")
                except Exception, err:
                    Console.error("failed exporting to {0}"
                                  .format(arguments['FILEPATH']))
                    print (traceback.format_exc())
                    print (sys.exc_info()[0])

    def filter_launcher(self, stacks, _filter):
        """Returns if it satisfies the condition of the filter.

        Description:
            This is being used to filter out other stacks not related
            to launcher.  Launcher should starts with 'launcher-xxx'
            in its stack_name.  This way, we can separate general
            stacks and launcher stacks.

        parameter:
            stacks (dict): all stacks
            _filter (dict): key, value, search
        """
        new_stacks = {}
        for k0, v0 in stacks.iteritems():
            new_stacks[k0] = {}
            for k1, v1 in stacks[k0].iteritems():
                try:
                    value = stacks[k0][k1][_filter['key']]
                    if _filter['search'] == "contain":
                        if _filter['value'] in value:
                            new_stacks[k0][k1] = v1
                except KeyError:
                    pass
        return new_stacks

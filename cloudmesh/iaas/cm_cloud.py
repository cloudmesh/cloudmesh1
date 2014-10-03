from cloudmesh_common.logger import LOGGER
from cmd3.console import Console
from cloudmesh.config.cm_config import cm_config
from cloudmesh.cm_mongo import cm_mongo
from tabulate import tabulate
from pprint import pprint
from cloudmesh.util.menu import menu_return_num
from cloudmesh_install.util import yn_choice, path_expand
import sys
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.util.shellutil import shell_commands_dict_output
import csv
from cloudmesh.server.database import Database

log = LOGGER(__file__)


def shell_command_cloud(arguments):
    """
    ::

        Usage:
            cloud [list] [--column=COLUMN] [--format=FORMAT]
            cloud info [CLOUD|--all] [--format=FORMAT]
            cloud alias NAME [CLOUD]
            cloud select [CLOUD]
            cloud on [CLOUD]
            cloud off [CLOUD]
            cloud add <cloudYAMLfile> [--force]
            cloud remove [CLOUD|--all]
            cloud default [CLOUD|--all]
            cloud set flavor [CLOUD] [--name=NAME|--id=ID]
            cloud set image [CLOUD] [--name=NAME|--id=ID]

        Arguments:

          CLOUD                  the name of a cloud
          <cloudYAMLfile>        a yaml file (with full file path) containing
                                 cloud information
          NAME                   name for a cloud (or flavor and image)

        Options:

           --column=COLUMN       specify what information to display in
                                 the columns of the list command. For
                                 example, --column=active,label prints the
                                 columns active and label. Available
                                 columns are active, label, host,
                                 type/version, type, heading, user,
                                 credentials, defaults (all to diplay all,
                                 semiall to display all except credentials
                                 and defaults)
                                 
           --format=FORMAT       output format: table, json, csv

           --all                 display all available columns

           --force               if same cloud exists in database, it will be
                                 overwritten

           --name=NAME           provide flavor or image name

           --id=ID               provide flavor or image id


        Description:

            The cloud command allows easy management of clouds in the
            command shell. The following subcommands exist:

            cloud [list] [--column=COLUMN] [--json|--table]
                lists the stored clouds, optionally, specify columns for more
                cloud information. For example, --column=active,label

            cloud info [CLOUD|--all] [--json|--table]
                provides the available information about the cloud in dict
                format
                options: specify CLOUD to display it, --all to display all,
                         otherwise selected cloud will be used

            cloud alias NAME [CLOUD]
                sets a new name for a cloud
                options: CLOUD is the original label of the cloud, if
                         it is not specified the default cloud is used.


            cloud select [CLOUD]
                selects a cloud to work with from a list of clouds.If the cloud 
                is not specified, it asks for the cloud interactively

            cloud on [CLOUD]
            cloud off [CLOUD]
                activates or deactivates a cloud. if CLOUD is not
                given, the default cloud will be used.


            cloud add <cloudYAMLfile> [--force]
                adds the cloud information to database that is
                specified in the <cloudYAMLfile>. This file is a yaml. You
                need to specify the full path. Inside the yaml, a
                cloud is specified as follows:

                cloudmesh:
                   clouds:
                     cloud1: ...
                     cloud2: ...

                For examples on how to specify the clouds, please see
                cloudmesh.yaml

                options: --force. By default, existing cloud in
                         database cannot be overwirtten, the --force
                         allows overwriting the database values.

            cloud remove [CLOUD|--all]
                remove a cloud from the database, The default cloud is
                used if CLOUD is not specified.
                This command should be used with caution. It is also
                possible to remove all clouds with the option --all

            cloud default [CLOUD|--all]

                show default settings of a cloud, --all to show all clouds

            cloud set flavor [CLOUD] [--name=NAME|--id=ID]

                sets the default flavor for a cloud. If the cloud is
                not specified, it used the default cloud.

            cloud set image [CLOUD] [--name=NAME|--id=ID]

                sets the default flavor for a cloud. If the cloud is
                not specified, it used the default cloud.

    """

    call = CloudCommand(arguments)
    call.call_procedure()


class CloudManage(object):

    '''
    a class provides funtions used to manage cloud info in the mongo
    '''
    connected_to_mongo = False
    mongo = None

    # def __init__(self):
    # self._connect_to_mongo()

    def _connect_to_mongo(self):
        """connects to the mongo database with cm_mongo"""

        #
        # TODO: Fugang i think that cm_mongo or the get function in cm_mongo should be used here
        #
        
        if not self.connected_to_mongo:
            try:
                self.mongo = cm_mongo()
            except:
                log.error("There is a problem with the mongo server")
                return
            self.connected_to_mongo = True

    def _get_user(self, username):
        self._connect_to_mongo() # TODO: i think that cm_mongo does this?
        return self.mongo.db_user.find_one({'cm_user_id': username})

    def get_clouds(self, username, admin=False, getone=False, cloudname=None):
        '''
        retreive cloud information from db_clouds.
        TODO: duplicates functionality from Mongobase class and cm_mongo
        '''
        # DEBUG
        try:
            _args = locals()
            del(_args['self'])
            log.debug("[{0}()] called with [{1}]".format(sys._getframe().f_code.co_name,
                                            str(_args)))
        except:
            pass
        self._connect_to_mongo()
        if getone:
            return self.mongo.db_clouds.find_one({'cm_kind': 'cloud',
                                                  'cm_user_id': username,
                                                  'cm_cloud': cloudname})
        if admin:
            return self.mongo.db_clouds.find({'cm_kind': 'cloud'})
        else:
            return self.mongo.db_clouds.find({'cm_kind': 'cloud',
                                              'cm_user_id': username})

    def get_selected_cloud(self, username):
        # DEBUG
        try:
            _args = locals()
            del(_args['self'])
            log.debug("[{0}()] called with [{1}]".format(sys._getframe().f_code.co_name,
                                            str(_args)))
        except:
            pass

        self._connect_to_mongo()
        user = self.mongo.db_user.find_one({'cm_user_id': username})
        try:
            cloud = user['selected_cloud']
        except:
            defaults = self.mongo.db_defaults.find_one(
                {'cm_user_id': username})
            try:
                cloud = defaults['cloud']
            except:
                Console.warning("no selected cloud and no default cloud is setup, "
                                "please use command 'cloud select [CLOUD]' to select a cloud")
                sys.exit()
            self.mongo.db_user.update({'cm_user_id': username},
                                      {'$set': {'selected_cloud': cloud}})

        return cloud.encode("ascii")

    def update_selected_cloud(self, username, cloudname):
        '''
        set user selected cloud, which is current worked on cloud in the shell
        '''
        self._connect_to_mongo()
        self.mongo.db_user.update({'cm_user_id': username},
                                  {'$set': {'selected_cloud': cloudname}})

    def get_default_cloud(self, username):
        '''
        get the default cloud, return None if not set
        '''
        self._connect_to_mongo()
        try:
            cloud = self.mongo.db_defaults.find_one(
                {'cm_user_id': username})['cloud']
        except:
            cloud = None
        return cloud

    def update_default_cloud(self, username, cloudname):
        '''
        set default cloud
        '''
        self._connect_to_mongo()
        self.mongo.db_defaults.update({'cm_user_id': username},
                                      {'$set': {'cloud': cloudname}})

    def update_cloud_name(self, username, cloudname, newname):
        '''
        change the cloud name in db
        before use this function, check whether cloud exists in db_clouds
        '''
        self._connect_to_mongo()
        self.mongo.db_clouds.update({'cm_kind': 'cloud',
                                     'cm_user_id': username,
                                     'cm_cloud': cloudname},
                                    {'$set': {'cm_cloud': newname}})
        try:
            if cloudname == self.mongo.db_user.find_one(
                    {'cm_user_id': username})['selected_cloud']:
                self.update_selected_cloud(username, newname)
        except:
            pass
        try:
            if cloudname == self.mongo.db_defaults.find_one({'cm_user_id': username})['cloud']:
                self.update_default_cloud(username, newname)
        except:
            pass

    def activate_cloud(self, username, cloudname):
        '''
        activate a cloud
        '''
        # DEBUG
        try:
            _args = locals()
            del(_args['self'])
            log.debug("[{0}()] called with [{1}]".format(sys._getframe().f_code.co_name,
                                            str(_args)))
        except:
            pass

        self._connect_to_mongo()
        cloud = self.mongo.get_cloud(
            cm_user_id=username, cloud_name=cloudname, force=True)

        if not cloud:
            return 0
        else:
            defaults = self.mongo.db_defaults.find_one(
                {'cm_user_id': username})
            if cloudname not in defaults['registered_clouds']:
                defaults['registered_clouds'].append(cloudname)
            if cloudname not in defaults['activeclouds']:
                defaults['activeclouds'].append(cloudname)
            self.mongo.db_defaults.update(
                {'cm_user_id': username}, defaults, upsert=True)
            return 1

    def deactivate_cloud(self, username, cloudname):
        '''
        deactivate a cloud
        simply delete the cloud name from activecloud in db_defaults
        if the cloud is the current default cloud, it will be removed
        '''
        self._connect_to_mongo()
        defaults = self.mongo.db_defaults.find_one({'cm_user_id': username})
        if cloudname in defaults['activeclouds']:
            defaults['activeclouds'].remove(cloudname)
        if "cloud" in defaults and defaults["cloud"] == cloudname:
            del defaults["cloud"]
        self.mongo.db_defaults.update(
            {'cm_user_id': username}, defaults, upsert=True)

    def remove_cloud(self, username, cloudname):
        '''
        remove selected_cloud value if such cloud is removed
        [NOT IMPLEMENTED]default cloud, active cloud, register cloud too if necessary
        '''
        self._connect_to_mongo()
        self.mongo.db_clouds.remove({'cm_kind': 'cloud',
                                     'cm_user_id': username,
                                     'cm_cloud': cloudname})
        cloud = None
        try:
            cloud = self.mongo.db_user.find_one(
                {'cm_user_id': username})['selected_cloud']
        except:
            pass
        if cloudname == cloud:
            self.mongo.db_user.update(
                {'cm_user_id': username}, {'$unset': {'selected_cloud': ''}})

    def get_cloud_defaultinfo(self, username, cloudname):
        '''
        return names of dfault flavor and image of a cloud, none if not exits
        '''
        res = {}

        flavor_id = self.get_default_flavor_id(username, cloudname)
        if flavor_id in [None, 'none']:
            flavorname = "none"
        else:
            try:
                flavorname = self.get_flavors(
                    cloudname=cloudname, getone=True, id=flavor_id)['name']
            except:
                Console.error("problem in retriving flavor name")
                flavorname = 'none'
        res['flavor'] = flavorname

        image_id = self.get_default_image_id(username, cloudname)
        if image_id in [None, 'none']:
            imagename = "none"
        else:
            try:
                imagename = self.get_images(
                    cloudname=cloudname, getone=True, id=image_id)['name']
            except:
                Console.error("problem in retriving image name")
                imagename = 'none'
        res['image'] = imagename

        return res

    def get_default_flavor_id(self, username, cloudname):
        '''
        return the id of the dafault flavor of a cloud
        '''
        self._connect_to_mongo()
        flavor_id = None
        try:
            flavor_id = self.mongo.db_defaults.find_one(
                {'cm_user_id': username})['flavors'][cloudname]
        except:
            pass
        return flavor_id

    def update_default_flavor_id(self, username, cloudname, id):
        '''
        update the id of default flavor of a cloud
        '''
        self._connect_to_mongo()
        flavors = {}
        try:
            flavors = self.mongo.db_defaults.find_one(
                {'cm_user_id': username})['flavors']
        except:
            pass
        flavors[cloudname] = id
        self.mongo.db_defaults.update({'cm_user_id': username},
                                      {'$set': {'flavors': flavors}})

    def get_flavors(self, getall=False, cloudname=None, getone=False, id=None):
        '''
        retrieve flavor information from db_clouds
        '''
        self._connect_to_mongo()
        if getone:
            return self.mongo.db_clouds.find_one({'cm_kind': 'flavors',
                                                  'cm_cloud': cloudname,
                                                  'id': id})
        elif getall:
            return self.mongo.db_clouds.find({'cm_kind': 'flavors'})
        else:
            return self.mongo.db_clouds.find({'cm_kind': 'flavors',
                                              'cm_cloud': cloudname})

    def get_default_image_id(self, username, cloudname):
        '''
        return the id of the dafault image of a cloud
        '''
        self._connect_to_mongo()
        image_id = None
        try:
            image_id = self.mongo.db_defaults.find_one(
                {'cm_user_id': username})['images'][cloudname]
        except:
            pass
        return image_id

    def update_default_image_id(self, username, cloudname, id):
        '''
        update the id of default image of a cloud
        '''
        self._connect_to_mongo()
        images = {}
        try:
            images = self.mongo.db_defaults.find_one(
                {'cm_user_id': username})['images']
        except:
            pass
        images[cloudname] = id
        self.mongo.db_defaults.update({'cm_user_id': username},
                                      {'$set': {'images': images}})

    #
    # TODO: id is built in
    #
    def get_images(self, getall=False, cloudname=None, getone=False, id=None):
        '''
        retrieve image information from db_clouds
        '''
        self._connect_to_mongo()
        if getone:
            return self.mongo.db_clouds.find_one({'cm_kind': 'images',
                                                  'cm_cloud': cloudname,
                                                  'id': id})
        elif getall:
            return self.mongo.db_clouds.find({'cm_kind': 'images'})
        else:
            return self.mongo.db_clouds.find({'cm_kind': 'images',
                                              'cm_cloud': cloudname})

    # ------------------------------------------------------------------------
    # supporting functions for shell
    # ------------------------------------------------------------------------
    def print_cloud_flavors(self, username=None, cloudname=None, itemkeys=None,
                            refresh=False, output=False, print_format="table"):
        '''
        prints flavors of a cloud in shell
        :param username: string user name
        :param cloudname: string one cloud name
        :param itemkesys: a list of lists, The first item in a sublist
                          is used as header name, the folling ones are
                          the path to the value that user wants in the
                          dict, for example:

                          itemkeys = [
                                   ['id', 'id'],
                                   ['name', 'name'],
                                   ['vcpus', 'vcpus'],
                                   ['ram', 'ram'],
                                   ['disk', 'disk'],
                                   ['refresh time', 'cm_refrsh']
                                 ]
                          The first id is the header name, second id is a path.
        :param refresh: refresh flavors of the cloud before printing
        :param output: designed for shell command 'cloud setflavor', output flavor names
        '''
        self._connect_to_mongo()
        if refresh:
            self.mongo.activate(cm_user_id=username, names=[cloudname])
            self.mongo.refresh(
                cm_user_id=username, names=[cloudname], types=['flavors'])

        flavors_dict = self.mongo.flavors(
            clouds=[cloudname], cm_user_id=username)

        if output:
            flavor_names = []
            flavor_ids = []
            headers = ['index']
        else:
            headers = []

        index = 1
        to_print = []

        def _getFromDict(dataDict, mapList):
            # ref:
            # http://stackoverflow.com/questions/14692690/access-python-nested-dictionary-items-via-a-list-of-keys
            return reduce(lambda d, k: d[k], mapList, dataDict)

        for i, v in flavors_dict[cloudname].iteritems():
            values = []
            if output:
                values.append(str(index))
                flavor_names.append(v['name'])
                flavor_ids.append(v['id'])

            for k in itemkeys:
                headers.append(k[0])
                try:
                    values.append(str(_getFromDict(v, k[1:])))
                except:
                    # print sys.exc_info()
                    values.append(None)
            index = index + 1
            to_print.append(values)

        count = index - 1

        # Output format supports json and plain text in a grid table.
        if print_format == "json":
            pprint(flavors_dict[cloudname])
        elif print_format == "csv":
            with open(".temp.csv", "wb") as f:
                w = csv.DictWriter(f, flavors_dict[cloudname].keys())
                w.writeheader()
                w.writerow(flavors_dict[cloudname])
        else:
            #sentence = "flavors of cloud '{0}'".format(cloudname)
            # print "+" + "-" * (len(sentence) - 2) + "+"
            # print sentence
            if to_print:
                print tabulate(to_print, headers, tablefmt="grid")
            #sentence = "count: {0}".format(count)
            # print sentence
            # print "+" + "-" * (len(sentence) - 2) + "+"

        if output:
            return [flavor_names, flavor_ids]

    def print_cloud_images(self, username=None, cloudname=None, itemkeys=None,
                           refresh=False, output=False, print_format="table"):
        '''
        refer to print_cloud_flavors
        '''
        self._connect_to_mongo()
        if refresh:
            self.mongo.activate(cm_user_id=username, names=[cloudname])
            self.mongo.refresh(
                cm_user_id=username, names=[cloudname], types=['images'])

        images_dict = self.mongo.images(
            clouds=[cloudname], cm_user_id=username)

        if output:
            image_names = []
            image_ids = []
            headers = ['index']
        else:
            headers = []

        index = 1
        to_print = []

        def _getFromDict(dataDict, mapList):
            # ref:
            # http://stackoverflow.com/questions/14692690/access-python-nested-dictionary-items-via-a-list-of-keys
            return reduce(lambda d, k: d[k], mapList, dataDict)

        for i, v in images_dict[cloudname].iteritems():
            values = []
            cm_type = v['cm_type']
            if output:
                values.append(str(index))
                image_names.append(v['name'])
                image_ids.append(v['id'])

            for k in itemkeys[cm_type]:
                headers.append(k[0])
                try:
                    values.append(str(_getFromDict(v, k[1:])))
                except:
                    # print sys.exc_info()
                    values.append(None)
            index = index + 1
            to_print.append(values)

        count = index - 1

        # Output format supports json and plain text in a grid table.
        if print_format == "json":
            pprint(images_dict[cloudname])
        elif print_format == "csv":
            with open(".temp.csv", "wb") as f:
                w = csv.DictWriter(f, images_dict[cloudname].keys())
                w.writeheader()
                w.writerow(images_dict[cloudname])
        else:
            #sentence = "images of cloud '{0}'".format(cloudname)
            # print "+" + "-" * (len(sentence) - 2) + "+"
            # print sentence
            if to_print:
                print tabulate(to_print, headers, tablefmt="grid")
            #sentence = "count: {0}".format(count)
            # print sentence
            # print "+" + "-" * (len(sentence) - 2) + "+"

        if output:
            return [image_names, image_ids]

    def print_cloud_servers(self,
                            username=None,
                            cloudname=None,
                            itemkeys=None,
                            refresh=False,
                            output=False,
                            serverdata=None,
                            print_format="table"):
        '''
        prints a cloud's vms or a given list of vms
        :param username: string user name
        :param cloudname: string one cloud name
        :param itemkesys: a list of lists, each list's first item will be used as header name, the folling ones
        are the path to the value that user wants in the dict, for example:
            itemkeys = [
                         ['id', 'id'],
                         ['name', 'name'],
                         ['vcpus', 'vcpus'],
                         ['ram', 'ram'],
                         ['disk', 'disk'],
                         ['refresh time', 'cm_refrsh']
                       ]
                       first id is the header name, second id is a path
        :param refresh: refresh vms of the cloud before printing
        :param output: designed for shell command for selection
        :param serverdata: if provided, the function will print this data instead of vms of a cloud
        '''
        self._connect_to_mongo()
        if refresh:
            self.mongo.activate(cm_user_id=username, names=[cloudname])
            self.mongo.refresh(
                cm_user_id=username,
                names=[cloudname],
                types=['images', 'flavors', 'servers'])

        if serverdata:
            servers_dict = serverdata
        else:
            servers_dict = self.mongo.servers(
                clouds=[cloudname], cm_user_id=username)[cloudname]

        images_dict = self.mongo.images(
            clouds=[cloudname], cm_user_id=username)
        flavors_dict = self.mongo.flavors(
            clouds=[cloudname], cm_user_id=username)

        if output:
            server_names = []
            server_ids = []
            headers = ['index']
        else:
            headers = []

        index = 1
        to_print = []

        def _getFromDict(dataDict, mapList):
            # ref:
            # http://stackoverflow.com/questions/14692690/access-python-nested-dictionary-items-via-a-list-of-keys
            return reduce(lambda d, k: d[k], mapList, dataDict)

        for i, v in servers_dict.iteritems():
            values = []
            cm_type = v['cm_type']
            if output:
                values.append(str(index))
                server_names.append(v['name'])
                server_ids.append(v['id'])

            for k in itemkeys[cm_type]:
                headers.append(k[0])
                try:
                    val = _getFromDict(v, k[1:])
                    # ----------------------------------------
                    # special handler
                    # ----------------------------------------
                    if k[0] == 'flavor':
                        if val in flavors_dict[cloudname]:
                            val = flavors_dict[cloudname][val]['name']
                        else:
                            val = "flavor '{0}' not available anymore".format(
                                val)

                    if k[0] == 'image':
                        if val in images_dict[cloudname]:
                            val = images_dict[cloudname][val]['name']
                        else:
                            val = "image '{0}' not available anymore".format(
                                val)

                    if cm_type == "openstack" and k[0] == 'addresses':
                        tmp = ''
                        for i in val['private']:
                            tmp = tmp + i['addr'] + ', '
                        val = tmp[:-2]
                    # ----------------------------------------
                    values.append(str(val))
                except:
                    # print sys.exc_info()
                    values.append(None)
            index = index + 1
            to_print.append(values)

        count = index - 1

        # Output format supports json and plain text in a grid table.
        if print_format == "json":
            pprint(servers_dict)
        elif print_format == "csv":
            with open(".temp.csv", "wb") as f:
                w = csv.DictWriter(f, servers_dict.keys())
                w.writeheader()
                w.writerow(servers_dict)
        else:
            #sentence = "cloud '{0}'".format(cloudname)
            # print "+" + "-" * (len(sentence) - 2) + "+"
            # print sentence
            if to_print:
                print tabulate(to_print, headers, tablefmt="grid")
            #sentence = "count: {0}".format(count)
            # print sentence
            # print "+" + "-" * (len(sentence) - 2) + "+"

        if output:
            return [server_names, server_ids]
    # ------------------------------------------------------------------------


class CloudCommand(CloudManage):

    '''
    a class provides cloud command functions
    '''

    #
    # TODO create init msg with flag if cm_congig is loaded
    #
    try:
        config = cm_config()
    except:
        Console.error("There is a problem with the configuration yaml files")

    username = config['cloudmesh']['profile']['username']

    def __init__(self, arguments):
        self.arguments = arguments

    def _cloud_list(self):
        if self.arguments["--column"]:
            col_option = [
                'active', 'user', 'label', 'host',
                'type/version', 'type', 'heading']
            if self.arguments["--column"] == 'all':
                col_option.append('credentials')
                col_option.append('defaults')
            elif self.arguments["--column"] == 'semiall':
                pass
            else:
                col_option = [x.strip()
                              for x in self.arguments["--column"].split(',')]

            if not set(col_option).issubset(set(['active',
                                                 'label',
                                                 'host',
                                                 'type/version',
                                                 'type',
                                                 'heading',
                                                 'user',
                                                 'credentials',
                                                 'defaults'])):
                Console.error("ERROR: one or more column type doesn't exist, available columns are: "
                              "active,label,host,type/version,type,heading,user,credentials,defaults  "
                              "('all' to diplay all, 'semiall' to display all except credentials and defauts)")
                return
        else:
            col_option = ['active']
        headers = ['cloud'] + col_option
        standard_headers = []
        combined_headers = []

        def attribute_name_map(name):
            if name == "cloud":
                return "cm_cloud"
            elif name == "label":
                return "cm_label"
            elif name == "host":
                return "cm_host"
            elif name == "type/version":
                return "cm_type_version"
            elif name == "type":
                return "cm_type"
            elif name == "heading":
                return "cm_heading"
            elif name == "user":
                return "cm_user_id"
            elif name == "credentials":
                return "credentials"
            elif name == "defaults":
                return "default"
            else:
                return name

        for item in headers:
            temp = attribute_name_map(item)
            standard_headers.append(temp)
            combined_headers.append([item, temp])

        combined_headers.remove(['cloud', 'cm_cloud'])

        clouds = self.get_clouds(self.username)
        clouds = clouds.sort([('cm_cloud', 1)])
        self._connect_to_mongo()
        activeclouds = self.mongo.active_clouds(self.username)

        if clouds.count() == 0:
            Console.warning(
                "no cloud in database, please import cloud information using the command")
        else:
            d = {}
            for cloud in clouds:
                res = {}
                for key in standard_headers:
                    # -------------------------------------------------
                    # special informations from other place
                    # -------------------------------------------------
                    if key == "active":
                        if cloud['cm_cloud'] in activeclouds:
                            res["active"] = 'True'
                    elif key == "default":
                        defaultinfo = self.get_cloud_defaultinfo(
                            self.username, cloud['cm_cloud'])
                        res["default"] = str(defaultinfo)
                    # -------------------------------------------------
                    else:
                        try:
                            res[key] = str(cloud[key])
                        except:
                            pass
                d[cloud['cm_cloud']] = res
                
            if self.arguments['--format']:
                if self.arguments['--format'] not in ['table', 'json', 'csv']:
                    Console.error("please select printing format among table, json and csv")
                    return
                else:
                    p_format = self.arguments['--format']
            else:
                p_format = None

            shell_commands_dict_output(d,
                                       print_format=p_format,
                                       firstheader="cloud",
                                       header=combined_headers,
                                       oneitem=False,
                                       title=None,
                                       count=False)

    def _cloud_info(self):
        def printing(cloud):
            if '_id' in cloud:
                del cloud['_id']
            # cloud = dict_uni_to_ascii(cloud)
            # banner(cloud['cm_cloud'])
            # -------------------------------------------------
            # special informations from other place
            # -------------------------------------------------
            self._connect_to_mongo()
            # print "#", 70 * "-"
            if cloud['cm_cloud'] in self.mongo.active_clouds(self.username):
                cloud["active"] = "True"
            else:
                cloud["active"] = "False"

            defaultinfo = self.get_cloud_defaultinfo(
                self.username, cloud['cm_cloud'])
            cloud["default flavor"] = defaultinfo['flavor']
            cloud["default image"] = defaultinfo['image']
            # print "#", 70 * "#", "\n"
            # -------------------------------------------------
            
            if self.arguments['--format']:
                if self.arguments['--format'] not in ['table', 'json', 'csv']:
                    Console.error("please select printing format among table, json and csv")
                    return
                else:
                    p_format = self.arguments['--format']
            else:
                p_format = None
            
            shell_commands_dict_output(cloud,
                                       print_format=p_format,
                                       # "cloud '{0}' information".format(cloud['cm_cloud']),
                                       title=None,
                                       oneitem=True)

        if self.arguments['CLOUD']:
            cloud = self.get_clouds(
                self.username, getone=True, cloudname=self.arguments['CLOUD'])
            if cloud is None:
                Console.warning(
                    "ERROR: could not find cloud '{0}'".format(self.arguments['CLOUD']))
            else:
                printing(cloud)
        elif self.arguments['--all']:
            clouds = self.get_clouds(self.username)
            clouds = clouds.sort([('cm_cloud', 1)])
            if clouds.count() == 0:
                Console.info(
                    "no cloud in database, please import cloud information by 'cloud add <cloudYAMLfile>'")
                return
            for cloud in clouds:
                printing(cloud)
        else:
            selected_cloud = self.get_selected_cloud(self.username)
            cloud = self.get_clouds(
                self.username, getone=True, cloudname=selected_cloud)
            if cloud is None:
                Console.warning(
                    "no cloud information of '{0}' in database".format(selected_cloud))
                return
            printing(cloud)

    def _cloud_select(self):
        if self.arguments['CLOUD']:
            cloud = self.get_clouds(
                self.username, getone=True, cloudname=self.arguments['CLOUD'])
            if cloud is None:
                Console.warning("no cloud information of '{0}' in database, please import it by 'cloud add <cloudYAMLfile>'".format(
                    self.arguments['CLOUD']))
                return
            self.update_selected_cloud(self.username, self.arguments['CLOUD'])
            Console.ok("cloud '{0}' is selected".format(self.arguments['CLOUD']))
        else:
            clouds = self.get_clouds(self.username)
            cloud_names = []
            for cloud in clouds:
                cloud_names.append(cloud['cm_cloud'].encode("ascii"))
            cloud_names.sort()
            res = menu_return_num(
                title="select a cloud", menu_list=cloud_names, tries=3)
            if res == 'q':
                return
            self.update_selected_cloud(self.username, cloud_names[res])
            Console.ok("cloud '{0}' is selected".format(cloud_names[res]))

    def _cloud_alias(self):
        if self.arguments['CLOUD']:
            name = self.arguments['CLOUD']
        else:
            name = self.get_selected_cloud(self.username)
        if self.get_clouds(self.username, getone=True, cloudname=name) is None:
            log.error("no cloud information of '{0}' in database".format(name))
            return
        if yn_choice("rename cloud '{0}' to '{1}'?".format(name,
                                                           self.arguments['NAME']),
                     default='n',
                     tries=3):
            self.update_cloud_name(self.username, name, self.arguments['NAME'])
        else:
            return

    def _cloud_activate(self):
        # DEBUG
        try:
            _args = locals()
            del(_args['self'])
            log.debug("[{0}()] called with [{1}]".format(sys._getframe().f_code.co_name,
                                            str(_args)))
        except:
            pass

        if self.arguments['CLOUD']:
            name = self.arguments['CLOUD']
        else:
            name = self.get_selected_cloud(self.username)
        if self.get_clouds(self.username, getone=True, cloudname=name) is None:
            log.error("no cloud information of '{0}' in database".format(name))
            return

        # confirmation
        # if yn_choice("activate cloud '{0}'?".format(name), default = 'n', tries = 3):
        #    res = self.activate_cloud(self.username, name)
        #    if res == 0:
        #        return
        #    elif res == 1:
        #        print "cloud '{0}' activated.".format(name)
        # else:
        #    return

        res = self.activate_cloud(self.username, name)
        if res == 0:
            Console.warning("failed to activate cloud '{0}'".format(name))
        elif res == 1:
            Console.ok("cloud '{0}' activated.".format(name))

    def _cloud_deactivate(self):
        if self.arguments['CLOUD']:
            name = self.arguments['CLOUD']
        else:
            name = self.get_selected_cloud(self.username)
        if self.get_clouds(self.username, getone=True, cloudname=name) is None:
            log.error("no cloud information of '{0}' in database".format(name))
            return
        '''
        # confirmation
        if yn_choice("deactivate cloud '{0}'?".format(name), default = 'n', tries = 3):
            self.deactivate_cloud(self.username, name)
            print "cloud '{0}' deactivated.".format(name)
        else:
            return
        '''
        self.deactivate_cloud(self.username, name)
        Console.ok("cloud '{0}' deactivated.".format(name))

    def _cloud_import(self):
        try:
            filename = path_expand(self.arguments["<cloudYAMLfile>"])
            fileconfig = ConfigDict(filename=filename)
        except:
            log.error(
                "ERROR: could not load file, please check filename and its path")
            return

        try:
            cloudsdict = fileconfig.get("cloudmesh", "clouds")
        except:
            log.error("ERROR: could not get clouds information from yaml file, "
                      "please check you yaml file, clouds information must be "
                      "under 'cloudmesh' -> 'clouds' -> cloud1...")
            return
        cloud_names = []
        clouds = self.get_clouds(self.username)
        for cloud in clouds:
            cloud_names.append(cloud['cm_cloud'].encode("ascii"))

        for key in cloudsdict:
            if key in cloud_names:
                if self.arguments['--force']:
                    self.remove_cloud(self.username, key)
                    Database.import_cloud_to_mongo(
                        cloudsdict[key], key, self.username)
                    print "cloud '{0}' overwritten.".format(key)
                else:
                    print "ERROR: cloud '{0}' exists in database, please remove it from database first, or enable '--force' when add".format(key)
            else:
                Database.import_cloud_to_mongo(
                    cloudsdict[key], key, self.username)
                print "cloud '{0}' added.".format(key)

    def _cloud_remove(self):
        if self.arguments['--all']:
            if yn_choice("CAUTION: Do you want to remove all clouds from database?",
                         default='n',
                         tries=3):
                cloud_names = []
                clouds = self.get_clouds(self.username)
                for cloud in clouds:
                    cloud_names.append(cloud['cm_cloud'].encode("ascii"))
                for name in cloud_names:
                    self.remove_cloud(self.username, name)
                    print "cloud '{0}' removed.".format(name)
                return
            else:
                return

        if self.arguments['CLOUD']:
            name = self.arguments['CLOUD']
        else:
            name = self.get_selected_cloud(self.username)
        if self.get_clouds(self.username, getone=True, cloudname=name) is None:
            log.error("no cloud information of '{0}' in database".format(name))
            return
        if yn_choice("remove cloud '{0}' from database?".format(name),
                     default='n',
                     tries=3):
            self.remove_cloud(self.username, name)
            print "cloud '{0}' removed.".format(name)
            return
        else:
            return

    def _cloud_list_default(self):
        '''
        think: refresh before list?
        '''
        headers = ['cloud', 'default flavor', 'default image']
        to_print = []
        if self.arguments['--all']:
            # list all clouds' default flavor and image, default cloud

            clouds = self.get_clouds(self.username)
            clouds = clouds.sort([('cm_cloud', 1)])
            for cloud in clouds:
                defaultinfo = self.get_cloud_defaultinfo(
                    self.username, cloud['cm_cloud'])
                row = [cloud['cm_cloud'].encode("ascii"),
                       defaultinfo['flavor'],
                       defaultinfo['image']]
                to_print.append(row)
            print tabulate(to_print, headers, tablefmt="grid")

            current_default = self.get_default_cloud(self.username)
            sentence = "current default cloud '{0}'".format(current_default)
            print "+" + "-" * (len(sentence) - 2) + "+"
            print sentence
            print "+" + "-" * (len(sentence) - 2) + "+"
        else:
            name = self.get_working_cloud_name()
            if name:
                defaultinfo = self.get_cloud_defaultinfo(self.username, name)
                to_print = [
                    [name, defaultinfo['flavor'], defaultinfo['image']]]
                print tabulate(to_print, headers, tablefmt="grid")
            else:
                return

    
    def _cloud_set_flavor(self):
        '''
        refresh before actually select a flaovr of the cloud
        '''
        cloudname = self.get_working_cloud_name()
        if cloudname:
            flavor_id = None
            flavor_name = None
            if self.arguments['--name'] or self.arguments['--id']:
                self._connect_to_mongo()
                self.mongo.activate(
                    cm_user_id=self.username, names=[cloudname])
                self.mongo.refresh(
                    cm_user_id=self.username, names=[cloudname], types=['flavors'])
                flavor_dict = self.mongo.flavors(
                    clouds=[cloudname], cm_user_id=self.username)[cloudname]
                if self.arguments['--name']:
                    for k, v in flavor_dict.iteritems():
                        if v['name'] == self.arguments['--name']:
                            flavor_name = self.arguments['--name']
                            flavor_id = k
                    if flavor_name is None:
                        Console.warning("Could not find flavor name '{0}' on '{1}'".format(
                            self.arguments['--name'], cloudname))
                        return
                elif self.arguments['--id']:
                    if self.arguments['--id'] in flavor_dict.keys():
                        flavor_name = flavor_dict[
                            self.arguments['--id']]['name']
                        flavor_id = self.arguments['--id']
                    else:
                        Console.warning("Could not find flavor id '{0}' on '{1}'".format(
                            self.arguments['--id'], cloudname))
                        return
            else:
                itemkeys = [
                    ['id', 'id'],
                    ['name', 'name'],
                    ['vcpus', 'vcpus'],
                    ['ram', 'ram'],
                    ['disk', 'disk'],
                    ['refresh time', 'cm_refresh']
                ]
                flavor_lists = self.print_cloud_flavors(username=self.username,
                                                        cloudname=cloudname,
                                                        itemkeys=itemkeys,
                                                        refresh=True,
                                                        output=True)
                
                current_default_flavor = self.get_cloud_defaultinfo(self.username, 
                                                                   cloudname)['flavor']
                
                res = menu_return_num(
                    title="select a flavor by index (current default: {0})".format(current_default_flavor), 
                    menu_list=flavor_lists[0], tries=3)
                if res == 'q':
                    return
                flavor_id = flavor_lists[1][res]
                flavor_name = flavor_lists[0][res]

            self.update_default_flavor_id(self.username, cloudname, flavor_id)
            Console.ok("'{0}' is selected".format(flavor_name))
        else:
            return

    def _cloud_set_image(self):
        '''
        refresh before actually select a image of the cloud
        '''
        cloudname = self.get_working_cloud_name()
        if cloudname:
            image_id = None
            image_name = None
            if self.arguments['--name'] or self.arguments['--id']:
                self._connect_to_mongo()
                self.mongo.activate(
                    cm_user_id=self.username, names=[cloudname])
                self.mongo.refresh(
                    cm_user_id=self.username, names=[cloudname], types=['images'])
                image_dict = self.mongo.images(
                    clouds=[cloudname], cm_user_id=self.username)[cloudname]
                if self.arguments['--name']:
                    for k, v in image_dict.iteritems():
                        if v['name'] == self.arguments['--name']:
                            image_name = self.arguments['--name']
                            image_id = k
                    if image_name is None:
                        Console.warning("Could not find image name '{0}' on '{1}'".format(
                            self.arguments['--name'], cloudname))
                        return
                elif self.arguments['--id']:
                    if self.arguments['--id'] in image_dict.keys():
                        image_name = image_dict[
                            self.arguments['--id']]['name']
                        image_id = self.arguments['--id']
                    else:
                        Console.warning("Could not find image id '{0}' on '{1}'".format(
                            self.arguments['--id'], cloudname))
                        return
            else:
                itemkeys = {"openstack":
                            [
                                # [ "Metadata", "metadata"],
                                ["name", "name"],
                                ["status", "status"],
                                ["id", "id"],
                                ["type_id", "metadata", "instance_type_id"],
                                ["iname", "metadata", "instance_type_name"],
                                ["location", "metadata", "image_location"],
                                ["state", "metadata", "image_state"],
                                ["updated", "updated"],
                                # [ "minDisk" , "minDisk"],
                                ["memory_mb", "metadata",
                                    'instance_type_memory_mb'],
                                ["fid", "metadata", "instance_type_flavorid"],
                                ["vcpus", "metadata", "instance_type_vcpus"],
                                # [ "user_id" , "metadata", "user_id"],
                                # [ "owner_id" , "metadata", "owner_id"],
                                # [ "gb" , "metadata", "instance_type_root_gb"],
                                # [ "arch", ""]
                            ],
                            "ec2":
                            [
                                # [ "Metadata", "metadata"],
                                ["state", "extra", "state"],
                                ["name", "name"],
                                ["id", "id"],
                                ["public", "extra", "is_public"],
                                ["ownerid", "extra", "owner_id"],
                                ["imagetype", "extra", "image_type"]
                            ],
                            "azure":
                            [
                                ["name", "label"],
                                ["category", "category"],
                                ["id", "id"],
                                ["size", "logical_size_in_gb"],
                                ["os", "os"]
                            ],
                            "aws":
                            [
                                ["state", "extra", "state"],
                                ["name", "name"],
                                ["id", "id"],
                                ["public", "extra", "ispublic"],
                                ["ownerid", "extra", "ownerid"],
                                ["imagetype", "extra", "imagetype"]
                            ]
                            }
                image_lists = self.print_cloud_images(username=self.username,
                                                      cloudname=cloudname,
                                                      itemkeys=itemkeys,
                                                      refresh=True,
                                                      output=True)
                current_default_image = self.get_cloud_defaultinfo(self.username, 
                                                                   cloudname)['image']
                res = menu_return_num(
                    title="select a image by index (current default: {0})".format(current_default_image), 
                    menu_list=image_lists[0], tries=3)
                if res == 'q':
                    return
                image_id = image_lists[1][res]
                image_name = image_lists[0][res]

            self.update_default_image_id(self.username, cloudname, image_id)
            Console.ok("'{0}' is selected".format(image_name))
        else:
            return

    # --------------------------------------------------------------------------
    def get_working_cloud_name(self):
        '''
        get the name of a cloud to work on, if CLOUD not given, will pick the
        selected cloud
        '''
        if self.arguments['CLOUD']:
            name = self.arguments['CLOUD']
        else:
            name = self.get_selected_cloud(self.username)
        if self.get_clouds(self.username, getone=True, cloudname=name) is None:
            Console.error("no cloud information of '{0}' in database".format(name))
            return False
        return name

    def call_procedure(self):
        # print self.arguments ###########
        if 'list' in self.arguments and self.arguments['list']:
            self._cloud_list()

        elif 'info' in self.arguments and self.arguments['info']:
            self._cloud_info()

        elif 'alias' in self.arguments and self.arguments['alias']:
            self._cloud_alias()

        elif 'select' in self.arguments and self.arguments['select']:
            self._cloud_select()

        elif 'on' in self.arguments and self.arguments['on']:
            self._cloud_activate()

        elif 'off' in self.arguments and self.arguments['off']:
            self._cloud_deactivate()

        elif 'add' in self.arguments and self.arguments['add']:
            self._cloud_import()

        elif 'remove' in self.arguments and self.arguments['remove']:
            self._cloud_remove()

        elif 'default' in self.arguments and self.arguments['default']:
            self._cloud_list_default()

        elif 'set' in self.arguments and self.arguments['set']:

            if 'flavor' in self.arguments and self.arguments['flavor']:
                self._cloud_set_flavor()

            elif 'image' in self.arguments and self.arguments['image']:
                self._cloud_set_image()
        else:
            self._cloud_list()

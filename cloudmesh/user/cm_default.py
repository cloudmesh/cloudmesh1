from __future__ import print_function
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.tables import row_table
from cmd3.console import Console
from cloudmesh.user.cm_user import cm_user
from cloudmesh.config.cm_config import cm_config
from cloudmesh.util.shellutil import shell_commands_dict_output
from cloudmesh.iaas.cm_cloud import shell_command_cloud

log = LOGGER(__file__)


def shell_command_default(arguments):
    """
    ::

    Usage:
        default [--column=COLUMN] [--format=FORMAT]
        default cloud [VALUE]
        default format [VALUE]
        default flavor [CLOUD] [--name=NAME|--id=ID]
        default image [CLOUD] [--name=NAME|--id=ID]

    Arguments:

        VALUE    provide a value to update default setting
        CLOUD   provide a cloud name to work with, if not
                      specified, the default cloud or a selected
                      cloud will be used

    Options:

        --column=COLUMN  specify what information to display.
                         The columns are specified as a comma
                         separated list. For example: cloud,format
        --format=FORMAT  output format: table, json, csv
        --name=NAME      provide flavor or image name
        --id=ID          provide flavor or image id

    Description:

        default [--column=COLUMN] [--format=FORMAT]
            print user defaults settings

        default cloud [VALUE]
            print or change (if VALUE provided) default cloud. To set
            a cloud as default, it must be registered and active (to
            list clouds: cloud [list]; to activate a cloud: cloud on
            [CLOUD])

        default format [VALUE]
            print or change(if VALUE provided) default print format,
            available formats are table, json, csv

        default flavor [CLOUD] [--name=NAME|--id=ID]
            set default flavor for a cloud, same as command:

                cloud set flavor [CLOUD] [--name=NAME|--id=ID]

            (to check a cloud's default settings:
             cloud default [CLOUD|--all])

        default image [CLOUD] [--name=NAME|--id=ID]
            set default image for a cloud, same as command:

             cloud set image [CLOUD] [--name=NAME|--id=ID]

            (to check a cloud's default settings:
             cloud default [CLOUD|--all])

    """
    call = DefaultCommand(arguments)
    call.execute()


class DefaultCommand(object):
    try:
        config = cm_config()
    except:
        Console.error("There is a problem with the configuration yaml files")

    username = config['cloudmesh']['profile']['username']

    started_cm_user = False
    user_obj = None

    def _start_cm_user(self):
        if not self.started_cm_user:
            try:
                self.user_obj = cm_user()
            except:
                Console.error("There is a problem with "
                              "cm_user object initialization")
                return
            self.started_cm_user = True

    def __init__(self, arguments):
        self.arguments = arguments

    def _default_format(self):
        self._start_cm_user()
        defaults_data = self.user_obj.info(self.username)['defaults']
        if self.arguments['VALUE']:
            allowed_formats = ['table', 'json', 'csv']
            if self.arguments['VALUE'] not in allowed_formats:
                Console.warning("allowed formats are {0}".format(str(allowed_formats)))
                return
            else:
                defaults_data['shell_print_format'] = self.arguments['VALUE']
                self.user_obj.set_defaults(self.username, defaults_data)
                Console.ok("set '{0}' as default print format".format(self.arguments['VALUE']))
        else:
            format = None
            try:
                format = defaults_data['shell_print_format']
            except:
                pass
            if format not in [None, 'none']:
                print(defaults_data['shell_print_format'])
            else:
                defaults_data['shell_print_format'] = "table"
                self.user_obj.set_defaults(self.username, defaults_data)
                defaults_data = self.user_obj.info(self.username)
                print(defaults_data['shell_print_format'])

    def get_defaults(self):
        '''
        return all defaults in dict
        '''
        self._start_cm_user()
        defaults_data = self.user_obj.info(self.username)['defaults']
        if '_id' in defaults_data:
            del defaults_data['_id']
        return defaults_data

    def _print_default(self, attr=None):
        to_print = self.get_defaults()

        columns = None
        if attr:
            columns = [attr]
        elif self.arguments['--column'] and self.arguments['--column'] != "all":
            columns = [x.strip() for x in self.arguments['--column'].split(',')]
            # ----------------------------------
            # flexible input
            for index, item in enumerate(columns):
                if item in ['format']:
                    columns[index] = "shell_print_format"
            # ----------------------------------

        if self.arguments['--format']:
            if self.arguments['--format'] not in ['table', 'json', 'csv']:
                Console.error("please select printing format among table, json and csv")
                return
            else:
                p_format = self.arguments['--format']
        else:
            p_format = None

        if p_format == 'table' or p_format is None:
            print(row_table(to_print, order=None, labels=["Default", "Value"]))
        else:
            shell_commands_dict_output(to_print,
                                       print_format=p_format,
                                       header=columns,
                                       oneitem=True,
                                       vertical_table=True)

    def _default_cloud(self):
        self._start_cm_user()
        defaults_data = self.user_obj.info(self.username)['defaults']
        if self.arguments['VALUE']:
            value = self.arguments['VALUE']
            if (value in defaults_data['activeclouds'] and
                value in defaults_data['registered_clouds']):
                defaults_data['cloud'] = value
                self.user_obj.set_defaults(self.username, defaults_data)
                Console.ok("set '{0}' as default cloud".format(value))
            else:
                Console.warning("To set a default cloud, it must be registered and "
                                "active, to register and activate a CLOUD: cloud on [CLOUD]")
        else:
            if "cloud" in defaults_data:
                print(defaults_data['cloud'])
            else:
                print("default cloud not set")

    def _default_flavor(self):
        '''
        same as command: cloud set flavor [CLOUD] [--name=NAME|--id=ID]
        '''
        arguments = dict(self.arguments)
        arguments["cloud"] = True
        arguments["set"] = True
        shell_command_cloud(arguments)

    def _default_image(self):
        '''
        same as command: cloud set image [CLOUD] [--name=NAME|--id=ID]
        '''
        arguments = dict(self.arguments)
        arguments["cloud"] = True
        arguments["set"] = True
        shell_command_cloud(arguments)

    def execute(self):
        if self.arguments['format']:
            self._default_format()
        elif self.arguments['cloud']:
            self._default_cloud()
        elif self.arguments['flavor']:
            self._default_flavor()
        elif self.arguments['image']:
            self._default_image()
        else:
            self._print_default()

from cloudmesh_common.logger import LOGGER
from cmd3.console import Console
from cloudmesh.user.cm_user import cm_user
from pprint import pprint
from cloudmesh.config.cm_config import cm_config
from cloudmesh.util.shellutil import shell_commands_dict_output

log = LOGGER(__file__)


def shell_command_default(arguments):
    """
    ::

    Usage:
        default [--column=COLUMN] [--format=FORMAT]
        default cloud [VALUE]
        default format [VALUE]

    Arguments:

    Options:

    Description:


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
                Console.error("There is a problem with cm_user object initialization")
                return
            self.started_cm_user = True

    def __init__(self, arguments):
        self.arguments = arguments
        #print self.arguments #############

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
                print "default print format: ", defaults_data['shell_print_format']
            else:
                defaults_data['shell_print_format'] = "table"
                self.user_obj.set_defaults(self.username, defaults_data)
                defaults_data = self.user_obj.info(self.username)
                print "default print format: ", defaults_data['shell_print_format']
    
    
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
        
        shell_commands_dict_output(to_print,
                                   print_format=p_format,
                                   header=columns,
                                   oneitem=True)
    
    def _default_cloud(self):
        self._start_cm_user()
        defaults_data = self.user_obj.info(self.username)['defaults']
        if self.arguments['VALUE']:
            if self.arguments['VALUE'] in defaults_data['activeclouds'] and\
                self.arguments['VALUE'] in defaults_data['registered_clouds']:
                defaults_data['cloud'] = self.arguments['VALUE']
                self.user_obj.set_defaults(self.username, defaults_data)
                Console.ok("set '{0}' as default cloud".format(self.arguments['VALUE']))
            else:
                Console.warning("To set a default cloud, it must be registered and " + 
                                "active, to register and activate a CLOUD: cloud on [CLOUD]")
        else:
            if "cloud" in defaults_data:
                print "default cloud: ", defaults_data['cloud']
            else:
                print "default cloud not set"
    
    def execute(self):
        if self.arguments['format'] == True:
            self._default_format()
        elif self.arguments['cloud'] == True:
            self._default_cloud()
        else:
            self._print_default()
        

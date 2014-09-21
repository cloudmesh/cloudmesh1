from cloudmesh_common.logger import LOGGER
from cmd3.console import Console
from cloudmesh.user.cm_user import cm_user
from pprint import pprint
from cloudmesh.config.cm_config import cm_config


log = LOGGER(__file__)


def shell_command_defaults(arguments):
    """
    ::

    Usage:
        defaults format [--json|--table]

    Arguments:

    Options:

    Description:

        defaults format [--json|--table]
            some commands can output in json form or table form, this command
            sets the default printing form, if no form is given, it shows the
            current default form


    """
    call = DefaultsCommand(arguments)
    call.execute()


class DefaultsCommand(object):
    try:
        config = cm_config()
    except:
        Console.error("There is a problem with the configuration yaml files")

    username = config['cloudmesh']['profile']['username']

    def __init__(self, arguments):
        self.arguments = arguments
        #print self.arguments #############

    def _defaults_format(self):
        user_obj = cm_user()
        userdata = user_obj.info(self.username)
        if self.arguments['--json']:
            userdata['defaults']['shell_print_format'] = "json"
            user_obj.set_defaults(self.username, userdata['defaults'])
        elif self.arguments['--table']:
            userdata['defaults']['shell_print_format'] = "table"
            user_obj.set_defaults(self.username, userdata['defaults'])
        else:
            format = None
            try:
                format = userdata['defaults']['shell_print_format']
            except:
                pass
            if format not in [None, 'none']:
                print "default print format: ", userdata['defaults']['shell_print_format']
            else:
                userdata['defaults']['shell_print_format'] = "table"
                user_obj.set_defaults(self.username, userdata['defaults'])
                userdata = user_obj.info(self.username)
                print "default print format: ", userdata['defaults']['shell_print_format']

    def execute(self):
        if self.arguments['format'] == True:
            self._defaults_format()

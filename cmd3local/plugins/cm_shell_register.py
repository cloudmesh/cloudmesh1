import types
import textwrap
import inspect
import sys
import importlib
import simplejson as json
import time
import cmd
import docopt
import yaml
import subprocess
from bson.json_util import dumps
from cmd3.shell import command
from cloudmesh.user.cm_user import cm_user
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from pprint import pprint
from prettytable import PrettyTable
from cloudmesh.util.logger import LOGGER
from cm_shell_defaults import cm_shell_defaults

log = LOGGER(__file__)

class cm_shell_register:

    @command
    def do_reg(self, args, arguments):
        '''
        Usage:
          reg NAME

        Arguments:
          NAME      Name of the cloud to be registered
        '''
        config = cm_config()
        cm_user_id = config.username()
        user_obj = cm_user()
        user = user_obj.info(cm_user_id)


        cloudtypes = {}
        for cloud in config.get("cloudmesh.clouds"):
            cloudtypes[cloud] = config['cloudmesh']['clouds'][cloud]['cm_type']


        credentials = user_obj.get_credentials(cm_user_id)
        pprint(credentials)
        return

def main():
    print "test correct"

if __name__ == "__main__":
    main()
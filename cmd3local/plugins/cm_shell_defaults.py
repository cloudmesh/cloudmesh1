import types
import textwrap
import inspect
import sys
import importlib
import simplejson as json
import time
import cmd
from bson.json_util import dumps
from cmd3.shell import command
from cloudmesh.user.cm_user import cm_user
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from pprint import pprint
from prettytable import PrettyTable
from cloudmesh.util.logger import LOGGER
import docopt

log = LOGGER(__file__)

class cm_shell_defaults:

    def createDefaultDict(self, cloudName):
        defaultDict = {}
        config = cm_config()
        pprint(config.cloud(cloudName))


    def activate_cm_shell_defaults(self):
        try:
            config = cm_config()
            self.user = config.username()
            self.mongoClass = cm_mongo()
            self.mongoClass.activate(cm_user_id=self.user)
        except Exception, e:
            print e
            print "Please check if mongo service is running."
            sys.exit()
	@command
    def do_defaults(self, args, arguments):
        """
        Usage:
               defaults [-v] clean
               defaults [-v] load CLOUD
               defaults [options] info
               defaults list [options] CLOUD

        Manages the defaults

        Arguments:

          NAME           The name of a service or server
          N              The number of defaultss to be started
          CLOUD          The name of Cloud

        Options:

           -v             verbose mode
           -j --json      json output

        """
        if arguments["clean"]:
            log.info ("clean the vm")
            print arguments['-v']
            return

        if arguments["load"] and arguments["CLOUD"]:
            createDefaultDict(arguments["CLOUD"])
            return

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

config = cm_config()

class cm_shell_defaults:


    def openstackDefs(self):
        defDict = {}
        cloudName = 'sierra_openstack_grizzly'
        defDict['cloud'] = cloudName
        cloudDict = config.cloud(cloudName)
        defDict['flavor'] = cloudDict['default']['flavor']
        defDict['image'] = cloudDict['default']['image']
        keys = config.userkeys()
        defKeyName = keys['default']
        defKey = keys['keylist'][defKeyName]
        defDict['keyname'] = defKeyName
        defDict['prefix'] = defKeyName
        return defDict

    def hpDefs(self):
        return {}
    def azureDefs(self):
        return {}
    def awsDefs(self):
        return {}


    def createDefaultDict(self, cmType):
        #image
        #flavor
        #keyname
        #nodename
        #number of nodes

        if( cmType == 'openstack'):
            defDict = self.openstackDefs()
        if( cmType == 'hp'):
            defDict = self.hpDefs()
        if( cmType == 'azure'):
            defDict = self.azureDefs()
        if( cmType == 'aws'):
            defDict = self.awsDefs()
        if( cmType == 'ec2'):
            defDict == self.awsDefs()

        return defDict
        '''

        defDict['cloud'] = cloudName
        #pprint(config.cloud(cloudName))
        cloudDict = config.cloud(cloudName)
        defDict['flavor'] = cloudDict['default']['flavor']
        defDict['image']  = cloudDict['default']['image']
        keys = config.userkeys()
        defKeyName = keys['default']
        defKey = keys['keylist'][defKeyName]
        defDict['keyname'] = defKeyName
        defDict['prefix'] = defKeyName
        return defDict
        '''

    def activate_cm_shell_defaults(self):
        try:
            print "shell_Def"
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
               defaults [-v] load [CLOUD]
               defaults [options] info
               defaults list [options] [CLOUD]

        Manages the defaults

        Arguments:

          NAME           The name of a service or server
          N              The number of defaultss to be started
          CLOUD          The name of Cloud

        Options:

           -v             verbose mode
           -j --json      json output

        """

        print arguments

        if arguments["clean"]:
            log.info ("clean the vm")
            print arguments['-v']
            return

        if arguments["load"]:
            self.createDefaultDict(arguments["CLOUD"])
            return

def main():
    def1 = cm_shell_defaults()
    def1.createDefaultDict(None)

if __name__ == "__main__":
    main()


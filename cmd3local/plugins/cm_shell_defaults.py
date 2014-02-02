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
mongoClass = cm_mongo()

class cm_shell_defaults:

    def openstackDefs(self, dbDict):
        defDict = {}
        cloudName = config.default_cloud
        defDict['cloud'] = cloudName
        cloudDict = config.cloud(cloudName)

        #check the flavor
        if 'flavors' in dbDict:
            if cloudName in dbDict['flavors'] and dbDict['flavors'][cloudName]:
                defDict['flavors'] = dbDict['flavors'][cloudName]
            else:
                print 'saving default flavor to Mongo.'
                defDict['flavor'] = cloudDict['default']['flavor']
                flavors = dbDict['flavors']
                flavors[cloudName] = cloudDict['default']['flavor']
                mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'flavors': flavors}},upsert=False, multi=False)
        else:
            print 'Creating and saving default flavor to Mongo.'
            flavors = {}
            flavors[cloudName] = cloudDict['default']['flavor']
            mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'flavors': flavors}},upsert=False, multi=False)

        #check the image
        if 'images' in dbDict:
            if cloudName in dbDict and dbDict['images'][cloudName]:
                defDict['image'] = dbDict['images'][cloudName]
            else:
                print 'saving default image to Mongo.'
                defDict['image'] = cloudDict['default']['image']
                images = dbDict['images']
                images[cloudName] = cloudDict['default']['image']
                mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'images': images}},upsert=False, multi=False)
        else:
            print 'Creating and saving default image to Mongo.'
            images = {}
            images[cloudName] = cloudDict['default']['image']
            mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'images': images}},upsert=False, multi=False)

        if dbDict['key']:
            defDict['keyname'] = dbDict['key']
        else:
            defDict['keyname'] = config.userkeys()['default']
            mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'key': defDict['keyname']}},upsert=False, multi=False)

        if dbDict['prefix']:
            defDict['prefix'] = dbDict['prefix']
        else:
            defDict['prefix'] = config.username()
            mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'prefix': defDict['prefix']}},upsert=False, multi=False)

        if dbDict['index']:
            defDict['index'] = dbDict['index']
        else:
            defDict['index'] = 1
            mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'index': 1}},upsert=False, multi=False)
        return defDict

    # gvl: this is the wrong approach

    def hpDefs(self):
        return {}
    def azureDefs(self):
        return {}
    def awsDefs(self):
        return {}


    def createDefaultDict(self):
        #image
        #flavor
        #keyname
        #nodename
        #number of nodes

        dbDict = mongoClass.db_defaults.find_one({'cm_user_id': config.username()})

        defCloud = config.default_cloud
        cmType = config.cloud(defCloud)['cm_type']

        if( cmType == 'openstack' ):
            defDict = self.openstackDefs(dbDict)
        if( cmType == 'hp' ):
            defDict = self.hpDefs(dbDict)
        if( cmType == 'azure' ):
            defDict = self.azureDefs(dbDict)
        if( cmType == 'aws' ):
            defDict = self.awsDefs(dbDict)
        if( cmType == 'ec2' ):
            defDict == self.awsDefs(dbDict)
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
    '''
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
    def1.createDefaultDict('openstack')

if __name__ == "__main__":
    main()


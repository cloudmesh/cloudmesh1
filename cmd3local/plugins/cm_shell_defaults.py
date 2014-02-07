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

    dictionary = None
    dbDict = None

    def openstackDefs(self):
        defDict = {}
        cloudName = config.default_cloud
        defDict['cloud'] = cloudName
        cloudDict = config.cloud(cloudName)

        #check the flavor
        if 'flavors' in self.dbDict:
            if cloudName in self.dbDict['flavors'] and self.dbDict['flavors'][cloudName]:
                defDict['flavors'] = self.dbDict['flavors'][cloudName]
            else:
                print 'saving default flavor to Mongo.'
                defDict['flavor'] = cloudDict['default']['flavor']
                flavors = self.dbDict['flavors']
                flavors[cloudName] = cloudDict['default']['flavor']
                mongoClass.db_defaults.update({'_id': self.dbDict['_id']}, {'$set':{'flavors': flavors}},upsert=False, multi=False)
        else:
            print 'Creating and saving default flavor to Mongo.'
            flavors = {}
            flavors[cloudName] = cloudDict['default']['flavor']
            mongoClass.db_defaults.update({'_id': self.dbDict['_id']}, {'$set':{'flavors': flavors}},upsert=False, multi=False)

        #check the image
        if 'images' in self.dbDict:
            if cloudName in self.dbDict['images'] and self.dbDict['images'][cloudName]:
                defDict['image'] = self.dbDict['images'][cloudName]
            else:
                print 'saving default image to Mongo.'
                defDict['image'] = cloudDict['default']['image']
                images = self.dbDict['images']
                images[cloudName] = cloudDict['default']['image']
                mongoClass.db_defaults.update({'_id': self.dbDict['_id']}, {'$set':{'images': images}},upsert=False, multi=False)
        else:
            print 'Creating and saving default image to Mongo.'
            images = {}
            images[cloudName] = cloudDict['default']['image']
            mongoClass.db_defaults.update({'_id': self.dbDict['_id']}, {'$set':{'images': images}},upsert=False, multi=False)

        if self.dbDict['key']:
            defDict['keyname'] = self.dbDict['key']
        else:
            defDict['keyname'] = config.userkeys()['default']
            mongoClass.db_defaults.update({'_id': self.dbDict['_id']}, {'$set':{'key': defDict['keyname']}},upsert=False, multi=False)

        if self.dbDict['prefix']:
            defDict['prefix'] = self.dbDict['prefix']
        else:
            defDict['prefix'] = config.username()
            mongoClass.db_defaults.update({'_id': self.dbDict['_id']}, {'$set':{'prefix': defDict['prefix']}},upsert=False, multi=False)

        if self.dbDict['index']:
            defDict['index'] = self.dbDict['index']
        else:
            defDict['index'] = 1
            mongoClass.db_defaults.update({'_id': self.dbDict['_id']}, {'$set':{'index': 1}},upsert=False, multi=False)
        self.dictionary = defDict
        return defDict

    # gvl: this is the wrong approach

    def hpDefs(self):
        return {}
    def azureDefs(self):
        return {}
    def awsDefs(self):
        return {}


    def createDefaultDict(self, cloudName=None):
        #image
        #flavor
        #keyname
        #nodename
        #number of nodes

        self.dbDict = mongoClass.db_defaults.find_one({'cm_user_id': config.username()})
        if cloudName == None:
            defCloud = config.default_cloud
            cmType = config.cloud(defCloud)['cm_type']
        else:
            cmType = config.cloud(cloudName)['cm_type']

        if( cmType == 'openstack' ):
            defDict = self.openstackDefs()
        if( cmType == 'hp' ):
            defDict = self.hpDefs()
        if( cmType == 'azure' ):
            defDict = self.azureDefs()
        if( cmType == 'aws' ):
            defDict = self.awsDefs()
        if( cmType == 'ec2' ):
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
               defaults set [--prefix=<prefix> | --index=<index>]
               defaults list [--verbose | --json] [--cloud=<cloud>]

        Manages the defaults

        Options:

           -v --verbose                   Verbose mode
           -j --json                      Json output
           -p <prefix> --prefix=<prefix>  Prefix to be set for batch VM creation
           -i <index> --index=<index>     Index to be set for batch VM creation
           -c <cloud> --cloud=<cloud>     Name of the cloud

        """

        if arguments["list"]:
            if arguments["--cloud"]:
                pprint(self.createDefaultDict(arguments["--cloud"]))
            else:
                defCloud = config.default_cloud
                pprint(self.createDefaultDict(config.default_cloud))
            return

        if arguments["set"]:
            try:
                if arguments['--index']:
                    if arguments['--index'] > 0:
                        indexToSet = arguments['--index']
                    else:
                        print 'Invalid index specified.'
                        return
                    self.mongoClass.db_defaults.update({'_id': self.dbDict['_id']}, {'$set':{'index': indexToSet}},upsert=False, multi=False)
                    return
                if arguments['--prefix']:
                    self.mongoClass.db_defaults.update({'_id': self.dbDict['_id']}, {'$set':{'index': indexToSet}},upsert=False, multi=False)
                    return
            except:
                print "Unexpected error: ", sys.exc_info()[0]

def main():
    def1 = cm_shell_defaults()
    def1.createDefaultDict()

if __name__ == "__main__":
    main()


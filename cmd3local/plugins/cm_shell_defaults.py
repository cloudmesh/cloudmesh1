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

    defDict = {}

    def openstackDefs(self, dbDict):
        cloudName = config.default_cloud
        self.defDict['cloud'] = cloudName
        cloudDict = config.cloud(cloudName)

        #check the flavor
        if 'flavors' in dbDict:
            if cloudName in dbDict['flavors'] and dbDict['flavors'][cloudName]:
                self.defDict['flavors'] = dbDict['flavors'][cloudName]
            else:
                print 'saving default flavor to Mongo.'
                self.defDict['flavor'] = cloudDict['default']['flavor']
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
            if cloudName in dbDict['images'] and dbDict['images'][cloudName]:
                self.defDict['image'] = dbDict['images'][cloudName]
            else:
                print 'saving default image to Mongo.'
                self.defDict['image'] = cloudDict['default']['image']
                images = dbDict['images']
                images[cloudName] = cloudDict['default']['image']
                mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'images': images}},upsert=False, multi=False)
        else:
            print 'Creating and saving default image to Mongo.'
            images = {}
            images[cloudName] = cloudDict['default']['image']
            mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'images': images}},upsert=False, multi=False)

        if dbDict['key']:
            self.defDict['keyname'] = dbDict['key']
        else:
            self.defDict['keyname'] = config.userkeys()['default']
            mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'key': self.defDict['keyname']}},upsert=False, multi=False)

        if dbDict['prefix']:
            self.defDict['prefix'] = dbDict['prefix']
        else:
            self.defDict['prefix'] = config.username()
            mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'prefix': self.defDict['prefix']}},upsert=False, multi=False)

        if dbDict['index']:
            self.defDict['index'] = dbDict['index']
        else:
            self.defDict['index'] = 1
            mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'index': 1}},upsert=False, multi=False)
        return self.defDict

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
            self.defDict = self.openstackDefs(dbDict)
        if( cmType == 'hp' ):
            self.defDict = self.hpDefs(dbDict)
        if( cmType == 'azure' ):
            self.defDict = self.azureDefs(dbDict)
        if( cmType == 'aws' ):
            self.defDict = self.awsDefs(dbDict)
        if( cmType == 'ec2' ):
            self.defDict == self.awsDefs(dbDict)
        return self.defDict

    @command
    def do_defaults(self, args, arguments):
        """
        Usage:
               defaults clean
               defaults load [CLOUD]
               defaults list [--json] [CLOUD]

        This manages the defaults associated with the user.
        You can load, list and clean defaults associated with a user and a cloud.
        The default parameters include index, prefix, flavor and image.

        Arguments:

          CLOUD          The name of Cloud

        Options:

           -j --json      json output

        """

        if arguments["clean"]:
            self.defDict = {}
            return

        if arguments["load"]:
            self.createDefaultDict()
            return

        if arguments["list"]:
            if arguments["--json"]:
                print json.dumps(self.defDict)
                return
            pprint(self.defDict)
            return

def main():
    print "test correct"
if __name__ == "__main__":
    main()

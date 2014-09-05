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
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.tables import two_column_table
import docopt


log = LOGGER(__file__)

# BUGS:

# TODO: the try methods at the beginning should be called on teh first
# call of this method to load the data. otherwise they should not be
# called, e.g. dynamic loading

# TODO: the defaults should be read at the beginning and when any
# command is used that needs them. a logic needs to be defined so that
# defaults are included in other methods after their first loading. a
# boolean should help prevent constant reloading.

# TODO: when printing flavors or images numbers are given instead of
# user readable labels. in case of images the uuid is given


try:
    config = cm_config()
except:
    log.error("There is a problem with the configuration yaml files")
    
try:
    mongoClass = cm_mongo()
except:
    log.error("There is a problem with the mongo server")


class cm_shell_defaults:

    defDict = {}

    default_loaded = False
    
    def activate_cm_shell_defaults(self):
        self.register_command_topic('cloud','defaults')
        self.default_loaded = False
        pass
    
    def _default_update(self, dbDict, attribute, value):
        mongoClass.db_defaults.update(
            {'_id': dbDict['_id']},
            {'$set': {attribute: value}},
            upsert=False, multi=False)

    def createDefaultDict(self):
        # image
        # flavor
        # keyname
        # nodename
        # number of nodes


        dbDict = mongoClass.db_defaults.find_one(
            {'cm_user_id': config.username()})

        defCloud = config.default_cloud
        cmType = config.cloud(defCloud)['cm_type']

        cloudName = config.default_cloud
        self.defDict['cloud'] = cloudName
        cloudDict = config.cloud(cloudName)

        # check the flavor
        if 'flavors' in dbDict:
            if cloudName in dbDict['flavors'] and dbDict['flavors'][cloudName]:
                self.defDict['flavors'] = dbDict['flavors'][cloudName]
            else:
                print 'saving default flavor to Mongo.'
                self.defDict['flavor'] = cloudDict['default']['flavor']
                flavors = dbDict['flavors']
                flavors[cloudName] = cloudDict['default']['flavor']
                self._default_update(dbDict, 'flavors', flavors)
        else:
            print 'Reading and saving default flavor to Mongo.'
            flavors = {}
            flavors[cloudName] = cloudDict['default']['flavor']
            self._default_update(dbDict, 'flavors', flavors)

        # check the image
        if 'images' in dbDict:
            if cloudName in dbDict['images'] and dbDict['images'][cloudName]:
                self.defDict['image'] = dbDict['images'][cloudName]
            else:
                print 'saving default image to Mongo.'
                self.defDict['image'] = cloudDict['default']['image']
                images = dbDict['images']
                images[cloudName] = cloudDict['default']['image']
                self._default_update(dbDict, 'images', images)
        else:
            print 'Reading and saving default image to Mongo.'
            images = {}
            images[cloudName] = cloudDict['default']['image']
            self._default_update(dbDict, 'images', images)

        if dbDict['key']:
            self.defDict['keyname'] = dbDict['key']
        else:
            self.defDict['keyname'] = config.userkeys()['default']
            self._default_update(dbDict, 'key', self.defDict['keyname'])

        if dbDict['prefix']:
            self.defDict['prefix'] = dbDict['prefix']
        else:
            self.defDict['prefix'] = config.username()
            self._default_update(dbDict, 'prefix', self.defDict['prefix'])

        if dbDict['index']:
            self.defDict['index'] = dbDict['index']
        else:
            self.defDict['index'] = 1
            self._default_update(dbDict, 'index', 1)            

        if dbDict['activeclouds']:
            self.defDict['activeclouds'] = dbDict['activeclouds']
        else:
            self.defDict['activeclouds'] = config.active()
            self._default_update(dbDict, 'activeclouds',
                                 self.defDict['activeclouds'])

        return self.defDict

    @command
    def do_defaults(self, args, arguments):
        """
        Usage:
               defaults clean
               defaults load
               defaults [list] [--json]
               defaults set variable value NOTIMPLEMENTED
               defaults variable  NOTIMPLEMENTED
               defaults format (json|table)  NOTIMPLEMENTED

        Cloudmesh allows to use a number of defaults to more easily
        use the cloudmesh shell. defaults are managed by user and each
        user can set its own defaults.  You can load, list and clean
        defaults. Default parameters allow to store a prefix that is
        prepended whne a vm is started, the default images and flavors
        for each cloud.

        Arguments:

          CLOUD          The name of Cloud - this has to be implemented

        Options:

           -j --json      json output

        Description:

          defaults set a hallo

             sets the variable a to the value hallo
             NOT YET IMPLEMENTED

          defaults a

             returns the value of the variable
             NOT YET IMPLEMENTED

          default format json
          default format table

             sets the default format how returns are printed.
             if set to json json is returned,
             if set to table a pretty table is printed
             NOT YET IMPLEMENTED
        """
        if arguments["clean"]:
            self.defDict = {}
            return

        if arguments["load"]:
            if not self.default_loaded:
                self.createDefaultDict()
                self.default_loaded = True
            return

        if (arguments["list"] or (args == '') or (args == '--json')):
            self.do_defaults("load")
            if arguments["--json"]:
                print json.dumps(self.defDict, indent=4)
                return
            else:
                print two_column_table(self.defDict)
                return
    
            return


def main():
    print "test correct"
    defaults = cm_shell_defaults()
    defaults.createDefaultDict()
    pprint(defaults.defDict)
if __name__ == "__main__":
    main()

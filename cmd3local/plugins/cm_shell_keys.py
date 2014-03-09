import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
import json
from pprint import pprint

from cmd3.shell import command
from cloudmesh.cm_mongo import cm_mongo

from cloudmesh.config.cm_keys import cm_keys
from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_keys:

    """opt_example class"""

    def activate_shell_keys(self):
        filename = "$HOME/.futuregrid/cloudmesh.yaml"
        self.keys = cm_keys(filename)
        self.mongo = cm_mongo()
        if self.echo:
            log.info("Reading keys information from -> {0}".format(filename))
        pass

    @command
    def do_keys(self, args, arguments):
        """
        Usage:
               keys info [--json] [NAME]
               keys default NAME
               keys show NAME

        Manages the keys

        Arguments:

          NAME           The name of a key


        Options:

           -v --verbose     verbose mode
           -j --json        json output

        """

        if arguments["default"] and arguments["NAME"]:
            if arguments["NAME"] in self.keys.names():
                self.keys.setdefault(arguments["NAME"])
                #Update mongo db defaults with new default key
                dbDict = self.mongoClass.db_defaults.find_one({'cm_user_id': self.user})
                self.mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'key': arguments["NAME"]}},upsert=False, multi=False)
                print 'The default key is set to: ', arguments['NAME']
            else:
                print "Specified key is not registered."
            return

        if arguments["show"] and arguments["NAME"]:
            try:
                name = arguments["NAME"]
                key = self.keys[name]
                print
                print "Key Information"
                print "-------------------"
                print
                print "%15s:" % name, key
            except:
                print "Could not find the key with the name", arguments["NAME"]
            print
            return

        if arguments["info"] and arguments["NAME"] is None:
            # log.info ("keys info for all")
            if arguments["--json"]:
                pprint(self.keys["keys"])
                return
            else:
                print
                print "Key Information"
                print "-------------------"

                print
                if self.keys["default"] is not None:
                    # print "%15s:" % "name", self.keys.default()
                    print "%15s:" % "default", self.keys.get_default_key()
                    for name in self.keys.names():
                        print "%15s:" % name, self.keys.fingerprint(name)
                    print
                else:
                    print "%10s:" % "default", "default is not set, please set it"


                print

                return






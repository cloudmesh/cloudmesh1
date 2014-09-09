import json
from cmd3.shell import command
from cloudmesh.config.cm_keys import cm_keys_yaml, cm_keys_mongo
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.tables import two_column_table
from cloudmesh_install.util import yn_choice
from cloudmesh.util.menu import menu_return_num
from os import listdir
from os.path import expanduser
from cloudmesh_install import config_file

log = LOGGER(__file__)


class cm_shell_key:

    """opt_example class."""

    def activate_shell_key(self):

        self.mongo_loaded = False
        self.keys_loaded = False
        self.keys_loaded_mongo = False
        self.use_yaml = True
        self.register_command_topic('cloud', 'keys')
        pass

    def _load_mongo(self):
        if not self.mongo_loaded:
            try:
                self.mongoClass = cm_mongo()
                self.mongo_loaded = True
            except:
                print("ERROR: could not access Mongodb. " \
                      "Have you started the mongo server?")

    def _load_keys(self):
        try:
            filename = config_file("/cloudmesh.yaml")
            if self.echo:
                log.info("Reading keys information from -> {0}"
                         .format(filename))
            self.keys = cm_keys_yaml(filename)
            self.keys_loaded = True
        except:
            print "ERROR: could not find the keys in %s" % filename

    def _load_keys_mongo(self):
        # try:
        from cloudmesh.config.cm_config import cm_config
        config = cm_config()
        self.user = config.get('cloudmesh.profile.username')

        if self.echo:
            log.info("Reading keys information from -> mongo")
        self.keys_mongo = cm_keys_mongo(self.user)
        self.keys_loaded_mongo = True
        # except:
        #   print "ERROR: could not find the keys in %s" % filename

    @command
    def do_key(self, args, arguments):
        """
        Usage:
               key list [--json] [NAME][--yaml][--mongo]
               key info [--json] [NAME][--yaml][--mongo]
               key mode MODENAME
               key default NAME [--yaml][--mongo]
               key add NAME [KEY] [--yaml][--mongo]
               key delete NAME [--yaml][--mongo]
               key save
               keys

        Manages the keys

        Arguments:

          NAME           The name of a key
          MODENAME       This is used to specify the mode name. Mode
                                  name can be either 'yaml' or 'mongo'
                  KEY            This is the actual key that has to added

        Options:

           -v --verbose     verbose mode
           -j --json        json output
           -y --yaml        forcefully use yaml mode
           -m --mongo       forcefully use mongo mode


        Description:

        key list
        key info

             Prints list of keys. NAME of the key can be specified

        key mode MODENAME

             Used to change default mode. Valid MODENAMES are
             yaml(default) and mongo mode.

        key default NAME

             Used to set a key from the key-list as the default key

        key add NAME [KEY]

             adding/updating keys. KEY is the key file with full file
             path, if KEY is not provided, you can select a key among
             the files with extension .pub under ~/.ssh. If NAME exists,
             current key value will be overwritten

        key delete NAME

             deletes a key. In yaml mode it can delete only key that
             are not saved in mongo

        key save

             Saves the temporary yaml data structure to mongo
        """
        if arguments["mode"]:
            if arguments["MODENAME"] == "yaml":
                self.use_yaml = True
                print "SUCCESS: Set mode to yaml"
                return
            elif arguments["MODENAME"] == "mongo":
                self.use_yaml = False
                print "SUCCESS: Set mode to mongo"
                return
            else:
                print "ERROR: Wrong MODENAME. only valid modes are 'mongo' and 'yaml'"
                return

        if arguments["--yaml"] and arguments["--mongo"]:
            print "ERROR: you can specify only one mode"
            return
        elif arguments["--yaml"]:
            self.use_yaml = True
        elif arguments["--mongo"]:
            self.use_yaml = False

        if self.use_yaml:
            # print "Mode: yaml"
            if not self.keys_loaded:
                self._load_keys()
            key_container = self.keys
        else:
            # print "Mode: mongo"
            if not self.mongo_loaded:
                self._load_mongo()
            if not self.keys_loaded_mongo:
                self._load_keys_mongo()
            key_container = self.keys_mongo

        if arguments["default"] and arguments["NAME"]:
            if arguments["NAME"] in key_container.names():
                key_container.setdefault(arguments["NAME"])
                # Update mongo db defaults with new default key
                print 'The default key is set to: ', arguments['NAME']
            else:
                print "ERROR: Specified key is not registered."
            return

        if arguments["add"] and arguments["NAME"]:
            def func():
                if arguments["KEY"]:
                    key_container.__setitem__(
                        arguments["NAME"], arguments["KEY"])
                else:
                    files = [file for file in listdir(
                        expanduser("~/.ssh")) if file.lower().endswith(".pub")]
                    result = menu_return_num(
                        title="Select a public key", menu_list=files, tries=3)
                    if result == 'q':
                        return
                    else:
                        key_container.__setitem__(
                            arguments["NAME"], "~/.ssh/{0}".format(files[result]))
                        
            if arguments["NAME"] in key_container.names():
                if yn_choice("key {0} exists, update?".format(arguments["NAME"]), default='n'):
                    print "Updating key {0} ...".format(arguments["NAME"])
                    func()
                else:
                    return
            else:
                print "adding key {0} ...".format(arguments["NAME"])
                func()

        if arguments["delete"]:
            print "Attempting to delete key. {0}".format(arguments["NAME"])
            if self.use_yaml:

                print("WARNING: This will only remove the keys that"
                      "have not been written to the databse already when 'keys save' is"
                      "called. If your key is already in the database, you should use mongo"
                      "mode\n")
                
            key_container.delete(arguments["NAME"])
            return
        if arguments["save"]:
            if not self.mongo_loaded:
                self._load_mongo()
            if not self.keys_loaded_mongo:
                self._load_keys_mongo()
            key_mongo = self.keys_mongo
            key_yaml = self.keys
            names = key_yaml.names()
            for name in names:
                key_mongo.__setitem__(
                    name, key_yaml._getvalue(name), key_type="string")
            key_mongo.setdefault(key_yaml.get_default_key())
            return

        if arguments["info"] or arguments["list"] or (args == ""):
            if arguments["--json"]:
                if arguments["NAME"] is None:
                    name = "keys"
                else:
                    name = arguments["NAME"]
                try:
                    print json.dumps(key_container[name], indent=4)
                except:
                    print("ERROR: Something went wrong in looking up keys. "
                          "Did you give the correct key name?")
                return
            else:
                mykeys = {}
                header = ["Default", "Fingerprint"]
                try:
                    mykeys["default"] = key_container.get_default_key()
                except:
                    mykeys["default"] = "default is not set, please set it"
                for name in key_container.names():
                    mykeys[name] = key_container.fingerprint(name)
                print two_column_table(mykeys)
                return


if __name__ == '__main__':
    arguments = {}
    arguments['mode'] = True
    arguments['MODENAME'] = "yaml"

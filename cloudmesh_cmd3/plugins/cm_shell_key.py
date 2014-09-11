from cloudmesh.config.cm_config import cm_config
# cm_config_server, get_mongo_db
import yaml
import json
from cmd3.shell import command
from cloudmesh.config.cm_keys import cm_keys_yaml, cm_keys_mongo
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.tables import two_column_table
# from cloudmesh_install.util import yn_choice
# from cloudmesh.util.menu import menu_return_num
from os import listdir
from os.path import expanduser
from cloudmesh_install import config_file
from cloudmesh_install.util import path_expand
# from cloudmesh.util.keys import read_key
from cloudmesh.util.keys import get_fingerprint

log = LOGGER(__file__)


class cm_shell_key:

    """opt_example class."""

    def activate_shell_key(self):
        self.mongo_loaded = False
        self.keys_loaded = False
        self.keys_loaded_mongo = False
        self.use_yaml = True
        self.register_command_topic('cloud', 'keys')

    def _load_mongo(self):
        if not self.mongo_loaded:
            try:
                self.mongoClass = cm_mongo()
                self.mongo_loaded = True
            except:
                print("ERROR: could not access Mongodb. "
                      "Have you started the mongo server?")

    def _load_keys_from_yaml(self):
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
               key
               key list [--source=SOURCE] [--dir=DIR] [--format=FORMAT]
               key add [KEYNAME] FILENAME
               key default KEYNAME
               key delete KEYNAME

        Manages the keys

        Arguments:

          SOURCE         mongo, yaml, ssh
          KEYNAME        The name of a key
          FORMAT         The format of the output
          FILENAME       The filename in which the key is located

        Options:

           -v --verbose     verbose mode
           --dir=DIR        the directory with keys [default: ~/.ssh]
           --format=FORMAT  the format of the output [default: table]
           --source=SOURCE  the source for the keys [default: mongo]

        Description:


        key list --source=ssh  [--dir=DIR] [--format=FORMAT]

           lists all keys in the directory. If the directory is not
           specified the defualt will be ~/.ssh

        key list --source=yaml  [--dir=DIR] [--format=FORMAT]

           lists all keys in cloudmesh.yaml file in the specified directory.
            dir is by default ~/.cloudmesh

        key list [--format=FORMAT]

            list the keys in mongo

        key add [KEYNAME] FILENAME

            adds the key specifid by the filename to either
            the yaml file or the mongodb

        key add [--dir=DIR]
        key add select [--dir=DIR]

             interactively selct a key from the specified dir to be added

        key list

             Prints list of keys. NAME of the key can be specified

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

        """
        print arguments

        def _find_keys(directory):
            return [file for file in listdir(expanduser(directory))
                    if file.lower().endswith(".pub")]

        #
        # DIR (OK)
        #

        directory = path_expand(arguments["--dir"])
        source = arguments["--source"]

        if source not in ["ssh", "yaml", "mongo"]:
            print "ERROR: source is not defined"
            return

        #
        # PRINT DICT (OK)
        #

        def _print_dict(d, header=None):
            print_format = arguments['--format']
            if print_format == "json":
                return json.dumps(d, indent=4)
            elif print_format == "yaml":
                return yaml.dump(d, default_flow_style=False)
            else:
                return two_column_table(keys, header)

        #
        # PRINT SYSTEM (OK)
        #

        if arguments["list"] and source == "ssh":

            files = _find_keys(directory)

            keys = {}
            for key in files:
                keys[key] = directory + "/" + key
            print _print_dict(keys, header=["Key", "Location"])

            return

        #
        # PRINT YAML (OK)
        #

        if arguments["list"] and source == "yaml":

            key_store = cm_keys_yaml()
            keynames = key_store.names()
            keys = {}
            for key in keynames:
                keys[key] = get_fingerprint(key_store[key])

            print _print_dict(keys, header=["Key", "Fingerprint"])

            return

        #
        # FROM HERE ON BROKEN
        #

        if arguments["list"] and source == "mongo":

            username = cm_config().username()
            key_store = cm_keys_mongo(username)
            keynames = key_store.names()

            keys = {}
            for key in keynames:

                keys[key] = key_store[key]
                # get_fingerprint(key_store[key])

            print _print_dict(keys, header=["Key", "Fingerprint"])

            return

        # self._load_keys_from_yaml()
        # self._load_mongo()
        # self._load_keys_mongo()

        if arguments["add"] and arguments["KEYNAME"]:

            keyname = arguments["KEYNAME"]
            filename = arguments["FILENAME"]

            # check if file exists

            # check if key is valid

            key_store[keyname] = filename

            """
            def func():
                if arguments["KEY"]:
                    key_store.__setitem__(
                        arguments["NAME"], arguments["KEY"])
                else:
                    files = _find_keys(directory)

                    result = menu_return_num(
                        title="Select a public key", menu_list=files, tries=3)
                    if result == 'q':
                        return
                    else:
                        key_store.__setitem__(arguments["NAME"],
                                                  "{0}/{1}".format(directory,files[result]))

            if arguments["NAME"] in key_store.names():
                if yn_choice("key {0} exists, update?"
                             .format(arguments["NAME"]), default='n'):
                    print "Updating key {0} ...".format(arguments["NAME"])
                    func()
                else:
                    return
            else:
                print "adding key {0} ...".format(arguments["NAME"])
                func()
            """

        if arguments["default"] and arguments["NAME"]:
            if arguments["NAME"] in key_store.names():
                key_store.setdefault(arguments["NAME"])
                # Update mongo db defaults with new default key
                print 'The default key is set to: ', arguments['NAME']
            else:
                print "ERROR: Specified key is not registered."
            return

        if arguments["delete"]:
            print "Attempting to delete key. {0}".format(arguments["NAME"])
            if self.use_yaml:

                print("WARNING: This will only remove the keys that"
                      "have not been written to the databse already when "
                      "'keys save' is"
                      "called. If your key is already in the database, "
                      "you should use mongo mode\n")

            key_store.delete(arguments["NAME"])
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
                    print json.dumps(key_store[name], indent=4)
                except:
                    print("ERROR: Something went wrong in looking up keys. "
                          "Did you give the correct key name?")
                return
            else:
                mykeys = {}
                # header = ["Default", "Fingerprint"]
                try:
                    mykeys["default"] = key_store.get_default_key()
                except:
                    mykeys["default"] = "default is not set, please set it"
                for name in key_store.names():
                    mykeys[name] = get_fingerprint(key_store[name])
                print two_column_table(mykeys)
                return


if __name__ == '__main__':
    arguments = {}
    arguments['mode'] = True
    arguments['MODENAME'] = "yaml"

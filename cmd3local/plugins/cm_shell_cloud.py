from cloudmesh_common.logger import LOGGER
import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cloudmesh.cm_mongo import cm_mongo
from cmd3.shell import command
from cloudmesh_common.tables import column_table
from pprint import pprint
import yaml
import json

log = LOGGER(__file__)


class cm_shell_cloud:

    """opt_example class"""

    def activate_cm_shell_cloud(self):
        self.mongo_loaded = False
        self.register_command_topic('cloud','cloud')
        pass

    def _load_mongo(self):
        if not self.mongo_loaded:
            try:
                self.mongoClass = cm_mongo()
                self.mongo_loaded = True
            except:
                print "ERROR: could not access Mongodb. " \
                      "Have you started the mongo server?"


    def _print_dict(self, d, format):
        if format in ["table"]:
            print column_table(d)
        elif format in ["list"]:
            print d["Clouds"]
        elif format in ["dict"]:
            print yaml.safe_dump(d, indent=4,default_flow_style=False)
        elif format in ["json"]:
            print json.dumps(d, indent=4)

                     
    @command
    def do_cloud(self, args, arguments):
        """
        Usage:
            cloud list [--format=FORMAT]
            cloud info [NAME]
            cloud set NAME
            cloud select
            cloud on NAME
            cloud off NAME
            cloud add [--json | --yaml] CLOUD

        Manages the clouds

        Arguments:

          NAME           The name of a service or server
          CLOUD          The cloud to be added

        Options:

           -v       verbose mode
           --json   The format of the activation description:jsos
           --yaml   The format of the activation description:yaml
           --format=FORMAT   the format of the input or output.
                             Accepted values are table, list, json, dict. [default: table]
                          
        Description:

            cloud list
                Lists the cloud names

            cloud info [NAME]
                Provides the available information about the clouds
                and their status. A cloud can be activated or deactivated.
                If no name is specified the default cloud is used.
                If the name all is used, all clouds are displayed

            cloud setname NAME
                set the cloud with the NAME to the default cloud

            cloud select
                selects a cloud from the name of clouds

            cloud on [NAME]
            cloud off [NAME]
                activates or deactivates a cloud with a given name, if name
                is not specified, default or selected cloud will be activates
                or deactivates

            cloud add [--json | --yaml] CLOUD
                adds a cloud to the list of clouds.
                The format can either be `json` or `yaml`, default is yaml

        """

        log.info(arguments)
        print "<", args, ">"

        if arguments["list"]:
            #list the cloud names
            #
            # Bug, this does not list all possible clouds, but just the clouds register in the passwd database
            # it should probably come form cm_mongo().clouds() We skip this for now
            #
            if arguments["--format"] not in ["json","table", "dict", "list"]:
                print "ERROR: format {0} not supported".format(arguments["--format"])
            else:
            
                if not self.mongo_loaded:
                    self._load_mongo()
                result = self.mongoClass.userdb_passwd.find().sort("cloud")
                cloudnames = {"Clouds":[]}
                for result_object in result:
                    cloudnames["Clouds"].append(result_object["cloud"])

                self._print_dict(cloudnames, arguments["--format"])
            return


        if arguments["select"]:
            #select a cloud from a list
            pass
            
        if arguments["info"]:
            if argument["NAME"]:
                if argument["NAME"] == "all":
                    print "---------------------->"
                    #display all clouds
                else:
                    print "---------------------->"
                    #provide information about cloud "NAME"
            else:
                #display default cloud
                pass
            return


        if arguments["set"] and argument["NAME"]:

            #set the cloud with the name to the default
            return

        if arguments["on"] and arguments["NAME"]:
            #activate cloud NAME
            log.info("activatethe cloud")
            return

        if arguments["off"] and arguments["NAME"]:
            #deactivate cloud NAME
            log.info("activatethe cloud")
            return

        if arguments["add"] and arguments["CLOUD"]:
            if arguments["--jason"]:
                # adds a cloud to the list of clouds in jason format
                pass
            elif arguments["--yaml"]:
                # adds a cloud to the list of clouds in yaml format
                pass
            else:
                # adds a cloud to the list of clouds in yaml format
                pass
            return
 


if __name__ == '__main__':
	pass

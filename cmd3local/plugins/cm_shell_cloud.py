from cloudmesh_common.logger import LOGGER
import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
#from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.cm_cloudsinfo import cm_cloudsinfo
from cmd3.shell import command
from cloudmesh_common.tables import column_table
from cloudmesh_common.bootstrap_util import yn_choice
from pprint import pprint
import yaml
import json

log = LOGGER(__file__)


class cm_shell_cloud:

    """opt_example class"""

    # For now, a default cloud is just a randomly picked cloud in the db
    # [default: india_openstack_havana], once you restart cm, previous
    # selection will be erased
    def activate_cm_shell_cloud(self):
        self.register_command_topic('cloud', 'cloud')
        pass
    
    def __init__(self):
        self._db_loaded = False
        self._requery = True
        self._cloud_selected = False
        self.selected_cloud = None
        self.clouds = None
        

    def _load_mongodb(self):
        if not self._db_loaded:
            try:
                self.cloudsinfo = cm_cloudsinfo()
                self._db_loaded = True
            except:
                print "ERROR: Could not load mongo, did you start the db?"
                      
    def _requery_db(self):
        if self._requery:
            self.clouds = self.cloudsinfo.get_clouds()
            self._requery = False
        else:
            return
        
    def _check_empty(self):
        if self.clouds.count() == 0:
            return True
        else:
            return False

    def _print_dict(self, d, format):
        if format in ["table"]:
            print column_table(d)
        elif format in ["json"]:
            print json.dumps(d, indent=4)
        elif format in ["list"]:
            print d["Clouds"]
        elif format in ["yaml"]:
            print yaml.safe_dump(d, indent=4, default_flow_style=False)
        elif format in ["dict"]:
            print d

    def _get_default_cloud(self):
        if not self._loaded:
            self._load()
        if not self._default_setted:
            self.cloudsinfo._load()
            if self.cloudsinfo.cloud_names == []:
                # print "ERROR: There is no cloud in the database, can't set
                # default cloud!"
                return ""
            else:
                if "india_openstack_havana" in self.cloudsinfo.cloud_names:
                    self.default_cloud = "india_openstack_havana"
                    self._default_setted = True
                    return self.default_cloud
                else:
                    self.default_cloud = self.cloudsinfo.cloud_names[0]
                    self._default_setted = True
                    return self.default_cloud
        else:
            return self.default_cloud

    def _num(self, num):
        try:
            return int(num)
        except:
            return num

    def _sub_select(self, clouds, i, j=0):
        var = raw_input("Please select a cloud (input index or name, type 'q' to discard): ")
        varnum = self._num(var)
        if var == 'q' or j >= 3:
            return
        elif isinstance(varnum, int) and varnum in range(1, i):
            self.default_cloud = clouds[varnum - 1]
            self._default_setted = True
            print "cloud '{0}' is selected.".format(clouds[varnum - 1])
        elif var in clouds:
            self.default_cloud = var
            self._default_setted = True
            print "cloud '{0}' is selected.".format(var)
        else:
            print "Invalid input, try again..."
            self._sub_select(clouds, i, j=j + 1)


    @command
    def do_cloud(self, args, arguments):
        """
        Usage:
            cloud list [--column=COLUMN]
            cloud info [NAME] [--format=FORMAT]
            cloud set NAME
            cloud select [NAME]
            cloud on [NAME]
            cloud off [NAME]
            cloud add CLOUD
            cloud remove [NAME]

        Manages the clouds

        Arguments:

          NAME           the name of a service or server
          CLOUD          a yaml file contains cloud information
          
        Options:

           -v       verbose model
           --format=FORMAT   the format of the output. Accepted values
                             are table, list, json, yaml, dict.
                             [default: table]
           --column=COLUMN   specify what information to display. For
                             example, --column=active, label. Available
                             columns are active, label, host, type/version,
                             type, heading, user, credentials, defaults

        Description:

            cloud list [--column=COLUMN]
                lists the cloud names, optionally, specify columns for more
                cloud information

            cloud info [NAME] [--format=FORMAT]
                provides the available information about cloud and its status.
                If no NAME is given, default or selected cloud is used. If the 
                name all is used, all clouds are displayed

            cloud set NAME
                sets a new name for selected or default cloud

            cloud select [NAME]
                selects a cloud from a list of clouds if NAME not given

            cloud on [NAME]
            cloud off [NAME]
                activates or deactivates a cloud, if name is not given, 
                default or selected cloud will be activated or deactivated

            cloud add CLOUD
                adds cloud information to database. CLOUD is a yaml file with 
                full file path. Inside yaml, clouds should be contained in 
                "cloudmesh: clouds: ..."

            cloud remove [NAME]
                remove a cloud from mongo, if name is not given, default or 
                selected cloud will be reomved.
                CAUTION: remove all is enabled

        """

        log.info(arguments)
        print "<", args, ">"

        if arguments["list"]:
            self._load_mongodb()
            self._requery_db()
            if self._check_empty():
                print "Can't preceed, no cloud in database"
                return
            else:
                if arguments["--column"]:
                    col_option = [x.strip() for x in arguments["--column"].split(',')]
                    if set(col_option).issubset(set(['active', 'label', 'host', 'type/version',\
                             'type', 'heading', 'user', 'credentials', 'defaults'])):
                        col = {'cm_cloud':[]}
                        for co in col_option:
                            col[co] = []
                    else:
                        print "ERROR: one or more column type doesn't exist"
                else:
                    col = {'cm_cloud':[]}
                for cloud in self.clouds:
                    for key in col.keys():
                        if cloud[key]:
                            try:
                                val = cloud[key].encode("ascii")
                            except:
                                val = cloud[key]
                            col[key].append(val)
                        else:
                            col[key].append(" ")
                print column_table(col)
                    
            

'''
        if arguments["list"]:
            if arguments["--format"] not in ["json", "table", "dict", "list", "yaml"]:
                print "ERROR: format {0} not supported.".format(arguments["--format"])
            else:
                if not self._loaded:
                    self._load()
                names = self.cloudsinfo._list()
                names.sort()
                cloudnames = {"Clouds": names}
                self._print_dict(cloudnames, arguments["--format"])
            return

        if arguments["select"]:
            # select a cloud from a list
            if not self._loaded:
                self._load()
            self.cloudsinfo._load()
            clouds = self.cloudsinfo.cloud_names
            if clouds == []:
                print "There is no cloud in database."
            else:
                if arguments["NAME"]:
                    if arguments["NAME"] in clouds:
                        self.default_cloud = arguments["NAME"]
                        self._default_setted = True
                        print "cloud '{0}' is selected.".format(arguments["NAME"])
                    else:
                        print "'{0}' is not in the database.".format(arguments["NAME"])
                else:
                    current_selected = self._get_default_cloud()
                    table = {"index": ["current selected", " "], "Clouds": [current_selected, " "]}
                    i = 1
                    clouds.sort()
                    for cloud in clouds:
                        table["index"].append(i)
                        table["Clouds"].append(cloud)
                        i = i + 1
                    print column_table(table)
                    self._sub_select(clouds, i)

        if arguments["info"]:
            if not self._loaded:
                self._load()
            self.cloudsinfo._load()
            clouds = self.cloudsinfo.cloud_names
            if clouds == []:
                print "There is no cloud in database."
            else:
                if arguments["NAME"]:
                    if arguments["NAME"] == "all":
                        clouds = self.cloudsinfo.get_cloud_info_all().sort([('cm_cloud', 1)])
                        for cloud in clouds:
                            print "   {0} {1} {2}\n{3}\n".format("*" * 8, cloud['cm_cloud'].encode('ascii'), "*" * 8, "-" * 80)
                            pprint(cloud)
                            print "\n{0}\n\n".format("-" * 80)
                    elif arguments["NAME"] in clouds:
                        cloud = self.cloudsinfo.get_cloud_info(arguments["NAME"])
                        print "   {0} {1} {2}\n{3}\n".format("*" * 8, cloud['cm_cloud'].encode('ascii'), "*" * 8, "-" * 80)
                        pprint(cloud)
                        print "\n{0}\n\n".format("-" * 80)
                    else:
                        print "ERROR: Could not find '{0}' in database.".format(arguments["NAME"])
                else:
                    current_selected = self._get_default_cloud()
                    cloud = self.cloudsinfo.get_cloud_info(current_selected)
                    print "   {0} {1} {2}\n{3}\n".format("*" * 8, cloud['cm_cloud'].encode('ascii'), "*" * 8, "-" * 80)
                    pprint(cloud)
                    print "\n{0}\n\n".format("-" * 80)

        if arguments["set"] and arguments["NAME"]:
            if not self._loaded:
                self._load()
            self.cloudsinfo._load()
            clouds = self.cloudsinfo.cloud_names
            if clouds == []:
                print "There is no cloud in database."
            else:
                current_selected = self._get_default_cloud()
                question = "Change the name of cloud '{0}' into '{1}'?: ".format(current_selected, arguments["NAME"])
                if yn_choice(question, default='n', tries = 3):
                    self.cloudsinfo.set_name(current_selected, arguments["NAME"])
                    self.default_cloud = arguments["NAME"]
                    print "Name of cloud '{0}' is changed to '{1}'.".format(current_selected, arguments["NAME"])
                else:
                    return

        if arguments["on"]:
            if not self._loaded:
                self._load()
            self.cloudsinfo._load()
            clouds = self.cloudsinfo.cloud_names
            if clouds == []:
                print "There is no cloud in database."
            else:
                if arguments["NAME"]:
                    if arguments["NAME"] in clouds:
                        self.cloudsinfo.activate(arguments["NAME"])
                        print "cloud '{0}' activated.".format(arguments["NAME"])
                    else:
                        print "ERROR: Could not find '{0}' in database.".format(arguments["NAME"])
                else:
                    current_selected = self._get_default_cloud()
                    self.cloudsinfo.activate(current_selected)
                    print "cloud '{0}' activated.".format(current_selected)

        if arguments["off"]:
            if not self._loaded:
                self._load()
            self.cloudsinfo._load()
            clouds = self.cloudsinfo.cloud_names
            if clouds == []:
                print "There is no cloud in database."
            else:
                if arguments["NAME"]:
                    if arguments["NAME"] in clouds:
                        self.cloudsinfo.deactivate(arguments["NAME"])
                        print "cloud '{0}' deactivated.".format(arguments["NAME"])
                    else:
                        print "ERROR: Could not find '{0}' in database.".format(arguments["NAME"])
                else:
                    current_selected = self._get_default_cloud()
                    self.cloudsinfo.deactivate(current_selected)
                    print "cloud '{0}' deactivated.".format(current_selected)

        if arguments["add"] and arguments["CLOUD"]:
            if not self._loaded:
                self._load()
            self.cloudsinfo.add_from_yaml(arguments["CLOUD"])

        if arguments["remove"]:
            if not self._loaded:
                self._load()
            self.cloudsinfo._load()
            clouds = self.cloudsinfo.cloud_names
            if clouds == []:
                print "There is no cloud in database."
            else:
                if arguments["NAME"]:
                    if arguments["NAME"] in clouds:
                        question = "Remove cloud '{0}' from database?: ".format(arguments["NAME"])
                        if yn_choice(question, default='n', tries = 3):
                            self.cloudsinfo.remove(arguments["NAME"])
                            if self.default_cloud == arguments["NAME"]:
                                self._default_setted = False
                        else:
                            return
                    elif arguments["NAME"] == "all":
                        question = "!!!CAUTION!!! Remove all clouds from database?: "
                        if yn_choice(question, default='n', tries = 3):
                            for cloud in clouds:
                                self.cloudsinfo.remove(cloud)
                            self._default_setted = False
                        else:
                            return
                    else:
                        print "ERROR: Could not find '{0}' in database.".format(arguments["NAME"])
                else:
                    current_selected = self._get_default_cloud()
                    question = "Remove cloud '{0}' from database?: ".format(current_selected)
                    if yn_choice(question, default='n', tries = 3):
                        self.cloudsinfo.remove(current_selected)
                        self._default_setted = False
                    else:
                        return
'''

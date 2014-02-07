import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
import cloudmesh
from pprint import pprint
from cloudmesh.util.logger import LOGGER
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from prettytable import PrettyTable


log = LOGGER(__file__)

class cm_shell_list:

    """opt_example class"""

    def activate_cm_shell_list(self):
        pass

    @command
    def do_list(self, args, arguments):
        """
        Usage:
               list flavors [CLOUD...]
               list servers [CLOUD...]
               list images [CLOUD...]
               list [CLOUD...]

        Arguments:

                CLOUD    the name of the cloud

        Options:

           -v       verbose mode

        """
        mesh = cloudmesh.mesh()
        mongo = cm_mongo()
        config = cm_config()
        user = config.username()
        dbDict = self.mongoClass.db_defaults.find_one({'cm_user_id': user})
        #log.info(args)
        #pprint(arguments)
        #log.info(arguments)
        all = False
        if len(arguments["CLOUD"]) == 0:
            print "get all active clouds"
            all = True
            if 'activeclouds' in dbDict and dbDict['activeclouds']:
                clouds = dbDict['activeclouds']
            else:
                clouds = [config.default_cloud]
        else:
            clouds = arguments['CLOUD']

        if arguments["flavors"]:
            #log.info ("list images")

            x = PrettyTable()
            x.field_names = ["Id", "Name"]
            x.align["Name"] = "l"
            x.align["Id"] = "l"

            for cloud in clouds:
                mesh.refresh(names=[cloud], types=['flavor'])
                print "\nCloud: ", cloud
                if cloud in mesh.clouds and mesh.clouds[cloud]:
                    flavors = mesh.clouds[cloud]['flavor']
                    for key, value in flavors.iteritems():
                        x.add_row([value['id'], key])
                    print x.get_string(sortby="Id")
                    print "\n\n"
            return

        if arguments["servers"]:
#            log.info ("count servers")

            x = PrettyTable()
            x.field_names = ["Id", "Name", "Status"]
            x.align["Name"] = "l"
            x.align["Id"] = "l"
            x.align["Status"] = "l"
            try:
                for cloud in clouds:
                    mesh.refresh(names=[cloud], types=['server'])
                    if cloud in mesh.clouds and mesh.clouds[cloud]:
                        servers = mesh.clouds[cloud]['server']
                        for key, value in servers.iteritems():
                            x.add_row([key, value['name'], value['status']])
                        print x.get_string(sortby="Id")
                        print "\n\n"
                    else:
                        print "No results on servers for", cloud
            except:
                print "Unexpected error: ", sys.exc_info()[0]

        if arguments["images"]:
            #log.info ("list images")

            x = PrettyTable()
            x.field_names = ["Id", "Name"]
            x.align["Name"] = "l"
            x.align["Id"] = "l"

            try:
                for cloud in clouds:
                    mesh.refresh(names=[cloud], types=['image'])
                    print "\nCloud: ", cloud
                    if cloud in mesh.clouds and mesh.clouds[cloud]:
                        images = mesh.clouds[cloud]['image']
                        for key, value in images.iteritems():
                            x.add_row([value['id'], value['name']])
                        print x.get_string(sortby="Name")
                        print "\n\n"
                return
            except:
                print "Unexpected error: ", sys.exc_info()[0]

    @command
    def do_count(self, args, arguments):
        """
        Usage:
               count flavors [CLOUD...]
               count servers [CLOUD...]
               count images [CLOUD...]
               count [CLOUD...]

        Arguments:

                CLOUD    the name of the cloud

        Options:

           -v       verbose mode

        """
        log.info(args)

        log.info(arguments)

        if len(arguments["CLOUD"]) == 0:
            print "get all active clouds"
            all = True
            clouds = ['a', 'b']
        else:
            clouds = arguments['CLOUD']
        print clouds

        if arguments["flavors"] or all:
            log.info ("count flavors")
            for cloud in clouds:
                print "cloud: flavors", cloud, None

        if arguments["servers"] or all:
            log.info ("count servers")
            for cloud in clouds:
                print "cloud: servers", cloud, None

        if arguments["images"] or all:
            log.info ("list images")
            for cloud in clouds:
                print "cloud: images", cloud, None


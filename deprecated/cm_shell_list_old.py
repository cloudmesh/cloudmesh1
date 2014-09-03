import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
import cloudmesh
from pprint import pprint

from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from prettytable import PrettyTable

from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)


class cm_shell_list:

    """opt_example class"""

    def activate_cm_shell_list(self):
        self.register_command_topic('cloud','list')
        pass

    def _printList(self, parameter, fieldList, clouds):
        mesh = cloudmesh.mesh()

        x = PrettyTable()
        x.field_names = fieldList
        for field in fieldList:
            x.align[field] = "c"  # center aligned

        try:
            for cloud in clouds:
                mesh.refresh(names=[cloud], types=[parameter])
                if cloud in mesh.clouds and mesh.clouds[cloud]:
                    params = mesh.clouds[cloud][parameter]
                    if len(params) > 0:
                        print "\nCloud: ", cloud, "\n"
                        for key, value in params.iteritems():
                            # since value is a dictionary of multiple items,
                            # we add to table only fields from the fieldList
                            rowList = []
                            for field in fieldList:
                                rowList.append(value[field])
                            x.add_row(rowList)
                        print x.get_string(sortby=fieldList[0])
                        print "\n\n"
            return
        except:
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

    @command
    def do_list(self, args, arguments):
        """
        Usage:
               list flavors [CLOUD]
               list servers [CLOUD]
               list images [CLOUD]
               list

         Arguments:

                CLOUD    the name of the cloud

        Options:

           -v       verbose mode

        Description:

           missing

           This should be similar to the count command,
           e.g. multiple clouds could be specified.

        """
        mesh = cloudmesh.mesh()
        mongo = cm_mongo()
        config = cm_config()
        user = config.username()
        self.mongoClass = mongo
        dbDict = self.mongoClass.db_defaults.find_one({'cm_user_id': user})
        # log.info(args)
        # pprint(arguments)
        # log.info(arguments)
        print '\n\n'
        all = False
        if not arguments["CLOUD"]:
            all = True
            if 'activeclouds' in dbDict and dbDict['activeclouds']:
                clouds = dbDict['activeclouds']
            else:
                clouds = [config.default_cloud]
        else:
            clouds = [arguments["CLOUD"]]

        if arguments["flavors"]:

            fieldList = ['id', 'name']
            self._printList('flavors', fieldList, clouds)

        elif arguments["servers"]:

            fieldList = ["id", "name", "status"]
            self._printList('server', fieldList, clouds)

        elif arguments["images"]:

            fieldList = ["id", "name"]
            self._printList('image', fieldList, clouds)
        else:
            print 70*"-"
            print 'List of Clouds:'
            for cloud in clouds:
                print cloud
            print '\n'
            return

    @command
    def do_count(self, args, arguments):
        """
        Usage:
               count flavors [CLOUD...] NOTIMPLEMENTED
               count servers [CLOUD...] NOTIMPLEMENTED
               count images [CLOUD...] NOTIMPLEMENTED
               count [CLOUD...] NOTIMPLEMENTED

        Arguments:

                CLOUD    the name of the cloud

        Options:

           -v       verbose mode

        Description:

          missing

          Seems this has not been implemented.

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
            log.info("count flavors")
            for cloud in clouds:
                print "cloud: flavors", cloud, None

        if arguments["servers"] or all:
            log.info("count servers")
            for cloud in clouds:
                print "cloud: servers", cloud, None

        if arguments["images"] or all:
            log.info("list images")
            for cloud in clouds:
                print "cloud: images", cloud, None


def main():
    print "test correct"
    clouds = ['sierra']
    fieldList = ["id", "name", "status"]

    ls = cm_shell_list()
    ls._printList('image', fieldList, clouds)

if __name__ == "__main__":
    main()

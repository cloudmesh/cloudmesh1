import types
import textwrap
import inspect
import sys
import importlib
import simplejson as json
from bson import Binary, Code
from bson.json_util import dumps
from cmd3.shell import command
from cloudmesh.user.cm_user import cm_user
from cloudmesh.cm_mongo import cm_mongo
from pprint import pprint
from prettytable import PrettyTable
from cloudmesh.util.logger import LOGGER
from docopt import docopt

log = LOGGER(__file__)

class cm_shell_vm:

    """opt_example class"""

    def activate_cm_shell_vm(self):
        pass

    @command
    def do_vm(self, args, arguments):
        """
        Usage:
               vm clean
               vm delete NAME
               vm create [NAME]
               vm info [NAME]
               vm cloud NAME
               vm image NAME
               vm flavour NAME
               vm index NAME
               vm count N
               vm list

        Manages the vm

        Arguments:

          NAME           The name of a service or server
          N              The number of VMs to be started


        Options:

           -v       verbose mode

        """
        log.info(arguments)
        #opt = docopt(__doc__, sys.argv[1:])

        if arguments["clean"]:
            log.info ("clean the vm")
            return

        if arguments["delete"] and arguments["NAME"]:
            log.info ("delete the vm")
            return

        if arguments["info"] and arguments["NAME"]:
            log.info ("vm info")
            c = cm_mongo()
            user_obj = cm_user()
            """
            TODO -- get user info //'g' alternative
            """
            user = user_obj.info('psjoshi')
            user_id = user['cm_user_id']

            clouds = c.servers(cm_user_id=user_id)
            vmFound = False

            for key, value in clouds.items():
                for k, v in value.items():
                    if(v['name'] == arguments['NAME']):
                        reqdVM = v
                        vmFound = True
                        break
                if(vmFound == True):
                    break

            pprint(reqdVM)

            jsonReqd = False #ToDo -- assign the value from option "-json"

            if(jsonReqd):
                jsonObj = dumps(reqdVM)
                return jsonObj
            return


        if arguments["create"] and arguments["NAME"]:
            log.info ("vm info")
            return

        """
        Currently presents list of following parameters for the VM
            -- name
            -- status
            -- flavor
            -- id
            -- user_id
        We can add parameters by taking them as args from user.
        """
        if arguments["list"]:
            c = cm_mongo()
            #c.activate(cm_user_id="psjoshi")
            clouds = c.servers(cm_user_id="psjoshi")
            vmList = clouds["sierra_openstack_grizzly"]


            userParamList = [] #ToDo -- assign the parameters from user to display
            jsonList = []
            x = PrettyTable()
            jsonReqd = True    #ToDo -- assign the value from option "-json"

            parameterList = ["name", "status", "flavor", "id", "user_id"]

            for parameter in userParamList:
                parameterList.append(parameter)

            x.field_names = (parameterList)
            for key, vm in vmList.items():

                tableRowList = []

                for parameter in parameterList:
                    tableRowList.append(vm[parameter])

                x.add_row(tableRowList)
                if(jsonReqd):
                    insDict = {}
                    insDict[vm['name']]  = tableRowList
                    jsonList.append(insDict)
            print x
            if(jsonReqd):
                jsonArray = json.dumps(jsonList)
                print jsonArray


import types
import textwrap
import inspect
import sys
import importlib
import simplejson as json
import time
import cmd
import docopt
import yaml
import subprocess
import re
from bson.json_util import dumps
from cmd3.shell import command
from cloudmesh.user.cm_user import cm_user
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from pprint import pprint
from prettytable import PrettyTable
from cloudmesh.util.logger import LOGGER
from cm_shell_defaults import cm_shell_defaults
from Interface.vmInterface import vmInterface

log = LOGGER(__file__)

class cm_shell_vm:
    """opt_example class"""

    def chkActivation(self, userId):
        ret = False
        userinfo = cm_user().info(userId)
        if "activeclouds" in userinfo["defaults"] and\
            len(userinfo["defaults"]["activeclouds"]) > 0:
            ret = True
        return ret

    def activate_cm_shell_vm(self):
        try:
            self.config = cm_config()
            self.user = self.config.username()
            self.mongoClass = cm_mongo()
            print "activating!!"
            self.mongoClass.activate(cm_user_id=self.user)
            self.vmi = vmInterface(self.user, self.config.default_cloud, self.mongoClass)
            defaults = cm_shell_defaults()
            self.defDict = defaults.createDefaultDict()
            if self.chkActivation(self.user) is False:
                print "No Active clouds set! Please register and activate a cloud."

        except Exception:
            print 'Unexpected error at cmd VM: ', sys.exc_info()[0], sys.exc_info()[1]
            sys.exit()

    def findVM(self, user, server):
        try:
            clouds = self.mongoClass.servers(cm_user_id=user)
            for key, value in clouds.items():
                for k, v in value.items():
                    if(v['name'] == server):
                        return v
            print "VM not found."
            return None
        except:
            print "Unexpected error: ", sys.exc_info()[0]

    def deleteVM(self, serverName):
        print "deleting ", serverName
        server = self.findVM(self.user, serverName)
        if(server):
            cloud = server['cm_cloud']
            serverId = server['id']
            try:
                self.mongoClass.vm_delete(cloud, serverId, self.user)
                time.sleep(5)
                self.mongoClass.release_unused_public_ips(cloud, self.user)
                self.mongoClass.refresh(names=[cloud], types=["servers"], cm_user_id=self.user)
                print serverName, "deleted successfully!\n"
                return 0

            except StandardError:
                print "Error deleting the VM."
                return -1

    @command
    def do_vm(self, args, arguments):
        '''
        Usage:
          vm create [--count=<count>] [--image=<imgName>] [--flavor=<FlavorId>] [--cloud=<CloudName>]
          vm delete [[--count=<count>] | [--name=<NAME>]] [--cloud=<CloudName>]
          vm cloud [--name=<NAME>]
          vm image [--name=<NAME>]
          vm flavor [--name=<NAME>]
          vm index [--index=<index>]
          vm info [--verbose | --json] [--name=<NAME>]
          vm list [--verbose | --json] [--cloud=<CloudName>]

        Arguments:
          NAME name of the VM

        Options:
           -v --verbose                         verbose mode
           -j --json                            json output
           -x <count> --count=<count>           number of VMs
           -n <NAME> --name=<NAME>              Name of the VM
           -c <CloudName> --cloud=<CloudName>   Name of the Cloud
           -i <index> --index=<index>           Index for default VM Name
           -img <imgName> --image=<imgName>     Name of the image for VM
           -f <FlavorId> --flavor=<FlavorId>    Flavor Id for VM
        '''
        userParams = {}

        for key, value in arguments.iteritems():
            if re.findall(r'[--]', key):
                #Check if its an option, if yes add it to userParam dict
                arg = re.findall(r'[a-z]+', key)
                userParams[arg[0]] = value

        if arguments["index"]:
            setIndex = arguments["--index"]
            if int(setIndex) < 1:
                print "Please set the index greater than 0."
                return
            dbDict = self.mongoClass.db_defaults.find_one({'cm_user_id': self.user})
            self.mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'index': setIndex}},upsert=False, multi=False)
            print 'Next index value is set to: ', setIndex


        if arguments["cloud"] and arguments["--name"]:
            log.info ("get the VM cloud")
            server = self.vmi.findVM(self.user, arguments["--name"])
            if(server):
                vmCloud = server['cm_cloud']
                print "--------------------------------------------------------------------------------\n"
                print arguments["--name"],"is running on: ", vmCloud
            return

        if arguments["flavor"] and arguments["--name"]:
            self.vmi.getImageOrFlavor('flavor', userParams)
            return

        if arguments["image"] and arguments["--name"]:
            self.vmi.getImageOrFlavor('image', userParams)
            return

        if arguments["info"] and arguments["--name"]:
            log.info ("vm info")
            reqdVM = self.findVM(self.user, arguments["--name"])

            x = PrettyTable()
            x.field_names = ["Property", "Value"]
            x.align["Property"] = "l"
            x.align["Value"] = "l"

            if(reqdVM):
                jsonReqd = arguments['--json']
                cmCloud = reqdVM['cm_cloud']

                if(jsonReqd):
                    jsonObj = dumps(reqdVM, sys.stdout, sort_keys=True, indent=4, separators=(',',':'))
                    print jsonObj
                    return jsonObj
                else:
                    #get the VM image for the info display
                    try:
                        vmImageId = reqdVM['image']['id']
                        self.mongoClass.refresh(self.user, types=["images"])
                        allImages = self.mongoClass.images(clouds = [reqdVM['cm_cloud']], cm_user_id = self.user)

                        imageValue = allImages[cmCloud][vmImageId]['name'] + " ("
                        imageValue = imageValue + allImages[cmCloud][vmImageId]['id'] + ")"

                        x.add_row(['image', imageValue])

                        for key, value in reqdVM.items():
                            if type(value) != dict and type(value) != list:
                                x.add_row([key, value])
                        print x.get_string(sortby="Property")
                    except:
                        print 'Unexpected error: ', sys.exc_info()[0]
            return

        if arguments["create"]:
            self.vmi.launchVM(self.defDict, userParams)

        if arguments["delete"]:
            self.vmi.deleteVM(self.defDict, userParams)
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
            currentCloud = None
            if arguments["--cloud"]:
                currentCloud = arguments["--cloud"]
            else:
                currentCloud = self.defDict['cloud']

            try:
                self.mongoClass.refresh(names=[currentCloud], types=["servers"], cm_user_id=self.user)
                clouds = self.mongoClass.servers(cm_user_id=self.user)
                if clouds is not None:
                    vmList = clouds[currentCloud]
                else:
                    print "No Cloud registered."
                    return
            except Exception:
                print 'Unexpected error getting the list of VMs: ', sys.exc_info()[1]
                return
            try:

                if(len(vmList) == 0):
                    print "No VMs on this cloud."
                    return
                else:
                    userParamList = [] #ToDo -- assign the parameters from user to display
                    jsonList = []
                    x = PrettyTable()
                    jsonReqd = arguments['--json']

                    parameterList = ["id", "name", "status", "addresses"]

                    for parameter in userParamList:
                        parameterList.append(parameter)
                    x.field_names = (parameterList)
                    for key, vm in vmList.items():

                        tableRowList = []

                        for parameter in parameterList:
                            if parameter == "addresses" and 'private' in vm[parameter]:
                                addresses = (vm[parameter]['private'])
                                addrList = []
                                for address in addresses:
                                    addr = address['OS-EXT-IPS:type']+"="+address['addr']
                                tableRowList.append(addr)
                            else:
                                tableRowList.append(vm[parameter])

                        x.add_row(tableRowList) #toDo, send it to 'if !jsonReqd'
                        if(jsonReqd):
                            insDict = {}
                            insDict[vm['name']]  = tableRowList
                            jsonList.append(insDict)
                    if(jsonReqd):
                        jsonArray = json.dumps(jsonList)
                        print jsonArray
                    else:
                        print x.get_string(sortby="name")
            except:
                print "Unexpected error:", sys.exc_info()[0]
def main():
    print "test correct"

if __name__ == "__main__":
    main()



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
from cm_shell_defaults import cm_shell_defaults
from cloudmesh.iaas.tmp_vm_interface import vm_interface

from cloudmesh_common.logger import LOGGER


log = LOGGER(__file__)


class cm_shell_vm:

    """CMD3 plugin to manage virtul machines in a multicloud environment."""

    clouds_activated = False

    def activate_cm_shell_vm(self):
        self.register_command_topic('cloud', 'vm')
        self.clouds_activated = False

    # Check if there are any active clouds for user
    def _check_activation(self, userId):
        ret = False
        userinfo = cm_user().info(userId)
        if "activeclouds" in userinfo["defaults"] and \
                len(userinfo["defaults"]["activeclouds"]) > 0:
            ret = True
        return ret

    def _the_clouds(self):
        try:
            self.config = cm_config()
            self.user = self.config.username()
            self.mongoClass = cm_mongo()

            print "Activating clouds ..."
            try:
                self.mongoClass.activate(cm_user_id=self.user)
                print "Activation done."
                self.clouds_activated = True
            except:
                print "Activation failed"
                self.clouds_activated = False

            self.vmi = vm_interface(
                self.user, self.config.default_cloud, self.mongoClass)
            defaults = cm_shell_defaults()
            self.defDict = defaults.createDefaultDict()
            if self._check_activation(self.user) is False:
                print "No active clouds found. " \
                      "Please register and activate a cloud."

        except Exception:
            print 'Unexpected error at cmd VM: ', \
                  sys.exc_info()[0], sys.exc_info()[1]

    @command
    def do_login(self, args, arguments):
        '''
        Usage:
           login
        '''
        self._the_clouds()

    @command
    def do_vm(self, args, arguments):
        '''
        Usage:
          vm create [--count=<count>]
                    [--image=<imgName>]
                    [--flavor=<FlavorId>]
                    [--cloud=<CloudName>]
          vm delete [[--count=<count>] | [--name=<NAME>]]
                    [--cloud=<CloudName>]
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
           --img=<imgName>                      Name of the image for VM
           -f <FlavorId> --flavor=<FlavorId>    Flavor Id for VM
        '''
        # prepare user parameters from the switch options from user

        if not self.clouds_activated:
            print "ERROR: you have not yet logged into the clouds"
            print
            print "use the command: login"
            print
            return

        userParams = {}

        for key, value in arguments.iteritems():
            if re.findall(r'[--]', key):
                # Check if its an option, if yes add it to userParam dict
                arg = re.findall(r'[a-z]+', key)
                userParams[arg[0]] = value

        # Change default index for vm
        if arguments["index"]:
            setIndex = arguments["--index"]
            if int(setIndex) < 1:
                print "Please set the index greater than 0."
                return
            dbDict = self.mongoClass.db_defaults.find_one(
                {'cm_user_id': self.user})
            self.mongoClass.db_defaults.update(
                {'_id': dbDict['_id']},
                {'$set': {'index': setIndex}},
                upsert=False, multi=False)
            print 'Next index value is set to: ', setIndex

        # get the cloud which hosts the specified VM
        if arguments["cloud"] and arguments["--name"]:
            log.info("get the VM cloud")
            server = self.vmi.findVM(self.user, arguments["--name"])
            if(server):
                vmCloud = server['cm_cloud']
                print 70 * "-"
                print arguments["--name"], "is running on: ", vmCloud
            return

        # Get the flavor of specified VM
        if arguments["flavor"] and arguments["--name"]:
            self.vmi.getImageOrFlavor('flavor', userParams)
            return

        # Get the image of specified VM
        if arguments["image"] and arguments["--name"]:
            self.vmi.getImageOrFlavor('image', userParams)
            return

        # Get the info of specified VM
        if arguments["info"] and arguments["--name"]:
            log.info("vm info")
            reqdVM = self.vmi.findVM(self.user, arguments["--name"])

            x = PrettyTable()
            x.field_names = ["Property", "Value"]
            x.align["Property"] = "l"
            x.align["Value"] = "l"

            if(reqdVM):
                jsonReqd = arguments['--json']
                cmCloud = reqdVM['cm_cloud']

                if(jsonReqd):
                    jsonObj = dumps(reqdVM,
                                    sys.stdout,
                                    sort_keys=True,
                                    indent=4,
                                    separators=(',', ':'))
                    print jsonObj
                    return jsonObj
                else:
                    # get the VM image for the info display
                    try:
                        vmImageId = reqdVM['image']['id']
                        self.mongoClass.refresh(self.user, types=["images"])
                        allImages = self.mongoClass.images(
                            clouds=[reqdVM['cm_cloud']], cm_user_id=self.user)

                        imageValue = allImages[cmCloud][
                            vmImageId]['name'] + " ("
                        imageValue = imageValue + \
                            allImages[cmCloud][vmImageId]['id'] + ")"

                        x.add_row(['image', imageValue])

                        for key, value in reqdVM.items():
                            if type(value) != dict and type(value) != list:
                                x.add_row([key, value])
                        print x.get_string(sortby="Property")
                    except:
                        print 'Unexpected error: ', sys.exc_info()[0]
            return

        # Launch a new VM
        if arguments["create"]:
            self.vmi.launchVM(self.defDict, userParams)

        # Delete a VM on cloud
        if arguments["delete"]:
            self.vmi.deleteVM(self.defDict, userParams)
            return

        # List all running VMs on the cloud
        if arguments["list"]:
            currentCloud = None
            if arguments["--cloud"]:
                currentCloud = arguments["--cloud"]
            else:
                currentCloud = self.defDict['cloud']

            try:
                self.mongoClass.refresh(
                    names=[currentCloud],
                    types=["servers"],
                    cm_user_id=self.user)
                clouds = self.mongoClass.servers(cm_user_id=self.user)
                if clouds is not None:
                    vmList = clouds[currentCloud]
                else:
                    print "No Cloud registered."
                    return
            except Exception:
                print 'Unexpected error getting the list of VMs: ', \
                      sys.exc_info()[1]
                return
            try:

                if(len(vmList) == 0):
                    print "No VMs on this cloud."
                    return
                else:
                    # ToDo -- assign the parameters from user to display
                    userParamList = []
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
                            if (parameter == "addresses") and ('private' in vm[parameter]):
                                addresses = (vm[parameter]['private'])
                                addrList = []
                                for address in addresses:
                                    addr = address['OS-EXT-IPS:type'] + \
                                        "=" + address['addr']
                                tableRowList.append(addr)
                            else:
                                tableRowList.append(vm[parameter])

                        # toDo, send it to 'if !jsonReqd'
                        x.add_row(tableRowList)
                        if(jsonReqd):
                            insDict = {}
                            insDict[vm['name']] = tableRowList
                            jsonList.append(insDict)
                    if(jsonReqd):
                        jsonArray = json.dumps(jsonList)
                        print jsonArray
                    else:
                        print x.get_string(sortby="name")
            except:
                print "Unexpected error:", sys.exc_info()[0]

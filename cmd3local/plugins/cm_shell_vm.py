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
from bson.json_util import dumps
from cmd3.shell import command
from cloudmesh.user.cm_user import cm_user
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from pprint import pprint
from prettytable import PrettyTable
from cloudmesh.util.logger import LOGGER
from cm_shell_defaults import cm_shell_defaults

log = LOGGER(__file__)

class cm_shell_vm:
    """opt_example class"""

    def activate_cm_shell_vm(self):
        try:
            self.config = cm_config()
            self.user = self.config.username()
            self.mongoClass = cm_mongo()
            print "activating!!"
            self.mongoClass.activate(cm_user_id=self.user)
            defaults = cm_shell_defaults()
            self.defDict = defaults.createDefaultDict()
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
          vm index [--name=<NAME>]
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
        if arguments["cloud"] and arguments["--name"]:
            log.info ("get the VM cloud")
            server = self.findVM(self.user, arguments["--name"])
            if(server):
                vmCloud = server['cm_cloud']
                print "--------------------------------------------------------------------------------\n"
                print arguments["--name"],"is running on: ", vmCloud
            return

        if arguments["flavor"] and arguments["--name"]:
            log.info ("get the VM flavor")
            server = self.findVM(self.user, arguments["--name"])
            if(server):
                try:
                    vmFlavorId = server['flavor']['id']
                    flavors = self.mongoClass.flavors(cm_user_id=self.user)
                    if len(flavors[server['cm_cloud']]) == 0:
                        print 'Flavor not available anymore.'
                        return
                    else:
                        reqdFlavor = flavors[server['cm_cloud']][vmFlavorId]
                        jsonObj = dumps(reqdFlavor, sys.stdout, sort_keys=True, indent=4, separators=(',',':'))
                        print "--------------------------------------------------------------------------------\n"
                        print "The Flavor for:", arguments["--name"]
                        print jsonObj, "\n"
                        return jsonObj
                except:
                    print "Unexpected error: ", sys.exc_info()[0]
            return

        if arguments["image"] and arguments["--name"]:
            log.info ("get the VM image")
            server = self.findVM(self.user, arguments["--name"])
            if(server):
                try:
                    vmImageId = server['image']['id']
                    self.mongoClass.refresh(self.user, types=["images"])
                    images = self.mongoClass.images(cm_user_id=self.user)
                    if len(images[server['cm_cloud']]) == 0:
                        print 'Image not available anymore.'
                        return
                    else:
                        reqdImage = images[server['cm_cloud']][vmImageId]
                        jsonObj = dumps(reqdImage, sys.stdout, sort_keys=True, indent=4, separators=(',',':'))
                        print "--------------------------------------------------------------------------------\n"
                        print "The image for:", arguments["--name"]
                        print jsonObj, "\n"
                        return jsonObj
                except:
                    print "Unexpected error: ", sys.exc_info()[0]
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
            cloudName = self.defDict['cloud']
            dbDict = self.mongoClass.db_defaults.find_one({'cm_user_id': self.user})
            dbIndex = int(dbDict['index'])
            defCloud = self.config.default_cloud
            if arguments['--count']:
                numberOfVMs = int(arguments['--count'])
            else:
                numberOfVMs = 1
            imgId = None
            images = None
            if arguments['--image']:
                imgName = arguments['--image']
                self.mongoClass.refresh(self.user, types=["images"])
                images = self.mongoClass.images(cm_user_id=self.user)
                if defCloud in images:
                    cloudImages = images[defCloud]
                    for key, value in cloudImages.iteritems():
                        if value['name'] == imgName:
                            imgId = key
                            break
                else:
                    print "The default cloud does not have images!"
                    imgId = 'NotNull'
                if imgId == None:
                    print "\nImage not found for this cloud. Please choose one of the following!\n"
                    for key, value in images[defCloud].items():
                        print value['name']
                    return

            flavorId = None
            if arguments['--flavor']:
                flavor = arguments['--flavor']
                self.mongoClass.refresh(self.user, types=["flavors"])
                flavors = self.mongoClass.flavors(cm_user_id=self.user)
                if defCloud in flavors:
                    cloudFlavors = flavors[defCloud]
                    if flavor in cloudFlavors:
                        flavorId = flavor
                    else:
                        print "\nFlavor not found for this cloud. Please choose one id from the following!\n"
                        x
                        for key, value in flavors[defCloud].items():
                            print key, value['name']
                        return
                else:
                    print "The default  cloud does not have images!"
                    flavId = "NotNull"
            try:
                for i in range(numberOfVMs):

                    if imgId == None: #implies default image to be used.
                        imgId = self.defDict['image']
                    if flavorId == None: #implies default flavor to be used.
                        flavorId = 1

                    result = self.mongoClass.vm_create(cloudName, self.defDict['prefix'], dbIndex, flavorId, imgId, self.defDict['keyname'], None, self.user)

                    self.mongoClass.refresh(names=[cloudName], types=["servers"], cm_user_id=self.user)

                    if ('server' not in result):
                        badReq = 'badRequest'
                        if(badReq in result):
                            print result[badReq]['message']
                        return
                    #update the index for next VM
                    print 'VM successfully launched!'
                    pprint(result)
                    dbIndex = unicode(int(dbIndex) + 1)
                dbDict = self.mongoClass.db_defaults.find_one({'cm_user_id': self.user})
                dbIndex = int(dbDict['index'])
                dbIndex = unicode(dbIndex + numberOfVMs)
                self.mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'index': dbIndex}},upsert=False, multi=False)
                time.sleep(5)
            except:
                print "Unexpected error:", sys.exc_info()[0]
            return

        if arguments["delete"]:
            try:
                dbDict = self.mongoClass.db_defaults.find_one({'cm_user_id': self.user})
                nextIndex = int(dbDict['index'])
                deletedVMs = 0
                if arguments['--name']:
                    servName = arguments["--name"]
                    retVal = self.deleteVM(servName)
                else:
                    if arguments['--count']:
                        numberOfVMs = int(arguments['--count'])
                        if nextIndex < numberOfVMs:
                            print "Number of VMs specified is greater than running VMs. Deleting all VMs."
                            numberOfVMs = nextIndex - 1
                    else:
                        if nextIndex == 1:
                            print "No default VM to delete. Please specify a name for a VM to be deleted."
                            return
                        numberOfVMs = 1
                    for i in range(numberOfVMs):
                        nextIndex = nextIndex - 1
                        servName = "%s_%s" % (self.defDict['prefix'], nextIndex)
                        retVal = self.deleteVM(servName)
                        if retVal != 0:
                            break
                        deletedVMs = deletedVMs + 1

                #update the index for db defaults
                index = int(dbDict['index'])
                #on deleting vm <prefix>_1 keep the index fixed to 1
                index = unicode(index - deletedVMs)
                self.mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'index': index}},upsert=False, multi=False)
            except:
                print "Unexpected error: ", sys.exc_info()[0]
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



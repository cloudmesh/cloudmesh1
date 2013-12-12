import types
import textwrap
import inspect
import sys
import importlib
import simplejson as json
import time
import cmd
from bson.json_util import dumps
from cmd3.shell import command
from cloudmesh.user.cm_user import cm_user
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from pprint import pprint
from prettytable import PrettyTable
from cloudmesh.util.logger import LOGGER
import docopt
from cm_shell_defaults import cm_shell_defaults

log = LOGGER(__file__)

class cm_shell_vm:
    """opt_example class"""

    def activate_cm_shell_vm(self):
        try:
            config = cm_config()
            self.user = config.username()
            self.mongoClass = cm_mongo()
            self.mongoClass.activate(cm_user_id=self.user)
            defaults = cm_shell_defaults()
            self.defDict = defaults.createDefaultDict()
            self.index = 0
        except Exception, e:
            print e
            print "Please check if mongo service is running."
            sys.exit()

    def findVM(self, user, server):
        clouds = self.mongoClass.servers(cm_user_id=user)
        for key, value in clouds.items():
            for k, v in value.items():
                if(v['name'] == server):
                    return v
        print "VM not found."
        return None

    @command
    def do_vm(self, args, arguments):
        """
        Usage:
               vm clean [options]
               vm delete NAME
               vm create [CLOUD]
               vm info [options] [NAME]
               vm cloud NAME
               vm image NAME
               vm flavor NAME
               vm index NAME
               vm count N
               vm list [options] CLOUD

        Manages the vm

        Arguments:

          NAME           The name of a service or server
          N              The number of VMs to be started
          CLOUD          The name of Cloud

        Options:

           -v             verbose mode
           -j --json      json output

        """
        if arguments["clean"]:
            log.info ("clean the vm")
            print arguments['-v']
            return

        if arguments["cloud"] and arguments["NAME"]:
            log.info ("get the VM cloud")
            try:
                server = self.findVM(self.user, arguments["NAME"])
            except StandardError:
                print "Could not activate mongoDB. Please check if mongo running."
            if(server):
                vmCloud = server['cm_cloud']
                print "--------------------------------------------------------------------------------\n"
                print arguments["NAME"],"is under the cloud:", vmCloud
            return

        if arguments["flavor"] and arguments["NAME"]:
            log.info ("get the VM flavor")
            try:
                server = self.findVM(self.user, arguments["NAME"])
            except StandardError:
                print "Could not activate mongoDB. Please check if mongo running."
            if(server):
                vmFlavorId = server['flavor']['id']
                flavors = self.mongoClass.flavors(cm_user_id=user)
                reqdFlavor = flavors[server['cm_cloud']][vmFlavorId]

                jsonObj = dumps(reqdFlavor, sys.stdout, sort_keys=True, indent=4, separators=(',',':'))
                print "--------------------------------------------------------------------------------\n"
                print "The Flavor for:", arguments["NAME"]
                print jsonObj, "\n"
                return jsonObj
            return

        if arguments["image"] and arguments["NAME"]:
            log.info ("get the VM image")
            try:
                server = self.findVM(self.user, arguments["NAME"])
            except:
                print "Could not activate mongoDB. Please check if mongo running."
                return
            if(server):
                vmImageId = server['image']['id']
                images = self.mongoClass.images(cm_user_id=self.user)

                reqdImage = images[server['cm_cloud']][vmImageId]

                jsonObj = dumps(reqdImage, sys.stdout, sort_keys=True, indent=4, separators=(',',':'))
                print "--------------------------------------------------------------------------------\n"
                print "The image for:", arguments["NAME"]
                print jsonObj, "\n"
                return jsonObj
            return

        if arguments["delete"] and arguments["NAME"]:
            log.info ("delete the vm")
            #ToDo -- get user info //'g' alternative
            #ToDo -- check if activate is necessary
            server = self.findVM(self.user, arguments["NAME"])
            if(server):
                cloud = server['cm_cloud']
                serverId = server['id']
                try:
                    self.mongoClass.vm_delete(cloud, serverId, self.user)
                    time.sleep(5)
                    self.mongoClass.release_unused_public_ips(cloud, self.user)
                    self.mongoClass.refresh(names=[cloud], types=["servers"], cm_user_id=self.user)
                    print arguments["NAME"], "deleted successfully\n"
                except StandardError:
                    print "Error deleting the VM."
            return


        if arguments["info"] and arguments["NAME"]:
            log.info ("vm info")
            """
            TODO -- get user info //'g' alternative
            private network
            flavor
            security_groups
            metadata
            """
            reqdVM = self.findVM(self.user, arguments["NAME"])

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
                    vmImageId = reqdVM['image']['id']
                    allImages = self.mongoClass.images(clouds = [reqdVM['cm_cloud']], cm_user_id = self.user)

                    imageValue = allImages[cmCloud][vmImageId]['name'] + " ("
                    imageValue = imageValue + allImages[cmCloud][vmImageId]['id'] + ")"

                    x.add_row(['image', imageValue])

                    for key, value in reqdVM.items():
                        if type(value) != dict and type(value) != list:
                            x.add_row([key, value])
                    print x.get_string(sortby="Property")
            return


        if arguments["create"]:
            #toDo -- Replace this with actual nova call
            #check if we can retrieve previously created vms and
            #print "nova boot --image {0} --flavor {1} --key-name {2} defDict['image'] }
            #def vm_create(self, cloud, prefix, index, vm_flavor, vm_image, key, meta, cm_user_id):
            #decide about index and prefix

            #log.info ("vm create")

            if(arguments["CLOUD"]):
                cloudName = arguments["CLOUD"]
            else:
                cloudName = self.defDict['cloud']
            result = self.mongoClass.vm_create(cloudName, self.defDict['prefix'], self.index, 1, self.defDict['image'], self.defDict['keyname'], None, 'psjoshi')
            badReq = 'badRequest'
            if(badReq in result):
                print result[badReq]['message']
                return
            pprint(result)
            return
            '''
            log.info ("vm create")

            print "Select the cloud you want to create VM for."
            activeClouds = self.mongoClass.active_clouds(self.user)
            cloudIndex = 0
            for item in activeClouds:
                cloudIndex = cloudIndex + 1
                print str(cloudIndex)+".", item
            cloudIndex = raw_input('')
            #0 based in indexing
            selectedCloud = activeClouds[int(cloudIndex) - 1]

            print "Please enter parameters to create VM as required.\n",
            print "--Select an image from following."
            time.sleep(1)
            try:
                allImages = self.mongoClass.images(clouds = [selectedCloud], cm_user_id = self.user)
                imgCounter = 1
                imageList = allImages[selectedCloud]
                if len(imageList) > 0:
                    x = PrettyTable()
                    x.field_names = ["Index", "ID", "Name"]
                    for key, val in imageList.items():
                        x.add_row([imgCounter, key,val['name']])
                        imgCounter = imgCounter + 1
                    print x
                    imageIndex = raw_input('Enter the index for image to boot VM ')
                    selectedImage = imageList.items()[int(imageIndex)]
                    pprint(selectedImage)
                else:
                    print "No images found for selected cloud"
            except:
                print sys.exc_info()
                sys.exit()
            return'''



        """
        Currently presents list of following parameters for the VM
            -- name
            -- status
            -- flavor
            -- id
            -- user_id
        We can add parameters by taking them as args from user.
        """
        if arguments["list"] and arguments["CLOUD"]:
            clouds = self.mongoClass.servers(cm_user_id=self.user)

            vmList = clouds[arguments["CLOUD"]]

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
                        if parameter == "addresses":
                            addresses = (vm[parameter]['private'])
                            addrList = []
                            for address in addresses:
                                addr = address['OS-EXT-IPS:type']+"="+address['addr']
                            tableRowList.append(addr)
                        else:
                            tableRowList.append(vm[parameter])

                    x.add_row(tableRowList)
                    if(jsonReqd):
                        insDict = {}
                        insDict[vm['name']]  = tableRowList
                        jsonList.append(insDict)
                if(jsonReqd):
                    jsonArray = json.dumps(jsonList)
                    print jsonArray
                else:
                    print x
def main():
    print "test correct"

if __name__ == "__main__":
    main()



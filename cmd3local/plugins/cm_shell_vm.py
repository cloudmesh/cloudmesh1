import types
import textwrap
import inspect
import sys
import importlib
import simplejson as json
import time
import cmd
import errno
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
    user = None

    """opt_example class"""

    def __init__(self):
        cmd.Cmd.__init__(self)
        try:
            self.user = 'psjoshi'
            self.mongoClass = cm_mongo()
            #ToDo -- get user -- 'g' alternative
            self.mongoClass.activate(cm_user_id=self.user)
        except:
            print sys.exc_info()
            sys.exit(errno.ECONNREFUSED)


    def activate_cm_shell_vm(self):
        pass

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
               vm clean
               vm delete NAME
               vm create [NAME]
               vm info [NAME]
               vm cloud NAME
               vm image NAME
               vm flavor NAME
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

        if arguments["cloud"] and arguments["NAME"]:
            log.info ("get the VM cloud")
            user = 'psjoshi'
            try:
                server = self.findVM(user, arguments["NAME"])
            except StandardError:
                print "Could not activate mongoDB. Please check if mongo running."
            if(server):
                vmCloud = server['cm_cloud']
                print "--------------------------------------------------------------------------------\n"
                print arguments["NAME"],"is under the cloud:", vmCloud
            return

        if arguments["flavor"] and arguments["NAME"]:
            log.info ("get the VM flavor")
            user = 'psjoshi'
            try:
                server = self.findVM(user, arguments["NAME"])
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
            user = 'psjoshi'
            try:
                server = self.findVM(user, arguments["NAME"])
            except StandardError:
                print "Could not activate mongoDB. Please check if mongo running."
                return
            if(server):
                vmImageId = server['image']['id']
                images = self.mongoClass.images(cm_user_id=user)

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
            user = 'psjoshi'
            #ToDo -- check if activate is necessary
            server = self.findVM(user, arguments["NAME"])
            if(server):
                cloud = server['cm_cloud']
                serverId = server['id']
                try:
                    self.mongoClass.vm_delete(cloud, serverId, user)
                    time.sleep(5)
                    self.mongoClass.release_unused_public_ips(cloud, user)
                    self.mongoClass.refresh(names=[cloud], types=["servers"], cm_user_id=user)
                    print arguments["NAME"], "deleted successfully\n"
                except StandardError:
                    print "Error deleting the VM."
            return


        if arguments["info"] and arguments["NAME"]:
            log.info ("vm info")
            """
            TODO -- get user info //'g' alternative
            """
            user = 'psjoshi'
            reqdVM = self.findVM(user, arguments["NAME"])

            if(reqdVM):
                jsonReqd = True #ToDo -- assign the value from option "-json"

                if(jsonReqd):
                    jsonObj = dumps(reqdVM, sys.stdout, sort_keys=True, indent=4, separators=(',',':'))
                    print jsonObj
                    return jsonObj
                else:
                    pprint(reqdVM)
                return
            else:
                return

        if arguments["create"]:
            log.info ("vm info")

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
            jsonReqd = False #ToDo -- assign the value from option "-json"

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
                            print address['OS-EXT-IPS:type'], address['addr']
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


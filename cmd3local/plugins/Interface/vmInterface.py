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

from pprint import pprint
from prettytable import PrettyTable

#Get rid of this
from cloudmesh.user.cm_user import cm_user
from cmd3.shell import command
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class vmInterface:

    def __init__(self, user, config, mongo):
        self.user = user
        self.mongoClass = mongo
        self.defCloud = config.default_cloud

    def chkActivation(self, userId):
        ret = False
        userinfo = cm_user().info(userId)
        if "activeclouds" in userinfo["defaults"] and\
            len(userinfo["defaults"]["activeclouds"]) > 0:
            ret = True
        return ret

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


    def chkFlavor(self, userFlavor):
        flavor = userFlavor
        flavorId = None
        self.mongoClass.refresh(self.user, types=["flavors"])
        flavors = self.mongoClass.flavors(cm_user_id=self.user)
        if self.defCloud in flavors:
            cloudFlavors = flavors[self.defCloud]
            if flavor in cloudFlavors:
                flavorId = flavor
                return True
            else:
                print "\nFlavor not found for this cloud. Please use one id from the following!\n"
                for key, value in flavors[self.defCloud].items():
                    print key, value['name']
                return False
        else:
            print "The default cloud does not have flavors listed!"
            return None
    def chkImage(self, userImage):
        imgName = userImage
        imgId = None
        self.mongoClass.refresh(self.user, types=["images"])
        images = self.mongoClass.images(cm_user_id=self.user)
        if self.defCloud in images:
            cloudImages = images[self.defCloud]
            for key, value in cloudImages.iteritems():
                if value['name'] == imgName:
                    imgId = key
                    return imgId
        else:
            print "The default cloud does not have images!"
            return None
        if imgId == None:
            print "\nImage not found for this cloud. Please choose one of the following!\n"
            for key, value in images[self.defCloud].items():
                print value['name']
            return False

def main():
    config = cm_config()
    defCloud = config.default_cloud
    user = config.username()
    mongoClass = cm_mongo()
    mongoClass.activate(user)
    vmi = vmInterface(user, config, mongoClass)
    flavor = raw_input("Input the test flavor for vm: ")
    assert vmi.chkFlavor(flavor)
    image = raw_input("Input the test image for vm: ")
    print vmi.chkImage(image)


if __name__ == "__main__":
    main()


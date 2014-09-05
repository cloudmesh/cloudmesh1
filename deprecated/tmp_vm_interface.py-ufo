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
import paramiko as pm
import os

from bson.json_util import dumps

from pprint import pprint
from prettytable import PrettyTable

#Get rid of this
from cloudmesh.user.cm_user import cm_user
from cmd3.shell import command
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)

class vm_interface:

    def __init__(self, user, defCloud, mongo):
        self.user = user
        self.mongoClass = mongo
        self.defCloud = defCloud

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

    def _destroy(self, serverName):
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

    def _chkFlavor(self, userFlavor):
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

    def _getImageId(self, userImage):
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
            print "\nImage not found for this cloud. Please use one of the following available images!\n"
            for key, value in images[self.defCloud].items():
                print value['name']
            return False

    def deleteVM(self, defDict, userParameters):
        try:
            dbDict = self.mongoClass.db_defaults.find_one({'cm_user_id': self.user})
            nextIndex = int(dbDict['index'])
            deletedVMs = 0
            if userParameters['name']:
                servName = userParameters['name']
                retVal = self._destroy(servName)
            else:
                if userParameters['count']:
                    numberOfVMs = int(userParameters['count'])
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
                    servName = "%s_%s" % (defDict['prefix'], nextIndex)
                    retVal = self._destroy(servName)
                    if retVal != 0:
                        break
                    deletedVMs = deletedVMs + 1

            #update the index for db defaults
            index = int(dbDict['index'])
            #on deleting vm <prefix>_1 keep the index fixed to 1
            index = unicode(index - deletedVMs)
            self.mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'index': index}},upsert=False, multi=False)
        except:
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

    def launchVM(self, defDict, userParameters):
        dbDict = self.mongoClass.db_defaults.find_one({'cm_user_id': self.user})
        dbIndex = int(dbDict['index'])

        if userParameters['count']:
            numberOfVMs = int(userParameters['count'])
        else:
            numberOfVMs = 1

        #Check for image and flavor, if specified by the user.
        imgId = None
        if userParameters['image']:
            imgId = self._getImageId(userParameters['image'])
            if not imgId:
                return

        flavorId = None
        if userParameters['flavor']:
            checkFlavor = self._chkFlavor(userParameters['flavor'])
            if checkFlavor == False:
                return
            elif checkFlavor == True:
                flavorId = userParameters['flavor']

        try:
            for i in range(numberOfVMs):

                if imgId == None: #implies default image to be used.
                    imgId = defDict['image']
                if flavorId == None: #implies default flavor to be used.
                    flavorId = 1

                result = self.mongoClass.vm_create(self.defCloud, defDict['prefix'], dbIndex, flavorId, imgId, defDict['keyname'], None, self.user)

                self.mongoClass.refresh(names=[self.defCloud], types=["servers"], cm_user_id=self.user)

                if ('server' not in result):
                    badReq = 'badRequest'
                    if(badReq in result):
                        print result[badReq]['message']
                    return

                #update the index for next VM
                print 'VM successfully launched!'
                pprint(result)
                dbIndex = unicode(int(dbIndex) + 1)
            dbIndex = int(dbDict['index'])
            dbIndex = unicode(dbIndex + numberOfVMs)
            self.mongoClass.db_defaults.update({'_id': dbDict['_id']}, {'$set':{'index': dbIndex}},upsert=False, multi=False)
            time.sleep(5)
        except:
            print "Unexpected error:", sys.exc_info()[0], sys.exc_info()[1]
        return

    def getImageOrFlavor(self, paramToSet, userParameters):
        log.info ("get the VM ", paramToSet)
        server = self.findVM(self.user, userParameters["name"])
        if(server):
            try:
                paramId = server[paramToSet]['id']
                if paramToSet is 'flavor':
                    params = self.mongoClass.flavors(cm_user_id=self.user)
                else:
                    params = self.mongoClass.images(cm_user_id=self.user)

                if len(params[server['cm_cloud']]) == 0:
                    print paramToSet, 's not available anymore.'
                    return
                else:
                    reqdParam = params[server['cm_cloud']][paramId]
                    jsonObj = dumps(reqdParam, sys.stdout, sort_keys=True, indent=4, separators=(',',':'))
                    print "--------------------------------------------------------------------------------\n"
                    print "The %s for:"% (paramToSet), userParameters["name"]
                    print jsonObj, "\n"
                    return jsonObj
            except:
                print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        return

    def sshVm(self):
        """this method contains bugs"""
        
        print 'In SSH'
        ssh = pm.SSHClient()
        #
        # gvl:  this is a bug
        #
        

        ssh.load_host_keys(os.path.expanduser('/Users/pushkarjoshi/.ssh/known_hosts'))
        ssh.set_missing_host_key_policy(pm.AutoAddPolicy())

        #
        # gvl:  this is a bug
        #


        privKey = pm.RSAKey.from_private_key_file('/Users/pushkarjoshi/testKey.pem')

        #
        # gvl:  this is a bug
        #
        
        ssh.connect('198.202.120.7', username='psjoshi', pkey=privKey)
        chan = ssh.invoke_shell()
        print repr(ssh.get_transport())
        print '*** Here we go!'
        #cmd = raw_input("Enter the command")
        chan.send(cmd+'\n')
        tCheck = 0
        while not chan.recv_ready():
            time.sleep(10)
            tCheck += 1
        out = chan.recv(1024)
        print out


def main():

    config = cm_config()
    defCloud = config.default_cloud
    user = config.username()
    mongoClass = 'a' #cm_mongo()
#    mongoClass.activate(user)
    #vmi = vm_interface(user, defCloud, mongoClass)
    #vm = vmi.findVM('psjoshi', 'gvonlasz_1')
    vmi = vm_interface('a', 'b', 'c')
    vmi.sshVm()


    #vmi.testVM(cnt='10')
    """ Test the functions.
    defDict = { 'prefix': 'psjoshi', 'keyname': 'fg_pro'}
    userParameters = { 'image': 'futuregrid/sl-6', 'flavor': '2', 'count': 5}
    vmi.launchVM(defDict, userParameters)
    flavor = raw_input("Input the test flavor for vm: ")
    assert vmi.chkFlavor(flavor)
    image = raw_input("Input the test image for vm: ")
    print vmi.chkImage(image)
    """


if __name__ == "__main__":
    main()


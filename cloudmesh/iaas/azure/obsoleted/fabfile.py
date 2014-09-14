from fabric.api import *
import ConfigParser
import pickle
import os
import commands
from sh import azure as _azure
import getpass
import pprint
import re


from multiprocessing import Pool as _Pool
global vmName, vmImage, vmPassword, maxparallel
maxparallel = 5
CONFIGPATH = 'config.cfg'
DBFILEPATH = 'database.db'

config = ConfigParser.ConfigParser()
config.read(CONFIGPATH)
regex = re.compile("\x1b\[(?:\d{1,2}m?)?", re.UNICODE)


vm_start = azure.bake("vm", "start")
vm_restart = azure.bake("vm", "restart")
vm_shutdown = azure.bake("vm", "shutdown")
vm_list = azure.bake("vm", "list")
vm_create = azure.bake("vm", "create")
vm_show = azure.bake("vm", "show")
vm_delete = azure.bake("vm", "delete")


def activate():
    settingsFilePath = config.get('cloudmesh.azurepublishsettings_file_path')
    _azure('account', 'clear')
    errmsg = 'No account information found'
    cmd = 'azure account import \'' + settingsFilePath + '\''

    text = commands.getstatusoutput(cmd)
    if not errmsg in text[1]:
        print 'Activated'
    else:
        print 'There was an error while activation'


def _selectImage():
    images = _buildAzureImageDict()
    print 'Please select Image'
    allItems = images.items()
    # for (arg1, arg2) in allItems:
    for item in allItems:
        print item[0] + "\t" + item[1][0] + "\t" + item[1][1] + "\t" + item[1][2]

    while 1:
        var = raw_input("Image : ")
        if var in images:
            print images[var][0]
            return images[var][0]
        else:
            print "Incorrect Image name"
    return var


def create(index, name=config.get('cloudmesh.azure.username')):
    global vmName, vmImage, vmPassword
    vmImage = config.get('cloudmesh.azure.image')
    userName = config.get('cloudmesh.azure.username')
    vmPassword = config.get('cloudmesh.azure.password')
    vmName = name

    if(vmImage == ''):
        print('image name not set, use set:image,value)')
    elif(userName == ''):
        print('image name not set, use set:username,value)')
    elif(vmPassword == ''):
        print('image name not set, use set:password,value)')
    else:
        """Creates a number of vms with the labels prefix-0 to prefix-<number-1>. It uses a threadpool"""
        pool = _Pool(processes=maxparallel)
        list = range(0, int(index))
        result = pool.map(_boot, list)
        # _boot(index)
        print result


def start(name):
    result = vm_start(name)
    print result


def restart(name):
    result = vm_restart(name)
    print result


def shutdown(name):
    result = vm_shutdown(name)
    print result


def _boot(index):
    global vmName, vmImage, vmPassword
    number = str(index).zfill(3)
    name = '%s-%s' % (vmName, number)
    vm = {'vmname': name,
          'username': config.get('azure', 'username'),
          'image': vmImage,
          'password': vmPassword
          }

    # cmd = 'azure vm create %(vmname)s %(image)s %(username)s --ssh --location "East US" %(password)s' % vm
    # print cmd
    result = vm_create("%(vmname)s" % vm,
                       "%(image)s" % vm,
                       "%(username)s" % vm,
                       "--ssh",
                       "--location",
                       "East US",
                       "%(password)s" % vm)
    return result


def list():
    result = vm_list()
    print result


def show(name):
    result = vm_show()
    print result


def delete(name):
    result = vm_delete()
    print result


def set(option, value=''):
    cfgFile = open(CONFIGPATH, 'w')
    if(option == 'password'):
        config.set('azure', 'password', value)
    if(option == 'image'):
        value = _selectImage()
        config.set('azure', 'image', value)
    if(option == 'username'):
        config.set('azure', 'username', value)
    config.write(cfgFile)
    cfgFile.close()


def _buildAzureImageDict():
    allText = _azure('vm', 'image', 'list')
    imageNamePrefix = 'azure_img'
    imageNameCounter = 0
    allLines = allText.splitlines()
    cleanLines = []
    counter = 2
    images = {}
    # skip counter number of lines
    for line in allLines:
        if 'data' in line:
            if not counter:
                cleanLines.append(line)
            else:
                counter = counter - 1

    for line in cleanLines:
        imageNameCounter = imageNameCounter + 1
        l = []
        # (name, id, os) = line.split()
        # l.append(name)
        # l.append(id)
        # l.append(os)

        l.append(line.split()[1])
        l.append(line.split()[2])
        l.append(line.split()[3])
        images[imageNamePrefix + str(imageNameCounter)] = l

    return images


def _getVmDict(name):
    text = vm_show(name)

    allLines = text.splitlines()
    cleanLines = []
    vm = {}
    # skip counter number of lines

    for line in allLines:
        if 'data' in line:
            cleanLines.append(regex.sub("", line))

    for line in cleanLines:
        line = line.replace(':', '"')
        splits = line.split('"')
        vm[str(splits[1].strip())] = str(splits[2].strip())
    allItems = vm.items()
    return vm


def save():
    text = vm_list()
    allLines = text.splitlines()
    cleanLines = []
    # skip counter number of lines
    azure = {}
    vms = {}
    counter = 2
    # allines = allines [2:-1]
    for line in allLines:
        if 'data' in line:
            # not needed make sure you have in all lines only the lines that need to be parsed
            # see above [2:-1] you may have to use [2:-2] dependent if new line
            # is added, find out what the right thing is ...

            if not counter:
                cleanLines.append(regex.sub("", line))
            else:
                counter = counter - 1

    for line in cleanLines:
        splits = line.split()
        # (arg1, arg2) = line.split();
        # vms[arg1] = _getVMDict(arg2)
        vms[splits[1]] = _getVmDict(splits[2])

    # _getVmDict('shwetaVM1-000');
    azure['name'] = 'azure'
    azure['servers'] = vms
    pickle.dump(azure, open(DBFILEPATH, "wb"))
    azure = pickle.load(open(DBFILEPATH, "rb"))
    print azure

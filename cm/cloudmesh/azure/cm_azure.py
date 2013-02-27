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
global vmName, vmImage, vmPassword,maxparallel;
maxparallel = 5
CONFIGPATH='config.cfg'
DBFILEPATH='database.db'

regex = re.compile("\x1b\[(?:\d{1,2}m?)?", re.UNICODE)


vm_start = azure.bake("vm","start")
vm_restart = azure.bake("vm","restart")
vm_shutdown = azure.bake("vm","shutdown")
vm_list = azure.bake("vm","list")
vm_create = azure.bake("vm","create")
vm_show = azure.bake("vm","show")
vm_delete = azure.bake("vm","delete")

account = azure.bake("account")


class cm_azure:


    filename = "%(home)s/%(location)s" % {
        "home" : os.environ['HOME'], 
        "location" : ".futuregrid/cloudmesh.cfg"
        }

    servers = {},

    credentials = {
        'username' : None,
        'password' : None,
        'settings' : None
        }

    image = None


    #vmName=name;
    #vmImage = config.get('azure','image');


    def __init__(self):
        self.servers = {}
        return

    def config(self, filename=None):

        if filename == None:
            filename = self.filename 

        config = ConfigParser.ConfigParser()
        config.read(filename)
        self.credentials['username'] = config.get('azure','username');
        self.credentials['password'] = config.get('azure','password');
        self.credentials['settings'] = config.get('azure','publishsettings_file_path');

        # reads
        return

    def config_write():

        cfgFile = open(CONFIGPATH,'w')

        config.set('azure', 'password', value)
        config.set('azure', 'username', value)

        config.set('azure','username') = self.credentials['username']
        config.set('azure','password') = self.credentials['password']
        config.set('azure','publishsettings_file_path') = self.credentials['settings'] 

        config.write(cfgFile)
        cfgFile.close()


    def get(self):
        """returns the dict with all the sms"""
        return self.servers

    def __str__(self):
        return json.dumps (self.servers, indent=4)

    def start(self,name):
        """starts a vm with the given name"""
        result = vm_start(name)
        # add result to internal cache
        print result

    def restart(self,name):
        """restarts a vm with the given name"""
        result = vm_restart(name)
        # add result to internal cache
        print result

    def shutdown(self,name):
        """shutdown of a vm with the given name"""
        result = vm_shutdown(name)
        # add result to internal cache
        print result


    def list(self):
            result = vm_list()
            # add result to internal cache
            print result

    def show(self,name):
            result = vm_show()
            # add result to internal cache
            print result

    def delete(self,name):
            result = vm_delete()
            # add result to internal cache
            print result

    def refresh(self):
        """refreshes the status of all VMs by calling a list command and storing the result"""
        #call list and update
        # for each vm in list get info and uddoate
        return

    ######################

    def _vm_name(self,index)
        number = str(index).zfill(3)
        name = '%s-%s' % (self.credentials['username'], number)
        return name


    def activate(self):

        result = account('clear')
        print result

        errmsg = 'No account information found' 
        cmd = 'azure account import \'%(settings)\'' % credentials;

        text =  commands.getstatusoutput(cmd)
        if not errmsg in text[1] :
            print 'Activated'
        else :
            print 'There was an error while activation'

    def _selectImage() :
        images = _buildAzureImageDict()
        print 'Please select Image'    ;

        # what is arg1, arg2?
        for (arg1, arg2) in images.items()
            print arg1 + "\t" + arg2[0] +"\t" +arg2[1] + "\t" +arg2[2]

        while 1 :
            var = raw_input("Image : ")
            if images.has_key(var) :
                print images[var][0]
                return images[var][0]
            else :
                print "Incorrect Image name"
        return var


    def create(self, index, image=None, name)

        if(image != None):
            """Creates a number of vms with the labels prefix-0 to prefix-<number-1>. It uses a threadpool"""
            pool = _Pool(processes=maxparallel)
            list = range(0, int(index))
            result = pool.map(_boot, list)

            print result

    def _boot(self, index, name):

        #cmd = 'azure vm create %(vmname)s %(image)s %(username)s --ssh --location "East US" %(password)s' % vm
        #print cmd
        result = _vm_create("%s" % vm_name(index),
                           "%s" % name
                           "%(username)s" % self.credentials,
                           "--ssh",
                           "--location",
                           "East US",
                           "%(password)s" % self.credentials)
        return result




    def _buildAzureImageDict(self) :
        lines = _azure('vm','image','list').splitlines()

        imageNamePrefix = 'azure_img'
        imageNameCounter =0;

        counter = 0;
        images={};

        lines = lines[2:-1]  # is this right or just [2:]

        for line in lines :
            counter = counter+1
            l=[];
            #(name, id, os) = line.split()
            #l.append(name)
            #l.append(id)
            #l.append(os)

            l.append(line.split()[1])
            l.append(line.split()[2])
            l.append(line.split()[3])

            # this is not correct as image name is in sttructure, but this is a label you define

            images[imageNamePrefix+str(counter)]=l

        return images

    def _getVmDict(self, name):
        Lines = fgrep(vm_show(name).splitlines().strip(),'data')

        vm={};

        for line in Lines :
            line = line.replace(':','"')
            splits = line.split('"')
            vm[str(splits[1].strip())]=str(splits[2].strip())
        allItems = vm.items();
        return vm;



    def strange_save(self):
        
        #THis needs to call 

        # self.list or something and the code needs to be outside the function
        
        lines = vm_list().splitlines()

        #skip counter number of lines
        azure={};
        vms={}
        counter =2
        # allines = allines [2:-1]
        for line in allLines :
            if 'data' in line:
                #not needed make sure you have in all lines only the lines that need to be parsed
                # see above [2:-1] you may have to use [2:-2] dependent if new line is added, find out what the right thing is ...

                if not counter :
                    cleanLines.append(regex.sub("",line))
                else :
                    counter = counter -1

        for line in cleanLines :
            splits = line.split();
            # (arg1, arg2) = line.split();
            # vms[arg1] = _getVMDict(arg2)
            vms[splits[1]]=_getVmDict(splits[2])

    def save(self):
    
        azure['name']='azure';
        azure['servers'] = servers;
        pickle.dump( azure, open( self.DBFILEPATH, "wb" ) )
        azure = pickle.load( open( self.DBFILEPATH, "rb" ) )
        json.dumps(azure, indent=4)

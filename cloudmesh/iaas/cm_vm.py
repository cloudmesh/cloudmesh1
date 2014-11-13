from __future__ import print_function
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.user.cm_user import cm_user
from cloudmesh_common.logger import LOGGER
from cloudmesh.iaas.cm_cloud import CloudManage
from cloudmesh.config.cm_config import cm_config
from cloudmesh.util.ssh import ssh_execute
from cloudmesh import banner
from cloudmesh import yn_choice
from cmd3.console import Console
from sh import ssh
from subprocess import call
from pprint import pprint
import sys
import time
from cloudmesh.shell.cm_list import shell_command_list
from cloudmesh.keys.util import _keyname_sanitation
from cloudmesh.config.cm_keys import cm_keys_mongo
from cloudmesh.util.shellutil import get_vms_look_for, shell_commands_dict_output\
                                    ,get_command_list_refresh_default_setting

log = LOGGER(__file__)

def shell_command_vm(arguments):
    """
        ::

            Usage:
                vm start [--name=<vmname>]
                         [--count=<count>]
                         [--cloud=<CloudName>]
                         [--image=<imgName>|--imageid=<imgId>]
                         [--flavor=<flavorName>|--flavorid=<flavorId>]
                         [--group=<group>]
                vm delete [NAME|--id=<id>] 
                          [--group=<group>]
                          [--cloud=<CloudName>]
                          [--prefix=<prefix>|--hostlist=<hostlist>]
                          [--force]
                vm ip assign (NAME|--id=<id>) 
                             [--cloud=<CloudName>]
                vm ip show [NAME|--id=<id>] 
                           [--group=<group>]
                           [--cloud=<CloudName>]
                           [--prefix=<prefix>|--hostlist=<hostlist>]
                           [--format=FORMAT] 
                           [--refresh] 
                vm login (--name=<vmname>|--id=<id>|--addr=<address>) --ln=<LoginName>
                         [--cloud=<CloudName>]
                         [--key=<key>]
                         [--] [<command>...]
                vm login NAME --ln=<LoginName>
                         [--cloud=<CloudName>]
                         [--key=<key>]
                         [--] [<command>...]
                vm list [CLOUD|--all] 
                        [--refresh] 
                        [--format=FORMAT] 
                        [--column=COLUMN]
                        [--group=<group>]
                         
            Arguments:
                <command>              positional arguments, the commands you want to
                                       execute on the server(e.g. ls -a), you will get 
                                       a return of executing result instead of login to 
                                       the server, note that type in -- is suggested before 
                                       you input the commands
                NAME                   server name
                
            Options:
                --addr=<address>       give the public ip of the server
                --cloud=<CloudName>    give a cloud to work on, if not given, selected
                                       or default cloud will be used
                --count=<count>        give the number of servers to start
                --flavor=<flavorName>  give the name of the flavor
                --flavorid=<flavorId>  give the id of the flavor
                --group=<group>        give the group name of server
                --hostlist=<hostlist>  e.g. sample[1-3] => ['sample1', 'sample2', 'sample3']
                                       sample[1-3,18] => ['sample1', 'sample2', 'sample3', 'sample18']
                --id=<id>              give the server id
                --image=<imgName>      give the name of the image
                --imageid=<imgId>      give the id of the image
                --key=<key>            spicfy a private key to use, input a string which 
                                       is the full path to the key file
                --ln=<LoginName>       give the login name of the server that you want 
                                       to login
                --name=<vmname>        give the name of the virtual machine
                --prefix=<prefix>      give the prefix of the server, standand server
                                       name is in the form of prefix_index, e.g. abc_9
                --force                delete vms without user's confirmation

            Description:
                commands used to start or delete servers of a cloud

                vm start [options...]       start servers of a cloud, user may specify
                                            flavor, image .etc, otherwise default values
                                            will be used, see how to set default values
                                            of a cloud: cloud help
                vm delete [options...]      delete servers of a cloud, user may delete
                                            a server by its name or id, delete servers
                                            of a group or servers of a cloud, give prefix
                                            and/or range to find servers by their names.
                                            Or user may specify more options to narrow
                                            the search
                vm ip assign [options...]   assign a public ip to a VM of a cloud
                vm ip show [options...]     show the ips of VMs
                vm login [options...]       login to a server or execute commands on it
                vm list [options...]        same as command "list vm", please refer to it

            Examples:
                vm start --count=5 --group=test --cloud=india
                        start 5 servers on india and give them group
                        name: test

                vm delete --group=test --range=,9
                        delete servers on selected or default cloud with search conditions:
                        group name is test and index in the name of the servers is no greater
                        than 9

    """

    call_proc = VMcommand(arguments)
    return call_proc.call_procedure()


class VMcommand(object):

    def __init__(self, arguments):
        self.arguments = arguments

        # print self.arguments ########

        try:
            self.config = cm_config()
        except:
            log.error("There is a problem with the configuration yaml files")
    
        self.username = self.config['cloudmesh']['profile']['username']

    def _vm_create(self):
        # -------------------------
        # check input
        count = 1
        if self.arguments['--count']:
            try:
                count = int(self.arguments['--count'])
            except:
                Console.error("--count must be assigned with an integer")
                return False
            if count < 1:
                Console.error(
                    "--count must be assigned with an integer greater than 0")
                return False
            watch = time.time()
        # -------------------------
        # select cloud
        cloudname = self.get_working_cloud_name()
        if cloudname == False: return
        # -------------------------
        # starting vm
        res = start_vm(self.username,
                       cloudname,
                       count=count,
                       flavorname=self.arguments['--flavor'],
                       flavorid=self.arguments['--flavorid'],
                       imagename=self.arguments['--image'],
                       imageid=self.arguments['--imageid'],
                       groupname=self.arguments['--group'],
                       servername=self.arguments['--name'])
        # -------------------------
        if res:
            if self.arguments['--count']:
                watch = time.time() - watch
                print(("time consumed: %.2f" % watch), "s")

            print("to check realtime vm status: list vm --refresh")

    def _vm_delete(self):
        # -------------------------
        # check input
        if self.arguments['NAME'] is None and\
           self.arguments['--id'] is None and\
           self.arguments['--group'] is None and\
           self.arguments['--cloud'] is None and\
           self.arguments['--prefix'] is None and\
           self.arguments['--hostlist'] is None:
            print("Please specify at least one option, to get more information: vm help")
            return
        
        cloudname = self.get_working_cloud_name()
        if cloudname == False: return

        deleteAllCloudVMs = False
        if self.arguments['--cloud'] and\
        self.arguments['NAME'] is None and\
        self.arguments['--id'] is None and\
        self.arguments['--group'] is None and\
        self.arguments['--prefix'] is None and\
        self.arguments['--hostlist'] is None:
            deleteAllCloudVMs = True

        if self.arguments['--force']:
            preview = False
        else:
            preview = True

        server_id_list = get_vms_look_for(self.username,
                                          cloudname,
                                          servername=self.arguments['NAME'],
                                          serverid=self.arguments['--id'],
                                          groupname=self.arguments['--group'],
                                          prefix=self.arguments['--prefix'],
                                          hostls=self.arguments['--hostlist'],
                                          getAll=deleteAllCloudVMs,
                                          refresh=True)
        if server_id_list == False: return
        delete_vm(self.username,
                  cloudname,
                  server_id_list=server_id_list,
                  preview=preview,
                  refresh=False)

    def _assign_public_ip(self):
        cloudname = self.get_working_cloud_name()
        if cloudname == False:
            return
        serverid = self.get_working_server_id(cloudname)
        if serverid == False:
            return
        assign_public_ip(
            username=self.username, cloudname=cloudname, serverid=serverid)

    def _vm_login(self):
        cloudname = self.get_working_cloud_name()
        if cloudname == False: return
        address = None
        if self.arguments['--addr']:
            address = self.arguments['--addr']
        else:
            serverid = self.get_working_server_id(cloudname)
            if serverid == False:
                return
            mongo = cm_mongo()
            serverdata = mongo.servers(clouds=[cloudname], 
                                        cm_user_id=self.username)[cloudname]
            serverdata = serverdata[serverid]['addresses']['private']
            for i in serverdata:
                if i['OS-EXT-IPS:type'] == "floating":
                    address = i['addr']
            if address == None:
                Console.warning("Please assign a public ip to the VM first"\
                                "(vm ip (--name=<vmname>|--id=<id>))")
                return
        if self.arguments['<command>']:
            commands = ' '.join(self.arguments['<command>'])
            try:
                print(">>>\n")
                print(ssh_execute(self.arguments['--ln'], address, 
                                  commands, key=self.arguments['--key']))
            except:
                err = sys.exc_info()
                Console.error("Can not execute ssh on {0}:{1}".format(address, err))
        else:
            host = "{0}@{1}".format(self.arguments['--ln'], address)
            option = "-o StrictHostKeyChecking=no "
            if self.arguments['--key']:
                call(['ssh', option, '-i', self.arguments['--key'], host])
            else:
                call(['ssh', option, host])
                
                
    def _vm_list(self):
        '''
        same as command vm list
        '''
        arguments = dict(self.arguments)
        arguments["vm"] = True
        shell_command_list(arguments)
        
    def _show_ip(self):
        '''
        list the ips of VMs
        '''
        mongo = cm_mongo()
        cloudname = self.get_working_cloud_name()
        if cloudname == False: return
        if get_command_list_refresh_default_setting(self.username) or self.arguments['--refresh']:
            mongo.activate(cm_user_id=self.username, names=[cloudname])
            mongo.refresh(cm_user_id=self.username,
                          names=[cloudname],
                          types=['servers'])
            
        servers_dict = mongo.servers(
                    clouds=[cloudname], cm_user_id=self.username)[cloudname]
                    
        AllCloudVMs = False
        if self.arguments['--cloud'] and\
        self.arguments['NAME'] is None and\
        self.arguments['--id'] is None and\
        self.arguments['--group'] is None and\
        self.arguments['--prefix'] is None and\
        self.arguments['--hostlist'] is None:
            AllCloudVMs = True
                    
        server_id_list = get_vms_look_for(self.username,
                                          cloudname,
                                          servername=self.arguments['NAME'],
                                          serverid=self.arguments['--id'],
                                          groupname=self.arguments['--group'],
                                          prefix=self.arguments['--prefix'],
                                          hostls=self.arguments['--hostlist'],
                                          getAll=AllCloudVMs,
                                          refresh=False)
        if server_id_list == False: return
        if server_id_list == []:
            Console.warning("no vm meets the condition")
            return
        
        res = {}
        for item in server_id_list:
            temp = servers_dict[item]['addresses']['private']
            fixed = ""
            floating = ""
            for item0 in temp:
                if item0['OS-EXT-IPS:type'] == 'fixed':
                    fixed = fixed + item0['addr'] + ", "
                elif item0['OS-EXT-IPS:type'] == 'floating':
                    floating = floating + item0['addr'] + ", "
            if fixed != "": fixed = fixed[:-2]
            if floating != "": floating = floating[:-2]
            temp0 = {}
            temp0['name'] = servers_dict[item]['name']
            temp0['fixed'] = fixed
            temp0['floating'] = floating
            res[item] = temp0
            
        if self.arguments['--format']:
            if self.arguments['--format'] not in ['table', 'json', 'csv']:
                Console.error("please select printing format among table, json and csv")
                return
            else:
                p_format = self.arguments['--format']
        else:
            p_format = None
        
        header = ['name', 'fixed', 'floating']
        
        shell_commands_dict_output(res,
                                   print_format=p_format,
                                   firstheader="id",
                                   header=header)
            
        
        

    # --------------------------------------------------------------------------
    def get_working_cloud_name(self):
        '''
        get the name of a cloud to work on, if CLOUD not given, will pick the
        selected or default cloud
        '''
        cloudname = None
        cloudobj = CloudManage()
        mongo = cm_mongo()
        if self.arguments['--cloud']:
            cloud = cloudobj.get_clouds(
                self.username, getone=True, cloudname=self.arguments['--cloud'])
            if cloud is None:
                Console.error(
                    "could not find cloud '{0}'".format(self.arguments['--cloud']))
                return False
            else:
                cloudname = self.arguments['--cloud']
        else:
            cloudname = cloudobj.get_selected_cloud(self.username)
        if cloudname not in mongo.active_clouds(self.username):
            Console.warning(
                "cloud '{0}' is not active, to activate a cloud: cloud on [CLOUD]".format(cloudname))
            return False
        else:
            return cloudname

    def get_working_server_id(self, cloudname):
        serverid = None
        mongo = cm_mongo()
        mongo.activate(cm_user_id=self.username, names=[cloudname])
        mongo.refresh(self.username, names=[cloudname], types=['servers'])
        serverdata = mongo.servers(
            clouds=[cloudname], cm_user_id=self.username)[cloudname]
        vmname = self.arguments['--name'] or self.arguments['NAME']
        if vmname:
            ls = []
            for k, v in serverdata.iteritems():
                if vmname == v['name']:
                    ls.append(k)
            if len(ls) > 1:
                Console.warning("There are more than one VM named {0}, please use VM id instead"
                                .format(vmname))
                return False
            elif len(ls) == 0:
                Console.error(
                    "Could not find VM named {0}".format(vmname))
                return False
            else:
                serverid = ls[0]
        elif self.arguments['--id']:
            for k, v in serverdata.iteritems():
                if self.arguments['--id'] == k:
                    serverid = self.arguments['--id']
                    break
            if serverid == None:
                Console.error(
                    "Could not find VM with id {0}".format(self.arguments['--id']))
                return False
        else:
            Console.warning("Please specify a VM name or id")
            return False
        return serverid

    def call_procedure(self):
        if 'start' in self.arguments and self.arguments['start']:
            return self._vm_create()
        elif 'delete' in self.arguments and self.arguments['delete']:
            self._vm_delete()
        elif 'ip' in self.arguments and self.arguments['ip'] and\
        'assign' in self.arguments and self.arguments['assign']:
            self._assign_public_ip()
        elif 'login' in self.arguments and self.arguments['login']:
            self._vm_login()
        elif 'list' in self.arguments and self.arguments['list']:
            self._vm_list()
        elif 'ip' in self.arguments and self.arguments['ip'] and\
        'show' in self.arguments and self.arguments['show']:
            self._show_ip()

    # --------------------------------------------------------------------------

# ------------------------------------------------------------------------
# supporting functions
# ------------------------------------------------------------------------


def start_vm(username,
             cloudname,
             count=1,
             flavorname=None,
             flavorid=None,
             imagename=None,
             imageid=None,
             groupname=None,
             servername=None):
    '''
    create a vm of a cloud of a user
    will check flavor, image existence if provided
    user can specify groupname which will be written in metadata, servername which
    will replace prefix+index as the vm name
    it's better to check cloud active status before use this function
    :param username: string
    :param cloudname: string
    :param count: number of vms to start
    :return False if error

    TODO: what if fail, how to acknowledge it; no return now as using celery
          input key
          missing security group
    '''

    mongo = cm_mongo()
    userobj = cm_user()
    cloudobj = CloudManage()
    mongo.activate(cm_user_id=username, names=[cloudname])
    userinfo = userobj.info(username)
    key = None
    vm_image_id = None
    vm_flavor_id = None

    error = ''

    # -------------------------
    # refresh flavor or image
    to_refresh = []

    if flavorname is not None or flavorid is not None:
        to_refresh.append("flavors")
    if imagename is not None or imageid is not None:
        to_refresh.append("images")
    if to_refresh != []:
        mongo.refresh(username, names=[cloudname], types=to_refresh)

    # -------------------------
    # flavor handler
    if flavorname is not None or flavorid is not None:
        flavordata = mongo.flavors(
            clouds=[cloudname], cm_user_id=username)[cloudname]
        same_name_count = 0
        for k, v in flavordata.iteritems():
            if flavorname is not None:
                if flavorname == v['name']:
                    vm_flavor_id = k
                    same_name_count = same_name_count + 1
            else:
                if flavorid == k:
                    vm_flavor_id = k
                    break
        if vm_flavor_id is None:
            error = error + "The flavor you provide doesn't exist. "
        if same_name_count > 1:
            error = error + "There are more than one flavor with the name you provide" \
                            "please use flavorid instead or select one by command cloud" \
                            "set flavor [CLOUD]. "
    else:
        try:
            vm_flavor_id = userinfo["defaults"]["flavors"][cloudname]
        except:
            pass
        if vm_flavor_id in [None, 'none']:
            error = error + \
                "Please specify a default flavor(command: cloud set flavor [CLOUD]). "
    # -------------------------
    # image handler
    if imagename is not None or imageid is not None:
        imagedata = mongo.images(
            clouds=[cloudname], cm_user_id=username)[cloudname]
        same_name_count = 0
        for k, v in imagedata.iteritems():
            if imagename is not None:
                if imagename == v['name']:
                    vm_image_id = k
                    same_name_count = same_name_count + 1
            else:
                if imageid == k:
                    vm_image_id = k
                    break
        if vm_image_id is None:
            error = error + "The image you provide doesn't exist. "
        if same_name_count > 1:
            error = error + "There are more than one image with the name you provide" \
                            "please use imageid instead or select one by command cloud" \
                            "set image [CLOUD]. "
    else:
        try:
            vm_image_id = userinfo["defaults"]["images"][cloudname]
        except:
            pass
        if vm_image_id in [None, 'none']:
            error = error + \
                "Please specify a default image(command: cloud set flavor [CLOUD]). "

    # -------------------------
    # key handler
    if "key" in userinfo["defaults"]:
        key = userinfo["defaults"]["key"]
    elif len(userinfo["keys"]["keylist"].keys()) > 0:
        key = userinfo["keys"]["keylist"].keys()[0]

    if key:
        keycontent = userinfo["keys"]["keylist"][key]
        if keycontent.startswith('key '):
            keycontent = keycontent[4:]
        cm_keys_mongo(username).check_register_key(username, cloudname, key, keycontent)
        keynamenew = _keyname_sanitation(username, key)
    else:
        error = error + \
            "No sshkey found. Please Upload one"
    # -------------------------

    if error != '':
        Console.error(error)
        return False
    # -------------------------
    metadata = {'cm_owner': username}
    if groupname:
        metadata['cm_group'] = groupname

    tmpnamefl = cloudobj.get_flavors(
        cloudname=cloudname, getone=True, id=vm_flavor_id)['name']
    tmpnameim = cloudobj.get_images(
        cloudname=cloudname, getone=True, id=vm_image_id)['name']

    while count > 0:
        userinfo = userobj.info(username)
        if servername:
            prefix = ''
            index = ''
            givenvmname = servername
            tmpnameser = servername
        else:
            prefix = userinfo["defaults"]["prefix"]
            index = userinfo["defaults"]["index"]
            givenvmname = None
            tmpnameser = prefix + '_' + str(index)
        # ------------------------
        # vm start procedure

        banner("Starting vm->{0} on cloud->{1} using image->{2}, flavor->{3}, key->{4}"
               .format(tmpnameser, cloudname, tmpnameim, tmpnamefl, keynamenew))
        
        useQueue = True
        if useQueue:
            result = mongo.vm_create_queue(cloudname,
                                            prefix,
                                            index,
                                            vm_flavor_id,
                                            vm_image_id,
                                            keynamenew,
                                            meta=metadata,
                                            cm_user_id=username,
                                            givenvmname=givenvmname)
            print("job status:", result.state)
        else:
            result = mongo.vm_create(cloudname,
                                        prefix,
                                        index,
                                        vm_flavor_id,
                                        vm_image_id,
                                        keynamenew,
                                        meta=metadata,
                                        cm_user_id=username,
                                        givenvmname=givenvmname)
            pprint(result)

        # ------------------------
        # increase index if it is used
        if not servername:
            userobj.set_default_attribute(username, "index", int(index) + 1)
        # ------------------------

        count = count - 1

#
# TODO: Mark this is very complicated, think about what we want to do
#

#
#  delete all
#  delete [1-10]
#  delete gvonlasz[1-10]
#  delate --group=test [1-10]
#  delete --cloud=india [1-10]
#

# l = search_vm("[1-10]")
# l = search_vm("gregor[1-10]")

# delete_vms(l, interactive=False, force=True)

def delete_vm(username,
              cloudname,
              server_id_list=None,
              preview=False,
              refresh=False):
    '''
    delete vms of a cloud of a user, this function provides several ways to find and
    delete vms
    :param server_id_list:: the list of VMs(id) to delete
    :param preview:: True if the user wants to preview and confirm before start to delete

    TODO: what if fail, how to acknowledge it
          range search: now if prefix not given, all vms whose index are in the range will
          be deleted, regardless of its prefix
          it looks like even though delete a vm and return {msg: seccess}, sometimes refresh
          after 5 sec, it might be still there
    '''
    try:
        mongo = cm_mongo()
    except:
        Console.error("There is a problem with the mongo server")
        return False
    if refresh:
        mongo.activate(cm_user_id=username, names=[cloudname])
        mongo.refresh(cm_user_id=username,
                        names=[cloudname],
                        types=['servers'])
    serverdata = mongo.servers(
                        clouds=[cloudname], cm_user_id=username)[cloudname]
    # -------------------------
    # preview and confirm
    confirm_deletion = True
    if preview:
        if server_id_list == []:
            Console.warning("no vm meets the condition")
            return False
        else:    
            resserverdata = {}
            for i in server_id_list:
                resserverdata[i] = serverdata[i]
            cloudobj = CloudManage()
            itemkeys = {"openstack":
                        [
                            ['name', 'name'],
                            ['status', 'status'],
                            ['addresses', 'addresses'],
                            ['id', 'id'],
                            ['flavor', 'flavor', 'id'],
                            ['image', 'image', 'id'],
                            ['user_id', 'cm_user_id'],
                            ['metadata', 'metadata'],
                            ['key_name', 'key_name'],
                            ['created', 'created'],
                            ['cloud', 'cm_cloud']
                        ],
                        "ec2":
                        [
                            ["name", "id"],
                            ["status", "extra", "status"],
                            ["addresses", "public_ips"],
                            ["flavor", "extra", "instance_type"],
                            ['id', 'id'],
                            ['image', 'extra', 'imageId'],
                            ["user_id", 'user_id'],
                            ["metadata", "metadata"],
                            ["key_name", "extra", "key_name"],
                            ["created", "extra", "launch_time"]
                        ],
                        "aws":
                        [
                            ["name", "name"],
                            ["status", "extra", "status"],
                            ["addresses", "public_ips"],
                            ["flavor", "extra", "instance_type"],
                            ['id', 'id'],
                            ['image', 'extra', 'image_id'],
                            ["user_id", "user_id"],
                            ["metadata", "metadata"],
                            ["key_name", "extra", "key_name"],
                            ["created", "extra", "launch_time"]
                        ],
                        "azure":
                        [
                            ['name', 'name'],
                            ['status', 'status'],
                            ['addresses', 'vip'],
                            ['flavor', 'flavor', 'id'],
                            ['id', 'id'],
                            ['image', 'image', 'id'],
                            ['user_id', 'user_id'],
                            ['metadata', 'metadata'],
                            ['key_name', 'key_name'],
                            ['created', 'created'],
                        ]
                        }

            cloudobj.print_cloud_servers(username=username,
                                         cloudname=cloudname,
                                         itemkeys=itemkeys,
                                         refresh=False,
                                         output=False,
                                         serverdata=resserverdata)
            if yn_choice("confirm to delete these vms?", default='n', tries=3):
                pass
            else:
                confirm_deletion = False

    # -------------------------
    # deleting
    if confirm_deletion:
        if server_id_list == []:
            return

        watch = time.time()

        useQueue = False
        if useQueue:
            # not functioning
            cloudmanager = mongo.clouds[username][cloudname]["manager"]
            cm_type = mongo.get_cloud_info(username, cloudname)['cm_type']
            package = "cloudmesh.iaas.%s.queue" % cm_type
            name = "tasks"
            imported = getattr(__import__(package, fromlist=[name]), name)
            queue_name = "%s-%s" % (cm_type, "servers")
            for i in server_id_list:
                tempservername = serverdata[i]['name'].encode("ascii")
                banner(
                    "Deleting vm->{0} on cloud->{1}".format(tempservername, cloudname))
                result = imported.vm_delete.apply_async(
                    (cloudname, i, username), queue=queue_name)
                print("job status:", result.state)
                # print result.traceback  #########
            imported.wait.apply_async(
                args=None, kwargs={'t': 10}, queue=queue_name)
            handleip = imported.release_unused_public_ips.apply_async(
                (cloudname, username), queue=queue_name)
            handlerefresh = imported.refresh.apply_async(args=None,
                                                         kwargs={'cm_user_id': username,
                                                                 'names': [cloudname],
                                                                 'types': ['servers']},
                                                         queue=queue_name)

            # print handleip.state
            # print handleip.traceback
            # print handlerefresh.state
            # print handlerefresh.traceback
            if preview:
                print("to check realtime vm status: list vm --refresh")
        else:
            for i in server_id_list:
                tempservername = serverdata[i]['name'].encode("ascii")
                banner(
                    "Deleting vm->{0} on cloud->{1}".format(tempservername, cloudname))
                result = mongo.vm_delete(cloudname, i, username)
                pprint(result)
            time.sleep(5)
            mongo.release_unused_public_ips(cloudname, username)
            mongo.refresh(username, names=[cloudname], types=['servers'])

        watch = time.time() - watch
        print(("time consumed: %.2f" % watch), "s")


def assign_public_ip(username=None, cloudname=None, serverid=None):

    config = cm_config()
    mongo = cm_mongo()
    mongo.activate(cm_user_id=username)

    mycloud = config.cloud(cloudname)
    if not mycloud.has_key('cm_automatic_ip') or mycloud['cm_automatic_ip'] is False:
        mongo.assign_public_ip(cloudname, serverid, username)
        mongo.refresh(
            names=[cloudname], types=["servers"], cm_user_id=username)
    # else:
    # return "Manual public ip assignment is not allowed for {0}
    # cloud".format(cloud)





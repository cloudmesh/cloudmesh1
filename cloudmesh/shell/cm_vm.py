from __future__ import print_function
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.user.cm_user import cm_user
from cloudmesh_common.util import _getFromDict
from cloudmesh_common.logger import LOGGER
from cloudmesh.shell.cm_cloud import CloudManage
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
from cloudmesh.shell.shellutil import get_vms_look_for
from cloudmesh.shell.shellutil import shell_commands_dict_output
from cloudmesh.shell.shellutil import get_command_list_refresh_default_setting
import json
from cloudmesh_common.util import address_string


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
                          [--prefix=<prefix>|--names=<hostlist>]
                          [--force]
                vm ip assign (NAME|--id=<id>)
                             [--cloud=<CloudName>]
                vm ip show [NAME|--id=<id>]
                           [--group=<group>]
                           [--cloud=<CloudName>]
                           [--prefix=<prefix>|--names=<hostlist>]
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
                        [--group=<group>]
                        [--refresh] 
                        [--format=FORMAT] 
                        [--column=COLUMN] 
                        [--detail]

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
                --detail               for table print format, a brief version 
                                       is used as default, use this flag to print
                                       detailed table
                --flavor=<flavorName>  give the name of the flavor
                --flavorid=<flavorId>  give the id of the flavor
                --group=<group>        give the group name of server
                --id=<id>              give the server id
                --image=<imgName>      give the name of the image
                --imageid=<imgId>      give the id of the image
                --key=<key>            spicfy a private key to use, input a string which
                                       is the full path to the key file
                --ln=<LoginName>       give the login name of the server that you want
                                       to login
                --name=<vmname>        give the name of the virtual machine
                --names=<hostlist>     give the VM name, but in a hostlist style, which is very
                                       convenient when you need a range of VMs e.g. sample[1-3]
                                       => ['sample1', 'sample2', 'sample3']
                                       sample[1-3,18] => ['sample1', 'sample2', 'sample3', 'sample18']
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

                vm delete --group=test --names=sample_[1-9]
                        delete servers on selected or default cloud with search conditions:
                        group name is test and the VM names are among sample_1 ... sample_9

                vm ip show --names=sample_[1-5,9] --format=json
                        show the ips of VM names among sample_1 ... sample_5 and sample_9 in
                        json format

    """


    command_execute = VMcommand(arguments)
    return command_execute.execute()


class VMcommand(object):

    def __init__(self, arguments):
        self.arguments = arguments

        # print self.arguments ########

        try:
            self.config = cm_config()
        except:
            log.error("There is a problem with the configuration yaml files")

        self.username = self.config['cloudmesh']['profile']['username']

    # IMPROVE NAME def _create(self):
    def _vm_create(self):

        """creates a virtual machine through the command shell via the
        arguments passed at initialization time of VMcommand"""

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
        if not cloudname:
            return
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
           self.arguments['--names'] is None:
            print("Please specify at least one option, to get more information: vm help")
            return

        cloudname = self.get_working_cloud_name()
        if not cloudname:
            return

        deleteAllCloudVMs = False
        if (self.arguments['--cloud'] and
            self.arguments['NAME'] is None and
            self.arguments['--id'] is None and
            self.arguments['--group'] is None and
            self.arguments['--prefix'] is None and
            self.arguments['--names'] is None):
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
                                          hostls=self.arguments['--names'],
                                          getAll=deleteAllCloudVMs,
                                          refresh=True)
        if not server_id_list:
            return
        delete_vm(self.username,
                  cloudname,
                  server_id_list=server_id_list,
                  preview=preview,
                  refresh=False)

    def _assign_public_ip(self):
        cloudname = self.get_working_cloud_name()
        if not cloudname:
            return
        serverid = self.get_working_server_id(cloudname)
        if not serverid:
            return
        assign_public_ip(
            username=self.username, cloudname=cloudname, serverid=serverid)

    def _vm_login(self):
        cloudname = self.get_working_cloud_name()
        if not cloudname:
            return
        address = None
        if self.arguments['--addr']:
            address = self.arguments['--addr']
        else:
            serverid = self.get_working_server_id(cloudname)
            if not serverid:
                return
            mongo = cm_mongo()
            serverdata = mongo.servers(clouds=[cloudname],
                                       cm_user_id=self.username)[cloudname]
            serverdata = serverdata[serverid]['addresses']
            temp_val = serverdata.keys()[0]
            serverdata = serverdata[temp_val]
            for i in serverdata:
                if i['OS-EXT-IPS:type'] == "floating":
                    address = i['addr']
            if address is None:
                Console.warning("Please assign a public ip to the VM first"
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
        if not cloudname:
            return
        if get_command_list_refresh_default_setting(self.username) or self.arguments['--refresh']:
            mongo.activate(cm_user_id=self.username, names=[cloudname])
            mongo.refresh(cm_user_id=self.username,
                          names=[cloudname],
                          types=['servers'])

        servers_dict = mongo.servers(
            clouds=[cloudname], cm_user_id=self.username)[cloudname]

        AllCloudVMs = False
        if (self.arguments['--cloud'] and
            self.arguments['NAME'] is None and
            self.arguments['--id'] is None and
            self.arguments['--group'] is None and
            self.arguments['--prefix'] is None and
            self.arguments['--names'] is None):
                AllCloudVMs = True

        server_id_list = get_vms_look_for(self.username,
                                          cloudname,
                                          servername=self.arguments['NAME'],
                                          serverid=self.arguments['--id'],
                                          groupname=self.arguments['--group'],
                                          prefix=self.arguments['--prefix'],
                                          hostls=self.arguments['--names'],
                                          getAll=AllCloudVMs,
                                          refresh=False)
        if not server_id_list:
            return
        if server_id_list == []:
            Console.warning("no vm meets the condition")
            return

        res = {}
        for item in server_id_list:
            temp = servers_dict[item]['addresses']
            temp_val = temp.keys()[0]
            temp = temp[temp_val]
            fixed = ""
            floating = ""
            for item0 in temp:
                if item0['OS-EXT-IPS:type'] == 'fixed':
                    fixed = fixed + item0['addr'] + ", "
                elif item0['OS-EXT-IPS:type'] == 'floating':
                    floating = floating + item0['addr'] + ", "
            if fixed != "":
                fixed = fixed[:-2]
            if floating != "":
                floating = floating[:-2]
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

        shell_commands_dict_output(self.username,
                                   res,
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
            if serverid is None:
                Console.error(
                    "Could not find VM with id {0}".format(self.arguments['--id']))
                return False
        else:
            Console.warning("Please specify a VM name or id")
            return False
        return serverid

    # IMPROVE NAMW def execute():
    def execute(self):
        if 'start' in self.arguments and self.arguments['start']:
            return self._vm_create()
        elif 'delete' in self.arguments and self.arguments['delete']:
            self._vm_delete()
        elif ('ip' in self.arguments and self.arguments['ip'] and
              'assign' in self.arguments and self.arguments['assign']):
            self._assign_public_ip()
        elif 'login' in self.arguments and self.arguments['login']:
            self._vm_login()
        elif 'list' in self.arguments and self.arguments['list']:
            self._vm_list()
        elif ('ip' in self.arguments and self.arguments['ip'] and
              'show' in self.arguments and self.arguments['show']):
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
    # Changed scope of this import - hyungro lee 12/01/2014
    from cloudmesh.experiment.group_usage import add_vm_to_group_while_creating

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
    # refresh server flavor or image
    to_refresh = ["servers"]

    if flavorname is not None or flavorid is not None:
        to_refresh.append("flavors")
    if imagename is not None or imageid is not None:
        to_refresh.append("images")
    if to_refresh != []:
        mongo.refresh(username, names=[cloudname], types=to_refresh)

    # -------------------------
    # get exist VM names list, to prevent names duplicate
    serverdata = mongo.servers(
        clouds=[cloudname],
        cm_user_id=username)[cloudname]
    servers_names_list = []
    for k, v in serverdata.iteritems():
        servers_names_list.append(v['name'])

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
        # do not allow server name duplicate
        if tmpnameser in servers_names_list:
            Console.error("vm name '{0}' exists, please "
                          "use other names or delete it first".format(tmpnameser))
            if not servername:
                userobj.set_default_attribute(username, "index", int(index) + 1)
            count = count - 1
            continue
        # ------------------------
        # vm start procedure

        banner("Starting vm->{0} on cloud->{1} using image->{2}, flavor->{3}, key->{4}"
               .format(tmpnameser, cloudname, tmpnameim, tmpnamefl, keynamenew))

        useQueue = False
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
            if "server" in result and "adminPass" in result["server"]:
                result["server"]["adminPass"] = "******"
            pprint(result)

        # ------------------------
        # add it to the group in database if groupname provided
        if groupname:
            try:
                add_vm_to_group_while_creating(username, groupname, tmpnameser)
            except Exception, err:
                Console.error(str(err))
                return

        # ------------------------
        # increase index if it is used
        if not servername:
            userobj.set_default_attribute(username, "index", int(index) + 1)
        # ------------------------
        servers_names_list.append(tmpnameser)

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
    # changed the scope of this import
    # Benefit: other functions are not affected with this import
    # drawback: hard to see which module is being loaded in this file
    # Hyungro Lee 12/01/2014
    from cloudmesh.experiment.group_usage import remove_vm_from_group_while_deleting

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
                try:
                    remove_vm_from_group_while_deleting(username, tempservername)
                except Exception, err:
                    Console.error(str(err))
                    return
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
                try:
                    remove_vm_from_group_while_deleting(username, tempservername)
                except Exception, err:
                    Console.error(str(err))
                    return
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
    # BUG
    if 'cm_automatic_ip' not in mycloud or not mycloud['cm_automatic_ip']:
        mongo.assign_public_ip(cloudname, serverid, username)
        mongo.refresh(
            names=[cloudname], types=["servers"], cm_user_id=username)
    # else:
    # return "Manual public ip assignment is not allowed for {0}
    # cloud".format(cloud)



# import json
# from cloudmesh.config.cm_config import cm_config
# from cloudmesh_common.util import _getFromDict
# from cloudmesh.shell.shellutil import shell_commands_dict_output

class VMs(object):
    """
    vm api 
    """
    def __init__(self):
        self.config = cm_config()
        self.username = self.config.username()
        self.mongodb = cm_mongo()
        pass
        
    def _helper_vm_cli_printer(self, vms_dict, 
                               print_format=None, 
                               columns=None,
                               refresh=True,
                               detailed=True):
        """
        accept a dict of VMs, change some informtion and get it ready for
        printing such as tables in CLI
        """
        clouds_list = []
        if columns:
            temp_columns = []
        for key, value in vms_dict.iteritems():
            if 'cm_cloud' in value and value['cm_cloud'] not in clouds_list:
                clouds_list.append(value['cm_cloud'])
            if '_id' in value:
                del value['_id']  
        if print_format == "json" and columns == None:
            print(json.dumps(vms_dict, indent=4))
        else:
            res = {}
            headers = []
            # refresh the image and flavor information to get their names
            if refresh:
                self.mongodb.activate(cm_user_id=self.username,
                                      names=clouds_list)
                self.mongodb.refresh(cm_user_id=self.username,
                                     names=clouds_list,
                                     types=['images', 'flavors'])
            images_dict = self.mongodb.images(clouds=clouds_list, 
                                              cm_user_id=self.username)
            flavors_dict = self.mongodb.flavors(clouds=clouds_list, 
                                                cm_user_id=self.username)
            
            for key, value in vms_dict.iteritems():
                res[key] = {}
                cm_type = value['cm_type']
                itemkeys = self._helper_itemkeys(cm_type, detailed=detailed)
                for item in itemkeys:
                    if item[0] not in headers:
                        headers.append(item[0])
                    try:
                        temp = _getFromDict(value, item[1:])
                        # ----------------------------------------
                        # special handlers
                        # ----------------------------------------
                        if item[0] == 'flavor':
                            if temp in flavors_dict[value["cm_cloud"]]:
                                temp = flavors_dict[value["cm_cloud"]][temp]['name']
                            else:
                                temp = "unavailable"

                        elif item[0] == 'image':
                            if temp in images_dict[value["cm_cloud"]]:
                                temp = images_dict[value["cm_cloud"]][temp]['name']
                            else:
                                temp = "unavailable"

                        elif item[0] == 'addresses':
                            temp = address_string(temp)
                        # ----------------------------------------
                        temp_res = temp
                    except:
                        temp_res = None
                    if columns:
                        if item[0] in columns:
                            res[key][item[0]] = temp_res
                            if item[0] not in temp_columns:
                                temp_columns.append(item[0])
                        else:
                            pass
                    else:
                        res[key][item[0]] = temp_res
            if columns:
                columns_to_print = []
                for item in columns:
                    if item in temp_columns:
                        columns_to_print.append(item)
                headers = columns_to_print
            
            shell_commands_dict_output(self.username,
                                       res,
                                       print_format=print_format,
                                       firstheader="name",
                                       header=headers)
                        
                
                
    def _helper_itemkeys(self, cm_type, detailed=True):
        if detailed:
            itemkeys = {"openstack":
                        [
                            #['name', 'name'],
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
                            #["name", "id"],
                            ["status", "extra", "status"],
                            ["addresses", "public_ips"],
                            ['id', 'id'],
                            ["flavor", "extra", "instance_type"],
                            ['image', 'extra', 'imageId'],
                            ["user_id", 'user_id'],
                            ["metadata", "metadata"],
                            ["key_name", "extra", "key_name"],
                            ["created", "extra", "launch_time"]
                        ],
                        "aws":
                        [
                            #["name", "name"],
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
                            #['name', 'name'],
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
        else:
            itemkeys = {"openstack":
                        [
                            #['name', 'name'],
                            ['status', 'status'],
                            ['addresses', 'addresses'],
                            ['flavor', 'flavor', 'id'],
                            ['image', 'image', 'id']
                        ],
                        "ec2":
                        [
                            #["name", "id"],
                            ["status", "extra", "status"],
                            ["addresses", "public_ips"],
                            ["flavor", "extra", "instance_type"],
                            ['image', 'extra', 'imageId']
                        ],
                        "aws":
                        [
                            #["name", "name"],
                            ["status", "extra", "status"],
                            ["addresses", "public_ips"],
                            ["flavor", "extra", "instance_type"],
                            ['image', 'extra', 'image_id']
                        ],
                        "azure":
                        [
                            #['name', 'name'],
                            ['status', 'status'],
                            ['addresses', 'vip'],
                            ['flavor', 'flavor', 'id'],
                            ['image', 'image', 'id']
                        ]
                        }
        if cm_type in itemkeys:
            return itemkeys[cm_type]
        else:
            raise Exception("no itemkeys for cm_type '{0}'".format(cm_type))
            
    
    

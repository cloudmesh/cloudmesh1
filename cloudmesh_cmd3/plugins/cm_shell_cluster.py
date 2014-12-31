from __future__ import print_function
import sys
import os
import time
import json
from sh import cm
from pprint import pprint
from cmd3.console import Console
from cmd3.shell import command
from cloudmesh.shell.cm_vm import VMcommand
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.user.cm_user import cm_user
from cloudmesh.config.cm_config import cm_config
from cloudmesh.config.cm_keys import cm_keys_mongo
from cloudmesh.shell.cm_cloud import CloudManage
from cloudmesh.util.ssh import generate_keypair
from cloudmesh.keys.util import _keyname_sanitation
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.util import get_rand_string
from cloudmesh_install.util import yn_choice
from cloudmesh.shell.shellutil import (shell_commands_dict_output,
        ALLOWED_PRINT_FORMAT)
from cloudmesh.shell.clusters import Clusters
from cloudmesh.shell.cm_vm import VMs

log = LOGGER(__file__)

class cm_shell_cluster:

    def activate_cm_shell_cluster(self):
        self.register_command_topic('cloud', 'cluster')

    @command
    def do_cluster(self, args, arguments):
        """
        ::
        
          Usage:
              cluster list [--format=FORMAT]
              cluster create <name>
                             [--count=<count>]
                             [--ln=<LoginName>]
                             [--cloud=<CloudName>]
                             [--image=<imgName>|--imageid=<imgId>]
                             [--flavor=<flavorName>|--flavorid=<flavorId>]
                             [--force]
              cluster show <name> [--format=FORMAT]
              cluster remove <name> [--grouponly]

          Description:
              Cluster Management
              
              cluster list
                  list the clusters

              cluster create <name> --count=<count> --ln=<LoginName> [options...]
                  Start a cluster of VMs, and each of them can log into all others.
                  CAUTION: you sould do some default setting before using this command:
                  1. select cloud to work on, e.g. cloud select india
                  2. activate the cloud, e.g. cloud on india
                  3. set the default key to start VMs, e.g. key default [NAME]
                  4. set the start name of VMs, which is prefix and index, e.g. label --prefix=test --id=1
                  5. set image of VMs, e.g. default image
                  6. set flavor of VMs, e.g. default flavor
                  Also, it is better to choose a unused group name
              
              cluster show <name> [--format=FORMAT]
                  show the detailed information about the cluster VMs

              cluster remove <name> [--grouponly]
                  remove the cluster and its VMs, if you want to remove the cluster(group name)
                  without removing the VMs, use --grouponly flag
          
          Arguments:
              <name>        cluster name or group name

          Options:
              --count=<count>            give the number of VMs to add into the cluster
              --ln=<LoginName>           give a login name for the VMs, e.g. ubuntu
              --cloud=<CloudName>        give a cloud to work on
              --flavor=<flavorName>      give the name of the flavor
              --flavorid=<flavorId>      give the id of the flavor
              --image=<imgName>          give the name of the image
              --imageid=<imgId>          give the id of the image
              --force                    if a group exists and there are VMs in it, the program will
                                         ask user to proceed or not, use this flag to respond yes as 
                                         default(if there are VMs in the group before creating this 
                                         cluster, the program will include the exist VMs into the cluster)
              --grouponly                remove the group only without removing the VMs, otherwise 
                                         cluster remove command will remove all the VMs of this cluster
              --format=FORMAT            output format: table, json, csv

        """
        #pprint(arguments)
        clusterobj = Clusters()
        userobj = cm_user()
        config = cm_config()
        username = config.username()
        
       
        if arguments['list']:
            try:
                clusters_list = clusterobj.list_clusters()
            except Exception, err:
                Console.error(str(err))
                return
            if arguments['--format']:
                if arguments['--format'] not in ALLOWED_PRINT_FORMAT:
                    Console.error("wrong print format: {0}. (allowed print format: {1})".format(format_type, 
                        ", ".join(ALLOWED_PRINT_FORMAT)))
                    return
                else:
                    p_format = arguments['--format']
            else:
                p_format = None
            shell_commands_dict_output(username,
                                       clusters_list,
                                       print_format=p_format,
                                       firstheader="cluster",
                                       header=[["num of nodes", "num_of_nodes"],
                                               ["num of active nodes", "num_of_active_nodes"]])

        elif arguments['show']:
            try:
                vms_dict = clusterobj.vms(arguments['<name>'])[arguments['<name>']]
            except Exception, err:
                Console.error(str(err))
                return
            if arguments['--format']:
                if arguments['--format'] not in ALLOWED_PRINT_FORMAT:
                    Console.error("wrong print format: {0}. (allowed print format: {1})".format(format_type,
                        ", ".join(ALLOWED_PRINT_FORMAT)))
                    return
                else:
                    p_format = arguments['--format']
            else:
                p_format = None
            
            vmobj = VMs()
            vmobj._helper_vm_cli_printer(vms_dict, print_format=p_format)
                
            


        elif arguments['remove']: 
            try:
                clusterobj.delete(arguments['<name>'], grouponly=arguments['--grouponly'])
            except Exception, err:
                Console.error(str(err))
                return

        elif arguments['create']:
            cloudname = arguments['--cloud'] or CloudManage().get_selected_cloud(username)
            temp_dir_name = ".temp_cluster_create_" + username + "_0"
            while os.path.isdir("./{0}".format(temp_dir_name)):
                temp_dir_name = temp_dir_name[:-1] + str(int(temp_dir_name[-1]) + 1)
            dir_name = temp_dir_name
            
            #NumOfVM = None
            GroupName = None

            vm_login_name = "ubuntu"

            
            temp_key_name = "sshkey_temp"
            _key = ""
            #_key = "-i ./{0}/{1}".format(dir_name, temp_key_name)
            StrictHostKeyChecking = "-o StrictHostKeyChecking=no"
            
            res = None
            to_print = []
            '''
            try:
                NumOfVM = abs(int(argument['--count']))
            except:
                Console.error("<count> must be an integer")
                return
            '''
            GroupName = arguments['<name>']
            
            if arguments['--ln']:
                if arguments['--ln'] == '':
                    Console.error("<LoginName> cannot be empty")
                    return
                else:
                    vm_login_name = arguments['--ln']
            # Moved the import inside of this function
            # If this import goes up to the top, monodb connection will be
            # estabilished. Due to that reason, this import stays here
            # Hyungro Lee 12/01/2014
            from cloudmesh.experiment.group import GroupManagement
            GroupManage = GroupManagement(username)
            groups_list = GroupManage.get_groups_names_list()
            vms_in_group_list = {}
            if GroupName in groups_list:
                vms_in_group_list = GroupManage.list_items_of_group(GroupName, _type="VM")["VM"]

            if not arguments['--force'] and len(vms_in_group_list) != 0:
                if yn_choice("The group you provide exists and it has VMs in it, " + \
                             "do you want to proceed? (if you choose yes, these exist " +\
                             "VMs will be included in the cluster, this could also " +\
                             "rewrite the key on the exist VMs)",
                             default='n',
                             tries=3):
                    pass
                else:
                    return
            
            if GroupName not in groups_list:
                GroupManage.create_group(GroupName)
            GroupManage.add_tag_to_group(GroupName, "cluster")

            # start VMs 
            print ("starting VMs...")
            arguments_temp = arguments
            arguments_temp['start'] = True
            arguments_temp['--name'] = None
            arguments_temp['--group'] = GroupName

            
            vmclass = VMcommand(arguments_temp)
            res = vmclass.call_procedure()
            if res == False: return
        
            def string_to_dict(s):
                h = s.find("{")
                t = s.rfind("}")
                return json.loads(s[h:t+1])
            
            def check_public_ip_existence(d):
                temp = d['addresses']['private']
                for item in temp:
                    if item["OS-EXT-IPS:type"] == "floating":
                        return True
                return False
            
            def get_ip(d, kind="floating"): # kind is either floating or fixed
                temp = d['addresses']['private']
                for item in temp:
                    if item["OS-EXT-IPS:type"] == kind:
                        return item['addr']#.encode('ascii')
                return "FAIL: doesn't exist"
            
            # check all VMs are active
            command_refresh = "vm list --refresh --group={0} --format=json".format(GroupName)
            def _help0(d):
                for k, v in d.iteritems():
                    if v['status'] != 'ACTIVE':
                        return False
                return True
                
            proceed = False
            repeat_index = 1
            while proceed != True:
                if repeat_index > 10:
                    Console.warning("Please check the network")
                    return
                print ("checking({0})...".format(repeat_index))
                time.sleep(5)
                res = str(cm(command_refresh))
                res = string_to_dict(res)
                if _help0(res):
                    proceed = True
                else:
                    repeat_index = repeat_index + 1
                    continue
            
            # assign ip to all VMs
            print ("assigning public ips...")
            for k, v in res.iteritems():
                if not check_public_ip_existence(v):
                    cm("vm ip assign --id={0}".format(k.encode('ascii')))
            
            def _help(d):
                for k, v in d.iteritems():
                    if check_public_ip_existence(v) != True:
                        return False
                return True
            
            # make sure all VMs have been assigned a public ip
            proceed = False
            repeat_index = 1
            while proceed != True:
                if repeat_index > 10:
                    Console.warning("Please check the network")
                    return
                print ("checking({0})...".format(repeat_index))
                time.sleep(5)
                res = str(cm(command_refresh))
                res = string_to_dict(res)
                if _help(res):
                    proceed = True
                else:
                    repeat_index = repeat_index + 1
                    continue
                
            
            # -------------------------
            # key handler
            userinfo = userobj.info(username)
            key = None
            if "key" in userinfo["defaults"]:
                key = userinfo["defaults"]["key"]
            elif len(userinfo["keys"]["keylist"].keys()) > 0:
                key = userinfo["keys"]["keylist"].keys()[0]
                Console.warning("default key is not set, trying to use a key in the database...")
        
            if key:
                keycontent = userinfo["keys"]["keylist"][key]
                if keycontent.startswith('key '):
                    keycontent = keycontent[4:]
                cm_keys_mongo(username).check_register_key(username, cloudname, key, keycontent)
            else:
                Console.error("No sshkey found. Please Upload one")
                return
            # -------------------------
            
            
            # generate ssh keys for VMs and prepare two files: authorized_keys and hosts
            print ("generating ssh keys...")
            os.popen("mkdir {0}".format(dir_name))

            fa = open("./{0}/authorized_keys_temp".format(dir_name), "w")
            fh = open("./{0}/hosts_temp".format(dir_name), "w")
            fk = open("./{0}/{1}".format(dir_name, temp_key_name), "w")
            
            fk.write(keycontent)
            fk.close()
            os.popen("chmod 644 ./{0}/{1}".format(dir_name, temp_key_name))
            
            for k, v in res.iteritems():
                address_floating = get_ip(v)
                address_fixed = get_ip(v, kind="fixed")
                vm_name = v['name']#.encode('ascii')
                to_print.append("{0} {1}, {2}".format(vm_name, address_floating, address_fixed))
                fh.write(address_floating + "  " + vm_name + "\n"
                         + address_fixed + "  " + vm_name + "-i\n")
                os.popen("ssh {2} {3} {0}@{1} \"ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa\""\
                         .format(vm_login_name,address_floating, _key, StrictHostKeyChecking))
                temp = os.popen("ssh {2} {3} {0}@{1} \"cat ~/.ssh/id_rsa.pub\""\
                                .format(vm_login_name, address_floating, _key, StrictHostKeyChecking)).read()
                fa.write(temp)
                
            fa.close()
            fh.close()
            
            # copy the files to VMs
            print ("copying the files...")
            os.popen("mkdir ./{0}/oops".format(dir_name))
            for k, v in res.iteritems():
                address_floating = get_ip(v)
                os.popen("scp {2} {3} {0}@{1}:~/.ssh/authorized_keys ./{4}/"\
                         .format(vm_login_name,address_floating, _key, StrictHostKeyChecking, dir_name))
                os.popen("cat ./{0}/authorized_keys_temp >> ./{0}/authorized_keys"\
                         .format(dir_name))
                os.popen("scp {2} {3} ./{4}/authorized_keys {0}@{1}:~"\
                         .format(vm_login_name,address_floating, _key, StrictHostKeyChecking, dir_name))
                os.popen("ssh {2} {3} {0}@{1} \"sudo mv authorized_keys ~/.ssh/\""\
                         .format(vm_login_name,address_floating, _key, StrictHostKeyChecking))
                os.popen("rm ./{0}/authorized_keys".format(dir_name))
                
                os.popen("cp ./{0}/hosts_temp ./{0}/oops/".format(dir_name))
                os.popen("mv ./{0}/oops/hosts_temp ./{0}/oops/hosts".format(dir_name))
                fh0 = open("./{0}/oops/hosts".format(dir_name), "a")
                os.popen("scp {2} {3} {0}@{1}:/etc/hosts ./{4}/"\
                         .format(vm_login_name,address_floating, _key, StrictHostKeyChecking, dir_name))
                with open("./{0}/hosts".format(dir_name)) as f0:
                    content = f0.readlines()
                for item in content:
                    fh0.write(item + "\n")
                fh0.close()
                os.popen("scp {2} {3} ./{4}/oops/hosts {0}@{1}:~"\
                         .format(vm_login_name,address_floating, _key, StrictHostKeyChecking, dir_name))
                os.popen("ssh {2} {3} {0}@{1} \"sudo mv hosts /etc/\""\
                         .format(vm_login_name,address_floating, _key, StrictHostKeyChecking))
                os.popen("rm ./{0}/oops/hosts".format(dir_name))
            
            
            print ("finishing...")
            os.popen("rm -rf {0}".format(dir_name))
            print ("DONE.")
            
            print ("cluster group: ", GroupName)
            for item in to_print:
                print (item)
            print ("(host name for private ips will have -i at the end of VM name, e.g. testVM -> testVM-i)")


from __future__ import print_function
from cmd3.shell import command
import sys
import os
import time
import json
from cmd3.console import Console
from pprint import pprint
from sh import cm
import sh
from cloudmesh.iaas.cm_vm import VMcommand
from cloudmesh.config.cm_config import cm_config


class cm_shell_cluster:

    def activate_cm_shell_cluster(self):

        self.register_command_topic('cloud', 'cluster')

    @command
    def do_cluster(self, args, arguments):
        """
        Usage:
            cluster create --count=<count>
                           --group=<group>
                           --ln=<LoginName>
                           [--cloud=<CloudName>]
                           [--image=<imgName>|--imageid=<imgId>]
                           [--flavor=<flavorName>|--flavorid=<flavorId>]
                                    
        Description:
            Cluster Management
            
            cluster create --count=<count> --cluster=<ClusterName> --login=<LoginName> [options...]
            --count=<count>            specify amount of VMs in the cluster
            --group=<group>            specify a group name of the cluster, make sure it's unique
            --ln=<LoginName>           login name for VMs, e.g. ubuntu
                Start a cluster of VMs, and each of them can log into all others.
                CAUTION: you sould do some default setting before using this command:
                1. select cloud to work on, e.g. cloud select india
                2. activate the cloud, e.g. cloud on india
                3. set the default key to start VMs, e.g. key default [NAME]
                4. set the start name of VMs, which is prefix and index, e.g. label --prefix=test --id=1
                5. set image of VMs, e.g. default image
                6. set flavor of VMs, e.g. default flavor
                Also, please make sure the group name of the cluster is unique
                
        Options:
            --cloud=<CloudName>        give a cloud to work on
            --flavor=<flavorName>      give the name of the flavor
            --flavorid=<flavorId>      give the id of the flavor
            --image=<imgName>          give the name of the image
            --imageid=<imgId>          give the id of the image


        """
        #pprint(arguments)
        
        # -----------------------------
        # TODO::
        # key management
        # -----------------------------
        
        if arguments['create']:
            try:
                config = cm_config()
            except:
                Console.error("There is a problem with the configuration yaml files")
                return
            username = config['cloudmesh']['profile']['username']
            dir_name = "temp_" + username
            
            #NumOfVM = None
            GroupName = None
            vm_login_name = None
            _key = ''
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
            if arguments['--group'] == '':
                Console.error("<group> cannot be empty")
                return
            else:
                GroupName = arguments['--group']
            if arguments['--ln'] == '':
                Console.error("<LoginName> cannot be empty")
                return
            else:
                vm_login_name = arguments['--ln']
            
            # start VMs 
            print ("starting VMs...")
            arguments_temp = arguments
            arguments_temp['start'] = True
            arguments_temp['--name'] = None
            
            vmclass = VMcommand(arguments_temp)
            res = vmclass.call_procedure()
            if res == False: return
        
            def string_to_dict(s):
                h = s.find("{")
                t = s.rfind("}")
                return json.loads(s[h:t+1])
            
            # check all VMs are active
            command_refresh = "vm list --refresh --group={0} --format=json".format(GroupName)
            proceed = False
            repeat_index = 1
            while proceed != True:
                if repeat_index > 5:
                    Console.warning("Please check the network")
                    return
                print ("checking({0})...".format(repeat_index))
                time.sleep(5)
                res = str(cm(command_refresh))
                res = string_to_dict(res)
                for k, v in res.iteritems():
                    if v['status'] != 'ACTIVE':
                        repeat_index = repeat_index + 1
                        continue
                proceed = True
            
            # assign ip to all VMs
            print ("assigning public ips...")
            for item in res.keys():
                cm("vm ip --id={0}".format(item.encode('ascii')))
                
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
            
            # make sure all VMs have been assigned a public ip
            proceed = False
            repeat_index = 1
            while proceed != True:
                if repeat_index > 5:
                    Console.warning("Please check the network")
                    return
                print ("checking({0})...".format(repeat_index))
                time.sleep(5)
                res = str(cm(command_refresh))
                res = string_to_dict(res)
                for k, v in res.iteritems():
                    if check_public_ip_existence(v) != True:
                        repeat_index = repeat_index + 1
                        continue
                proceed = True
            
            # generate ssh keys for VMs and prepare two files: authorized_keys and hosts
            print ("generating ssh keys...")
            sh.mkdir("{0}".format(dir_name))
            fa = open("./{0}/authorized_keys_temp".format(dir_name), "w")
            fh = open("./{0}/hosts_temp".format(dir_name), "w")
            
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
            sh.mkdir("./{0}/oops".format(dir_name))
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
                os.popen("rm ./{0}/oops/authorized_keys".format(dir_name))
                
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
            os.popen("rm -r {0}".format(dir_name))
            print ("DONE.")
            
            print ("cluster group: ", GroupName)
            for item in to_print:
                print (item)
            print ("(host name for private ips will have -i at the end of VM name, e.g. testVM -> testVM-i)")



            
        
        
        #if arguments['delete']:
            #print(cm("help"))

            


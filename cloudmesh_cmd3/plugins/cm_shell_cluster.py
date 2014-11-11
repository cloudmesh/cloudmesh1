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
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from cloudmesh.config.cm_keys import cm_keys_mongo
from cloudmesh.user.cm_user import cm_user
from cloudmesh.iaas.cm_cloud import CloudManage
from cloudmesh.util.ssh import generate_keypair
from cloudmesh.keys.util import _keyname_sanitation
from cloudmesh_common.util import get_rand_string
from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_cluster:

    _id = "t_stacks"

    def activate_cm_shell_cluster(self):

        self.register_command_topic('cloud', 'cluster')
        self.cm_config = cm_config()
        self.cm_mongo = cm_mongo()
        self.user = cm_user()

    @command
    def do_cluster(self, args, arguments):
        """
        Usage:
            cluster start CLUSTER_NAME
            cluster list
            cluster login CLUSTER_NAME
            cluster stop CLUSTER_NAME
            cluster create --count=<count>
                           --group=<group>
                           [--ln=<LoginName>]
                           [--cloud=<CloudName>]
                           [--image=<imgName>|--imageid=<imgId>]
                           [--flavor=<flavorName>|--flavorid=<flavorId>]
                                    
        Description:
            Cluster Management
            
            cluster create --count=<count> --group=<group> --ln=<LoginName> [options...]
            <count>            specify amount of VMs in the cluster
            <group>            specify a group name of the cluster, make sure it's unique
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
            --ln=<LoginName>           give a login name for the VMs, e.g. ubuntu
            --cloud=<CloudName>        give a cloud to work on
            --flavor=<flavorName>      give the name of the flavor
            --flavorid=<flavorId>      give the id of the flavor
            --image=<imgName>          give the name of the image
            --imageid=<imgId>          give the id of the image


        """
        #pprint(arguments)
        
        # -----------------------------
        # TODO::
        # add VMs to cluster
        # -----------------------------
       
        if arguments['start'] and arguments['CLUSTER_NAME']:
            '''Starts a cluster'''

            # Initialize default variables. e.g. userid, default cloud and
            # default keypair
            userid = self.cm_config.username()
            def_cloud = self.get_cloud_name(userid)
            self.cm_mongo.activate(userid)
            
            userinfo = self.user.info(userid)
            if "key" in userinfo["defaults"]:
                key = userinfo["defaults"]["key"]
            elif len(userinfo["keys"]["keylist"].keys()) > 0:
                key = userinfo["keys"]["keylist"].keys()[0]
        
            if key:
                keycontent = userinfo["keys"]["keylist"][key]
                if keycontent.startswith('key '):
                    keycontent = keycontent[4:]
                cm_keys_mongo(userid).check_register_key(userid, def_cloud, key, keycontent)
                keynamenew = _keyname_sanitation(userid, key)
            else:
                Console.warning("No sshkey found. Please Upload one")
                return
            
            clustername = arguments['CLUSTER_NAME']
            s_name = "cluster-{0}-{1}-{2}".format(userid, clustername, get_rand_string())
            # TEMP FOR HADOOP CLUSTER
            if clustername != "hadoop":
                Console.warning('hadoop is only available cluster')
                return
            
            # 1. keypair for the communication between master and worker nodes
            privatekey, publickey = generate_keypair()
            t_url = \
            "https://raw.githubusercontent.com/cloudmesh/cloudmesh/dev1.3/heat-templates/ubuntu-14.04/hadoop-cluster/hadoop-cluster.yaml"
            param = {'KeyName': keynamenew,
                     'PublicKeyString': publickey,
                     'PrivateKeyString': privatekey}
            log.debug(def_cloud, userid, s_name, t_url, param, publickey,
                      privatekey)
            res = self.cm_mongo.stack_create(cloud=def_cloud, cm_user_id=userid,
                                             servername=s_name,
                                             template_url=t_url,
                                             parameters=param)
            log.debug(res)
            if 'error' in res:
                print (res['error']['message'])
            return res

        elif arguments['list']:
            userid = self.cm_config.username()
            self.cm_mongo.activate(userid)
            self.cm_mongo.refresh(cm_user_id=userid, types=[self._id])
            stacks = self.cm_mongo.stacks(cm_user_id=userid)
            launchers = self.filter_launcher(
                stacks,
                {"search": "contain",
                 "key": "stack_name",
                 "value": "launcher"}
                )
            log.debug(launchers)

            d = {}
            for k0, v0 in launchers.iteritems():
                for k1, v1 in launchers[k0].iteritems():
                    d[v1['id']] = v1
            columns = ['stack_name', 'description', 'stack_status',
                       'creation_time', 'cm_cloud']
            if arguments['--column'] and arguments['--column'] != "all":
                columns = [x.strip() for x in arguments['--column'].split(',')]

            if arguments['--format']:
                if arguments['--format'] not in ['table', 'json', 'csv']:
                    Console.error("please select printing format among table, json and csv")
                    return
                else:
                    p_format = arguments['--format']
            else:
                p_format = None

            shell_commands_dict_output(d,
                                       print_format=p_format,
                                       firstheader="launcher_id",
                                       header=columns
                                       # vertical_table=True
                                       )

        elif arguments['login']:
            Console.error("Not implemented")
            return

        elif arguments['stop'] and arguments['CLUSTER_NAME']:
            userid = self.cm_config.username()
            def_cloud = self.get_cloud_name(userid)
            c_id = arguments['CLUSTER_NAME']
            self.cm_mongo.activate(userid)
            res = self.cm_mongo.stack_delete(cloud=def_cloud,
                                             cm_user_id=userid,
                                             server=c_id)
            log.debug(res)
            return res

        elif arguments['create']:
            try:
                config = cm_config()
            except:
                Console.error("There is a problem with the configuration yaml files")
                return
            username = config['cloudmesh']['profile']['username']
            cloudname = arguments['--cloud'] or CloudManage().get_selected_cloud(username)
            dir_name = ".temp_cluster_create_" + username
            
            #NumOfVM = None
            GroupName = None

            vm_login_name = "ubuntu"

            
            temp_key_name = "sshkey_temp"
            _key = "-i ./{0}/{1}".format(dir_name, temp_key_name)
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
            
            if arguments['--ln']:
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
            
            def _help(d):
                for k, v in d.iteritems():
                    if check_public_ip_existence(v) != True:
                        return False
                return True
            
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
                if _help(res):
                    proceed = True
                else:
                    repeat_index = repeat_index + 1
                    continue
                
            
            # -------------------------
            # key handler
            userinfo = cm_user().info(username)
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
            os.popen("rm -r {0}".format(dir_name))
            print ("DONE.")
            
            print ("cluster group: ", GroupName)
            for item in to_print:
                print (item)
            print ("(host name for private ips will have -i at the end of VM name, e.g. testVM -> testVM-i)")



            
        
        
        #if arguments['delete']:
            #print(cm("help"))

            


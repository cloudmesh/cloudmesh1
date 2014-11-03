from __future__ import print_function
from cmd3.shell import command
import sys
import os
import time
import json
from cmd3.console import Console
from pprint import pprint
from sh import cm
from cloudmesh.iaas.cm_vm import shell_command_vm


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
            cluster delete
        """
        pprint(arguments)
        
        if arguments['create']:
            pass
            
            NumOfVM = None
            GroupName = None
            vm_login_name = None
            '''
            try:
                NumOfVM = abs(int(argument['--count']))
            except:
                Console.error("<count> must be an integer")
                return
            '''
            if arguments['--group'] == '':
                Console("<group> cannot be empty")
                return
            else:
                GroupName = arguments['--group']
            if arguments['--ln'] == '':
                Console("<LoginName> cannot be empty")
                return
            else:
                vm_login_name = arguments['--ln']
            
            # start VMs 
            print ("starting VMs...")
            arguments_temp = arguments
            arguments_temp['start'] = True
            arguments_temp['--name'] = None
            try:
                shell_command_vm(arguments_temp)
            except:
                return
            
            print ("!!!!!!!!!!!!!!!!!!!!!")
            return
            
            def string_to_dict(s):
                h = s.find("{")
                t = s.rfind("}")
                return json.loads(s[h:t+1])
            
            command_refresh = "vm list --refresh --group={0} --format=json".format(GroupName)
            proceed = False
            repeat_times = 5
            while proceed != True:
                print ("checking...")
                time.sleep(5)
                res = os.popen(command_refresh).read()
                res = string_to_dict(res)
                for k, v in res.iteritems():
                    if v['status'] != 'ACTIVE':
                        continue
                proceed = True

            
        
        
        if arguments['delete']:
            print(cm("help"))

            


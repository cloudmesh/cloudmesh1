#!/usr/bin/env python
from docopt import docopt
import sys

from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from cloudmesh.user.cm_user import cm_user
from prettytable import PrettyTable

from cloudmesh_common.logger import LOGGER
from tabulate import tabulate

import threading

log = LOGGER(__file__)

def shell_command_vm(arguments):
    '''
    Usage:
      vm create [--count=<count>]
                [--image=<imgName>]
                [--flavor=<FlavorId>]
                [--cloud=<CloudName>]
                [--label=<LABEL>]
      vm delete <NAME>
                [--label=<LABEL>]
                [--cloud=<CloudName>]
      vm info [--verbose | --json] [--name=<NAME>]
      vm list [--verbose | --json] [--cloud=<CloudName>]

    Description:
       vm command provides procedures to manage VM instances of selected IaaS. 
 
    Arguments:
      NAME name of the VM

    Options:
       -v --verbose                         verbose mode
       -j --json                            json output
       -x <count> --count=<count>           number of VMs
       -n <NAME> --name=<NAME>              Name of the VM
       -c <CloudName> --cloud=<CloudName>   Name of the Cloud
       --img=<imgName>                      Name of the image for VM
       -f <FlavorId> --flavor=<FlavorId>    Flavor Id for VM
    
    Examples:
        $ vm create --cloud=sierra
        --image=futuregrid/ubuntu-14.04
    '''
    vm = ManageVM(arguments)
    vm.call_procedure()

class ManageVM(object):
    config = cm_config()
    clouds = cm_mongo()
    user = cm_user()
    key = None

    def __init__(self, args):
        #log.info(args)
        self.set_args(args)
        self.parse_args()
        self.username = self.config.username()
        self.clouds.activate(cm_user_id=self.username)
        self.userinfo = self.user.info(self.username)
        self.set_attributes()

    def set_args(self, args):
        self.args = args

    def parse_args(self):
        self.cloud = self.args['--cloud']
        self.flavor = self.args['--flavor']
        self.image = self.args['--image']
        self.server = self.args['--name'] or self.args['<NAME>']
        self.server_label = self.args['--label']

    def set_attributes(self):
        self.attributes = {"openstack":
                      [
                          ['name','name'],
                          ['status','status'],
                          ['addresses','addresses'],
                          ['flavor', 'flavor','id'],
                          ['id','id'],
                          ['image','image','id'],
                          ['user_id', 'user_id'],
                          ['metadata','metadata'],
                          ['key_name','key_name'],
                          ['created','created'],
                      ],
                      "ec2":
                      [
                          ["name", "id"],
                          ["status", "extra", "status"],
                          ["addresses", "public_ips"],
                          ["flavor", "extra", "instance_type"],
                          ['id','id'],
                          ['image','extra', 'imageId'],
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
                          ['id','id'],
                          ['image','extra', 'image_id'],
                          ["user_id","user_id"],
                          ["metadata", "metadata"],
                          ["key_name", "extra", "key_name"],
                          ["created", "extra", "launch_time"]
                      ],
                      "azure":
                      [
                          ['name','name'],
                          ['status','status'],
                          ['addresses','vip'],
                          ['flavor', 'flavor','id'],
                          ['id','id'],
                          ['image','image','id'],
                          ['user_id', 'user_id'],
                          ['metadata','metadata'],
                          ['key_name','key_name'],
                          ['created','created'],
                      ]
                     }

    def _vm_create(self):
        '''Create a vm instance of IaaS using cm_mongo class.
        vm_create() procedure of cm_mongo object launches new instance.

        Note. Most parts of codes are identical with start_vm() in cloudmesh_web/modules/cloud.py
        '''
        # Preparing required parameters of the vm_create() function
        cloud = self.cloud
        error = ''
        key = None
        vm_image = None
        vm_flavor_id = None
        userinfo = self.userinfo
        username = userinfo["cm_user_id"]

        try:
            vm_flavor_id = self.flavor \
                    or userinfo["defaults"]["flavors"][cloud]
        except:
            error = error + "Please specify a default flavor."
        if vm_flavor_id in [None, 'none']:        
            error = error + "Please specify a default flavor."

        try:
            vm_image = self.image \
                    or userinfo["defaults"]["images"][cloud]
        except:
            error = error + "Please specify a default image."
        if vm_image in [None, 'none']:
            error = error + "Please specify a default image."

        if "key" in userinfo["defaults"]:
            key = userinfo["defaults"]["key"]
        elif len(userinfo["keys"]["keylist"].keys()) > 0:
            key = userinfo["keys"]["keylist"].keys()[0]


        if key:
              keycontent = userinfo["keys"]["keylist"][key]
              if keycontent.startswith('key '):
                  keycontent = keycontent[4:]
              #check_register_key(cloud, key, keycontent)
              keynamenew = self._keyname_sanitation(username, key)
        else:
            error = error + "No sshkey found. Please <a \
            href='https://portal.futuregrid.org/my/ssh-keys'>Upload one</a>"

        metadata = {'cm_owner': username}
        prefix = userinfo["defaults"]["prefix"]
        index = userinfo["defaults"]["index"]

        log.info("STARTING {0} {1}".format(prefix, index))
        log.debug("Starting vm using image->%s, flavor->%s, key->%s" % (vm_image,
                                                                        vm_flavor_id,
                                                                        keynamenew))

        if self.server_label:
            prefix = "%s_%s" % (self.server_label , prefix)

        result = self.clouds.vm_create(cloud, prefix, index, vm_flavor_id, vm_image, keynamenew,
                                  meta=metadata, cm_user_id=username)
        try:
            result['server']['adminPass'] = "*******"
        except:
            pass
        log.info("{0}".format(result))

        # Upon success of launching vm instance, an index of vm instance is increased.
        userstore = cm_user()
        userstore.set_default_attribute(username, "index", int(index) + 1)

        t = threading.Thread(target=self.clouds.refresh,
                             kwargs={'cm_user_id':username, 'names':[cloud], \
                                    'types':['servers']})
        t.start()

    def _vm_delete(self):
        cloud = self.cloud
        server = self.server
        userid = self.userinfo['cm_user_id']
        if not self.server_label:
            self.clouds.vm_delete(cloud, server, userid)
        else:
            label = self.server_label
            userid = self.userinfo['cm_user_id']
            data = self.clouds.servers(cm_user_id=userid)
            result = self._select_servers(data, self.attributes)
            servers = []
            for instance in result:
                try:
                    # if instance['name'].startswith(label):
                    if instance[0].startswith(label):
                        # servers.append(instance['id'])
                        # servers.append(instance[4])
                        server = instance[4]
                        self.clouds.vm_delete(cloud, server, userid)
                except:
                    pass
        
        t = threading.Thread(target=self.clouds.refresh,
                             kwargs={'cm_user_id':userid, 'names':[cloud], \
                                    'types':['servers']})
        t.start()

    def _vm_info(self):
        print sys._getframe().f_code.co_name

    def _vm_list(self):

        attributes = self.attributes

        userid = self.userinfo['cm_user_id']
        if self.cloud:
            cloud = self.cloud
        else:
            cloud = None
        data = self.clouds.servers(cm_user_id=userid, clouds=cloud)
        result = self._select_servers(data, attributes)
        _display(result)

    def _keyname_sanitation(self, username, keyname):
        keynamenew = "%s_%s" % (username, keyname.replace('.', '_').replace('@',
                                                                            '_'))
        return keynamenew

    def call_procedure(self):
        cmds = self.get_commands()
        for cmd, tof in cmds.iteritems():
            if tof:
                func = getattr(self, "_vm_" + cmd)
                func()
                break

    def get_commands(self):
        '''Return commands only except options start with '--' from docopt
        arguments
        
        Example:
            get_commands({"info": True, "--count":None})
            returns
            {"info": True} 
        '''
        args = self.args
        result = {}
        for k,v in args.iteritems():
            if k.startswith('--'):
                continue
            result[k] = v
        return result


    def _select_servers(self, data, selected_keys): 
        servers = []
        for cm_cloud, _id in data.iteritems():
            for server_name, v in _id.iteritems():
                values = []
                # cm_type is required to use a selected_keys for the cm_type
                cm_type = v['cm_type']
                keys = []
                for k in selected_keys[cm_type]:
                    keys.append(k[0])
                    try:
                        values.append(str(_getFromDict(v, k[1:])))
                    except:
                        #print sys.exc_info()
                        values.append('0')
                servers.append(values)
        headers = [keys]
        return headers + servers

def _getFromDict(dataDict, mapList):
    '''Get values of dataDict by mapList
    mapList is a list of keys to find values in dict.
    dataDict is a nested dict and will be searched by the list.

    e.g.  Access to the value 5 in dataDict

    dataDict = { "abc": {
                    "def": 5 
                    } 
                }
    mapList = [ "abc", "def" ]

    _getFromDict(dataDict, mapList) returns 5

    ref: http://stackoverflow.com/questions/14692690/access-python-nested-dictionary-items-via-a-list-of-keys
    '''
    return reduce(lambda d, k: d[k], mapList, dataDict)

def _display(json_data, headers="firstrow", tablefmt="orgtbl"):
    table = tabulate(json_data, headers, tablefmt)
    try:
        separator = table.split("\n")[1].replace("|", "+")
    except:
        separator = "-" * 50
    print separator
    print table
    print separator

def main():
    arguments = docopt(shell_command_vm.__doc__)
    shell_command_vm(arguments)
        
if __name__ == "__main__":
    #print sys.argv
    main()

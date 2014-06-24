#!/usr/bin/env python
from docopt import docopt
import sys

from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from prettytable import PrettyTable

from cloudmesh_common.logger import LOGGER
from tabulate import tabulate

log = LOGGER(__file__)

def shell_command_vm(arguments):
    '''
    Usage:
      vm create [--count=<count>]
                [--image=<imgName>]
                [--flavor=<FlavorId>]
                [--cloud=<CloudName>]
      vm delete [[--count=<count>] | [--name=<NAME>]]
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
        $ vm create --cloud=sierra_openstack_grizzly
        --image=futuregrid/ubuntu-14.04
    '''

    #log.info(arguments)

    call_function(arguments)

def _vm_create(arguments):
    print sys._getframe().f_code.co_name

def _vm_delete(arguments):
    print sys._getframe().f_code.co_name

def _vm_info(arguments):
    print sys._getframe().f_code.co_name

def _vm_list(arguments):
    print sys._getframe().f_code.co_name


def call_function(arguments):
    cmds = get_commands(arguments)
    for cmd, tof in cmds.iteritems():
        if tof:
            func = globals()["_vm_"+cmd]
            func(arguments)
            break

def get_commands(args):
    '''Return commands only except options start with '--' from docopt
    arguments
    
    Example:
        get_commands({"info": True, "--count":None})
        returns
        {"info": True} 
    '''
    result = {}
    for k,v in args.iteritems():
        if k.startswith('--'):
            continue
        result[k] = v
    return result

def main():
    arguments = docopt(shell_command_vm.__doc__)
    shell_command_vm(arguments)
        
if __name__ == "__main__":
    #print sys.argv
    main()

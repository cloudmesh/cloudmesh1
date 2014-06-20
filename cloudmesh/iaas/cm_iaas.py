#!/usr/bin/env python
import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
import cloudmesh
from pprint import pprint

from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from prettytable import PrettyTable

from cloudmesh_common.logger import LOGGER
from tabulate import tabulate

log = LOGGER(__file__)

def shell_command_flavor(arguments):
    """
    Usage:
	flavor -h | --help
        flavor --version
        flavor [cloud_label]

   Options:
       -h                   help message
 
    Arguments:
        cloud_label         Name of the IaaS cloud e.g. india_openstack_grizzly.
    
    Description:
       flavor command provides list of available flavors. Flavor describes
       virtual hardware configurations such as size of memory, disk, cpu cores.

    Result:

    Examples:
        $ flavor india_openstack_grizzly
        
    """

    #log.info(arguments)
    config = cm_config()
    username = config.username()
    c = cm_mongo()
    c.activate(cm_user_id=username)
    flavors =c.flavors(cm_user_id=username)

    your_keys = [
                             'id',
                             'name',
                             'vcpus',
                             'ram',
                             'disk',
                             'cm_refresh',
                             ]

    _display(flavors)
    
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
    arguments = docopt(shell_command_flavor.__doc__)
    shell_command_flavor(arguments)
        
if __name__ == "__main__":
    #print sys.argv
    main()

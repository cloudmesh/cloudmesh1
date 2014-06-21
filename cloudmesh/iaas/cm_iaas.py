#!/usr/bin/env python
from docopt import docopt
import sys

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
        flavor <cm_cloud>...

   Options:
       -h                   help message
 
    Arguments:
        cm_cloud    Name of the IaaS cloud e.g. india_openstack_grizzly.
    
    Description:
       flavor command provides list of available flavors. Flavor describes
       virtual hardware configurations such as size of memory, disk, cpu cores.

    Result:

    Examples:
        $ flavor india_openstack_grizzly
        
    """

    #log.info(arguments)
    clouds_name = arguments['<cm_cloud>']
    config = cm_config()
    username = config.username()
    c = cm_mongo()
    c.activate(cm_user_id=username)
    flavors_dict = c.flavors(cm_user_id=username, clouds=clouds_name)

    your_keys = [
        'id',
        'name',
        'vcpus',
        'ram',
        'disk',
        'cm_refresh',
    ]

    flavors = _select_elements(flavors_dict, your_keys)

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

def _select_elements(data, selected_keys, env=[]):
    '''
    {"india_openstack_havana": {"1": 
        {"cm_cloud_type": "openstack", 
        "disk": 0,
        "name": "m1.tiny", 
        "links": [{"href":
            "http://149.165.146.57:8774/v1.1/8bc7e259464944b3bf4d8b050d1ab935/flavors/1",
            "rel": "self"}, {"href": "http://149.165.146.57
            :8774/8bc7e259464944b3bf4d8b050d1ab935/flavors/1", "rel": "bookmark"}],
        "ram": 512, 
        "cm_type_version": "havana", 
        "id": "1",
        "OS-FLV-DISABLED:disabled": false, 
        "cm_id": "india_openstack_havana-flavors-m1-tiny", 
        "vcpus": 1, 
        "cm_refresh": "2014-06-14T17-21-25Z", 
        "swap": "", 
        "os-flavor-access:is_public": true, 
        "rxtx_factor": 1.0, 
        "cm_kind": "flavors"}}}
    '''
    headers = ["cm_cloud"] + selected_keys
    flavors = [headers]
    for cm_cloud, _id in data.iteritems():
        for flavor_name, v in _id.iteritems():
            values = [cm_cloud]
            for k in selected_keys:
                try:
                    values.append(v[k])
                except:
                    values.append(0)
            flavors.append(values)
    return flavors

def main():
    arguments = docopt(shell_command_flavor.__doc__)
    shell_command_flavor(arguments)
        
if __name__ == "__main__":
    #print sys.argv
    main()

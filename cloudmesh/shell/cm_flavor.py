#!/usr/bin/env python
from __future__ import print_function
from docopt import docopt

from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from cloudmesh_common.logger import LOGGER
from tabulate import tabulate

log = LOGGER(__file__)


def shell_command_flavor(arguments):
    """
    ::

      Usage:
          flavor
          flavor CLOUD... [--refresh]
          flavor -h | --help
          flavor --version

     Options:
         -h                   help message
         --refresh            refresh flavors of IaaS

      Arguments:
          CLOUD    Name of the IaaS cloud e.g. india_openstack_grizzly.

      Description:
         flavor command provides list of available flavors. Flavor describes
         virtual hardware configurations such as size of memory, disk, cpu cores.

      Result:

      Examples:
          $ flavor india_openstack_grizzly

    """

    # log.info(arguments)
    cloud_names = arguments['CLOUD']
    # clouds in c.flavors treats None value as a ALL clouds
    if not cloud_names:
        cloud_names = None
    config = cm_config()
    username = config.username()
    c = cm_mongo()
    c.activate(cm_user_id=username)
    if arguments['--refresh']:
        c.refresh(cm_user_id=username, names=cloud_names, types=['flavors'])
    flavors_dict = c.flavors(cm_user_id=username, clouds=cloud_names)

    your_keys = [
        'id',
        'name',
        'vcpus',
        'ram',
        'disk',
        'cm_refresh',
    ]

    flavors = _select_flavors(flavors_dict, your_keys)

    _display(flavors)


def _display(json_data, headers="firstrow", tablefmt="orgtbl"):
    table = tabulate(json_data, headers, tablefmt)
    try:
        separator = table.split("\n")[1].replace("|", "+")
    except:
        separator = "-" * 50
    print(separator)
    print(table)
    print(separator)


def _select_flavors(data, selected_keys, env=[]):
    '''
    {"india": {"1":
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
        "cm_id": "india-flavors-m1-tiny",
        "vcpus": 1,
        "cm_refresh": "2014-06-14T17-21-25Z",
        "swap": "",
        "os-flavor-access:is_public": true,
        "rxtx_factor": 1.0,
        "cm_kind": "flavors"}}}
    '''
    headers = ["CLOUD"] + selected_keys
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
    # print sys.argv
    main()

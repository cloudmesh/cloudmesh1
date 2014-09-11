#!/usr/bin/env python
from docopt import docopt
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from cloudmesh_common.logger import LOGGER
from tabulate import tabulate

log = LOGGER(__file__)


def shell_command_security_group(arguments):
    """
    Usage:
        security_group list <cm_cloud>...
        security_group add <cm_cloud> <label> <parameters>  [NOT IMPLEMENTED]
        security_group delete <cm_cloud> <label>            [NOT IMPLEMENTED]
    security_group -h | --help
        security_group --version

   Options:
       -h                   help message

    Arguments:
        cm_cloud    Name of the IaaS cloud e.g. india_openstack_grizzly.

    Description:
       security_group command provides list of available security_groups.

    Result:

    Examples:
        $ security_group list india_openstack_grizzly

    """

    # log.info(arguments)

    cloud_names = arguments['<cm_cloud>']
    # None value means ALL clouds in c.security_groups() function
    if not cloud_names:
        cloud_names = None
    config = cm_config()
    username = config.username()
    c = cm_mongo()
    c.activate(cm_user_id=username)
    security_groups_dict = c.security_groups(
        cm_user_id=username, clouds=cloud_names)
    your_keys = {"openstack":
                 [
                     ['id', 'id'],
                     ['name', 'name'],
                     ['description', 'description'],
                     ['cm_refresh', 'cm_refresh']
                 ],
                 "ec2": [],
                 "azure": [],
                 "aws": []
                 }

    security_groups = _select_security_groups(security_groups_dict, your_keys)
    _display(security_groups)


def _select_security_groups(data, selected_keys, env=[]):

    security_groups = []
    keys = []

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

    for cm_cloud, _id in data.iteritems():
        for security_group_name, v in _id.iteritems():
            values = [cm_cloud]
            # cm_type is required to use a selected_keys for the cm_type
            cm_type = v['cm_type']
            keys = []
            for k in selected_keys[cm_type]:
                keys.append(k[0])
                try:
                    values.append(_getFromDict(v, k[1:]))
                except:
                    # print sys.exc_info()
                    values.append(0)
            security_groups.append(values)
    headers = [keys]
    return headers + security_groups


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
    arguments = docopt(shell_command_security_group.__doc__)
    shell_command_security_group(arguments)

if __name__ == "__main__":
    # print sys.argv
    main()

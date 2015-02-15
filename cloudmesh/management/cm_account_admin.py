#!/usr/bin/env python

from docopt import docopt
from cloudmesh.management.cloudmeshobject import CloudmeshObject
from cloudmesh.management.generate_classes import project_fields, user_fields
from cloudmesh.management.generate import generate_users
from cloudmesh.management.user import User, Users
import cloudmesh
import sys


def generate():
    fields = user_fields()
    fields_dict = {}
    for item in fields.split("\n"):
        # print item
        key, value = item.split(" = ")
        key = key.lstrip("\t")
        fields_dict[key] = value
    print fields_dict
    user_class = type('User','CloudmeshObject',fields_dict)
    print repr(user_class)
    pass


def main():
    management_command(sys.argv)


def management_command(args):
    """cm-management.

    Usage:
        cm-management user generate [--count=N]
        cm-management user clear
        cm-management user delete
        cm-management user list
        cm-management project generate
        cm-management version

    Options:
        -h --help Show this screen
        --version Show version
    """

    arguments = docopt(management_command.__doc__, args[1:])
    print arguments

    try:
        if arguments['version']:
            print cloudmesh.__version__
        elif arguments['user'] and arguments['list']:
            user = User()
            user.list_users()
        elif arguments['user'] and arguments['generate']:
            if arguments['--count']:
                count = int(arguments['--count'])
                generate_users(count)
            else:
                generate_users(10)
        elif arguments['user'] and arguments['clear']:
            user = Users()
            user.clear()
        elif arguments['project']:
            print "Dummy Projects"
            project_fields()
        elif arguments['list']:
            print "Listing Users"
    except:
        print "Invalid arguments Exception"


if __name__ == '__main__':
    management_command(sys.argv)
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
    """cm-management - Command line option to manage users and projects

    Usage:
        cm-management user generate [--count=N]
        cm-management user list [USERNAME] [--format=FORMAT]
        cm-management user clear
        cm-management user add [YAMLFILE]
        cm-management user delete [USERNAME]
        cm-management user activate [USERNAME]
        cm-management user deactivate [USERNAME]
        cm-management user approve [USERNAME]
        cm-management user deny [USERNAME]
        cm-management project generate
        cm-management version

    Options:
        -h --help       Show this screen
        --version       Show version
        --format=FORMAT Output format: table, json
        --all           Displays all users
    """

    arguments = docopt(management_command.__doc__, args[1:])

    try:
        if arguments['version']:
            print cloudmesh.__version__
        elif arguments['user'] and arguments['list']:
            user = Users()
            disp_fmt = None
            user_name = None
            if arguments['--format']:
                disp_fmt = arguments['--format']
            if arguments['USERNAME']:
                user_name = arguments['USERNAME']
            user.list_users(disp_fmt, user_name)
        elif arguments['user'] and arguments['generate']:
            if arguments['--count']:
                count = int(arguments['--count'])
                generate_users(count)
            else:
                generate_users(10)
        elif arguments['user'] and arguments['clear']:
            user = Users()
            user.clear()
        elif arguments['user'] and arguments['delete']:
            if arguments['USERNAME']:
                user = Users()
                user.delete_user(arguments['USERNAME'])
            else:
                print "Error: Please specify a user to be removed."
        elif arguments['user'] and arguments['approve']:
            if arguments['USERNAME']:
                user = Users()
                user.amend_user_status(arguments['USERNAME'],status='approved')
        elif arguments['user'] and arguments['deny']:
            if arguments['USERNAME']:
                user = Users()
                user.amend_user_status(arguments['USERNAME'],status='denied')
        elif arguments['project']:
            print "Dummy Projects"
            project_fields()
        elif arguments['list']:
            print "Listing Users"
    except:
        print "Invalid arguments Exception", sys.exc_info()[0]
        raise


if __name__ == '__main__':
    management_command(sys.argv)
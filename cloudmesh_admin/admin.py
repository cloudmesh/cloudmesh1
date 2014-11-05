#!/usr/bin/env python

from fabfile.server import start, stop, kill
from fabfile.queue import ls as queue_ls
from fabfile.mongo import info as mongo_info
from fabfile.user import mongo as set_mongo_password

from docopt import docopt
import cloudmesh
import sys

def main():
    admin_command(sys.argv)
        
def admin_command(args):
    """cm-admin.

    Usage:
      cm-admin server start
      cm-admin server stop
      cm-admin server status
      cm-admin mongo password
      cm-admin version

    Options:
      -h --help     Show this screen.
      --version     Show version.

    """
    print args
    arguments = docopt(admin_command.__doc__, args[1:])
    print(arguments)

    if arguments['version']:
        print cloudmesh.__version__
    
    if arguments['start']:
        start()
    elif arguments['stop']:
        stop()
        kill()
    elif arguments['status']:
        print "status"
        queue_ls()
        mongo_info()
    elif arguments['mongo'] and arguments['password']:
        set_mongo_password()


if __name__ == '__main__':
    admin_command(sys.argv)

#! /usr/bin/env python
"""
    Usage:
        cm-tasks menu    
        cm-tasks queue
        cm-tasks start
        cm-tasks stop
        cm-tasks halt
        cm-tasks kill                                
"""

from docopt import docopt
import os
import sys
from cloudmesh.util.menu import ascii_menu


def hallo():
    print "hallo"


def celery_start():
    os.system("celery worker --concurrency=10 --app=cloudmesh_task -l info & ")


def celery_stop():
    os.system(
        "ps auxww | grep 'celery worker' | awk '{print $$2}' | xargs kill -9 &")


def rabbit_start():
    os.system("sudo rabbitmq-server -detached")


def rabbit_stop():
    os.system("sudo rabbitmqctl stop")


def mongo_start():
    os.system("cd ../../; fab manage.mongo &")


def all_stop():
    celery_stop()
    rabbit_stop()


def all_start():
    rabbit_start()
    celery_start()


def menu():
    ascii_menu("Queue Management",
               [('all start', all_start),
                ('all stop', all_stop),
                ('rabbit start', rabbit_start),
                ('celery start', celery_start),
                ('rabbit stop', rabbit_stop),
                ('celery stop', celery_stop),
                ('mongo start', mongo_start)
                ])


def main(arguments):

    if arguments["menu"]:
        menu()

    elif arguments["queue"]:
        rabbit_start()

    elif arguments["start"]:
        celery_start()

    elif arguments["stop"]:
        rabbit_stop()

    elif arguments["kill"]:
        celery_worker_kill()

    elif arguments["halt"]:
        celery_worker_halt()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)

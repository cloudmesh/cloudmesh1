#! /usr/bin/env python
"""
    Usage:
        cm-tasks queue
        cm-tasks start
        cm-tasks stop
        cm-tasks halt
        cm-tasks kill                                
"""

from docopt import docopt
import os
import sys

def main(arguments):

    if arguments["queue"]: 
        os.system("sudo rabbitmq-server -detached")
        sys.exit(0)
            
    if arguments["start"]: 
        os.system("celery worker --concurrency=10 --app=cloudmesh_task -l info")

    if arguments["stop"]: 
        os.system("sudo rabbitmqctl stop")

    if arguments["kill"]: 
	    os.system("ps auxww | grep 'celery worker' | awk '{print $$2}' | xargs kill -9")

    if arguments["halt"]: 
        os.system("ps auxww | grep 'celery worker' | awk '{print $$2}' | xargs kill")


if __name__ == '__main__':
        arguments = docopt(__doc__)
        main(arguments)


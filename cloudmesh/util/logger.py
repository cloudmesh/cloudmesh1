'''
A simple class to set up a custom logger for a class
'''
from sh import grep
import logging
import sys
import os
from cloudmesh.util.util import path_expand

def LOGGER(filename):
    """creates a logger with the given name.

    You can use it as follows::

       log = cloudmesh.util.LOGGER(__file__)
       log.error("this is an error")
       log.info("this is an info")
       log.warning("this is a warning")

    """
    pwd = os.getcwd()
    name = filename.replace(pwd, "$PWD")
    try:
        (first, name) = name.split("site-packages")
        name = "... site" + name
    except:
        pass




    loglevel = logging.CRITICAL
    try:
        level = grep("loglevel:", path_expand("~/.futuregrid/cloudmesh_server.yaml")).strip().split(":")[1].strip().lower()

        if level == "debug":
            loglevel = logging.DEBUG
        elif level == "info":
            loglevel = logging.INFO
        elif level == "warning":
            loglevel = logging.WARNING
        else:
             level = logging.CRITICAL
    except:
        print "LOGLEVEL NOT FOUND"
        loglevel = logging.DEBUG

    log = logging.getLogger(name)
    log.setLevel(loglevel)


    formatter = logging.Formatter(
        'CM {0:>50}: %(levelname)6s - %(message)s'.format(name))
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log

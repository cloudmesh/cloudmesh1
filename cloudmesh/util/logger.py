'''
A simple class to set up a custom logger for a class
'''

import logging
import sys
import os

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

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        'CM {0:>50}: %(levelname)6s - %(message)s'.format(name))
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log

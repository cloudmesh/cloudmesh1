from cloudmesh_install import config_file
import logging
import os
from cloudmesh_install.util import grep

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
        level = grep("loglevel:", config_file(
            "/cloudmesh_server.yaml")).strip().split(":")[1].strip().lower()

        if level.upper() == "DEBUG":
            loglevel = logging.DEBUG
        elif level.upper() == "INFO":
            loglevel = logging.INFO
        elif level.upper() == "WARNING":
            loglevel = logging.WARNING
        elif level.upper() == "ERROR":
            loglevel = logging.ERROR
        else:
            level = logging.CRITICAL
    except:
        # print "LOGLEVEL NOT FOUND"
        loglevel = logging.DEBUG

    log = logging.getLogger(name)
    log.setLevel(loglevel)

    formatter = logging.Formatter(
        'CM {0:>50}:%(lineno)s: %(levelname)6s - %(message)s'.format(name))

    # formatter = logging.Formatter(
    #    'CM {0:>50}: %(levelname)6s - %(module)s:%(lineno)s %funcName)s: %(message)s'.format(name))
    handler = logging.StreamHandler()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log

def LOGGING_ON(log):
    try:
        log.setLevel(logging.DEBUG)
        return True
    except:
        return False

def LOGGING_OFF(log):
    try:
        log.setLevel(logging.CRITICAL)
        return True
    except:
        return False

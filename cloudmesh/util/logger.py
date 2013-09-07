import logging

"""A simple class to set up a custom logger for a class"""

def LOGGER(name):
    """creates a logger with the given name.

    You can use it as follows::

       log = cloudmesh.util.LOGGER(__file__)
       log.error("this is an error")
       log.info("this is an info")
       log.warning("this is a warning")

    """
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        'CM {0}: [%(levelname)s] %(message)s'.format(name))
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log

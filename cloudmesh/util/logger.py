import logging


def LOGGER(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        'CM {0}: [%(levelname)s] %(message)s'.format(name))
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log

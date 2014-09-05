"""Some simple yaml file reader"""

import os
import sys

from cloudmesh_common.logger import LOGGER
from cloudmesh_common.util import check_file_for_tabs
from cloudmesh_common.util import path_expand as cm_path_expand
import yaml
from string import Template
import traceback

log = LOGGER(__file__)


def read_yaml_config(filename, check=True, osreplace=True):
    '''
    reads in a yaml file from the specified filename. If check is set to true
    the code will faile if the file does not exist. However if it is set to
    false and the file does not exist, None is returned.
    
    :param filename: the file name
    :param check: if True fails if the file does not exist,
                  if False and the file does not exist return will be None
    '''
    location = filename
    if location is not None:
        location = cm_path_expand(location)

    if not os.path.exists(location) and not check:
        return None

    if check and os.path.exists(location):

        # test for tab in yaml file
        if check_file_for_tabs(location):
            log.error("The file {0} contains tabs. yaml "
                      "Files are not allowed to contain tabs".format(location))
            sys.exit()
        try:

            if osreplace:
                result = open(location, 'r').read()
                t = Template(result)
                result = t.substitute(os.environ)
                data = yaml.safe_load(result)
            else:
                f = open(location, "r")
                data = yaml.safe_load(f)
                f.close()

            return data
        except Exception, e:
            log.error(
                "The file {0} fails with a yaml read error".format(filename))
            log.error(str(e))
            print traceback.format_exc()
            sys.exit()

    else:
        log.error("The file {0} does not exist.".format(filename))
        # sys.exit()

    return None

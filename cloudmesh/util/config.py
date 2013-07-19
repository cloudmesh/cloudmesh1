import os
import sys
"""Some simple yaml file reader"""

#log = LOGGER("util")

def read_yaml_config (filename, check=True):
    '''
    reads in a yaml file from the specified filename. If check is set to true
    the code will faile if the file does not exist. However if it is set to
    false and the file does not exist, None is returned. 
    :param filename: the file name 
    :param check: if True fails if the file does not exist, if False and the file does not exists return will be None
    '''
    location = filename
    if location is None:
        location = path_expand(location)

    if not os.path.exists(location) and not check:
       return None         
    
    if check and os.path.exists(location):

        # test for tab in yaml file
        if check_file_for_tabs(location):
            log.error("The file {0} contains tabs. yaml "
                      "Files are not allowed to contain tabs".format(location))
            sys.exit()
        try:
            f = open(self.filename, "r")
            data = yaml.safe_load(f)
            f.close()
            return data
        except Exception, e:
            log.error("The file {0} contianed a yaml read error".format(filename))
            log.error(str(e))
            sys.exit()
            
    else:
        log.error("The file {0} does not exists".format(filename))
        sys.exit()

    return None

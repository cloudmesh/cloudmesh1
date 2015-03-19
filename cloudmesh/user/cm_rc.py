from __future__ import print_function
import os
import sys
import glob
from pprint import pprint
from cloudmesh_base.locatiosn import config_file
from ConfigParser import SafeConfigParser, NoOptionError

def get_rcfiles(fpath=None):
    dir = config_file("")
    read_values = ["OS_TENANT_NAME", "OS_USERNAME", "OS_PASSWORD",
                   "OS_AUTH_URL"] #, "OS_CACERT"]

    rcfile_path = dir + "/clouds/"
    new_values = {}
    for filepath in glob.glob(rcfile_path + "/*/*rc"):
        filename = os.path.basename(filepath)
        cloud_name = os.path.basename(
            os.path.normpath(filepath.replace(filename, "")))
        new_values[cloud_name] = get_variables(filepath, read_values)

    return new_values

class _Readrcfile(object):
    ''' Read novarc, eucarc and store variables with configparser
        - internal function -

        reference:
        http://stackoverflow.com/questions/2819696/parsing-properties-file-in-python/2819788#2819788
    '''

    def __init__(self, fp):
        self.fp = fp
        self.head = '[rcfile]\n'

    def readline(self):
        if self.head:
            try:
                return self.head
            finally:
                self.head = None
        else:
            return self.fp.readline().replace("export ", "")

def get_variables(fpath, read_values=["OS_TENANT_NAME", "OS_USERNAME",
                                      "OS_PASSWORD"]):
    ''' Read variables from novarc file. 
    '''

    section_title = "rcfile"
    result = {}
    # case-sensitive
    # read_values = ["OS_TENANT_NAME", "OS_USERNAME", "OS_PASSWORD"]

    cp = SafeConfigParser()
    try:
        cp.readfp(_Readrcfile(open(fpath)))
        # cp.items(section_title)
        for read_value in read_values:
            try:
                tmp = cp.get(section_title, read_value)
            # Exception for missing key
            # e.g. OS_CACERT is only available after openstack havana
            #      Old openstack has it as NOVA_CACERT.
            except NoOptionError:
                tmp = ""
            if tmp.startswith("$"):
                tmp = cp.get(section_title, tmp[1:])  # without $ sign
            result[read_value] = tmp
        return result
    except:
        print("ERROR: Failed to read rc files. Please check you have valid \
                rcfiles in %s." % fpath)
        print(sys.exc_info())



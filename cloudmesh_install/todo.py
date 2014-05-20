### Replace me.yaml with real values ###

rc_dir_location = {}
# (hostname, loaction of dir on remote host, location of dir on localhost)
rc_dir_location["india_openstack_havana"] = ("india.futuregird.org", "?", "?")
rc_dir_location["sierra_openstack_grizzly"] = ("sierra.futuregrid.org", "?", "?")
rc_dir_location["sierra_eucalyptus_v??"] = ("sierra.futuregrid.org", "?", "?")

from ??? import config_file
install_dir = config_file("") # ~/.futuregrid

def get_fg_username_password_from_rcfiles(hosts)

    """
    for label in rc_dir_location
        (host,dir) = rc_rdilocation(label)
        get rc file form the host and dir and copy to install_dir

    me_dict = read current me.yaml

    
    
    for label in rc_dir_location
        (host,dir) = rc_rdilocation(label)

        if label does not exist make it and also add the credentials for it,
            fill out initially with TBD
        
        if openstack:
           put values from local dir into dict

        elif eucalyptus:
           put values from local dir into dict

    return me dict
    """                
    


class Readrcfile(object):
    """ Read novarc, eucarc and store variables
        with configparser
        reference:
        http://stackoverflow.com/questions/2819696/parsing-properties-file-in-python/2819788#2819788
    """
    def __init__(self, fp):
       self.fp = fp
       self.head = '[rcfile]\n'

    def readline(self):
        if self.head:
            try: return self.head
            finally: self.head = None
        else: return self.fp.readline().replace("export ", "")

def get_variables(fpath):
    section_title = "rcfile"
    read_values = ["OS_TENANT_NAME", "OS_PASSWORD"]  # case-sensitive
    result = {}

    cp = SafeConfigParser()
    try:
        cp.readfp(Readrcfile(open(fpath)))
        # cp.items(section_title)
        for read_value in read_values:
            result[read_value] = cp.get(section_title, read_value)
        return result

    except:
        print "ERROR: Failed to read rc files. Please check you have valid \
                rcfiles in %s." % fpath
        print sys.exc_info()
        sys.exit(1)

# rcfile location
rcfile_path = dir + "/clouds/"
new_values = {}
for filepath in glob.glob(rcfile_path + "/*/*rc"):
    filename = os.path.basename(filepath)
    cloud_name = os.path.basename(os.path.normpath(filepath.replace(filename, "")))
    new_values[cloud_name] = get_variables(filepath)


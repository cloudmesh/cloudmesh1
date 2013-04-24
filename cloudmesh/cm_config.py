import sys
sys.path.insert(0, '..')
import yaml
import os
import json
from string import Template

def path_expand(text):
    """ returns a string with expanded variavble """
    template = Template(text)
    result = template.substitute(os.environ)
    return result


class cm_config:

    ######################################################################
    # global variables
    ######################################################################

    default_path = '.futuregrid/cloudmesh.yaml'
    filename = ""
    data = {}

    ######################################################################
    # initialization methods
    ######################################################################



    def __init__(self, filename=None):
        if filename == None:
            home = os.environ['HOME']
            self.filename = "%s/%s" % (home, self.default_path)
        else:
            self.filename = filename
        self.read(self.filename)
        return

    ######################################################################
    # read and write methods
    ######################################################################

    def read(self, filename):
        self.filename = filename
        f = open(self.filename, "r")
        self.data = yaml.safe_load(f)
        f.close()

    def write(self, filename):
        """ BUG DOES NOT WORK"""
        f = open(filename, "w")
        yaml.dump(self.data, f, default_flow_style=False, indent=4)
        f.close()

    ######################################################################
    # print methods
    ######################################################################

    def __str__(self):
        return json.dumps(self.data, indent=4)

    def export_line(self, attribute, value):
        return "export %s=%s\n" % (attribute, value)

    ######################################################################
    # get methods
    ######################################################################
    def default(self):
        return self.data['cloudmesh']['default']

    def active(self):
        return self.data['cloudmesh']['active']

    def projects(self, status):
        return self.data['cloudmesh']['projects'][status]

    def clouds(self):
        return self.data['cloudmesh']['clouds']

    def cloud(self, cloudname):
        return self.data['cloudmesh']['clouds'][cloudname]
        
    def cloud_default(self, cloudname, defname):
        cloud = self.cloud(cloudname)
        defaults = cloud['default'] if 'default' in cloud else []
        return defaults[defname] if defname in defaults else None

    def get(self, key=None, expand=False):
        if key == None:
            return self.data['cloudmesh']
        else:
            if expand:
                d = self.cloud(key)['credentials']
                for key in d:
                    d[key] = path_expand(d[key])
                return d
            else:
                return self.cloud(key)['credentials']

    # This method may not be exactly what I think it is, but based on usage it
    # appears as if it is supposed to get the keys of the clouds
    def keys(self):
        return self.clouds().keys()

    def rc(self, name):
        result = self.get(name)
        lines = ""
        for (attribute, value) in result.iteritems():
            lines += self.export_line(attribute, value)
        return lines

    def rc_euca(self, name, project):
        result = self.cloud(name)
        eucakeydir = 'EUCA_KEY_DIR'
        lines = self.export_line(eucakeydir, result[eucakeydir])

        for (attribute, value) in result.iteritems():
            if attribute != eucakeydir:
                if type(value) is dict:
                    if attribute == project:
                        for (pattribute, pvalue) in value.iteritems():
                            lines += self.export_line(pattribute, pvalue)
                else:    
                    lines += self.export_line(attribute, value)
        return lines

##########################################################################
# MAIN METHOD FOR TESTING
##########################################################################

if __name__ == "__main__":
    config = cm_config()

    print config

    print "================="
    print config.projects('active')
    print config.projects('completed')
    print "================="
    print config.get('india-openstack')
    print "================="
    print config.get()
    print "================="
    print config.keys()
    print "================="
    print config.rc('india-openstack')
    print "================="
    print config.default()
    print "================="
    outfile = "%s/%s" % (os.environ['HOME'], ".futuregrid/junk.yaml")
    print config.write(outfile)
    os.system("cat " + outfile)
    print "================="
    configuration = config.get('azure')

    print configuration['username']

    print "================="

    configuration = config.get('india-eucalyptus')
    print configuration

    print configuration['host']

import sys
sys.path.insert(0, '..')
import yaml
#import pyaml
import os
import json
import collections

from string import Template


def path_expand(text):
    """ returns a string with expanded variavble """
    template = Template(text)
    result = template.substitute(os.environ)
    return result


class cm_config(object):

    ######################################################################
    # global variables
    ######################################################################

    default_path = '.futuregrid/cloudmesh.yaml'
    yaml_template = 'cloudmesh-template.yaml'
    filename = ""
    data = collections.OrderedDict()

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
        self._userdata_handler = None
        self._cloudcreds_handler = None

    @property
    def userdata_handler(self):
        """Plug-in class that knows how to get all the user/project data"""
        return self._userdata_handler

    @userdata_handler.setter
    def userdata_handler(self, value):
        self._userdata_handler = value

    @property
    def cloudcreds_handler(self):
        """Plug-in class that knows how to get all the cloud credential data"""
        return self._cloudcreds_handler

    @cloudcreds_handler.setter
    def cloudcreds_handler(self, value):
        self._cloudcreds_handler = value


    ######################################################################
    # Methods to initialize (create) the config data
    ######################################################################
    def _initialize_user(self, username):
        """Loads user data, including profile, projects, and credentials"""
        user = self.userdata_handler(username)

        self.data['cloudmesh']['prefix'] = username

        self.data['cloudmesh']['profile'] = {
            'username': username,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'phone': user.phone,
            'e-mail': user.email,
            'address': user.address
            }

        keys = { 'default': None, 'keylist': {} }
        for key in user.keys.keys():
            if keys['default'] is None:
                keys['default'] = key
            keys['keylist'][key] = user.keys[key]
        self.data['cloudmesh']['keys'] = keys

        self.data['cloudmesh']['projects'] = {
            'active': user.activeprojects,
            'completed': user.completedprojects,
            'default': user.defaultproject
            }
                
        self.data['cloudmesh']['active'] = user.activeclouds
        self.data['cloudmesh']['default'] = user.defaultcloud


    def _initialize_clouds(self):
        """Creates cloud credentials for the user"""
        self.data['cloudmesh']['clouds'] = {}
        cloudlist = self.active()
        for cloud in cloudlist:
            cloudcreds = self.cloudcreds_handler(self.profile(), self.projects('default'), self.projects('active'), cloud)
            cloudcreds.initialize_cloud_user()
            self.data['cloudmesh']['clouds'][cloud] = cloudcreds.data


    def initialize(self, username):
        """Creates or resets the data for a user.  Note that the
        userdata_handler and cloudcreds_handler properties must be set
        with appropriate handler classes."""
        self.data = yaml.safe_load(open(self.yaml_template, "r"))
        self._initialize_user(username)
        self._initialize_clouds()

    ######################################################################
    # read and write methods
    ######################################################################

    def read(self, filename):
        self.filename = filename
        if os.path.exists(filename):
            f = open(self.filename, "r")
            self.data = yaml.safe_load(f)
            f.close()

    def write(self, filename=None):

        #pyaml.dump(self.data, f, vspacing=[2, 1, 1])
        text = yaml.dump(self.data, default_flow_style=False)
        # avoiding to think about regexp ;-)
        # shold be eplace all "\n  ." with "\\n  ." but not when . is -   
        text = text.replace("\n  ", "\n\n  ")
        text = text.replace("\n\n  -", "\n  -")
        text = text.replace("\n\n    ", "\n    ")
        text = text.replace("\n\n      ", "\n      ")
        text = text.replace("\n\n        ", "\n        ")

        f = open(filename or self.filename, "w")
        f.write(text)
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

    def prefix(self):
        return self.data['cloudmesh']['prefix']

    def profile(self):
        return self.data['cloudmesh']['profile']

    def userkeys(self, attribute=None, expand=True):
        if attribute == None:
            return self.data['cloudmesh']['keys']
        else:
            if attribute == 'default':
                name = self.data['cloudmesh']['keys']['default']
                value = self.data['cloudmesh']['keys']['keylist'][name]
            else:
                value = self.data['cloudmesh']['keys']['keylist'][attribute]
            if expand:
                value = path_expand(value)
            return value

    def default(self,cloudname):
        return self.data['cloudmesh']['clouds'][cloudname]['default']

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

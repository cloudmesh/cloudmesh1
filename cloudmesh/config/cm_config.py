import sys
import yaml
import os
import json
import collections
import copy

from pprint import pprint
from cloudmesh.util.util import path_expand
from cloudmesh.util.logger import LOGGER
from cloudmesh.util.util import check_file_for_tabs

from cloudmesh_cloud_handler import cloudmesh_cloud_handler
from cloudmesh.util.config import read_yaml_config
from cloudmesh.config.ConfigDict import ConfigDict

from pymongo import MongoClient
import yaml

log = LOGGER(__file__)

def get_mongo_db(mongo_collection):
    """
    Read in the mongo db information from the cloudmesh_server.yaml
    """
    filename = os.path.expanduser("~/.futuregrid/cloudmesh_server.yaml")

    mongo_config = ConfigDict(filename=filename).get("mongo")

    mongo_host = mongo_config["host"]
    mongo_port = int(mongo_config["port"])

    mongo_db_name = mongo_config["collections"][mongo_collection]['db']

    client = MongoClient(host=mongo_host,
                         port=mongo_port)
    db = client[mongo_db_name]
    db_clouds = db[mongo_collection]
    return db_clouds



class cm_config_server(ConfigDict):
    """
    reads the information contained in the file
    ~/.futuregrid/cloudmesh_server.yaml
    """
    filename = os.path.expanduser("~/.futuregrid/cloudmesh_server.yaml")

    def __init__(self, filename=None):
        if filename is None:
            filename = self.filename
        ConfigDict.__init__(self, filename=filename, kind="server")


class cm_config_launcher(ConfigDict):
    """
    reads the information contained in the file
    ~/.futuregrid/cloudmesh_server.yaml
    """
    filename = os.path.expanduser("~/.futuregrid/cloudmesh_launcher.yaml")

    def __init__(self, filename=None):
        if filename is None:
            filename = self.filename
        ConfigDict.__init__(self, filename=filename, kind="launcher")


class cm_config(ConfigDict):

    # ----------------------------------------------------------------------
    # global variables
    # ----------------------------------------------------------------------

    filename = os.path.expanduser('~/.futuregrid/cloudmesh.yaml')
    cloudmesh_server_path = os.path.expanduser('~/.futuregrid/cloudmesh_server.yaml')

    # ----------------------------------------------------------------------
    # initialization methods
    # ----------------------------------------------------------------------


    def __init__(self, filename=None):
        if filename is None:
            filename = self.filename
        ConfigDict.__init__(self, filename=filename, kind="user")


        self._userdata_handler = None
        self._serverdata = None


    # ----------------------------------------------------------------------
    # Internal helper methods
    # ----------------------------------------------------------------------
    def _get_cloud_handler(self, cloud, as_admin=False):
        """This gets a class that knows how to handle the specific type of
        cloud (how to provision users, etc)"""
        handler_args = { 'username': self.init_config['cloudmesh']['profile']['username'],
                         'email':  self.init_config['cloudmesh']['profile']['e_mail'],
                         'defaultproj': self.init_config['cloudmesh']['projects']['default'],
                         'projectlist': self.init_config['cloudmesh']['projects']['active'],
                         'cloudname': cloud,
                         'cloudcreds': self.get_data(cloud),
                         'cloudadmincreds': self.serverdata['keystone'][cloud] }
        cloud_handler_class = cloudmesh_cloud_handler(cloud)
        cloud_handler = cloud_handler_class(**handler_args)
        return cloud_handler


    # ----------------------------------------------------------------------
    # Methods to initialize (create) the config config
    # ----------------------------------------------------------------------
    def _initialize_user(self, username):
        """Loads user config, including profile, projects, and credentials"""
        user = self.userdata_handler(username)

        self.init_config['cloudmesh']['prefix'] = username
        self.init_config['cloudmesh']['index'] = "001"

        self.init_config['cloudmesh']['profile'] = {
            'username': username,
            'uid': user.uid,
            'gid': user.gid,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'phone': user.phone,
            'e_mail': user.email,
            'address': user.address
        }

        keys = {'default': None, 'keylist': {}}
        if user.keys:
            for key in user.keys.keys():
                if keys['default'] is None:
                    keys['default'] = key
                keys['keylist'][key] = user.keys[key]
        self.init_config['cloudmesh']['keys'] = keys

        self.init_config['cloudmesh']['projects'] = {
            'active': user.activeprojects,
            'completed': user.completedprojects,
            'default': user.defaultproject
        }

        self.init_config['cloudmesh']['active'] = user.activeclouds
        self.init_config['cloudmesh']['default'] = user.defaultcloud

    def _initialize_clouds(self):
        """Creates cloud credentials for the user"""
        self.init_config['cloudmesh']['clouds'] = {}
        cloudlist = self.init_config['cloudmesh']['active']
        for cloud in cloudlist:
            cloud_handler = self._get_cloud_handler(cloud, as_admin=True)
            cloud_handler.initialize_cloud_user()
            self.init_config['cloudmesh']['clouds'][cloud] = copy.deepcopy(cloud_handler.credentials)

    def initialize(self, username):
        """Creates or resets the config for a user.  Note that the
        userdata_handler property must be set with appropriate handler class."""
        self.init_config = collections.OrderedDict()
        self.init_config['cloudmesh'] = collections.OrderedDict()
        self._initialize_user(username)
        self._initialize_clouds()

    def change_own_password(self, cloudname, oldpass, newpass):
        cloud_handler = self._get_cloud_handler(cloudname)
        cloud_handler.change_own_password(oldpass, newpass)
        # Save the yaml file so the new password is saved
        self.write()

    def get_own_passwords(self):
        cloudlist = self.active()
        passwords = {}
        for cloud in cloudlist:
            cloud_handler = self._get_cloud_handler(cloud)
            passwords[cloud] = cloud_handler.get_own_password()
        return passwords


    # ----------------------------------------------------------------------
    # print methods
    # ----------------------------------------------------------------------

    def export_line(self, attribute, value):
        if isinstance(value, (list, tuple)):
            avalue = ','.join(value)
        else:
            avalue = value
        return 'export %s="%s"\n' % (attribute, avalue)


    # ----------------------------------------------------------------------
    # Properties
    # ----------------------------------------------------------------------
    @property
    def userdata_handler(self):
        """Plug-in class that knows how to get all the user/project config"""
        return self._userdata_handler

    @userdata_handler.setter
    def userdata_handler(self, value):
        self._userdata_handler = value

    @property
    def serverdata(self):
        if self._serverdata is None:
            self._serverdata = yaml.safe_load(open(self.cloudmesh_server_path, "r"))
        return self._serverdata

    @property
    def vmname(self):
        return "%s-%04d" % (self['cloudmesh']['prefix'], int(self['cloudmesh']['index']))

    @property
    def default_cloud(self):
        return self['cloudmesh']['default']

    @default_cloud.setter
    def default_cloud(self, value):
        self['cloudmesh']['default'] = str(value)

    @property
    def prefix(self):
        return self['cloudmesh']['prefix']

    @prefix.setter
    def prefix(self, value):
        self['cloudmesh']['prefix'] = value

    @property
    def index(self):
        return self['cloudmesh']['index']

    @index.setter
    def index(self, value):
        self['cloudmesh']['index'] = int(value)

    @property
    def firstname(self):
        return self['cloudmesh']['profile']['firstname']

    @firstname.setter
    def firstname(self, value):
        self['cloudmesh']['profile']['firstname'] = str(value)

    @property
    def lastname(self):
        return self['cloudmesh']['profile']['lastname']

    @lastname.setter
    def lastname(self, value):
        self['cloudmesh']['profile']['lastname'] = str(value)

    @property
    def phone(self):
        return self['cloudmesh']['profile']['phone']

    @phone.setter
    def phone(self, value):
        self['cloudmesh']['profile']['phone'] = str(value)

    @property
    def email(self):
        return self['cloudmesh']['profile']['e_mail']

    @email.setter
    def email(self, value):
        self['cloudmesh']['profile']['e_mail'] = str(value)

    @property
    def address(self):
        return self['cloudmesh']['profile']['address']

    @address.setter
    def address(self, value):
        self['cloudmesh']['profile']['address'] = str(value)


    # ----------------------------------------------------------------------
    # get methods
    # ----------------------------------------------------------------------
    def incr(self, value=1):
        self['cloudmesh']['index'] = int(
            self['cloudmesh']['index']) + int(value)
        # self.write(self.filename)

    #
    # warning we can not name a method default
    #
    def active(self):
        return self['cloudmesh']['active']

    def profile(self):
        return self['cloudmesh']['profile']

    def username(self):
        return self['cloudmesh']['hpc']['username']

    def userkeys(self, attribute=None, expand=True):
        if attribute is None:
            return self['cloudmesh']['keys']
        else:
            if attribute == 'default':
                name = self['cloudmesh']['keys']['default']
                value = self['cloudmesh']['keys']['keylist'][name]
            else:
                value = self['cloudmesh']['keys']['keylist'][attribute]
            if expand:
                value = path_expand(value)
            return value

    def default(self, cloudname):
        return self['cloudmesh']['clouds'][cloudname]['default']

    def projects(self, status):
        return self['cloudmesh']['projects'][status]

    def clouds(self):
        return self['cloudmesh']['clouds']

    def cloud(self, cloudname):
        return self['cloudmesh']['clouds'][cloudname] if cloudname in self['cloudmesh']['clouds'] else None

    def cloud_default(self, cloudname, defname):
        cloud = self.cloud(cloudname)
        defaults = cloud['default'] if 'default' in cloud else []
        return defaults[defname] if defname in defaults else None

    def credential(self, name):
        return self.get_data (key=name, expand=True)

    def get_data(self, key=None, expand=False):
        if key is None:
            return self['cloudmesh']
        else:
            if expand:
                d = self.cloud(key)['credentials']
                for key in d:
                    d[key] = path_expand(str(d[key]))
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
        for (attribute, value) in iter(sorted(result.iteritems())):
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


# ----------------------------------------------------------------------
# MAIN METHOD FOR TESTING
# ----------------------------------------------------------------------

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
    print config.default
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

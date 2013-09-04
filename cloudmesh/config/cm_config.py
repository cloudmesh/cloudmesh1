import sys
import yaml
import os
import stat
import json
import collections
import copy

from pprint import pprint
from cloudmesh.util.util import path_expand
from cloudmesh.util.logger import LOGGER
from cloudmesh.util.util import check_file_for_tabs

from cloudmesh_cloud_handler import cloudmesh_cloud_handler
from cloudmesh.util.config import read_yaml_config

from cloudmesh.user.cm_template import cm_template
from pymongo import MongoClient
import yaml

##### For testing
# import mock_keystone


log = LOGGER("cm_config")

package_dir = os.path.dirname(os.path.abspath(__file__))


def get_mongo_db(mongo_collection):
    """
    Read in the mongo db information from the cloudmesh_server.yaml
    """
    location = path_expand("~/.futuregrid/cloudmesh_server.yaml")
    result = open(location, 'r').read()
        
    mongo_config = yaml.load(result)["mongo"]
    mongo_host = mongo_config["host"]
    mongo_port = mongo_config["port"]
    
    mongo_db_name = mongo_config["collections"][mongo_collection]['db']
        
    client = MongoClient(host=mongo_host,
                              port=mongo_port)  
    db = client[mongo_db_name]          
    db_clouds = db[mongo_collection] 
    return db_clouds
    
class cm_config_server:
    """
    reads the information contained in the file
    ~/.futuregrid/cloudmesh_server.yaml
    """
    filename = "~/.futuregrid/cloudmesh_server.yaml"
    config = None

    def __init__(self, filename=None):
        if filename is not None:
            self.filename = filename
        
        self.config = read_yaml_config (self.filename, check=True) 
        
    def __str__(self):
        return json.dumps(self.config, indent=4)

    def __getitem__(self,*mykeys):        
        try:
            item = self.get(mykeys[0])
        except:
             log.error('calling cm_config_server.get("' + '", "'.join(mykeys) +'")')
             log.error("Your configuration file does not contain the proper variable")
             key_string = "[" + ']['.join(mykeys) + "]"
             log.error("Variable requested self.config" + mykey_string)
             log.error("Error occured while accessing " + v)
             sys.exit()
        return item

    def get(self,*keys):
        """
        returns the dict of the information as read from the yaml file. To
        access the file safely, you can use the keys in the order of the access.
        Example: get("provisiner","policy") will return the value of
        config["provisiner"]["policy"] from the yaml file if it does not exists
        an error will be printing that the value does not exists and we exit.
        Alternatively you can use the . notation e.g. get("provisiner.policy")
        """
        if keys is None:
            return self.config

        if "." in keys[0]:
            keys = keys[0].split('.')
        element = self.config
        for v in keys:
            try:
               element = element[v]
            except:
                log.error('calling cm_config_server.get("' + '", "'.join(keys) +'")')
                log.error("Your configuration file does not contain the proper variable")
                key_string = "[" + ']['.join(keys) + "]"
                log.error("Variable requested self.config" + key_string)
                log.error("Error occured while accessing " + v)
                sys.exit()
        return element
    
class cm_config_launcher:
    """
    reads the information contained in the file
    ~/.futuregrid/cloudmesh_launcher.yaml
    """
    filename = "~/.futuregrid/cloudmesh_launcher.yaml"
    config = None

    def __init__(self, filename=None):
        if filename is not None:
            self.filename = filename
        
        self.config = read_yaml_config (self.filename, check=True) 
        
    def __str__(self):
        return json.dumps(self.config, indent=4)

    def __getitem__(self,*mykeys):        
        try:
            item = self.get(mykeys[0])
        except:
             log.error('calling cm_config_launcher.get("' + '", "'.join(mykeys) +'")')
             log.error("Your configuration file does not contain the proper variable")
             key_string = "[" + ']['.join(mykeys) + "]"
             log.error("Variable requested self.config" + mykey_string)
             log.error("Error occured while accessing " + v)
             sys.exit()
        return item

    def get(self,*keys):
        """
        returns the dict of the information as read from the yaml file. To
        access the file safely, you can use the keys in the order of the access.
        Example: get("provisiner","policy") will return the value of
        config["provisiner"]["policy"] from the yaml file if it does not exists
        an error will be printing that the value does not exists and we exit.
        Alternatively you can use the . notation e.g. get("provisiner.policy")
        """
        if keys is None:
            return self.config

        if "." in keys[0]:
            keys = keys[0].split('.')
        element = self.config
        for v in keys:
            try:
               element = element[v]
            except:
                log.error('calling cm_config_launcher.get("' + '", "'.join(keys) +'")')
                log.error("Your configuration file does not contain the proper variable")
                key_string = "[" + ']['.join(keys) + "]"
                log.error("Variable requested self.config" + key_string)
                log.error("Error occured while accessing " + v)
                sys.exit()
        return element
     

class cm_config(object):

    # ----------------------------------------------------------------------
    # global variables
    # ----------------------------------------------------------------------

    default_path = '.futuregrid/cloudmesh.yaml'
    yaml_template_path = os.path.normpath(os.path.join(package_dir, '..', '..', 'etc', 'cloudmesh.yaml'))
    cloudmesh_server_path = os.path.join(os.environ['HOME'], '.futuregrid', 'cloudmesh_server.yaml')

    filename = ""

    config = collections.OrderedDict()

    # ----------------------------------------------------------------------
    # initialization methods
    # ----------------------------------------------------------------------

    def __init__(self, filename=None):
        if filename is None:
            home = os.environ['HOME']
            self.filename = "%s/%s" % (home, self.default_path)
        else:
            self.filename = filename
        try:
            self.read(self.filename)
        except Exception, e:
            log.error(str(e))
            log.error("Can not find the file: {0}".format(self.filename))
            sys.exit()
        self._userdata_handler = None
        self._serverdata = None

        # test for tab in yaml file
        if check_file_for_tabs(self.filename):
            log.error("The file {0} contains tabs. yaml Files are not allowed to contain tabs".format(filename))
            sys.exit()
        

    # ----------------------------------------------------------------------
    # Internal helper methods
    # ----------------------------------------------------------------------
    def _get_cloud_handler(self, cloud, as_admin=False):
        handler_args = { 'profiledata': self.profile(),
                         'defaultproj': self.projects('default'),
                         'projectlist': self.projects('active'),
                         'cloudname': cloud }
        if as_admin:
            handler_args['clouddata'] = self.serverdata
        else:
            handler_args['clouddata'] = self.cloud(cloud)
        cloud_handler_class = cloudmesh_cloud_handler(cloud)
        cloud_handler = cloud_handler_class(**handler_args)
        ########### for testing #############################################################
        # cloud_handler._client = mock_keystone.Client
        # cloud_handler._client.mockusername = self.config['cloudmesh']['profile']['username']
        # cloud_handler._client.mocktenants = ['fg82','fg110','fg296']
        #####################################################################################
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
            'e-mail': user.email,
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
        cloudlist = self.active()
        for cloud in cloudlist:
            cloud_handler = self._get_cloud_handler(cloud, as_admin=True)
            cloud_handler.initialize_cloud_user()
            self.init_config['cloudmesh']['clouds'][cloud] = copy.deepcopy(cloud_handler.data)

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
    # read and write methods
    # ----------------------------------------------------------------------

    def read(self, filename):
        self.filename = filename
        if os.path.exists(filename):
            f = open(self.filename, "r")
            self.config = yaml.safe_load(f)
            f.close()

    def write(self, filename=None):
        # pyaml.dump(self.config, f, vspacing=[2, 1, 1])
        # text = yaml.dump(self.config, default_flow_style=False)
        template_path = os.path.normpath(os.path.join(package_dir, '..', '..', 'etc', 'cloudmesh.yaml'))
        template = cm_template(template_path)
        content = template.replace(self.config['cloudmesh'], format="dict")

        fpath = filename or self.filename
        f = os.open(fpath, os.O_CREAT | os.O_TRUNC | 
                    os.O_WRONLY, stat.S_IRUSR | stat.S_IWUSR)
        os.write(f, content)
        os.close(f)

    # ----------------------------------------------------------------------
    # print methods
    # ----------------------------------------------------------------------
    def __str__(self):
        return json.dumps(self.config, indent=4)

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
        return "%s-%04d" % (self.config['cloudmesh']['prefix'], int(self.config['cloudmesh']['index']))

    @property
    def default_cloud(self):
        return self.config['cloudmesh']['default']

    @default_cloud.setter
    def default_cloud(self, value):
        self.config['cloudmesh']['default'] = str(value)

    @property
    def prefix(self):
        return self.config['cloudmesh']['prefix']

    @prefix.setter
    def prefix(self, value):
        self.config['cloudmesh']['prefix'] = value

    @property
    def index(self):
        return self.config['cloudmesh']['index']

    @index.setter
    def index(self, value):
        self.config['cloudmesh']['index'] = int(value)

    @property
    def firstname(self):
        return self.config['cloudmesh']['profile']['firstname']

    @firstname.setter
    def firstname(self, value):
        self.config['cloudmesh']['profile']['firstname'] = str(value)

    @property
    def lastname(self):
        return self.config['cloudmesh']['profile']['lastname']

    @lastname.setter
    def lastname(self, value):
        self.config['cloudmesh']['profile']['lastname'] = str(value)

    @property
    def phone(self):
        return self.config['cloudmesh']['profile']['phone']

    @phone.setter
    def phone(self, value):
        self.config['cloudmesh']['profile']['phone'] = str(value)

    @property
    def email(self):
        return self.config['cloudmesh']['profile']['e-mail']

    @email.setter
    def email(self, value):
        self.config['cloudmesh']['profile']['e-mail'] = str(value)

    @property
    def address(self):
        return self.config['cloudmesh']['profile']['address']

    @address.setter
    def address(self, value):
        self.config['cloudmesh']['profile']['address'] = str(value)


    # ----------------------------------------------------------------------
    # get methods
    # ----------------------------------------------------------------------
    def incr(self, value=1):
        self.config['cloudmesh']['index'] = int(
            self.config['cloudmesh']['index']) + int(value)
        # self.write(self.filename)

    #
    # warning we can not name a method default
    #
    def active(self):
        return self.config['cloudmesh']['active']

    def profile(self):
        return self.config['cloudmesh']['profile']

    def userkeys(self, attribute=None, expand=True):
        if attribute is None:
            return self.config['cloudmesh']['keys']
        else:
            if attribute == 'default':
                name = self.config['cloudmesh']['keys']['default']
                value = self.config['cloudmesh']['keys']['keylist'][name]
            else:
                value = self.config['cloudmesh']['keys']['keylist'][attribute]
            if expand:
                value = path_expand(value)
            return value

    def default(self, cloudname):
        return self.config['cloudmesh']['clouds'][cloudname]['default']

    def projects(self, status):
        return self.config['cloudmesh']['projects'][status]

    def clouds(self):
        return self.config['cloudmesh']['clouds']

    def cloud(self, cloudname):
        return self.config['cloudmesh']['clouds'][cloudname] if cloudname in self.config['cloudmesh']['clouds'] else None

    def cloud_default(self, cloudname, defname):
        cloud = self.cloud(cloudname)
        defaults = cloud['default'] if 'default' in cloud else []
        return defaults[defname] if defname in defaults else None

    def credential(self, name):
        return self.get (key=name, expand=True)
    
    def get(self, key=None, expand=False):
        if key is None:
            return self.config['cloudmesh']
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

    def set_filter(self, cloudname, filter, type='state'):
        # try:
        #    test = self.config['cloudmesh']['clouds'][cloudname]['default']['filter']
        # except:
        # self.config['cloudmesh']['clouds'][cloudname]['default']['filter'] = {}
        self.config['cloudmesh']['clouds'][cloudname][
            'default']['filter'][type] = filter

    def get_filter(self, cloudname, type='state'):
        print "getting the filter for cloud", cloudname
        # try:
        #    result = self.config['cloudmesh']['clouds'][cloudname]['default']['filter'][type]
        # except:
        #    self.set_filter(cloudname, {}, type)
        result = self.config['cloudmesh']['clouds'][
            cloudname]['default']['filter'][type]
        return result

    def create_filter(self, cloudname, states):
        self.config['cloudmesh']['clouds'][cloudname]['default']['filter'] = {}
        state_flags = {}
        for state in states:
            state_flags[state] = True
        self.set_filter(cloudname, state_flags, 'state')
        self.set_filter(cloudname, {'me': True}, 'select')


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

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
from cloudmesh.util.util import deprecated
from cloudmesh.util.util import path_expand
from cloudmesh.config.ConfigDict import ConfigDict

from pymongo import MongoClient
import yaml

log = LOGGER(__file__)

def get_mongo_db(mongo_collection):
    """
    Read in the mongo db information from the cloudmesh_server.yaml
    """
    filename = "~/.futuregrid/cloudmesh_server.yaml"

    mongo_config = ConfigDict(filename=filename).attribute("mongo")

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
    filename = "~/.futuregrid/cloudmesh_server.yaml"

    def __init__(self, filename=None):
        if filename is None:
            filename = self.filename
        ConfigDict.__init__(self, filename=filename, kind="server")


class cm_config_launcher(ConfigDict):
    """
    reads the information contained in the file
    ~/.futuregrid/cloudmesh_launcher.yaml
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

    # ----------------------------------------------------------------------
    # initialization methods
    # ----------------------------------------------------------------------


    def __init__(self, filename=None):
        if filename is None:
            filename = self.filename
        ConfigDict.__init__(self, filename=filename, kind="basic")

    # ======================================================================
    # Properties
    # ======================================================================

    # ----------------------------------------------------------------------
    # vmname
    # ----------------------------------------------------------------------

    @property
    def vmname(self):
        return "%s-%04d" % (self['cloudmesh']['prefix'], int(self['cloudmesh']['index']))

    # ----------------------------------------------------------------------
    # default cloud
    # ----------------------------------------------------------------------

    @property
    def default_cloud(self):
        return self['cloudmesh']['default']['cloud']

    @default_cloud.setter
    def default_cloud(self, value):
        self['cloudmesh']['default']['cloud'] = str(value)

    # ----------------------------------------------------------------------
    # generalized set/get default
    # ----------------------------------------------------------------------

    def get_default(self, cloudname=None, attribute=None):
        """
        get_default('sierra_openstack_grizzly')
        get_default('cloud')
        get_default('index')
        """
        if cloudname is None:
            return self['cloudmesh']['default'][attribute]
        else:
            return self['cloudmesh']['clouds'][cloudname]['default']

    def set_default(self, cloudname=None, attribute=None, value=None):
        if cloudname is None:
            if attribute == 'index':
                self['cloudmesh']['default'][attribute] = int(value)
            else:
                self['cloudmesh']['default'][attribute] = value
        else:
            self['cloudmesh']['clouds'][cloudname]['default'] = value

    # ----------------------------------------------------------------------
    # default prefix
    # ----------------------------------------------------------------------

    @property
    def prefix(self):
        return self['cloudmesh']['default']['prefix']

    @prefix.setter
    def prefix(self, value):
        self['cloudmesh']['default']['prefix'] = value

    # ----------------------------------------------------------------------
    # default index
    # ----------------------------------------------------------------------

    @property
    def index(self):
        return self['cloudmesh']['default']['index']

    @index.setter
    def index(self, value):
        self['cloudmesh']['default']['index'] = int(value)

    def incr(self, value=1):
        self['cloudmesh']['default']['index'] = int(
            self['cloudmesh']['default']['index']) + int(value)
        # self.write(self.filename)

    # ----------------------------------------------------------------------
    # profile fistname
    # ----------------------------------------------------------------------

    @property
    def firstname(self):
        return self['cloudmesh']['profile']['firstname']

    @firstname.setter
    def firstname(self, value):
        self['cloudmesh']['profile']['firstname'] = str(value)

    # ----------------------------------------------------------------------
    # profile lastname
    # ----------------------------------------------------------------------

    @property
    def lastname(self):
        return self['cloudmesh']['profile']['lastname']

    @lastname.setter
    def lastname(self, value):
        self['cloudmesh']['profile']['lastname'] = str(value)

    # ----------------------------------------------------------------------
    # profile phone
    # ----------------------------------------------------------------------

    @property
    def phone(self):
        return self['cloudmesh']['profile']['phone']

    @phone.setter
    def phone(self, value):
        self['cloudmesh']['profile']['phone'] = str(value)

    # ----------------------------------------------------------------------
    # profile email
    # ----------------------------------------------------------------------


    @property
    def email(self):
        return self['cloudmesh']['profile']['email']

    @email.setter
    def email(self, value):
        self['cloudmesh']['profile']['email'] = str(value)

    # ----------------------------------------------------------------------
    # profile address
    # ----------------------------------------------------------------------

    @property
    def address(self):
        return self['cloudmesh']['profile']['address']

    @address.setter
    def address(self, value):
        self['cloudmesh']['profile']['address'] = str(value)


    # ----------------------------------------------------------------------
    # get methods
    # ----------------------------------------------------------------------

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


    def projects(self, status):
        return self['cloudmesh']['projects'][status]


    def clouds(self):
        return self['cloudmesh']['clouds']

    @deprecated
    def default(self, cloudname):
        return self['cloudmesh']['clouds'][cloudname]['default']

    def cloud(self, cloudname):
        return self['cloudmesh']['clouds'][cloudname] if cloudname in self['cloudmesh']['clouds'] else None

    def cloud_default(self, cloudname, defname):
        cloud = self.cloud(cloudname)
        defaults = cloud['default'] if 'default' in cloud else []
        return defaults[defname] if defname in defaults else None

    def credential(self, name):
        return self.get_data (key=name, expand=True)

    def get_credential (self, cloud=None, expand=False):
        if expand:
            d = self.get("cloudmesh.{0}.credentials".format(cloud))
            for key in d:
               d[key] = path_expand(str(d[key]))
            return d
        else:
            return self.cloud(key)['credentials']

    def get_data(self, key=None, expand=False):
        if key is None:
            return self['cloudmesh']
        else:
            return self.get_credential(key, expand)

    # This method may not be exactly what I think it is, but based on usage it
    # appears as if it is supposed to get the keys of the clouds

    @deprecated
    def keys(self):
        return self.cloudnames()

    def cloudnames(self):
        return self.clouds().keys()

    def export_line(self, attribute, value):
        if isinstance(value, (list, tuple)):
            avalue = ','.join(value)
        else:
            avalue = value
        return 'export %s="%s"\n' % (attribute, avalue)


    def rc_openstack(self, name):
        """returns the lines that can be put in an rc file"""
        result = self.cloud(name)
        lines = ""
        for (attribute, value) in iter(sorted(result.iteritems())):
            if attribute not in ['credentials', 'default']:
                lines += self.export_line(attribute, value)
            else:
                for key in value:
                    lines += self.export_line(key, value[key])
        return lines

    def rc (self, name):
        kind = self.cloud(name)['cm_type']
        if kind == "openstack":
            return self.rc_openstack(name)
        else:
            print "CLOUDTYPE not supported:", kind

    @deprecated
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

    print "= ACTIVE ================"
    print config.projects('active')
    print "= COMPLETED ================"
    print config.projects('completed')
    print "= SIERRA ================"
    print config.cloud('sierra_openstack_grizzly')
    print "= PROFILE ================"
    print config.get("cloudmesh.profile")
    print "= CLOUDS ================"
    print config.cloudnames()
    print "= RC ================"
    print config.rc('sierra_openstack_grizzly')
    print "= DEFAULT ================"
    print config.default
    print "= TO FILE ================"
    outfile = path_expand("~/.futuregrid/junk.yaml")
    print config.write(outfile)
    os.system("cat " + outfile)
    print "= AZURE ================"
    configuration = config.credential('azure')

    print configuration['username']




    # print "================="

    # configuration = config.get('india-eucalyptus')
    # print configuration

    # print configuration['host']

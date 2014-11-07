from __future__ import print_function
from cloudmesh.config.ConfigDict import ConfigDict
# from cloudmesh.util.config import read_yaml_config
from cloudmesh_common.logger import LOGGER
# from cloudmesh_common.util import check_file_for_tabs, deprecated, path_expand

from cloudmesh_common.util import deprecated

from cloudmesh_install.util import path_expand

from pymongo import MongoClient
from mongoengine import connect
import os
from cloudmesh_install import config_file


log = LOGGER(__file__)

# todo: rename get_mongo_db to connect_to_mongo ...

# todo:
# why not "pymongo" and "mongoengine"
MONGOCLIENT = 0
MONGOENGINE = 1

class DBConnFactory(object):
    connectors = {}
    DBCONFIG = None
    TYPE_MONGOCLIENT = MONGOCLIENT
    TYPE_MONGOENGINE = MONGOENGINE

    @classmethod
    def getconn(cls, dbname, clientType=MONGOCLIENT):

        # DEBUG
        try:
            import sys
            _args = locals()
            log.debug("[{0}()] called with [{1}]".format(sys._getframe().f_code.co_name,
                                            str(_args)))
        except:
            pass

        dbkey = "%s_%s" % (dbname, clientType)
        if dbkey in cls.connectors:
            # print "RETURNING AN EXISTING DB CONNECTOR FROM FACTORY"
            return cls.connectors[dbkey]
        else:
            conn = None
            if cls.DBCONFIG is None:
                cls.DBCONFIG = {}
                config = cm_config_server().get("cloudmesh.server.mongo")
                cls.DBCONFIG["host"] = config["host"]
                cls.DBCONFIG["port"] = int(config["port"])
                cls.DBCONFIG["username"] = config["username"]
                cls.DBCONFIG["password"] = config["password"]

            if clientType == MONGOCLIENT:
                if cls.DBCONFIG["username"] and cls.DBCONFIG["password"]:
                    uri = "mongodb://{0}:{1}@{2}:{3}/{4}".format(cls.DBCONFIG["username"],
                                                                 cls.DBCONFIG[
                                                                     "password"],
                                                                 cls.DBCONFIG[
                                                                     "host"],
                                                                 cls.DBCONFIG[
                                                                     "port"],
                                                                 dbname)
                else:
                    uri = "mongodb://{2}:{3}/{4}".format(cls.DBCONFIG["username"],
                                                         cls.DBCONFIG[
                                                             "password"],
                                                         cls.DBCONFIG["host"],
                                                         cls.DBCONFIG["port"],
                                                         dbname)
                try:
                    conn = MongoClient(uri)[dbname]
                except:
                    msg = "Failed to connect to Mongoclient DB:\n\t%s" % uri
                    print(msg)
                    log.error(msg)

            elif clientType == MONGOENGINE:
                try:
                    conn = connect(dbname,
                                   host=cls.DBCONFIG["host"],
                                   port=cls.DBCONFIG["port"],
                                   username=cls.DBCONFIG["username"],
                                   password=cls.DBCONFIG["password"])
                except:
                    msg = "Failed to connect to MongoEngine DB:\n\t%s" % dbname
                    print(msg)
                    log.error(msg)

            cls.connectors[dbkey] = conn
            return conn


def get_mongo_db(mongo_collection, clientType=MONGOCLIENT):
    """
    Read in the mongo db information from the cloudmesh_server.yaml
    """
    # DEBUG
    try:
        import sys
        _args = locals()
        del(_args['self'])
        log.debug("[{0}()] called with [{1}]".format(sys._getframe().f_code.co_name,
                                        str(_args)))
    except:
        pass

    config = cm_config_server().get("cloudmesh.server.mongo")

    db_name = config["collections"][mongo_collection]['db']

    conn = None
    db = DBConnFactory.getconn(db_name, clientType)
    if db:
        conn = db[mongo_collection]
    else:
        try:
            log.debug("connection failed to {0}".format(db_name))
        except:
            pass

    return conn


class cm_config_server(ConfigDict):

    """
    reads the information contained in the file
    cloudmesh_server.yaml
    """
    filename = config_file("/cloudmesh_server.yaml")

    def __init__(self, filename=None):
        if filename is None:
            filename = self.filename
        ConfigDict.__init__(self, filename=filename, kind="server")


def load(kind="user"):
    if kind in ["launcher"]:
        return cm_config_launcher()
    elif kind in ["server"]:
        return cm_config_server()
    elif kind in ["flavor"]:
        return cm_config_flavor()
    elif kind in ["user"]:
        return cm_config()
    else:
        raise("kind not found")


class cm_config_launcher(ConfigDict):

    """
    reads the information contained in the file
    cloudmesh_launcher.yaml
    """
    filename = config_file("/cloudmesh_launcher.yaml")

    def __init__(self, filename=None):
        if filename is None:
            filename = self.filename
        ConfigDict.__init__(self, filename=filename, kind="launcher")


class cm_config_flavor(ConfigDict):

    """
    reads the information contained in the file
    cloudmesh_flavor.yaml
    """
    filename = config_file("/cloudmesh_flavor.yaml")

    def __init__(self, filename=None):
        if filename is None:
            filename = self.filename
        ConfigDict.__init__(self, filename=filename, kind="flavor")


class cm_config(ConfigDict):

    # ----------------------------------------------------------------------
    # global variables
    # ----------------------------------------------------------------------

    filename = config_file('/cloudmesh.yaml')

    # ----------------------------------------------------------------------
    # initialization methods
    # ----------------------------------------------------------------------

    def __init__(self, filename=None):
        if filename is None:
            filename = self.filename
        ConfigDict.__init__(self, filename=filename)

    # ======================================================================
    # Properties
    # ======================================================================

    # ----------------------------------------------------------------------
    # vmname
    # ----------------------------------------------------------------------

    @property
    def vmname(self):
        return "%s-%04d" % (self['cloudmesh']['default']['prefix'],
                            int(self['cloudmesh']['default']['index']))

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
        get_default('india')
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

    def default(self, cloudname):
        return self['cloudmesh']['clouds'][cloudname]['default']

    def cloud(self, cloudname):
        return self['cloudmesh']['clouds'][cloudname] if cloudname in self['cloudmesh']['clouds'] else None

    def cloud_default(self, cloudname, defname):
        cloud = self.cloud(cloudname)
        defaults = cloud['default'] if 'default' in cloud else []
        return defaults[defname] if defname in defaults else None

    def credential(self, name):
        return self.get_data(key=name, expand=True)

    def get_credential(self, cloud=None, expand=False):
        if expand:
            d = self.get("cloudmesh.clouds.{0}.credentials".format(cloud))
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
        print("please user the function cloudnames()")
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

    def rc(self, name):
        kind = self.cloud(name)['cm_type']
        if kind == "openstack":
            return self.rc_openstack(name)
        else:
            print("CLOUDTYPE not supported:", kind)

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


def yaml_attribute_replace(filename='abc.yaml',
                           replacements={}, indent_by=4):
    """ example::

        filename = config_file("/cloudmesh.yaml")
        replacements = {
            "cloudmesh.profile.phone": "hallo",
            }

        yaml_attribute_replace(filename,replacements)

    """
    result = ""

    max_indent = 10
    
    with open(filename, 'r') as f:
        content = f.read()

        
    for replacement in replacements:
        attributes = replacement.split('.')
        found = [''] * max_indent # just a high number
        
        for line in content.split('\n'):
            # find the indentation level
            indent = (len(line) - len(line.lstrip(' '))) / indent_by
            # set all previously higher found indent to '' 
            for x in range(indent,max_indent):
                found[x] = ''
            # get the attribute name    
            attribute = line.split(":")[0].strip()
            # set the attribute name for the indentation level
            found[indent] = attribute
            # create the attribute name from teh indentation levels and remove the traiing .
            name = '.'.join(found).split('..')[0]
            if name == replacement:
                result += "{0}{1}: {2}".format(' ' * indent * indent_by,
                                               attribute,
                                               replacements[replacement])
            else:
                result += line
            result += '\n'
    # for _old, _new in replacements.iteritems():
    #    content = content.replace(_old, _new)

    outfile = open(filename, 'w')
    outfile.write(result)
    outfile.close()


# ----------------------------------------------------------------------
# MAIN METHOD FOR TESTING
# ----------------------------------------------------------------------

if __name__ == "__main__":
    config = cm_config()

    print(config)

    print("= ACTIVE ================")
    print(config.projects('active'))
    print("= COMPLETED ================")
    print(config.projects('completed'))
    print("= INDIA ================")
    print(config.cloud('india'))
    print("= PROFILE ================")
    print(config.get("cloudmesh.profile"))
    print("= CLOUDS ================")
    print(config.cloudnames())
    print("= RC ================")
    print(config.rc('india'))
    print("= DEFAULT ================")
    print(config.default)
    print("= TO FILE ================")
    outfile = config_file("/junk.yaml")
    print(config.write(outfile))
    os.system("cat " + outfile)
    print("= AZURE ================")
    configuration = config.credential('azure')

    print(configuration['username'])

    # print "================="

    # configuration = config.get('india')
    # print configuration

    # print configuration['host']

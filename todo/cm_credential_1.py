from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.config.cm_config import get_mongo_db
from cloudmesh.util.logger import LOGGER
from cloudmesh import banner
from pprint import pprint
import traceback
from cloudmesh.util.encryptdata import encrypt as cm_encrypt
from cloudmesh.util.encryptdata import decrypt as cm_decrypt
from cloudmesh.cm_mongo import cm_mongo

log = LOGGER(__file__)


class CredentialBaseClass (dict):

    def __init__(self, username, cloud, datasource):
        dict.__init__({'username': username,
                       'cloud': cloud,
                       'datasource': datasource})

    def read(self, username, cloud):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()


class CredentialFromYaml(CredentialBaseClass):

    password = None

    def __init__(self,
                 username,
                 cloud,
                 datasource=None,
                 yaml_version=2.0,
                 style=2.0,
                 password=None):
        """datasource is afilename"""
        CredentialBaseClass.__init__(self, username, cloud, datasource)

        self.password = password

        if datasource != None:
            self.filename = datasource
        else:
            self.filename = "~/.cloudmesh/cloudmesh.yaml"

        self.config = ConfigDict(filename=self.filename)

        self.read(username, cloud, style=style)

    def read(self, username, cloud, style=2.0):
        self.style = style
        self['cm'] = {}
        self['cm']['source'] = 'yaml'
        self['cm']['filename'] = self.filename
        self['cm']['kind'] = self.config.get("meta.kind")
        self['cm']['yaml_version'] = self.config.get("meta.yaml_version")

        kind = self['cm']['kind']
        if kind == "clouds":
            self['cm']['filename'] = "~/.cloudmesh/cloudmesh.yaml"
            self.update(self.config.get("cloudmesh.clouds.{0}".format(cloud)))

        elif kind == "server":
            self['cm']['filename'] = "~/.cloudmesh/cloudmesh_server.yaml"
            self.update(
                self.config.get("cloudmesh.server.keystone.{0}".format(cloud)))
        else:
            log.error("kind wrong {0}".format(kind))
        self['cm']['username'] = username
        self['cm']['cloud'] = cloud
        self.clean_cm()
        self.transform_cm(self['cm']['yaml_version'], style)
        # self.remove_default()

    def clean_cm(self):
        '''temporary so we do not have to modify yaml files for now'''
        for key in self.keys():
            if key.startswith('cm_'):
                new_key = key.replace('cm_', '')
                self['cm'][new_key] = self[key]
                del self[key]
    """
    def remove_default(self):
        if 'default' in self.keys():
            del self['default']
    """

    def transform_cm(self, yaml_version, style):
        if yaml_version <= 2.0 and style == 2.0:
            for key in self['cm']:
                new_key = 'cm_' + key
                self[new_key] = self['cm'][key]
            del self['cm']


class CredentialStore(dict):

    password = None

    def __init__(self, username, filename, Credential, style=2.0, password=None):
        config = ConfigDict(filename=filename)
        self.password = password
        self[username] = {}
        for cloud in config.get("cloudmesh.clouds").keys():
            self[username][cloud] = Credential(username,
                                               cloud,
                                               filename,
                                               style=style,
                                               password=self.password)
            self.encrypt(username, cloud, style)

    def encrypt_value(self, username, cloud, variable):
        user_password = self[username][cloud]['credentials'][variable]
        safe_value = cm_encrypt(user_password, self.password)
        self[username][cloud]['credentials'][variable] = safe_value

    def decrypt_value(self, username, cloud, variable):
        user_password = self[username][cloud]['credentials'][variable]
        decrypted_value = cm_decrypt(user_password, self.password)
        return decrypted_value

    def encrypt(self, username, cloud, style):
        if style >= 2.0:
            cloudtype = self[username][cloud]['cm']['type']
            if cloudtype == 'openstack' and self.password != None:
                self.encrypt_value(username, cloud, 'OS_PASSWORD')
            elif cloudtype == 'ec2' and self.password != None:
                self.encrypt_value(username, cloud, 'EC2_ACCESS_KEY')
                self.encrypt_value(username, cloud, 'EC2_SECRET_KEY')

    def credential(self, username, cloud, style=3.0):
        credential = self[username][cloud]['credentials']
        if style >= 2.0:
            cloudtype = self[username][cloud]['cm']['type']
            if cloudtype == 'openstack' and self.password != None:
                password = self.decrypt_value(username, cloud, 'OS_PASSWORD')
                credential['OS_PASSWORD'] = password
            elif cloudtype == 'ec2' and self.password != None:
                access_key = self.decrypt_value(
                    username, cloud, 'EC2_ACCESS_KEY')
                secrest_key = self.decrypt_value(
                    username, cloud, 'EC2_SECRET_KEY')
                credential['EC2_ACCESS_KEY'] = access_key
                credential['EC2_SECERT_KEY'] = secret_key
        return credential


class CredentialFromMongo(CredentialBaseClass):

    def __init__(self, user, cloud, datasource=None):
        """data source is a collectionname in cloudmesh_server.yaml"""
        """if day=tasource is none than use the default on which is ?"""
        raise NotImplementedError()

if __name__ == "__main__":

    # -------------------------------------------------------------------------
    banner("YAML read test")
    # -------------------------------------------------------------------------
    banner("gvonlasz - sierra_openstack_grizzly - old")
    # -------------------------------------------------------------------------
    credential = CredentialFromYaml("gvonlasz", "sierra_openstack_grizzly")
    pprint(credential)

    banner("gvonlasz - sierra_openstack_grizzly - new")
    # -------------------------------------------------------------------------
    credential = CredentialFromYaml(
        "gvonlasz", "sierra_openstack_grizzly", style=3.0)
    pprint(credential)

    print credential['credentials']['OS_USERNAME']

    print credential.keys()

    banner("gvonlasz - hp - old")
    # -------------------------------------------------------------------------
    credential.read("gvonlasz", "hp")

    pprint(credential)

    banner("gvonlasz - hp - new")
    # -------------------------------------------------------------------------
    credential.read("gvonlasz", "hp", style=3.0)

    pprint(credential)

    # -------------------------------------------------------------------------
    banner("testing gets")

    try:
        print "credential cm.b", credential["cm"]["b"]
        pprint(credential)
    except Exception, e:
        print e
        print traceback.format_exc()

    credential["cm"]["b"] = 'b content'
    pprint(credential)

    banner("testing gets")

    # ---------------------------------------------

    banner("credentialstore")
    store = CredentialStore("gvonlasz",
                            "~/.cloudmesh/cloudmesh.yaml",
                            CredentialFromYaml,
                            style=3.0,
                            password="hallo")

    pprint(store)

    print store["gvonlasz"]["hp"]["credentials"]
    print store.credential("gvonlasz", "hp")

    #
    # experimenting to store yaml to mongo
    #

    collection = 'store'
    username = 'gvonlasz'

    db = get_mongo_db(collection)

    d = {'cm_user_id': username}

    # db.remove({'cm_user_id': username})
    db.update({'cm_user_id': username},
              {'cm_user_id': username,
               'clouds': store[username]},
              upsert=True)

    entries = db.find({})

    for e in entries:
        pprint(e)

    print entries.count()

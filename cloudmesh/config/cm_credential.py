from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.config.cm_config import get_mongo_db
from cloudmesh.util.logger import LOGGER
from cloudmesh.util.util import banner
from pprint import pprint
import traceback
from cloudmesh.util.encryptdata import encrypt as cm_encrypt
from cloudmesh.util.encryptdata import decrypt as cm_decrypt
from cloudmesh.cm_mongo import cm_mongo

log = LOGGER(__file__)

class UserBaseClass (dict):

    def __init__(self, username, datasource):
        dict.__init__({'username': username, 'datasource': datasource})

    def read(self, username, cloud):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()

class UserFromYaml(UserBaseClass):

    password = None

    def __init__(self,
                 username,
                 datasource=None,
                 password=None):
        """datasource is afilename"""
        UserBaseClass.__init__(self, username, datasource)

        self.password = password

        if datasource != None:
            self.filename = datasource
        else:
            self.filename = "~/.futuregrid/cloudmesh.yaml"

        config = ConfigDict(filename=self.filename)

        for key in config['cloudmesh']:
            self[key] = config['cloudmesh'][key]
        self['cm_user_id'] = username


class UserStore(dict):

    password = None
    User = None

    def __init__(self, UserFrom, password=None):
        self.password = password
        self.User = UserFrom

    def add(self, user, datasource=None, password=None):

        if (password is None) and (self.password is not None):
            password = self.password

        user = self.User(user, datasource, password)
        username = user['cm_user_id']
        self[username] = {}
        self[username].update(user)
        if password is not None:
            for cloud in self[username]['clouds']:
                self.encrypt(username, cloud, password)

    def check_keys(self, d, keys):
        for key in keys:
            if key not in d:
                error = error + "Key {0} is not in the cloud definition\n"
        if error != '':
            log.error("Cloud definition incomplete \n")
            log.error(error)
        return (error != '')

    def add_cloud_from_dict(self, d, password=password):
        #
        # check
        #
        if not check_keys(d, ['cm_heading',
                              'cm_host',
                              'cm_label',
                              'cm_type',
                              'cm_type_version',
                              'credentials']):
            return
        if d['cm_type'] == 'openstack':
            if not check_keys(d, ['OS_TENANT_NAME',
                                  'OS_USERNAME',
                                  'OS_PASSWORD',
                                  'OS_AUTH_URL']):
                return
        elif d['cm_type'] == 'ec2':
            if not check_keys(d, ['EC2_ACCESS_KEY',
                                  'EC2_SECRET_KEY',
                                  'EC2_URL']):
                return

        self[username]['clouds'][cloud] = d
        self.encrypt(username, cloud, password)


    def encrypt(self, username, cloud, password):
        cloudtype = self[username]['clouds'][cloud]['cm_type']
        if cloudtype == 'openstack' and password != None:
            self.encrypt_value(username, cloud, 'OS_PASSWORD', password)
        elif cloudtype == 'ec2' and password != None:
            self.encrypt_value(username, cloud, 'EC2_ACCESS_KEY', password)
            self.encrypt_value(username, cloud, 'EC2_SECRET_KEY', password)

    def encrypt_value(self, username, cloud, variable, password):
        user_password = self[username]['clouds'][cloud]['credentials'][variable]
        safe_value = cm_encrypt(user_password, password)
        self[username]['clouds'][cloud]['credentials'][variable] = safe_value

    def decrypt_value(self, username, cloud, variable, password):
        user_password = self[username]['clouds'][cloud]['credentials'][variable]
        decrypted_value = cm_decrypt(user_password, password)
        return decrypted_value


    def credential(self, username, cloud, password=None):
        credential = self[username]['clouds'][cloud]['credentials']
        cloudtype = self[username]['clouds'][cloud]['cm_type']
        if cloudtype == 'openstack' and self.password != None:
            password = self.decrypt_value(username, cloud, 'OS_PASSWORD', password)
            credential['OS_PASSWORD'] = password
        elif cloudtype == 'ec2' and self.password != None:
            access_key = self.decrypt_value(username, cloud, 'EC2_ACCESS_KEY', password)
            secrest_key = self.decrypt_value(username, cloud, 'EC2_SECRET_KEY', password)
            credential['EC2_ACCESS_KEY'] = access_key
            credential['EC2_SECERT_KEY'] = secret_key
        return credential

'''

class CredentialFromMongo(UserBaseClass):

    def __init__(self, user, cloud, datasource=None):
        """data source is a collectionname in cloudmesh_server.yaml"""
        """if day=tasource is none than use the default on which is ?"""
        raise NotImplementedError()
'''

if __name__ == "__main__":

    # -------------------------------------------------------------------------
    banner("YAML read test")
    # -------------------------------------------------------------------------
    user = UserFromYaml("gvonlasz")
    pprint (user)


    store = UserStore(UserFromYaml, password="hallo")
    store.add("gvonlasz", "~/.futuregrid/cloudmesh.yaml", password="Hallo")

    banner("credentialstore")
    pprint (store)

    banner("gvonlasz - hp")
    # -------------------------------------------------------------------------
    cred = store.credential("gvonlasz", "hp", password="Hallo")

    pprint (cred)


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


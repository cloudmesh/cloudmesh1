from cloudmesh_base.ConfigDict import ConfigDict
from cloudmesh.config.cm_config import get_mongo_db
from cloudmesh_base.logger import LOGGER
from cloudmesh_base.util import banner
from pprint import pprint
import traceback
from cloudmesh.util.encryptdata import encrypt as cm_encrypt
from cloudmesh.util.encryptdata import decrypt as cm_decrypt
from cloudmesh.cm_mongo import cm_mongo

log = LOGGER(__file__)


class UserStoreBaseClass (dict):

    def __init__(self, username, datasource):
        dict.__init__({'username': username, 'datasource': datasource})

    def get(self, username, cloud, password=None):
        """
        returns the information about a cloud for a user.
        Certain fields are encrypted which will be decrypted by the password.
        """
        raise NotImplementedError()

    def set(self, username, cloud, password=None):
        """
        Sets the information about a cloud for a user.
        Certain fields are encrypted by the password.
        """
        raise NotImplementedError()


class UserFromYaml(dict):

    password = None

    def __init__(self,
                 username,
                 datasource=None,
                 password=None):
        """datasource is afilename"""
        dict.__init__(self)
        self['username'] = username
        self['datasource'] = datasource

        self.password = password

        if datasource is not None:
            self.filename = datasource
        else:
            self.filename = "~/.cloudmesh/cloudmesh.yaml"

        config = ConfigDict(filename=self.filename)

        for key in config['cloudmesh']:
            self[key] = config['cloudmesh'][key]
        self['cm_user_id'] = username


class UserDictStore(dict):

    password = None
    User = None

    def __init__(self, UserFrom, password=None):
        self.password = password
        self.User = UserFrom

    def set(self, user, datasource=None, password=None):

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

    def add_cloud_from_dict(self, username, d, password=password):
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
        if cloudtype == 'openstack' and password is not None:
            self.encrypt_value(username, cloud, 'OS_PASSWORD', password)
        elif cloudtype == 'ec2' and password is not None:
            self.encrypt_value(username, cloud, 'EC2_ACCESS_KEY', password)
            self.encrypt_value(username, cloud, 'EC2_SECRET_KEY', password)

    def encrypt_value(self, username, cloud, variable, password):
        user_password = self[username]['clouds'][
            cloud]['credentials'][variable]
        safe_value = cm_encrypt(user_password, password)
        self[username]['clouds'][cloud]['credentials'][variable] = safe_value

    def decrypt_value(self, username, cloud, variable, password):
        user_password = self[username]['clouds'][
            cloud]['credentials'][variable]
        decrypted_value = cm_decrypt(user_password, password)
        return decrypted_value

    def credential(self, username, cloud, password=None):
        credential = self[username]['clouds'][cloud]['credentials']
        cloudtype = self[username]['clouds'][cloud]['cm_type']
        if cloudtype == 'openstack' and self.password is not None:
            password = self.decrypt_value(
                username, cloud, 'OS_PASSWORD', password)
            credential['OS_PASSWORD'] = password
        elif cloudtype == 'ec2' and self.password is not None:
            access_key = self.decrypt_value(
                username, cloud, 'EC2_ACCESS_KEY', password)
            secrest_key = self.decrypt_value(
                username, cloud, 'EC2_SECRET_KEY', password)
            credential['EC2_ACCESS_KEY'] = access_key
            credential['EC2_SECERT_KEY'] = secret_key
        return credential


class UserMongoStore():

    def __init__(self, password=None):
        self.password = password
        collection = 'store'
        self.db = get_mongo_db(collection)

    def set(self, username, d, password=None):
        if password is None and self.password is not None:
            password = self.password

        d['cm_user_id'] = username
        self.db.update({'cm_user_id': username}, d, upsert=True)

    def delete(self, username):
        self.db.remove({'cm_user_id': username})

    def credential(self, username, cloud, password=None):
        user = self.get(username)

        credential = user['clouds'][cloud]['credentials']
        print credential

        cloudtype = user['clouds'][cloud]['cm_type']
        print cloudtype

        if password is None and self.password is not None:
            password = self.password

        if cloudtype == 'openstack' and self.password is not None:
            password = self.decrypt_value(user, cloud, 'OS_PASSWORD', password)
            credential['OS_PASSWORD'] = password
        elif cloudtype == 'ec2' and self.password is not None:
            access_key = self.decrypt_value(
                user, cloud, 'EC2_ACCESS_KEY', password)
            secrest_key = self.decrypt_value(
                user, cloud, 'EC2_SECRET_KEY', password)
            credential['EC2_ACCESS_KEY'] = access_key
            credential['EC2_SECERT_KEY'] = secret_key
        return credential

    def encrypt_value(self, user, cloud, variable, password):
        user_password = user['clouds'][cloud]['credentials'][variable]
        safe_value = cm_encrypt(user_password, password)
        user['clouds'][cloud]['credentials'][variable] = safe_value

    def decrypt_value(self, user, cloud, variable, password):
        user_password = user['clouds'][cloud]['credentials'][variable]
        decrypted_value = cm_decrypt(user_password, password)
        return decrypted_value

    def projects(self, username):
        u = self.get(username)
        return u['projects']

    def active_clouds(self, username):
        u = self.get(username)
        return u['active']

    def default(self, username, cloudname):
        u = self.get(username)
        return u['clouds'][cloudname]['default']

    def get(self, username):
        return self.db.find_one({'cm_user_id': username})


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
    pprint(user)

    store = UserDictStore(UserFromYaml, password="hallo")
    store.set("gvonlasz", "~/.cloudmesh/cloudmesh.yaml", password="Hallo")

    banner("credentialstore")
    pprint(store)

    # banner("gvonlasz - hp")
    # -------------------------------------------------------------------------
    # cred = store.credential("gvonlasz", "hp", password="Hallo")

    # pprint (cred)

    #
    # experimenting to store yaml to mongo
    #

    banner("MONGO")
    collection = 'store'
    username = 'gvonlasz'

    users = UserMongoStore(password="Hallo")

    banner("STORE")
    pprint(store[username])

    users.set(username, store[username])

    user = users.get(username)

    pprint(user)

    banner("MONGO HP")

    cloudname = "hp"

    banner("mongo get user hp")
    pprint(users.get(username)['clouds'][cloudname])

    banner("mongo hp")
    hp = users.credential(username, cloudname, password="Hallo")

    pprint(hp)

    pprint(users.projects(username))
    pprint(users.default(username, cloudname))

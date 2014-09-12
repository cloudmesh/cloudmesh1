from cloudmesh.config.cm_config import cm_config
from string import Template
from cloudmesh.keys.util import get_fingerprint
from cloudmesh.keys.util import key_fingerprint, key_validate
from cloudmesh.cm_mongo import cm_mongo
import os
from cloudmesh_install.util import path_expand


def keytype(name):
    try:
        if name.startswith("ssh"):
            return "string"
        else:
            return "file"
    except:
        return name


def get_key_from_file(filename):
    ret = None
    # existence check
    if os.path.isfile(os.path.expanduser(filename)):
        ret = open(path_expand(filename), "r").read()
    return ret


class cm_keys_base(object):

    def defined(self, name):
        return name in self.names()

    def __delitem__(self, name):
        '''
        deletes the key with the given name. Will not succeed if the key is the default key
        '''
        self.delete(name)

    def __len__(self):
        return len(self.names())

    def no_of_keys(self):
        return len(self.names())


class cm_keys_yaml(cm_keys_base):

    filename = None

    def __init__(self, filename=None):
        """
        initializes based on cm_config and returns pointer
        to the keys dict.
        """

        # Check if the file exists
        self.config = cm_config(filename)

    def _getvalue(self, name):
        '''
        gets key corrosponding to the name
        '''

        if name == 'keys':
            return self.config.get("cloudmesh.keys")
        elif name == 'default':
            key = self.config.get("cloudmesh.keys.default")
        else:
            key = name
        value = self.config.get("cloudmesh.keys.keylist")[key]
        return value

    def __getitem__(self, name):
        '''
        gets key corrosponding to the name
        '''
        value = self._getvalue(name)
        if name != 'keys':
            key_type = keytype(name)

            if key_type == "file":
                value = get_key_from_file(value)

        return value

    def __setitem__(self, name, value):
        '''
        adds new key name and value. If name is already present the value is changed.
        The parameter key_type should  be set to file if you want to read the key from a file.
        '''

        if name == 'default':
            #
            # bug check if the key specified with value exists, otehrwise we can not set it.
            #
            self.config["cloudmesh"]["keys"]["default"] = value
            return

        key_value = value
        key_type = keytype(key_value)
        if key_type == "file":
            try:
                key_value = get_key_from_file(value)
            except:
                print "ERROR: reading key file {0}".format(value)
                return

        self.config["cloudmesh"]["keys"]["keylist"][name] = key_value

    def set(self, name, value, expand=False):
        '''
        adds new key name and value. If name is already present the value is changed.
        The parameter key_type should  be set to file if you want to read the key from a file.
        '''
        self.__setitem__(name, value)
        if expand:
            expanded_value = self.__getitem__(name)
            self.__setitem__(name, expanded_value)

    #
    # logic is wrong
    # * if default deleted than pick next key in the list as default. if no other key exists we can not delete
    # * if we secify regular key it will be removed from yaml
    #
    def delete(self, name):
        '''
        deletes the key with the given name. WIll not succeed if the key is the default key
        '''

        default = self.config.get("cloudmesh.keys.default")
        if name == default:
            print "ERROR: You are trying to delete the default key. Change the default key first"
            return
        else:
            if name in self.config.get("cloudmesh.keys.keylist"):
                print "Proceeding to delete key:", name
                del self.config.get("cloudmesh.keys.keylist")[name]
                return "SUCCESS: Key successfully deleted"
            else:
                print "ERROR: Key not found"
                return

    '''
    def delete(self, name):
        """ not tested"""
        newdefault = False
        if name == 'default':
            key = self.config.get("cloudmesh.keys.default")
            newdefault = True
        else:
            key = name

        del self.config.get("cloudmesh.keys.keylist")[key]

        # ERROR Defalut is not self?
        if newdefault:
            if len(self.config.get("cloudmesh.keys.keylist")) > 0:
                default = self.config.get("cloudmesh.keys.keylist")[0]
        else:
            default = None
    '''

    def setdefault(self, name):
        """
        sets the default key
        """
        self.config["cloudmesh"]["keys"]["default"] = name

    def names(self):
        """
        returns all key names in an list.
        """
        return self.config.get("cloudmesh.keys.keylist").keys()

    def __str__(self):
        """returns the dict in a string representing the project"""
        return str(self.config)

    def default(self):
        """gets the default key"""
        return self.config.get('cloudmesh.keys.default')


class cm_keys_mongo(cm_keys_base):

    def __init__(self, user):
        """
        initializes based on cm_config and returns pointer
        to the keys dict.
        """
        self.mongo = cm_mongo()
        self.user_info = self.mongo.db_user.find_one(
            {'cm_user_id': user}
        )
        self.defaults_info = self.mongo.db_defaults.find_one(
            {'cm_user_id': user}
        )

    # operations are done directly on mongo
    # def write(self):
    #    """writes the updated dict to the config"""
    #    self.config.write()

    def _getvalue(self, name):
        """
        returns value corresponding to the name of the key.
        """
        if name == 'keys':
            return {"default": self.get_default_key(), "keylist": self.user_info["keys"]}
        if name == 'default':
            key = self.defaults_info["key"]
        else:
            key = name
        value = self.user_info["keys"][name]
        return value

    def get_default_key(self):
        """
        returns default key.
        """
        return self.defaults_info["key"]

    def __getitem__(self, name):
        """
        returns the value corresponding to the name of the key
        """
        return self._getvalue(name)

    def __setitem__(self, name, value):
        '''
        adds new key name and value. If name is already present the value is changed.
        The parameter key_type should  be set to file if you want to read the key from a file.
        The parameter persist being set to true will cause all of the changes made locally to be written to mongo.
        '''

        key_value = value
        key_type = keytype(key_value)
        if key_type == "file":
            try:
                key_value = get_key_from_file(value)
            except:
                print "ERROR: reading key file {0}".format(value)
                return

        self.user_info["keys"][name] = key_value

        self.mongo.db_user.update(
            {'_id': self.user_info['_id']},
            {'$set': {'keys': self.user_info["keys"]}},
            upsert=False,
            multi=False
        )

    def set(self, name, value):
        '''
        adds new key name and value. If name is already present the value is changed.
        The parameter key_type should  be set to file if you want to read the key from a file.
        The parameter persist being set to true will cause all of the changes made locally to be written to mongo.
        '''
        self.__setitem__(name, value)

    def __delitem__(self, name):
        '''
        deletes key with given name. Will fail if the key is the default key.
        The parameter persist being set to true will cause all of the changes made locally to be written to mongo.
        '''
        self.delete(name)

    def delete(self, name):
        '''
        adds new key name and value. If name is already present the value is changed.
        The parameter persist being set to true will cause all of the changes made locally to be written to mongo.
        '''
        default = self.get_default_key()
        if name == default:
            print "ERROR: You are trying to delete the default key. Change the default key first"
            return
        else:
            if name in self.user_info["keys"]:
                print "Proceeding to delete key:", name
                del self.user_info["keys"][name]
            else:
                print "ERROR: Key not found"
                return

            self.mongo.db_user.update(
                {'_id': self.user_info['_id']},
                {'$set': {'keys': self.user_info["keys"]}},
                upsert=False,
                multi=False
            )

    def setdefault(self, name):
        """
        sets the default key.

        """
        if name in self.user_info["keys"]:
            self.defaults_info["key"] = name
        else:
            print "ERROR: Key is not there in the key list"
            return

        self.mongo.db_user.update(
            {'_id': self.user_info['_id']},
            {'$set': {'keys': self.user_info["keys"]}},
            upsert=False,
            multi=False
        )
        self.mongo.db_defaults.update(
            {'_id': self.defaults_info['_id']},
            {'$set': {'key': self.defaults_info["key"]}},
            upsert=False,
            multi=False
        )

    def default(self):
        """gets the default key"""
        return self.get_default_key()

    def names(self):
        """returns all key names in an list."""
        return self.user_info["keys"].keys()

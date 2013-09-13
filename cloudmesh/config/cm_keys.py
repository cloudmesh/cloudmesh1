from cloudmesh.config.cm_config import cm_config
import os
from string import Template
import base64
import hashlib
import sys


def key_fingerprint(key_string):
    key = base64.decodestring(key_string)
    fp_plain = hashlib.md5(key).hexdigest()
    return ':'.join(a + b for a, b in zip(fp_plain[::2], fp_plain[1::2]))


def key_validate(keytype, filename):
    keystring = "undefined"
    if keytype.lower() == "file":
        try:
            keystring = open(filename, "r").read()
        except:
            return False
    else:
        # TODO: BUG: what is file?
        keystring = file

    try:

        keytype, key_string, comment = keystring.split()
        data = base64.decodestring(key_string)
        int_len = 4
        str_len = struct.unpack('>I', data[:int_len])[
            0]  # this should return 7

        if data[int_len:int_len + str_len] == keytype:
            return True
    except Exception, e:
        print e
        return False


class cm_keys:

    filename = None

    def __init__(self, filename=None):
        """initializes based on cm_config and returns pointer to the keys dict."""
        # Check if the file exists
        self.config = cm_config(filename)

    def type(self, name):
        try:
            value = self._getvalue(name)
            if value.startswith("ssh"):
                return "string"
            else:
                return "file"
        except:
            return "keys"

    def _getvalue(self, name):
        if name == 'keys':
            return self.config.get("cloudmesh.keys")
        elif name == 'default':
            key = self.config.get("cloudmesh.keys.default")
        else:
            key = name
        value = self.config.get("cloudmesh.keys.keylist")[key]
        return value

    def get_default_key(self):
        return self.config.get("cloudmesh.keys.default")

    def __getitem__(self, name):
        value = self._getvalue(name)
        key_type = self.type(name)

        if key_type == "file":
            value = self._get_key_from_file(value)

        return value

    def __setitem__(self, name, value):
        if name == 'default':
            self.config["cloudmesh"]["keys"]["default"] = value
            return
        else:
            self.config["cloudmesh"]["keys"]["keylist"][name] = value

    def set(self, name, value, expand=False):
        self.__setitem__(name, value)
        if expand:
            expanded_value = self.__getitem__(name)
            self.__setitem__(name, expanded_value)
        print "EXPANDED", expanded_value

    def __delitem__(self, name):
        self.delete(name)

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

    def _path_expand(self, text):
        """ returns a string with expanded variavble """
        template = Template(text)
        result = template.substitute(os.environ)
        result = os.path.expanduser(result)
        return result

    def _get_key_from_file(self, filename):
        return open(self._path_expand(os.path.expanduser(filename)), "r").read()

    def setdefault(self, name):
        """sets the default key"""
        self.config["cloudmesh"]["keys"]["default"] = name

    def default(self):
        """sets the default key"""
        return self.config.userkeys('default')

    def names(self):
        """returns all key names in an array"""
        return self.config.get("cloudmesh.keys.keylist").keys()

    def validate(self, line):
        """validates if a default key os ok and follows 'keyencryptiontype keystring keyname'"""

    def __str__(self):
        """returns the dict in a string representing the project"""
        return str(self.config)

    def write(self):
        """writes the updated dict to the config"""
        self.config.write()

    def fingerprint(self, name):
        value = self.__getitem__(name)
        t, keystring, comment = value.split()
        return key_fingerprint(keystring)

    def defined(self, name):
        return name in self.names()

    def __len__(self):
        return len(self.names())

    def no_of_keys(self):
        return len(self.names())

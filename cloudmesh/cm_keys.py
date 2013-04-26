from cm_config import cm_config
import os
from string import Template
import base64
import hashlib

def key_fingerprint(key_string):
    key = base64.decodestring(key_string)
    fp_plain = hashlib.md5(key).hexdigest()
    return ':'.join(a+b for a,b in zip(fp_plain[::2], fp_plain[1::2]))

def key_validate(type,filename):
    if type.lower() == "file":
        try :
            keystring = open(filename, "r").read()
        except :
            return False
    else :
        keystring = file
    
    try :
        type, key_string, comment = keystring.split()
        data = base64.decodestring(key_string)
        int_len = 4
        str_len = struct.unpack('>I', data[:int_len])[0] # this should return 7

        if data[int_len:int_len+str_len] == type:
            return True
    except Exception, e:
        print e
        return False

class cm_keys:

    def __init__(self, filename=None):
        """initializes based on cm_config and returns pointer to the keys dict."""
        self.filename = filename
        if self.filename == None:
            self.config = cm_config()
        else:
            self.config = cm_config(self.filename)

    def type(self, name):
        try:
            value = self._getvalue(name)
            if value.startswith("ssh"):
                return "string"
            else:
                return "file"
        except:
            return "keys"
        
    def _getvalue (self,name):
        if name == 'keys':
            return self.config.data["cloudmesh"]["keys"]
        elif name == 'default':
            key = self.config.data["cloudmesh"]["keys"]["default"]
        else:
            key = name
        return self.config.data["cloudmesh"]["keys"]["keylist"][key]

    def __getitem__(self,name):

        key_type = self.type(name)
        print "TYPE", key_type
        if key_type == "file":
            filename = self.config.data["cloudmesh"]["keys"]["keylist"][name]
            print "FILENAME", filename
            value = self._get_key_from_file(filename)
        else:
            value = self._getvalue(name)
        print "VALUE", value
        return value
            
    def __setitem__(self, name, value):
        if name == 'default':
            key = self.config.data["cloudmesh"]["keys"]["default"]
        else:
            key = name
        self.config.data["cloudmesh"]["keys"]["keylist"][key] = value

    def _path_expand(self,text):
        """ returns a string with expanded variavble """
        template = Template(text)
        result = template.substitute(os.environ)
        return result

    def _get_key_from_file(self, filename):
        return open(self._path_expand(os.path.expanduser(filename)), "r").read()
                
    def setdefault(self, name):
        """sets the default key"""
        self.config.data["cloudmesh"]["keys"]["default"] = name

    def default(self):
        """sets the default key"""
        return self.config.userkeys('default')
        
    def addkey(self, line, name=None):
        """adds a key with a given name. If no name can be derived from line a unique name is chosen automatically"""

    def addkeyfile(self, filename):
        """adds a key with a given name. If no name can be derived from line a unique name is chosen automatically"""

    def names(self):
        """returns all key names in an array"""
        return self.config.data["cloudmesh"]["keys"]["keylist"].keys()

    def validate(self, line):
        """validates if a default key os ok and follows 'keyencryptiontype keystring keyname'"""

    def __str__(self):
        """returns the dict in a string representing the project"""
        return str(self.config)

    def update(self):
        """writes the updated dict to the config"""
    
    def fingerprint(self, name):
        value = self.__getitem__(name)
        print "XXXXXX", value
        t, keystring, comment = value.split()
        print keystring
        return key_fingerprint(keystring)

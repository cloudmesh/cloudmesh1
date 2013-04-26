from cm_config import cm_config

class cm_keys:

    def __init__(self, filename=None):
        """initializes based on cm_config and returns pointer to the keys dict."""
        self.filename = filename
        if self.filename == None:
            self.config = cm_config()
        else:
            self.config = cm_config(self.filename)

    def set(self, name):
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

class cm_keys:

    def __init__(self):
        """initializes based on cm_config and returns pointer to the keys dict."""
        
    def default(self, name)
        """sets the default key"""
        
    def add(self, line, name=None)
        """adds a key with a given name. If no name can be derived from line a unique name is chosen automatically"""

    def names(self):
        """returns all key names in an array"""

    def validate(self, line):
        """validates if a default key os ok and follows 'keyencryptiontype keystring keyname'"""

    def __str__(self):
        """returns the dict in a string representing the project"""

    def update(self):
        """writes the updated dict to the config"""

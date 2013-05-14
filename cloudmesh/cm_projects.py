class cm_projects:

    def __init__(self, filename=None):
        """initializes based on cm_config and returns pointer to the keys dict."""
        # Check if the file exists
        if filename == None:
            self.config = cm_config()
        else:
            self.filename = self._path_expand(filename)
            try:
                with open(self.filename): pass
            except IOError:
                print 'ERROR: cm_keys, file "%s" does not exist' % self.filename
                sys.exit()
            self.config = cm_config(self.filename)

    @property
    def default(self):
        """returns the default project"""
        
    @default.setter
    def default(self, name):
        """sets the default project"""

    def add(self, name, status="active")
        """adds a project with given status"""

    def names(self, status="active"):
        """returns all projects in an array with a specified status"""

    def __str__(self):
        """returns the dict in a string representing the project"""

    def save(self):
        """writes the updated dict to the config yaml file"""

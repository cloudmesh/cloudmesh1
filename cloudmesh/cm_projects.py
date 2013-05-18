from cm_config import cm_config
from string import Template
import os

class cm_projects:

    def _path_expand(self,text):
        """ returns a string with expanded variavble """
        template = Template(text)
        result = template.substitute(os.environ)
        result = os.path.expanduser(result)
        return result

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
        return self.data['cloudmesh']['projects']['default']

    @default.setter
    def default(self, name):
        """sets the default project"""
        # check if name is in active projects
        # if it is, set the new default project.
        # if it is not through an exception and spit out a nice msg explaining that the default project needs to be set
        self.data['cloudmesh']['projects']['default'] = name

    def add(self, name, status="active"):
        """adds a project with given status"""
        # add the name to the following array (make sure it is an array ;-)
        # self.data['cloudmesh']['projects']['default'][status]
        
    def names(self, status="active"):
        """returns all projects in an array with a specified status"""
        self.data['cloudmesh']['projects']['default'][status]
        
    def __str__(self):
        """returns the dict in a string representing the project"""
        # untested
        text = self.data['cloudmesh']['projects']
        return text
    
    def save(self):
        """writes the updated dict to the config yaml file"""
        # saves back into the same file from which we read.
        # uses the cm_config writer

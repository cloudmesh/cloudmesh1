class cm_projects:

    def __init__(self):
        """initializes based on cm_config and returns pointer to the keys dict."""
        
    def default(self, name)
        """sets the default project"""
        
    def add(self, name, status="active")
        """adds a project with given status"""

    def names(self, status="active"):
        """returns all projects in an array whi it is in a specified status"""

    def validate(self, line):
        """validates if a default project is set"""

    def __str__(self):
        """returns the dict in a string representing the project"""

    def update(self):
        """writes the updated dict to the config"""

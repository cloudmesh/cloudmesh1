class BaseClassLauncher:

    states = ["running", "deploy", "active", "error"]

    def states(self):
        """array of all valid status msges"""
        raise NotImplementedError()
    
    @property
    def status(self):
        """ returns string of status """
        raise NotImplementedError()
    
    @property
    def error(self):
        """returns  the late error msg"""
        raise NotImplementedError()
    
    @property
    def traceback(self):
        """returns the trackeback"""
        raise NotImplementedError()
    
    def run(self, host, recipie):
        """installs the chef stuff"""
        raise NotImplementedError()

class ChefLauncher(BaseclassLauncher):

    def register(self, yamlfilewithchefserverinfo):
        """
        will be in cludmesh_server.yaml in .futuregrid. reade available as
        cm_config_server (If I am not mistaken )
        """
        raise NotImplementedError()

class SimulatorLauncher(BaseclassLauncher):

    def register(self, yamlfilewithchefserverinfo):
        """
        will be in cludmesh_server.yaml in .futuregrid. reade available as
        cm_config_server (If I am not mistaken )
        """
        raise NotImplementedError()

    
    def run(self, host, recipie):
        """installs the chef stuff"""
        print "SimulatorLauncher: run {0}, {1}".format(host, recepie)
        return True

"""
debug = True




if debug:
    provider = SimulaterLauncher
else:
    provider = ChefLauncher
    
launcher = provider()

launcher.run("A", "B")
"""

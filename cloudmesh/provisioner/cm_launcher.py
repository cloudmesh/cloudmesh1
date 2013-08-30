from cloudmesh.config.cm_config import cm_config_server 


class BaseClassLauncher:

    states_list = ["running", "deploy", "active", "error"]

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

class ChefLauncher(BaseClassLauncher):
    def register(self, yamlfilewithchefserverinfo):
        """
        will be in cludmesh_server.yaml in .futuregrid. reade available as
        cm_config_server (If I am not mistaken )
        """
        raise NotImplementedError()

class SimulatorLauncher(BaseClassLauncher):
    def register(self, yamlfilewithchefserverinfo):
        #registering fake data
        self.recipies = {"india-openstack-essex":
                                    [
                                     {"name": "cluster",
                                      "description": "blabla"},
                                     {"name": "hadoop",
                                      "description": "blabla"},
                                     {"name": "whatever",
                                      "description": "blabla"},
                                     ],
                    "sierra-openstack-grizzly": 
                                    [
                                     {"name": "cluster",
                                      "description": "blabla"},
                                     {"name": "hadoop",
                                      "description": "blabla"},
                                     {"name": "whatever",
                                      "description": "blabla"},
                                     ],
                     }
        self.columns = {"india-openstack-essex" :
                       ["name", "description"] ,
                       "sierra-openstack-grizzly":
                        ["name", "description"] 
                        }
        print "SimulatorLuncher: register "
        for host in self.recipies:
            print "host : {}".format(host)
            for recipie in self.recipies[host]:
                for col in self.columns[host]:
                    print col,": ",recipie[col]
        return True        
    
    def run(self, host, recipie):
        """installs the chef stuff"""
        print "SimulatorLauncher: run {0}, {1}".format(host, recipie)
        return True
    
    def states(self):
        """array of all valid status msges"""
        for state in self.states_list:
            print "SimulatorLauncher: states {0}".format(state)
        return self.states_list
    
    @property
    def status(self):
        """ returns string of status - at the moment returning the 0th position value"""
        return_state = self.states_list[0]
        print "Simulalator launcher: status - returning {0}".format(return_state)
        return return_state
    
"""
debug = True




if debug:
    provider = SimulaterLauncher
else:
    provider = ChefLauncher
    
launcher = provider()

launcher.run("A", "B")
"""

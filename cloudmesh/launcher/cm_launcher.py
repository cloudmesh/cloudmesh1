from cloudmesh.config.cm_config import cm_config_launcher
from time  import sleep
from random import randint

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

    def run(self, task_dict):
        print "launching on server {0}, host - {1}".format(task_dict["name"],task_dict["host_list"])
        for task in task_dict["recipies"]:
            print "recipie " + task[0] +" type: " + task[1]
            if task[1]=='vm':
                for state in self.states():                                                              #scheduling only for VM
                    sleep(randint(1,3))
                    self.status = "in state {0}, server - {1}, recipie - {2}, host - {3}".format(state, task_dict["name"], task[0], task_dict["host_list"])
                    print "status: " + self.status
                if state == "error":                                #error message
                    self.error =  "error in state {0}, server - {1}, recipie - {2}, host - {3}".format(state, task_dict["name"], task[0], task_dict["host_list"])
                    self.traceback ="error in state {0}, server - {1}, recipie - {2}, host - {3}".format(state, task_dict["name"], task[0], task_dict["host_list"])
                    print "error and tracebacks"
            else:
                print "failed: at this moment we only launch only vms"

    def states(self):
        """array of all valid status msges"""
        for state in self.states_list:
            print "SimulatorLauncher: states {0}".format(state)
        return self.states_list
    
    @property
    def status(self):
        if self.status != None:
            return self.status
        else:
            return None
        
    @property
    def error(self):
        if self.error != None:
            return self.error
        else:
            return None
    
    @property
    def traceback(self):
        if self.traceback != None:
            return self.traceback
        else:
            return None    
"""
debug = True




if debug:
    provider = SimulaterLauncher
else:
    provider = ChefLauncher
    
launcher = provider()

launcher.run("A", "B")
"""

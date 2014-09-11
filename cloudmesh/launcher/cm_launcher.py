from cloudmesh.config.cm_config import cm_config_launcher
from time import sleep
from random import randint
from cloudmesh.launcher.cm_launcher_db import cm_launcher_db


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
        will be in cludmesh_server.yaml in .cloudmesh. reade available as
        cm_config_server (If I am not mistaken )
        """
        raise NotImplementedError()


class SimulatorLauncher(BaseClassLauncher):

    def __init__(self):
        self.db = cm_launcher_db()

    def set(self, user, host, server, recipie, status, error_message=""):
        query = {}
        query["user"] = user
        query["host"] = host
        query["server"] = server
        query["recipie"] = recipie
        # print query["host"]
        if self.db.find_one(query) == None:
            query["status"] = ""
            query["error"] = ""
            self.db.insert(query)
        status_dict = {"status": status, "error": error_message}
        # print "query, dict", query, status_dict
        self.db.update(query, status_dict)
        print "After Update"
        res = self.db.find(query)
        for r in res:
            print r

    def run(self, task_dict):
        for t in task_dict:
            sleep(randint(1, 3))
            print str(t) + ": " + str(task_dict[t])

#        print "launching on server {0}, host - {1}".format(task_dict["name"], task_dict["host_list"])
#         for task in task_dict["recipies"]:
# print "recipie " + task[0] +" type: " + task[1]
#             if task[1] == 'vm':
# for state in self.states():  # scheduling only for VM
#                     sleep(randint(1, 3))
# self.status = "in state {0}, server - {1}, recipie - {2}, host - {3}".format(state, task_dict["name"], task[0], task_dict["host_list"])
# print "status: " + self.status
#                     error = ""
# if state == "error":  # error message
#                         self.error = "error in state {0}, server - {1}, recipie - {2}, host - {3}".format(state, task_dict["name"],
#                                                                                                           task[0], task_dict["host_list"])
#                         self.traceback = "error in state {0}, server - {1}, recipie - {2}, host - {3}".format(state, task_dict["name"],
#                                                                                                               task[0], task_dict["host_list"])
#                         error = self.error
# print "error and tracebacks"
#                     self.set(task_dict["user"], task_dict["host_list"], task_dict["name"], task[0], state, error_message=error)
#             else:
#                 print "failed: at this moment we only launch only vms"

    def states(self):
        """array of all valid status msges"""
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

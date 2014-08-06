from cloudmesh.experiment.model_group import ExperimentGroup
from cloudmesh_common.logger import LOGGER
from docopt import docopt
from pprint import pprint
from cloudmesh.user.cm_user import cm_user

log = LOGGER(__file__)

def shell_command_experiment_group(arguments):
    """
    Usage:
        group info
        group list [NAME]
        group set NAME
        group add NAME
        group [-i] delete NAME

    Arguments:

        NAME   the name of the group

    Options:

        -v         verbose mode
        
    Description:
        
       group NAME  lists in formation about the group
        
    """

    pprint(arguments)    

    name = arguments["NAME"]
    print name

    username = "gvonlasz"
    user = cm_user()

    if arguments["info"]:
        
        print "Default experiment group:", user.get_defaults(username)["group"]
    
    elif arguments["list"] and name is None:
        print "list"

        
    elif arguments["list"]:
        print "list", name

        experiment = ExperimentGroup (username, name)
        print experiment.to_table(label)    
        
    elif arguments["set"]:
        print "sets the group to the given name, the group must exists"

        user.set_default_attribute(username, "group", "exp-1")
                
    elif arguments["add"]:
        print "adds the group to the given name, the group must not exist."

        user.set_default_attribute(username, "group", "exp-1")

    elif arguments["delete"]:
        print "deletes the entries and ask if -i is specified"

    
        
def main():
    arguments = docopt(shell_command_experiment_group.__doc__)
    shell_command_experiment_group(arguments)

if __name__ == '__main__':
    main()

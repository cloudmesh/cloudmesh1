from cloudmesh.experiment.model_group import ExperimentGroup
from cloudmesh_common.logger import LOGGER
from docopt import docopt
from pprint import pprint
from cloudmesh.user.cm_user import cm_user
from cloudmesh.config.cm_config import cm_config
#from cmd3.shell import cmd3_call

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

    name = arguments["NAME"]

    config = cm_config()
    username = config.username()
    # print username
    user = cm_user()

    if arguments["info"]:

        print "Default experiment group:", user.get_defaults(username)["group"]

    elif arguments["list"] and name is None:

        try:
            name = user.get_defaults(username)["group"]
        except:
            print "ERROR: no default experiment group set"
            return

        experiment = ExperimentGroup(username, name)
        print experiment.to_table(name)

    elif arguments["list"] and name in ["all"]:

        experiment = ExperimentGroup(username, name)
        print experiment.to_table(name)

    elif arguments["list"]:

        experiment = ExperimentGroup(username, name)
        print experiment.to_table(name)

    elif arguments["set"]:
        # "sets the group to the given name, the group must exists"

        user.set_default_attribute(username, "group", name)

    elif arguments["add"]:
        # "adds the group to the given name, the group must not exist."

        user.set_default_attribute(username, "group", name)

    elif arguments["delete"]:
        print "deletes the entries and ask if -i is specified"


def main():
    # cmd3_call(shell_command_experiment_group)
    pass

if __name__ == '__main__':
    main()

from __future__ import print_function
from cloudmesh.experiment.model_group import ExperimentGroup
from cloudmesh_common.logger import LOGGER
from cloudmesh.user.cm_user import cm_user
from cloudmesh.config.cm_config import cm_config

log = LOGGER(__file__)


def shell_command_experiment_group(arguments):
    """
    Usage:
        group info
        group list [NAME] [ATTRIBUTES] [--foramt=TABLEFORMAT]
        group set NAME
        group create NAME
        group [-i] delete NAME
        group add [--name=NAME] KIND LABEL         
        
    Arguments:

        NAME   the name of the group

    Options:

        -v         verbose mode

    Description:

       group NAME  lists in formation about the group

    Example:

       group create experiment_1
       vm start
       last = vm label
       group add experiment_1 vm last

       group create experiment_2
       vm start
       last = vm info label  # prints the vm label /prefix + number
       ipno = vm info ip # prints the ip of the last vm
       ipno = vm info ip gvonlasz_1  # get ip of vm with label gvonlasz_1

       group add expermiment_2 ip ipno

       groups are just tuples

       i can have multiple Kinds in the tuple

    mongoengine

    class groupObject

        def add (... name, kind, attribute ...)
        def printer ( ... kind, printfunction, name...)
        def getter ( .... kind, name)
        
    def getter ( .... kind, name ...)

       if kind == "vm":
          vm = get vm from mongo
          return vm
       elif kind = "image"
          iamge = get image from mongo
          return iamge
       ....

    def vmPrinter ( .... vm ...)

       print vm.ip
       print vm.name
       ....

    def imagePrinter ( .... image ...)

       print image.size
       print image.name
       ....

       

    g = groupObject()
    g.printer("vm", cmPrinter)
    g.printer("image", imagePrinter)

    
       
       
    """

    name = arguments["NAME"]

    config = cm_config()
    username = config.username()
    # print username
    user = cm_user()

    if arguments["info"]:

        print("Default experiment group:", user.get_defaults(username)["group"])

    elif arguments["list"] and name is None:

        try:
            name = user.get_defaults(username)["group"]
        except:
            print("ERROR: no default experiment group set")
            return

        experiment = ExperimentGroup(username, name)
        print(experiment.to_table(name))

    elif arguments["list"] and name in ["all"]:

        experiment = ExperimentGroup(username, name)
        print(experiment.to_table(name))

    elif arguments["list"]:

        experiment = ExperimentGroup(username, name)
        print(experiment.to_table(name))

    elif arguments["set"]:
        # "sets the group to the given name, the group must exists"

        user.set_default_attribute(username, "group", name)

    elif arguments["add"]:
        # "adds the group to the given name, the group must not exist."

        user.set_default_attribute(username, "group", name)

    elif arguments["delete"]:
        print("deletes the entries and ask if -i is specified")


def main():
    # cmd3_call(shell_command_experiment_group)
    pass

if __name__ == '__main__':
    main()

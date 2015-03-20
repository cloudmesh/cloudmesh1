from __future__ import print_function
# from cloudmesh.experiment.model_group import ExperimentGroup
from cloudmesh_base.logger import LOGGER
from cloudmesh.user.cm_user import cm_user
from cloudmesh.config.cm_config import cm_config
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.shell.shellutil import shell_commands_dict_output
from cmd3.console import Console
from pprint import pprint

log = LOGGER(__file__)


def shell_command_experiment_group(arguments):
    """
    ::

      Usage:
          group list [--format=FORMAT]
          group create NAME
          group remove NAME
          group add item NAME TYPE VALUE
          group remove item NAME TYPE VALUE
          group show NAME [TYPE] [--format=FORMAT]

      Arguments:

          NAME    name of the group
          TYPE    type of the item in the group, e.g. vm 
          VALUE   value of item to add, e.g. vm name

      Options:

          -v               verbose mode
          --format=FORMAT  output format: table, json, csv

      Description:

         group list           lists the groups
         group create         creates a new group
         group remove         removes a group
         group add item       addes an item of a type to a group
         group remove item    removes an item of a type from a group
         group show           lists items of a group

      Examples:
          group add item sample vm samplevm
              add vm named samplevm to group sample

          group show sample vm --format=json
              list all VMs of group sample in json format
    """

    """
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
    # Changed the scope of this import.
    from cloudmesh.experiment.group import GroupManagement
    from cloudmesh.experiment.group_usage import add_item_to_group

    name = arguments["NAME"]
    type_ = arguments["TYPE"]
    value = arguments["VALUE"]

    config = cm_config()
    username = config.username()
    # print username
    user = cm_user()

    GroupManage = GroupManagement(username)

    '''
    if arguments["info"]:

        print("Default experiment group:", user.get_defaults(username)["group"])

    '''
    if arguments["list"]:
        try:
            res = GroupManage.get_groups_names_list()
        except Exception, err:
            Console.error(str(err))
            return
        d = {}
        d["groups"] = res

        if arguments['--format']:
            p_format = arguments['--format']
        else:
            p_format = None

        shell_commands_dict_output(username,
                                   d,
                                   print_format=p_format,
                                   table_format="key_list",
                                   indexed=True)

    elif arguments["create"]:
        try:
            GroupManage.create_group(name)
        except Exception, err:
            Console.error(str(err))
            return
        Console.ok("group {0} created".format(name))

    elif arguments['remove'] and not arguments['item']:
        try:
            GroupManage.delete_group(name)
        except Exception, err:
            Console.error(str(err))
            return
        Console.ok("group {0} removed".format(name))

    elif arguments["add"] and arguments['item']:
        try:
            add_item_to_group(username, name, type_, value, refresh=True)
        except Exception, err:
            Console.error(str(err))
            return
        Console.ok("item '{0}' of type '{1}' added to group '{2}'".format(
            value, type_, name))

    elif arguments['show']:
        try:
            res = GroupManage.list_items_of_group(name, _type=type_)
        except Exception, err:
            Console.error(str(err))
            return

        if arguments['--format']:
            p_format = arguments['--format']
        else:
            p_format = None

        shell_commands_dict_output(username,
                                   res,
                                   print_format=p_format,
                                   table_format="key_list",
                                   indexed=True)

    elif arguments["remove"] and arguments['item']:
        try:
            GroupManage.delete_item_of_group(name, type_, value)
        except Exception, err:
            Console.error(str(err))
            return
        Console.ok("item '{0}' of type '{1}' removed from group '{2}'".format(
            value, type_, name))


def main():
    # cmd3_call(shell_command_experiment_group)
    pass


if __name__ == '__main__':
    main()

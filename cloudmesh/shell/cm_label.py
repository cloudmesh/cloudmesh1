from __future__ import print_function
from docopt import docopt
from cloudmesh_base.logger import LOGGER
from cmd3.console import Console
from cloudmesh.config.cm_config import cm_config
from cloudmesh.cm_mongo import cm_mongo

log = LOGGER(__file__)

# TODO: [--width=WIDTH]
# WIDTH   The width of the ID in teh label, padded with 0
def shell_command_label(arguments):
    """
    ::

      Usage:
             label [--prefix=PREFIX] [--id=ID] [--raw]

      Options:

        --prefix=PREFIX    provide the prefix for the label
        --id=ID            provide the start ID which is an integer
        --raw              prints label only

      Description:

          A command to set a prefix and an id for a name of VM. 
          Without a paremeter, it prints a current label.

    """
    try:
        config = cm_config()
    except:
        Console.error("There is a problem with the configuration yaml files")
        return

    username = config['cloudmesh']['profile']['username']

    # print arguments #######
    if arguments['--id'] or arguments['--prefix']:
        id = None
        if arguments['--id']:
            error = False
            try:
                id = int(arguments['--id'])
            except:
                error = True
            if not error:
                if id < 0:
                    error = True
            if error:
                Console.warning("id must be 0 or a positive integer")
                return
        prefix = None
        if arguments['--prefix']:
            prefix = arguments['--prefix']
        _helper(username, prefix=prefix, idx=id, raw=arguments['--raw'])
    else:
        _helper(username, raw=arguments['--raw'])


def _helper(username, prefix=None, idx=None, raw=False):
    mongo = cm_mongo()
    # New activation for userinfo added to cm_mongo.
    # mongo.activate is not required to use vmname() - Sep 25th, 2014
    # mongo.activate(username)
    if not raw:
        if prefix or idx:
            print("updating... next vm name:")
        else:
            print("next vm name:")
    print(mongo.vmname(prefix=prefix, idx=idx, cm_user_id=username))
    


def main():
    arguments = docopt(shell_command_label.__doc__)
    shell_command_label(arguments)

if __name__ == '__main__':
    main()

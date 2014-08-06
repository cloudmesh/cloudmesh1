from cloudmesh_common.logger import LOGGER
from docopt import docopt
from pprint import pprint

log = LOGGER(__file__)

def shell_command_experiment_group(arguments):
    """
    Usage:
        group [NAME]

    Arguments:

        NAME   the name of the group

    Options:

        -v         verbose mode
        
    Description:
        
       group NAME  lists in formation about the group
        
    """

    pprint(arguments)    

def main():
    arguments = docopt(shell_command_experiment_group.__doc__)
    shell_command_experiment_group(arguments)

if __name__ == '__main__':
    main()

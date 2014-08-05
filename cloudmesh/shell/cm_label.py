from docopt import docopt
from cloudmesh_common.util import banner

from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)

def shell_command_label(arguments):
    """
    Usage:
           label [--prefix=PREFIX] [--id=ID] [--width=WIDTH]

    A command to set the prefix and id for creating an automatic lable for VMs.
    Without paremeter it prints the currect label.
    
    Arguments:

      PREFIX     The prefix for the label
      ID         The start ID which is an integer
      WIDTH      The width of the ID in teh label, padded with 0

    Options:

       -v       verbose mode

    """
    print arguments
    banner("not yet implemented")
    return


def main():
    arguments = docopt(shell_command_label.__doc__)
    shell_command_label(arguments)

if __name__ == '__main__':
    main()

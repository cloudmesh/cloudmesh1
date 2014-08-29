from docopt import docopt
from cloudmesh_common.util import banner
from cloudmesh_common.logger import LOGGER
from cmd3.console import Console
from cloudmesh.user.cm_user import cm_user
from cloudmesh.config.cm_config import cm_config

log = LOGGER(__file__)

def shell_command_label(arguments):
    # TODO: [--width=WIDTH]
    # WIDTH   The width of the ID in teh label, padded with 0
    """
    Usage:
           label [--prefix=PREFIX] [--id=ID]

    Options:

      --prefix=PREFIX    provide the prefix for the label
      --id=ID            provide the start ID which is an integer
      
    Description:
    
        A command to set the prefix and id for creating an automatic lable for VMs.
        Without paremeter it prints the currect label.

    """
    try:
        config = cm_config()
    except:
        Console.error("There is a problem with the configuration yaml files")
        return
        
    username = config['cloudmesh']['profile']['username']

    #print arguments #######
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
        update_label(username, prefix=prefix, id=id)
    else:
        print_label(username)

def update_label(username, prefix=None, id=None):
    user_obj = cm_user()
    userdata = user_obj.info(username)
    if prefix != None:
        userdata['defaults']['prefix'] = prefix
    if id != None:
        userdata['defaults']['index'] = id
    user_obj.set_defaults(username, userdata['defaults'])

def print_label(username):
    user_obj = cm_user()
    userdata = user_obj.info(username)
    print "prefix: ", userdata['defaults']['prefix']
    print "index: ", userdata['defaults']['index']




def main():
    arguments = docopt(shell_command_label.__doc__)
    shell_command_label(arguments)

if __name__ == '__main__':
    main()

from docopt import docopt
from cloudmesh_common.util import banner
from cloudmesh.user.cm_user import cm_user
from cloudmesh.config.cm_config import cm_config
from pprint import pprint

from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)


def shell_command_user(arguments):
    """
    Usage:
           user list
           user info [ID]

    Administrative command to lists the users from LDAP

    Arguments:

      list       list the users
      ID         list the user with the given ID

    Options:

       -v       verbose mode

    """

    user = cm_user()

    if (arguments["info"]):

        id = arguments["ID"]
        if id is None:
            config = cm_config()
            id = config.username()
        banner("User Information in Mongo for user: {0}".format(id))
        user = cm_user()
        result = user.info(id)
        pprint(result)

    elif (arguments["list"]):

        user = cm_user()
        list_of_users = user.list_users()
        pprint(list_of_users)
        print
        print "========================="
        num = len(list_of_users)
        print str(num) + " users listed"

    else:
        print "WRONG PARAMETERS"

    return


def main():
    arguments = docopt(shell_command_user.__doc__)
    shell_command_user(arguments)

if __name__ == '__main__':
    main()

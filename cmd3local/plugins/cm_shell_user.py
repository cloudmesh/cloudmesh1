import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
from cloudmesh.util.util import path_expand
from cloudmesh.user.cm_user import cm_user
from cloudmesh.user.cm_template import cm_template
from cloudmesh.util.util import yn_choice
from sh import less
import os
from pprint import pprint

from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_user:

    """opt_example class"""

    def activate_cm_shell_user(self):
        pass

    @command
    def do_user(self, args, arguments):
        """
        Usage:
               user list
               user ID
               
        Administrative command to lists the users from LDAP 

        Arguments:

          list       list the users

          ID         list the user with the given ID

        Options:
           
           -v       verbose mode

        """
        log.info(arguments)
        print "<", args, ">"

        if arguments["ID"] is not None:

            id = arguments["ID"]
            user = cm_user()
            result = user.info(id)
            pprint (result)

        elif (arguments["list"]):
            print  "LIST ALL USERS"

        else:
            print "WRONG PARAMETERS"

        return






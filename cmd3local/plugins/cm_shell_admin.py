import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
from cloudmesh.util.util import path_expand

from jinja2 import Template
from cloudmesh.user.cm_template import cm_template
from cloudmesh.util.util import yn_choice
from sh import less
import os
import string
from random import choice



from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

# Helpers
def generate_password():
    """Credit: http://stackoverflow.com/questions/3854692/generate-password-in-python"""
    chars = string.letters + string.digits
    length = 12
    return ''.join([choice(chars) for _ in range(length)])

def create_user_in_cloud(username, password, cloudname):
    print "Create user {0} in {1}".format(username, cloudname)

def user_exists_in_cloud(username, cloudname):
    return False

def get_user_profile(username):
    return { "portalname": "jrandom",
             "profile": { "firstname": "J. Random",
                          "lastname": "User",
                          "e-mail": "jrandom@example.com" },
             "projects": { "active": [ "fg82", "fg83" ],
                           "competed": [ "fg84" ],
                           "default": "fg82" },
             "keys": { "keylist": { "defkey": "default-ssh-key"},
                       "default": "defkey" } }

class cm_shell_admin:

    """Administrative class"""

    def activate_cm_shell_admin(self):
        pass

    @command
    def do_admin(self, args, arguments):
        """
        Usage:
               admin [force] newuser USERNAME CLOUDNAME CONFIGDIR
               
        Initializes new user in the CLOUDNAME cloud. A cloudmesh.yaml
        file will be generated and placed in CONFIGDIR.

        Arguments:

          newuser    create a new user

          USERNAME   the username of the new user

          CLOUDNAME  the name of the cloud
          
          CONFIGDIR  where to place the cloudmesh.yaml file

          force      force mode does not ask. This may be dangerous.

        Options:
           
           -v       verbose mode

        """
        log.info(arguments)
        print "<", args, ">"

        if arguments["newuser"]:

            new_username = arguments["USERNAME"]
            cloudname = arguments["CLOUDNAME"]
            configdir = arguments["CONFIGDIR"]

            cm_yaml = path_expand('{0}/cloudmesh.yaml'.format(configdir))
            etc_yaml = path_expand("~/.futuregrid/etc/cloudmesh.yaml")
            me_yaml = path_expand("~/.futuregrid/etc/me.yaml")

            if user_exists_in_cloud(new_username, cloudname):
                print "User {0} is already defined in cloud {1}".format(new_username, cloudname)
            else:
                me_values = get_user_profile(new_username)
                new_password = generate_password()
                create_user_in_cloud(new_username, new_password, cloudname)

                me_content = open(me_yaml, 'r').read()
                me_values["password"] = { cloudname: new_password }
                t = Template(me_content)
                print t.render(**me_values)

            return






import types
import textwrap
import inspect
import sys
import importlib
import string
from random import choice

from jinja2 import Template
from docopt import docopt
from cmd3.shell import command
from cloudmesh.util.util import path_expand, yn_choice
from cloudmesh.user.cm_user import cm_user
from cloudmesh.iaas.openstack.cm_idm import keystone


from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

# Helpers
def generate_password():
    """Credit: http://stackoverflow.com/questions/3854692/generate-password-in-python"""
    chars = string.letters + string.digits
    length = 12
    return ''.join([choice(chars) for _ in range(length)])

class cm_shell_admin:

    """Administrative class"""

    def __init__(self):
        self._keystones = { }

    def activate_cm_shell_admin(self):
        pass

    def get_keystone(self, cloudname):
        if cloudname not in self._keystones:
            self._keystones[cloudname] = keystone(cloudname)
        return self._keystones[cloudname]

    def user_exists_in_cloud(self, username, cloudname):
        k = self.get_keystone(cloudname)
        k_id = k.get_user_by_name(username)
        return not k_id is None

    def get_user_profile(self, username):
        cmu = cm_user()
        profile = cmu.info(username)
        return profile

    def create_user_in_keystone(self, username, password, cloudname):
        print "Create user {0} in {1}".format(username, cloudname)


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

            if self.user_exists_in_cloud(new_username, cloudname):
                print "User {0} is already defined in cloud {1}".format(new_username, cloudname)
            else:
                me_values = self.get_user_profile(new_username)
                new_password = generate_password()
                self.create_user_in_keystone(new_username, new_password, cloudname)

                me_content = open(me_yaml, 'r').read()
                me_values["passwords"] = { cloudname: new_password }
                t = Template(me_content)
                print t.render(**me_values)

            return

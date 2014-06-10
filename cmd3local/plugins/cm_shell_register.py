import types
import textwrap
import inspect
import sys
import importlib
import simplejson as json
import time
import cmd
import docopt
import yaml
import subprocess
import getpass
from bson.json_util import dumps
from cmd3.shell import command
from cloudmesh.user.cm_user import cm_user
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from pprint import pprint
from prettytable import PrettyTable
from cm_shell_defaults import cm_shell_defaults

from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)


class cm_shell_register:

    def activate_cm_shell_register(self):
        self.register_command_topic('cloud','register')
        pass
    
    @command
    def do_register(self, args, arguments):
        '''
        Usage:
          register [options] NAME

        Arguments:
          NAME      Name of the cloud to be registered

        Options:
          -a --act      Activate the cloud to be registered
          -d --deact    Deactivate the cloud
        '''

        config = cm_config()
        cm_user_id = config.username()
        user_obj = cm_user()
        user = user_obj.info(cm_user_id)

        cloudtypes = {}
        error = {}
        registered = {}

        cloudname = arguments['NAME']

        # check all the registered clouds.
        for cloud in user['defaults']['registered_clouds']:
            registered[cloud] = True
            if (cloud == cloudname and not (arguments['--act'] or
                                            arguments['--deact'])):
                print "Cloud {0} is already registered.".format(cloud)
                return

        for cloud in config.get("cloudmesh.clouds"):
            cloudtypes[cloud] = \
                config['cloudmesh']['clouds'][cloud]['cm_type']

        # get credentials from cm_user -- files.
        credentials = user_obj.get_credentials(cm_user_id)

        # find if credentials for cloudname are present.
        if cloudname in credentials:
            if 'credential' in credentials[cloudname]:
                # Credentials specified
                credential = credentials[cloudname]['credential']
            else:
                # Credentials not present in files
                credentials[cloudname] = None
        else:
            print 'Please specify the right cloud name.'

        error[cloudname] = ''
        if cloudtypes[cloudname] == "openstack":
            d = {}
            # credentials not present in files.
            if credentials[cloudname] is None:
                print 'This will set credentials.'
                d = {'OS_USERNAME': cm_user_id,
                     'OS_PASSWORD': '',
                     'OS_TENANT_NAME': ''
                     }
                d['OS_PASSWORD'] = getpass.getpass("Please enter password: ")
                d['OS_TENANT_NAME'] = raw_input("Please specify the tenant: ")
                d['CM_CLOUD_TYPE'] = cloudtypes[cloudname]
                user_obj.set_credential(cm_user_id, cloudname, d)
                #

        elif cloudtypes[cloudname] == "ec2":
            error[cloudname] = ''

            d = {"CM_CLOUD_TYPE": cloudtypes[cloudname]}

            if credentials[cloudname] is None:
                d = {'EC2_URL': credential['EC2_URL'],
                     'EC2_ACCESS_KEY': credential['EC2_ACCESS_KEY'],
                     'EC2_SECRET_KEY': credential['EC2_SECRET_KEY']
                     }

                user_obj.set_credential(cm_user_id, cloudname, d)

        mongoClass = cm_mongo()
        cloud = mongoClass.get_cloud(
            cm_user_id=cm_user_id, cloud_name=cloudname, force=True)
        if cloud:
            registered[cloudname] = True
            if cloudname not in user['defaults']['registered_clouds']:
                user['defaults']['registered_clouds'].append(cloudname)
                user_obj.set_defaults(cm_user_id, user['defaults'])
        else:
            registered[cloudname] = False
            print "The cloud could not be registered."

        if registered[cloudname] is True:
            if arguments['--act']:
                try:
                    if cloudname not in user['defaults']['activeclouds']:
                        (user['defaults']['activeclouds']).append(cloudname)
                        user_obj.set_defaults(cm_user_id, user['defaults'])
                        print "Cloud {0} set to active".format(cloudname)
                except:
                    # create_dict(user, "defaults", "activeclouds")
                    log.info("ERROR user defaults activecloud does not exist")
            if arguments['--deact']:
                try:
                    if cloudname in user['defaults']['activeclouds']:
                        active = user['defaults']['activeclouds']
                        active.remove(cloudname)
                        user['defaults']['activeclouds'] = active
                        user_obj.set_defaults(cm_user_id, user['defaults'])
                        print "Cloud {0} deactived".format(cloudname)
                except:
                    # create_dict(user, "defaults", "activeclouds")
                    log.info("ERROR user defaults activecloud does not exist")

        return


def main():
    print "test correct"

if __name__ == "__main__":
    main()

import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
from cloudmesh.util.util import path_expand
from cloudmesh.util.util import banner
from cloudmesh.user.cm_user import cm_user
from cloudmesh.user.cm_template import cm_template
from cloudmesh.util.util import yn_choice
from cloudmesh.config.ConfigDict import ConfigDict
from sh import less
import os
from pprint import pprint
import yaml
import json, ast

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
               user ID me
               user ID yaml
               user ID ldap
               user ID new FORMAT [dict|yaml]

        Administrative command to lists the users from LDAP

        Arguments:

          list       list the users
          ID         list the user with the given ID
          me         specifies to generate the me related yaml file
          yaml       specifie to generate the cloudmesh.yaml file
          ldap       get the specifie to generate the cloudmesh.yaml file
          FORMAT     either me or cloudmesh
          OUTPUT     either yaml or dict

        Options:

           -v       verbose mode

        """

        '''
        def generate(id, basename):
            """id = username"""
            """basename = me, cloudmesh"""

            banner("GENERATE")
            user = cm_user()
            result = user.info(id)

            banner("RESULT")
            pprint (result)


            etc_filename = path_expand("~/.futuregrid/etc/{0}.yaml".format(basename))

            print etc_filename

            t = cm_template(etc_filename)
            out = t.replace(kind='dict', values=result)
            banner("{0} DATA".format(basename))

            return out
        '''

        user = cm_user()

        if (arguments["ID"] is not None) and arguments["me"]:

            out = user.generate_yaml(arguments["ID"], "me")
            print yaml.dump(out,
                            default_flow_style=False)


            # location = path_expand(out_file)
            # yaml_file = open(location, 'w+')
            # print >> yaml_file, yaml.dump(result, default_flow_style=False)
            # yaml_file.close()
            # log.info("Written new yaml file in " + location)

        elif (arguments["ID"] is not None) and arguments["yaml"]:

            print "HJDGHKJHSGHJK"

            # me_local_yaml = ConfigDict("~/.futuregrid/me.yaml")
            # cloudmesh_yaml = ConfigDict("~/.futuregrid/cloudmesh.yaml")

            out = user.generate_yaml(arguments["ID"], "cloudmesh")



            print yaml.dump(out,
                            default_flow_style=False)

            # location = path_expand(out_file)
            # yaml_file = open(location, 'w+')
            # print >> yaml_file, yaml.dump(result, default_flow_style=False)
            # yaml_file.close()
            # log.info("Written new yaml file in " + location)


        elif arguments["ID"] is not None and arguments["ldap"]:

            id = arguments["ID"]
            user = cm_user()
            result = user.info(id)
            pprint (result)

        elif arguments["ID"] is not None and arguments["new"]:

            # read ldap dict

            id = arguments["ID"]
            user = cm_user()
            ldap = user.info(id)


            # read me dict
            me_from_ldap = user.generate_yaml(arguments["ID"], "me")
            banner("ME FROM LDAP")
            pprint (me_from_ldap)


            # banner("LDAP")
            # pprint (ldap)

            me_local_yaml = path_expand("~/.futuregrid/me.yaml")
            if os.path.isfile(me_local_yaml):
                me = dict(ConfigDict(filename=me_local_yaml))
                banner("ME")
                pprint (me)
            else:
                print "WARNING: no file found", me_local_yaml


            new_me = dict(me_from_ldap)

            for key in ['password', 'aws', 'azure', 'username']:
                new_me[key] = me [key]


            banner("NEW")

            new_me["projects"]["completed"] = "fg-None"
            pprint(new_me)



            basename = arguments["FORMAT"]


            etc_filename = path_expand("~/.futuregrid/etc/{0}.yaml".format(basename))



            print etc_filename

            t = cm_template(etc_filename)
            print t
            out = t.replace(kind='dict', values=new_me)


            banner("{0} DATA".format(basename))
            pprint (out)

            banner("yaml")
            print yaml.dump(out, default_flow_style=False)

        elif (arguments["list"]):

             user = cm_user()
             list_of_users = user.list_users()
             pprint (list_of_users)
             print
             print "========================="
             num = len(list_of_users)
             print str(num) + " users listed"

        else:
            print "WRONG PARAMETERS"

        return






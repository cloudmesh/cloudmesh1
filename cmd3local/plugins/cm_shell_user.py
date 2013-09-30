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
               
        Administrative command to lists the users from LDAP 

        Arguments:

          list       list the users
          ID         list the user with the given ID
          me         specifies to generate the me related yaml file
          yaml       specifie to generate the cloudmesh.yaml file
          
        Options:
           
           -v       verbose mode

        """
        def correct_project_names(projects):
            tmp = [ "fg" + str(x) for x in projects]
            return tmp

        def generate(id, basename):
            """id = username"""
            """basename = me, cloudmesh"""

            banner("GENERATE")
            user = cm_user()
            result = user.info(id)

            projects = result["profile"]["projects"]
            try:
                projects["active"] = correct_project_names(projects["active"])
            except Exception, e:
                print e
                pass
            try:
                projects["completed"] = correct_project_names(projects["completed"])
            except:
                pass

            # HACK TO MAKE PROJECTS NOT SIT UNDER PROFILE
            result["projects"] = result["profile"]["projects"]
            del result["profile"]["projects"]

            result["keys"] = result["profile"]["keys"]
            del result["profile"]["keys"]

            result["portalname"] = result["profile"]["cm_user_id"]


            # del result["keys"]["keylist"]["default"]

            banner("RESULT")
            pprint (result)

            etc_filename = path_expand("~/.futuregrid/etc/{0}.yaml".format(basename))

            print etc_filename

            t = cm_template(etc_filename)
            out = t.replace(kind='dict', values=result)
            banner("{0} DATA".format(basename))



            print yaml.dump(out,
                            default_flow_style=False)



        log.info(arguments)
        print "<", args, ">"

        if (arguments["ID"] is not None) and arguments["me"]:

            generate(arguments["ID"], "me")

            # location = path_expand(out_file)
            # yaml_file = open(location, 'w+')
            # print >> yaml_file, yaml.dump(result, default_flow_style=False)
            # yaml_file.close()
            # log.info("Written new yaml file in " + location)

        elif (arguments["ID"] is not None) and arguments["yaml"]:

            generate(arguments["ID"], "cloudmesh")

            # location = path_expand(out_file)
            # yaml_file = open(location, 'w+')
            # print >> yaml_file, yaml.dump(result, default_flow_style=False)
            # yaml_file.close()
            # log.info("Written new yaml file in " + location)

        elif arguments["ID"] is not None:

            id = arguments["ID"]
            user = cm_user()
            result = user.info(id)
            pprint (result)

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






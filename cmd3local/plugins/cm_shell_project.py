import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command

from cloudmesh.config.cm_projects import cm_projects
from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_project:

    """opt_example class"""

    def activate_shell_project(self):
        filename = "$HOME/.futuregrid/cloudmesh.yaml"
        self.projects = cm_projects(filename)
        if self.echo:
            log.info("Reading project information from -> {0}".format(filename))
        pass

    @command
    def do_project(self, args, arguments):
        """
        Usage:
               project json info [NAME] 
               project info [NAME] 
               project members
               project default NAME
               
        Manages the project

        Arguments:

          NAME           The name of a service or server


        Options:

           -v       verbose mode

        """
        #log.info(70 * "-")
        #log.info(arguments)
        #log.info(70 * "-")


        if arguments["default"] and arguments["NAME"]:
            log.info ("delete the project")
            return
        
        if arguments["info"] and arguments["NAME"]:
            log.info ("project info for the NAMED one")
            return

        if arguments["info"] and arguments["NAME"] is None: 
            #log.info ("project info for all")
            if arguments["json"]:
                print self.projects.dump()            
                return
            else:
                print
                print "Project Information"
                print "-------------------"
                
                print
                if self.projects.names("default") is not "" and not []:
                    print "%10s:" % "default", self.projects.names("default")
                else:
                    print "%10s:" % "default", "default is not set, please set it"
                if len(self.projects.names("active")) > 0:
                    print "%10s:" % "projects", ' '.join(self.projects.names("active"))
                if len(self.projects.names("completed")) > 0:
                    print "%10s:" % "completed", ' '.join(self.projects.names("completed"))
                print
            
            return

        if arguments["members"]:
            log.info ("list the project members")
            return


        
        

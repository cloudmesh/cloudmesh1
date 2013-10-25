import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
import cloudmesh

from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_list:

    """opt_example class"""

    def activate_cm_shell_list(self):
        pass

    @command
    def do_list(self, args, arguments):
        """
        Usage:
               list
               list flavors [CLOUDNAME]
               list servers [CLOUDNAME]
               list images [CLOUDNAME]
        
        Arguments:
          CLOUDNAME      name of cloud to be queried
              
        Options:
           -v       verbose mode
           

        """
        log.info(args)

        log.info(arguments)


        if arguments["flavors"]:
            mesh = cloudmesh.mesh()
            mesh.refresh(names=[arguments["CLOUDNAME"]], types=['flavor'])
            flavors = mesh.clouds[arguments["CLOUDNAME"]]['flavor']
            return flavors
            

        if arguments["servers"]:
            mesh = cloudmesh.mesh()
            mesh.refresh(names=[arguments["CLOUDNAME"]], types=['server'])
            servers = mesh.clouds[arguments["CLOUDNAME"]]['server']
            return servers
            

        if arguments["images"]:
            mesh = cloudmesh.mesh()
            mesh.refresh(names=[arguments["CLOUDNAME"]], types=['image'])
            images = mesh.clouds[arguments["CLOUDNAME"]]['image']
            return images
        
        print "choose a valid option"
        print "list"
        print "list flavors"
        print "list servers"
        print "list images"
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
              
               list flavors [CLOUD...] 
               list servers [CLOUD...]
               list images [CLOUD...]
               list [CLOUD...]
                              
        Arguments:
        
                CLOUD    the name of the cloud
                
        Options:

           -v       verbose mode

        """
        log.info(args)

        log.info(arguments)

        if len(arguments["CLOUD"]) == 0:
            print "get all active clouds"
            all = True
            clouds = ['a', 'b']
        else:
            clouds = arguments['CLOUD']

        print clouds

        if arguments["flavors"] or all:
            log.info ("count flavors")
            for cloud in clouds:
                print "cloud: flavors", cloud, None

        if arguments["servers"] or all:
            log.info ("count servers")
            for cloud in clouds:
                print "cloud: servers", cloud, None

        if arguments["images"] or all:
            log.info ("list images")
            for cloud in clouds:
                print "cloud: images", cloud, None




    @command
    def do_count(self, args, arguments):
        """
        Usage: 
               count flavors [CLOUD...]
               count servers [CLOUD...]
               count images [CLOUD...]
               count [CLOUD...]
               
        Arguments:
        
                CLOUD    the name of the cloud
        
        Options:
           -v       verbose mode
           

        """
        log.info(args)

        log.info(arguments)

        if len(arguments["CLOUD"]) == 0:
            print "get all active clouds"
            all = True
            clouds = ['a', 'b']
        else:
            clouds = arguments['CLOUD']

        print clouds

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
        if arguments["flavors"] or all:
            log.info ("count flavors")
            for cloud in clouds:
                print "cloud: flavors", cloud, None

        if arguments["servers"] or all:
            log.info ("count servers")
            for cloud in clouds:
                print "cloud: servers", cloud, None

        if arguments["images"] or all:
            log.info ("list images")
            for cloud in clouds:
                print "cloud: images", cloud, None



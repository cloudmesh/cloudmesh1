import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command

from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_rain:

    """The command handler for rain"""

    def activate_cm_shell_rain(self):
        pass

    @command
    def do_rain(self, args, arguments):
        """
        Usage:
               rain info
               rain list NAME [IMAGE list]
               rain add HOSTLIST IMAGE [LABEL]
               
        Provisioning of the images on 

        Arguments:

          NAME           The name of the server
          IMAGE          The name of the image
          HOSTLIST       The names of hosts
          
        Options:

           -v       verbose mode

        Description:

          rain info

               provides information about the images and servers on
               which rain can be applied

          rain list india01

               list all images that can be provisioned on the server
               with the name india01

          rain add [india01-02] precise64.aaa precise64

               adding the
               
        """
        log.info(arguments)


        if arguments["info"]:
            log.info ("rain info")
            return





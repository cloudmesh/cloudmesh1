import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command

from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)


class cm_shell_rain_old:

    """The command handler for rain_old"""

    def activate_cm_shell_rain_old(self):
        pass

    @command
    def do_rain_old(self, args, arguments):
        """
        Usage:
               rain_old info
               rain_old list NAME [IMAGE list]
               rain_old add HOSTLIST IMAGE [LABEL]

        Provisioning of the images on

        Arguments:

          NAME           The name of the server
          IMAGE          The name of the image
          HOSTLIST       The names of hosts

        Options:

           -v       verbose mode

        Description:

          rain_old info

               provides information about the images and servers on
               which rain_old can be applied

          rain_old list india01

               list all images that can be provisioned on the server
               with the name india01

          rain_old add [india01-02] precise64.aaa precise64

               adding the

        """
        log.info(arguments)

        if arguments["info"]:
            log.info("rain_old info")
            return

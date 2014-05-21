from cloudmesh_common.logger import LOGGER
import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command


log = LOGGER(__file__)


class cm_shell_cloud:

    """opt_example class"""

    def activate_cm_shell_cloud(self):
        self.register_command_topic('cloud','cloud')
        pass

    @command
    def do_cloud(self, args, arguments):
        """
        Usage:
            cloud NOTIMPLEMENTED list
            cloud NOTIMPLEMENTED info [NAME|all]
            cloud NOTIMPLEMENTED NAME
            cloud NOTIMPLEMENTED select
            cloud NOTIMPLEMENTED --on | --off NAME
            cloud NOTIMPLEMENTED on NAME
            cloud NOTIMPLEMENTED off NAME
            cloud NOTIMPLEMENTED add [--format=FORMAT] CLOUD

        Manages the clouds

        Arguments:

          NAME           The name of a service or server
          JSON           A JSON
          CLOUD          The cloud to be added

        Options:

           -v       verbose mode
           --on     Activate the cloud
           --off    Deactivate the cloud
           --format=FORMAT  The format of the activation description.
                            [default: yaml]
        Description:

            cloud list
                Lists the cloud names

            cloud info [NAME]
                Provides the available information about the clouds
                and their status. A cloud can be activated or deactivated.
                If no name is specified the default cloud is used.
                If the name all is used, all clouds are displayed

            cloud NAME
                setst the cloud with the name to the default

            cloud select
                selects a cloud from the name of clouds

            cloud --on | --off NAME
            cloud on NAME
            cloud off NAME
                activates or deactivates a cloud with a given name

            cloud add [--format=FORMAT] CLOUD
                adds a cloud to the list of clouds.
                The format can either be `json` or `yaml`.
        """
        log.info(arguments)
        print "<", args, ">"

        if arguments["set"] or args is None:
            log.info("set the cloud")
            return

        if arguments["--on"] and arguments["NAME"]:
            log.info("activatethe cloud")
            return

        if arguments["--off"] and arguments["NAME"]:
            log.info("activatethe cloud")
            return

        if arguments["info"] and arguments["NAME"]:
            log.info("cloud info")
            return

        if arguments["create"] and arguments["NAME"]:
            log.info("cloud info")
            return

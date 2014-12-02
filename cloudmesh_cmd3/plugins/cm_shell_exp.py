from cmd3.shell import command
from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_exp:

    """opt_example class"""

    def activate_cm_shell_exp(self):
        # self.register_command_topic('cloud','exp')
        pass

    @command
    def do_exp(self, args, arguments):
        """
        Usage:
               exp NOTIMPLEMENTED clean
               exp NOTIMPLEMENTED delete NAME
               exp NOTIMPLEMENTED create [NAME]
               exp NOTIMPLEMENTED info [NAME]
               exp NOTIMPLEMENTED cloud NAME
               exp NOTIMPLEMENTED image NAME
               exp NOTIMPLEMENTED flavour NAME
               exp NOTIMPLEMENTED index NAME
               exp NOTIMPLEMENTED count N

        Manages the vm

        Arguments:

          NAME           The name of a service or server
          N              The number of VMs to be started


        Options:

           -v       verbose mode

        """
        log.info(arguments)

        if arguments["clean"]:
            log.info("clean the vm")
            return

        if arguments["delete"] and arguments["NAME"]:
            log.info("delete the vm")
            return

        if arguments["info"] and arguments["NAME"]:
            log.info("vm info")
            return

        if arguments["create"] and arguments["NAME"]:
            log.info("vm info")
            return

import os
import sys
from cmd3.shell import command
from cloudmesh.user import cm_rc
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.tables import row_table

log = LOGGER(__file__)


class cm_shell_nova:

    """opt_example class"""

    def activate_cm_shell_nova(self):
        self.register_command_topic('cloud','nova')
        pass

    def set_os_environ(cloudname):
        '''Set os environment variables on a given cloudname'''
        try:
            novars = self.rcfile[cloudname]
            for novar in novars:
                os.environ[novar] = novar
                # TEMP CODE FOR CACERT
                if novar == "OS_CACERT":
                    os.environ[novar] =
                    "{0}/.cloudmesh/india-havana-cacert.pem".format(os.environ['HOME'])

    @command
    def do_nova(self, args, arguments):
        """
        Usage:
               nova set     [CLOUD]
               nova info    [CLOUD]          
               nova help
               nova ARGUMENTS               

        A simple wrapper for the openstack nova command

        Arguments:

          ARGUMENTS      The arguments passed to nova
          help           Prints the nova manual
          set            reads the information from the current cloud
                         and updates the environment variables if
                         the cloud is an openstack cloud
          info           the environment values for OS
          
        Options:

           -v       verbose mode

        """
        # log.info(arguments)
        cloud = arguments['CLOUD']

        if arguments["help"]:
            os.system("nova help")
            return
        elif arguments["info"]:
            #
            # prints the current os env variables for nova
            #
            d = {}

            for attribute in ['OS_USER_ID',
                              'OS_USERNAME',
                              'OS_TENANT_NAME',
                              'OS_AUTH_URL',
                              'OS_CACERT',
                              'OS_PASSWORD',
                              'OS_REGION']:
                try:
                    d[attribute] = os.environ[attribute]
                    # d[attribute] = self.rcfiles[cloud or self.cloud][attribute]
                except:
                    log.warning(sys.exc_info())
                    d[attribute] = None
            print row_table(d, order=None, labels=["Variable", "Value"])
            return
        elif arguments["set"]:
            if cloud:   
                self.cloud = cloud

                self.rcfiles = cm_rc.get_rcfiles()
                self.set_os_environ(cloud)

                msg = "{0} is set".format(self.cloud)
                log.info(msg)
                print msg
            else:
                print "CLOUD is required"
            #
            # TODO: implemet
            #
            # cloud = get current default
            # if cloud type is openstack:
            #    credentials = get credentials 
            #    set the credentials in the current os system env variables
            #    
        else:
            os.system("nova {0}".format(arguments["ARGUMENTS"]))
            return


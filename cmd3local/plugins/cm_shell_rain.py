import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
from cloudmesh.cobbler.cobbler_rain import rain_command

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
            rain -h | --help
            rain --version
            rain admin add [LABEL] --file=FILE
            rain admin on HOSTS
            rain admin off HOSTS
            rain admin [-i] delete HOSTS
            rain admin [-i] rm HOSTS
            rain admin list users
            rain admin list projects
            rain admin list roles
            rain admin list hosts [--user=USERS|--project=PROJECTS|--role=ROLE]
                                  [--start=TIME_START]
                                  [--end=TIME_END]
                                  [--format=FORMAT]
            rain admin policy [--user=USERS|--project=PROJECTS|--role=ROLE]
                              (-l HOSTS|-n COUNT)
                              [--start=TIME_START]
                              [--end=TIME_END]
            rain list [--project=PROJECTS] [HOSTS]    
            rain list hosts [--start=TIME_START]
                            [--end=TIME_END]
                            [--format=FORMAT]
            rain status [--short|--summary][--kind=KIND] [HOSTS]
            rain provision --profile=PROFILE HOSTS
            rain provision list (--distro=DISTRO|--kickstart=KICKSTART)
            rain provision --distro=DITRO --kickstart=KICKSTART HOSTS
            rain provision add (--distro=URL|--kickstart=KICk_CONTENT) NAME

        Arguments:
            HOSTS     the list of hosts passed
            LABEL     the label of a host
            COUNT     the count of the bare metal provisioned hosts
            KIND      the kind

        Options:
            -n COUNT     count of teh bare metal hosts to be provisined
            -p PROJECTS  --projects=PROJECTS  
            -u USERS     --user=USERS        Specify users
            -f FILE, --file=FILE  file to be specified
            -i           interactive mode adds a yes/no 
                         question for each host specified
            --role=ROLE            Specify predefined role
            --start=TIME_START     Start time of the reservation, in 
                                   YYYY/MM/DD HH:MM:SS format. [default: current_time]
            --end=TIME_END         End time of the reservation, in 
                                   YYYY/MM/DD HH:MM:SS format. In addition a duration
                                   can be specified if the + sign is the first sign.
                                   The duration will than be added to
                                   the start time. [default: +1d]
            --kind=KIND            Format of the output -png, jpg, pdf. [default:png]
            --format=FORMAT        Format of the output json, cfg. [default:json]

        """

        log.info(arguments)
        log.info(args)

        rain_command(arguments)
        return


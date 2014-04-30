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
            rain -h | --help
            rain --version


            rain admin add [LABEL] -f FILE
            rain admin on HOSTS
            rain admin off HOSTS
            rain admin [-i] delete HOSTS
            rain admin [-i] rm HOSTS

            rain admin list users
            rain admin list projects
            rain admin list roles


            rain admin list hosts  
                         [--user=USERS|--project=PROJECTS|--role=ROLE]
                         [--start=TIME_START]
                         [--end=TIME_END|--duration=DURATION]
                         [--format=(json|cfg)]


            rain list hosts  
                         [--start=TIME_START]
                         [--end=TIME_END|--duration=DURATION]
                         [--format=(json|cfg)]

            rain list [-p PROJECTS] [HOSTS]
            rain list display [--type=png] --file==<file>


            rain status [--short|--summary] [HOSTS]


            rain admin policy   
                         [--user=USERS|--project=PROJECTS|--role=ROLE]
                         (-l HOSTS|-n COUNT) 
                         [--start=TIME_START]
                         [--end=TIME_END|--duration=DURATION]





        Arguments:


             HOSTS     the list of hosts passed
             LABEL     the label of a host
             FILE      file can be  specified as .json file or .cfg file. 
                       The ending of the file determines the format.



        Options:
             -n COUNT     count of teh bare metal hosts to be provisined
             -p           all projects
             -p PROJECTS  --projects=PROJECTS  the projects 
             -u USERS     --user=USERS        Specify users


             -f FILE      --file=FILE  file to be specified
             -i           interactive mode adds a yes/no 
                          question for each host specified
             --role=ROLE                Specify predefined role
             --start=TIME_START        Start time of the reservation, in 
                                    YYYY/MM/DD HH:MM:SS format. 
                                    [default: current_time]
             --end=TIME_END              End time of the reservation, in 
                                    YYYY/MM/DD HH:MM:SS format, 
             --duration=DURATION   ‘+[\d}[d|d]’ format. [default: +1d]
             --type                Type of the output -png, jpg, pdf [default:png]
             --file                Filename of the display output
             --format=(json|cfg}  the format [default:json]


        """





        log.info(arguments)
        log.info(args)

        print "==========="
        print arguments
        print "==========="
        print args


        if arguments["info"]:
            log.info ("rain info")
            return





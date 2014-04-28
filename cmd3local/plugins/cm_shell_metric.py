import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cmd3.shell import command
import cloudmesh
from pprint import pprint
from cloudmesh.util.logger import LOGGER
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from prettytable import PrettyTable


log = LOGGER(__file__)

class cm_shell_metric:

    """opt_example class"""


    def activate_cm_shell_metric(self):
        pass


    @command
    def do_metric(self, args, arguments):
        """
	Usage:
	       metric -u USER
	       metric [-s START] [-e END] [-u USER] [-metric (user|vm|runtime)] [-period (month|day|week)] 

	Arguments:

	       USER      ....
	       START     ....
	       END       ....

	Options:

	       -v       verbose mode

	Description:

	   As a cli version of fg-metric, this module provides usage data with search options.

	  - Excutable name is fg-metric-cli (defined by setup.py).
	  - CM Cloud Mesh would be one of the examples using fg-metric-cli.

	Result:

	      The result of the method is a datastructure specified in a given format.
	      If no format is specified, we return a JSON string of the following format:

	      Basic data structure
	      ====================

	     {
	      "start_date"    :   start date of search    (datetime),
	      "end_date"      :   end date of search      (datetime),
	      "ownerid"       :   portal user id          (str),
	      "metric"        :   selected metric name    (str),
	      "period"        :   monthly, weekly, daily  (str),
	      "clouds"        :   set of clouds           (list)
				[
				    { "service"     :   cloud service name  (str),
				     "hostname"     :   hostname (str),
				     "stats"        :   value (int) }
				     ...
				     ]
	     }

        Example 1.:

	    Get user statistics

	    cm> $ metric -u hrlee        

           
        """
        mesh = cloudmesh.mesh()
        mongo = cm_mongo()
        config = cm_config()
        user = config.username()
        dbDict = self.mongoClass.db_defaults.find_one({'cm_user_id': user})

                print args, arguments
        log.info(arguments)
        log.info(args)
        

def main():
    print "test correct"
    clouds = ['sierra_openstack_grizzly']
    fieldList = ["id", "name", "status"]

    ls = cm_shell_metric()
    ls._printList('image', fieldList, clouds)

if __name__ == "__main__":
    main()


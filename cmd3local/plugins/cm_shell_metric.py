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

    """cm_shell_metric class"""
    """IN DEVELOPMENT"""

    def activate_cm_shell_metric(self):
        pass

    @command
    def do_metric(self, args, arguments):

        """
        Usage:

            metric [CLOUD]
            metric [-s START] [-e END] [-u USER] [-metric (user|vm|runtime)]
            [-period (month|day|week)] [-c CLUSTER]

        Arguments:

            CLOUD               Name of the IaaS cloud e.g. openstack, nimbus, Eucalyptus
            START               First day of filter
            END                 Last day of filter
            USER                portal user id to filter
            (user|vm|runtime)   Metric to view
            (month|day|week)    Time period to view
            CLUSTER             Name of cluster e.g. india, sierra, foxtrot,
            hotel, alamo, lima

        Options:

           -h                   help message

        Description:

           metric command provides usage data with filter options.

        Result:

          The result of the method is a datastructure specified in a given format.
          If no format is specified, we return a JSON string of the following format:

          Basic data structure
          --------------------

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

        Example :

            Get user statistics
            cm> $ metric openstack -c india -u hrlee        

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
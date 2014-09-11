from bson import json_util
import json
import argparse
from pprint import pprint
from datetime import datetime, timedelta
#from fgmetric.shell.CMMetricAPI import CMMetricAPI


class CMMetricREST:

    """

    CMMetricREST
    ============

    Command Line Interface for fg-metric.

    Usage: fg-metric-cli

    Description
    ------------

    As a cli version of fg-metric, this module provides usage data with search options.

    - Excutable name is fg-metric-cli (defined by setup.py).
    - CM Cloud Mesh would be one of the examples using fg-metric-cli.

    Basic data structure
    ---------------------

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

    Example 1. Get user statistics

    $ fg-metric-cli -u hrlee

    """

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    development_status = (2, "Pre-alpha")

    def __init__(self):
        self.default_search_days = 180  # Search usage data for this number
        self.default_search_end = datetime.now(
        )  # Search starts from this date back to days within default_search_days
        self.api = CMMetricAPI()
        self.set_default_options()

    def set_default_options(self):
        self.end_date = self.default_search_end
        self.start_date = self.end_date + timedelta(-self.default_search_days)
        self.metric = 'count runtime cores mem disks'

    def set_argparse(self):
        parser = argparse.ArgumentParser(
            description='Specify search options for usage statistics')
        parser.add_argument(
            '-s', '--s_date', help="start date of search", default=self.start_date)
        parser.add_argument(
            '-e', '--e_date', help="end date of search", default=self.end_date)
        parser.add_argument(
            '-m', '--metric', help="metric name to search", default=self.metric)
        parser.add_argument(
            '-lm', '--listmetrics', help="list of metric possible to search")
        parser.add_argument(
            '-u', '--user', help='owerid (i.e. fg portal id) to search', required=True)
        parser.add_argument('-c', '--cloud', help='cloud name to search')
        parser.add_argument(
            '-lc', '--listclouds', help='list of cloud services possible to search')
        parser.add_argument('-H', '--host', help='host name to search')
        parser.add_argument(
            '-lh', '--listhost', help='list of hostnames possible to search')
        parser.add_argument('-p', '--period', help='search period')
        parser.add_argument(
            '-lp', '--listperiod', help='list of search period')

        args = parser.parse_args()
        self.args = args

        self._set_vars()

    def _set_vars(self):
        self._set_api_vars()
        self._set_dict_vars()

    def _set_api_vars(self):
        args = self.args
        self.api.set_date(args.s_date, args.e_date)
        self.api.set_metric(args.metric)
        self.api.set_user(args.user)
        self.api.set_cloud(args.cloud)
        self.api.set_hostname(args.host)
        self.api.set_period(args.period)

    def _set_dict_vars(self):
        self.result = {
            "start_date":   self.start_date,
            "end_date":   self.end_date,
            "ownerid":   self.args.user,
            "metric":   self.args.metric.split(),
            "period":   self.args.period or "All",
            "clouds":   self.args.cloud or "All",
            "hostname":   self.args.host or "All"
        }

    def get_stats(self):
        self.stats = self.api.get_stats()

    def return_dict(self):
        self.result['stats'] = self.stats
        return json.dumps(self.result, default=json_util.default)


def main():
    cli = CMMetricREST()
    cli.set_argparse()
    cli.get_stats()
    dic = cli.return_dict()
    print dic
    # deserialization
    # print json.loads(dic, object_hook=json_util.object_hook)

if __name__ == "__main__":
    main()

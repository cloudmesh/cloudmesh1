# from fgmetric.shell.FGDatabase import FGDatabase
import sys
from pprint import pprint
# from fgmetric.shell.FGSearch import FGSearch
# from fgmetric.shell.FGInstances import FGInstances


class CMMetricAPI:

    """ CloudMesh Metric Python API

    This API supports usage statistics in CM Metric way, but rely on database query.

    In a nutshell,
    CM Metric retrieves all records on the database and collects matching records on Python programmatically.
    However, CM Metric API retrieves records on the database with search condition, especially 'ownerid' is
    required field to search.
    Mainly, this API calls database with a query look like " select * from instance where start >= date and
    end <= date and ownerid = id "
    Other than that, rest of processes are same as CM Metric.

    return value is python 'dict' type

    Description
    ===========
    CM Metric Python API to provide usage data like CM Metric's cmd tool but through python API.

    Requirement
    ^^^^^^^^^^^
    set_user(ownerid) should be set
    get_stats() returns selected statistics

    Sample Usage
    ^^^^^^^^^^^^
    api = FGMetricAPI()
    api.set_user('hrlee')
    api.set_date('2012-01-01', '2012-12-31')
    api.set_metric('count')
    res = api.get_stats()
    print res

    Development Status :: 2 - Pre-Alpha

    """

    def __init__(self):
        """Initialize processes"""
        self.search = FGSearch()
        self.instances = FGInstances()
        self.init_db()
        self.init_vars()

    def init_db(self):
        """Connect database"""
        self.instances.db.conf()
        self.instances.db.connect()

    def init_vars(self):
        """Initialize variables"""
        self.start_date = None
        self.end_date = None
        self.metric = None
        self.cloud = None
        self.hostname = None
        self.period = None
        self.project = None
        self.userinfo = None
        self.projectinfo = None

    def set_date(self, *dates):
        self.start_date = dates[0]
        self.end_date = dates[1]

    def set_metric(self, name):
        self.metric = name

    def set_user(self, name):
        self.username = name

    def set_project(self, name):
        self.project = name

    def set_cloud(self, name):
        self.cloud = name

    def set_hostname(self, name):
        self.hostname = name

    def get_metric(self):
        # TBD
        return

    def get_cloud(self):
        # TBD
        return

    def set_period(self, name):
        self.period = name

    def get_period(self):
        # TBD
        return

    def set_groupby(self, name):
        self.groupby = name

    def get_groupby(self):
        return self.groupby

    def get_stats(self):
        """Return statistics based on search options.
        'search' object holds user inputs such as an owner id, a host name, etc
        to search.
        'instances' object provides usage data of a single VM instance. With the
        'search' object, instances is refined to provide requested information.

        For example,
        search can hold 'hrlee' user name and date between '2013-01-01' and
        '2013-12-31'.
        instances is going to be selected with these search options.
        """
        ownerids = self._get_ownerids()
        self._get_instances(ownerids)
        self.search.init_stats()
        self._set_search_vars()
        # pprint(vars(self.search.get_filter()))
        self._filtering_stats()
        return self.search.get_metric()

    def get_realtime(self):
        return

    def get_series(self):
        return self.search.get_series()

    def _set_search_vars(self):
        """Set search options.
        - Date
        - Metric
        - Platform (IaaS name i.e. openstack, nimbus, eucalyptus)
        - Nodename (host server name i.e. india, sierra, alamo, foxtrot, hotel)
        - Period (search period i.e. daily, monthly)
        - Group (grouping options i.e. project, ownerid, hostname, platform)
        """

        self.search.set_date([self.start_date, self.end_date])
        self.search.set_metric(self.metric)
        self.search.set_platform(self.cloud)
        self.search.set_nodename(self.hostname)
        self.search.set_period(self.period)
        self.search.set_groupby(self.groupby)

    def _filtering_stats(self):
        """Apply search options to obtain requested usage data
        """
        res = []
        for i in range(0, self.instances.count()):
            instance = self.instances.get_data(
                i, self.search._is_userinfo_needed())[0]
            if not self.search._is_in_date(instance):
                continue
            if not self.search._is_filtered(instance):
                continue
            res.append(self.search.collect(instance))

    def _get_ownerids(self):
        try:
            self.instances.read_userinfo({"username": self.username})
            userinfo = self.instances.userinfo
            ownerids = [element['ownerid'] for element in userinfo]
            return ownerids
        except:
            return None

    def _get_instances(self, ownerids=None):
        if ownerids:
            whereclause = " and ownerid in " + str(tuple(ownerids)) + ""
        else:
            whereclause = ""
        self.instances.read_instances({}, whereclause)

    def get_instances(self):
        return self.instances.instance

    def get_userinfo(self):
        """Return all users"""
        if self.userinfo:
            return self.userinfo
        try:
            # ({}, " group by username ")
            self.instances.read_userinfo_detail()
            self.userinfo = self.instances.get_userinfo()
            return self.userinfo
        except:
            print "failed to read userinfo %s" % sys.exc_info()
            return None

    def get_projectinfo(self):
        """Return all projects"""
        if self.projectinfo:
            return self.projectinfo
        try:
            prj_info = self.instances.get_projectinfo()
            self.projectinfo = prj_info
            return self.projectinfo
            # self.instances.read_projectinfo()
            #self.projectinfo = self.instances.projectinfo
        except:
            print "failed to read project info %s" % sys.exc_info()
            return None

    def _set_dict_vars(self):
        self.result = {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "ownerid": self.username,
            "metric": self.metric,
            "period": self.period or "All",
            "clouds": self.cloud or "All",
            "hostname": self.hostname or "All"
        }
        return self.result

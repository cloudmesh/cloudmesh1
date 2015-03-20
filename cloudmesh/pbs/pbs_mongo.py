from __future__ import print_function
from cloudmesh.pbs.pbs import PBS
from pprint import pprint
from cloudmesh import banner
from cloudmesh.config.cm_config import get_mongo_db
from datetime import datetime


class pbs_mongo:
    hosts = {}
    db_qstat = None
    db_pbsnodes = None
    client = None
    pbs_client = None

    config = None

    def __init__(self, collections=["qstat", "pbsnodes", "qinfo"]):
        self.db_qstat = get_mongo_db(collections[0])
        self.db_pbsnodes = get_mongo_db(collections[1])
        self.db_qinfo = get_mongo_db(collections[2])

    def activate(self, host, user):
        """activates a specific host to be queried"""
        self.pbs_client = PBS(user, host)
        self.hosts[host] = self.pbs_client

    def refresh(self, host, type):
        """refreshes the specified data from the given host"""
        data = None
        if type.startswith("q"):
            data = self.refresh_qstat(host)
        elif type.startswith("n"):
            data = self.refresh_pbsnodes(host)
        elif type.startswith("i"):
            data = self.refresh_qinfo(host)
        else:
            print("type not suported")
        return data

    def refresh_qinfo(self, host):
        '''
        obtains a refreshed qstat data set from the specified host. The result is written into the mongo db.
        :param host: The host on which to execute qstat
        '''

        host_data = dict(self.hosts[host].qinfo(refresh=True))

        for host in host_data:
            self._update_qinfo(host, host_data[host])

    def _update_qinfo(self, host, data):
        time_now = datetime.now()
        self.db_qinfo.remove({"cm_host": host, "cm_kind": "qinfo"}, safe=True)

        for name in data:
            id = "{0}-{1}-qinfo".format(host, name).replace(".", "-")
            data[name]["cm_host"] = host
            data[name]["cm_kind"] = "qinfo"
            data[name]["cm_id"] = id
            data[name]["cm_refresh"] = time_now

            self.db_qinfo.insert(data[name])

    def refresh_qstat(self, host):
        '''
        obtains a refreshed qstat data set from the specified host. The result is written into the mongo db.
        :param host: The host on which to execute qstat
        '''
        time_now = datetime.now()
        data = dict(self.hosts[host].qstat(refresh=True))

        self.db_qstat.remove({"cm_host": host, "cm_kind": "qstat"}, safe=True)
        for name in data:
            banner(name)
            for job in data[name]:
                entry = data[name][job]
                id = "{0}-{1}-qstat".format(host, name).replace(".", "-")
                entry["cm_host"] = name
                entry["cm_kind"] = "qstat"
                entry["cm_id"] = id
                entry["cm_qstat"] = host
                entry["cm_refresh"] = time_now
                self.db_qstat.insert(data[name][job])

    def get(self, host, type):
        """refreshes the specified data from the given host"""
        data = None
        if type.startswith("q"):
            data = self.get_qstat(host)
        elif type.startswith("n"):
            data = self.get_pbsnodes(host)
        elif type.startswith("i"):
            data = self.get_qinfo(host)
        else:
            print("type not suported")
        return data

    def get_qstat(self, host=None):
        '''
        returns the qstat data from the mongo db. The data can be put into the mongo db via refresh
        :param host:
        '''
        if host is None:
            data = self.db_qstat.find({"cm_kind": "qstat"})
        else:
            data = self.db_qstat.find({"cm_host": host, "cm_kind": "qstat"})
        return data

    def get_qinfo(self, host=None):
        '''
        returns the qstat data from the mongo db. The data can be put into the mongo db via refresh
        :param host:
        '''
        if host is None:
            data = self.db_qinfo.find({"cm_kind": "qinfo"})
        else:
            data = self.db_qinfo.find({"cm_host": host, "cm_kind": "qinfo"})
        return data

    def get_pbsnodes(self, host=None):
        '''
        retrieves the pbsnodes data for the ost from mongodb. the data can be put with a refresh method into mongo db.
        :param host:
        '''
        if host is None:
            data = self.db_pbsnodes.find({"cm_kind": "pbsnodes"})
        else:
            data = self.db_pbsnodes.find(
                {"cm_host": host, "cm_kind": "pbsnodes"})
        return data

    def refresh_pbsnodes(self, host):
        '''
        retrieves the qstat data from the host and puts it into mongodb
        :param host:
        '''
        time_now = datetime.now()
        data = self.hosts[host].pbsnodes(refresh=True)
        for name in data:
            print("mongo: add {0}, {1}".format(host,
                                               name))

            id = "{0}-{1}".format(host, name).replace(".", "-")
            data[name]["cm_host"] = host
            data[name]["cm_id"] = id
            data[name]["cm_kind"] = "pbsnodes"
            data[name]["cm_refresh"] = time_now
            self.db_pbsnodes.remove({"cm_id": id}, safe=True)
            self.db_pbsnodes.insert(data[name])

    def delete_qstat(self, host):
        '''
        Deletes the qstat information from mongodb
        :param host:
        '''
        self.db_qstat.remove({"cm_host": host, "cm_kind": "qstat"}, safe=True)

    def delete_pbsnodes(self, host):
        '''
        Deletes the pbsnodes information from mongodb
        :param host:
        '''
        self.db_qstat.remove(
            {"cm_host": host, "cm_kind": "qbsnodes"}, safe=True)

    def clear(self):
        '''
        NOT IMPLEMENTED. clears the mongo db data for pbs and qstat
        '''
        """deletes the data in the collection"""


def main():
    host = "india.futuregrid.org"
    pbs = pbs_mongo()
    pbs.activate(host, "gvonlasz")
    print(pbs.hosts)

    d = pbs.refresh_qstat(host)
    d = pbs.get_qstat(host)
    for e in d:
        pprint(e)

        # d = pbs.refresh_pbsnodes(host)
        # d = pbs.get_pbsnodes(host)
        # for e in d:
        #    pprint(e)


if __name__ == "__main__":
    main()

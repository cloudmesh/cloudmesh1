"""
Fetch cluster's information, for example: temperature, service type and etc.
Currently, FetchCluster only knows existing cluster,
that is ['india', 'bravo', 'echo', 'delta']
If more cluster are added later, this class MUST be modified carefully
"""
from cloudmesh.rack.rack_data import RackData
from cloudmesh.rack.rack_work import RackWork
from time import sleep
import threading
from cloudmesh.rack.queue.tasks import temperature, pbs_service
from cloudmesh.rack.rack_progress import get_temperature_progress, get_service_progress

from cloudmesh_common.logger import LOGGER


log = LOGGER(__file__)


class FetchClusterInfo:

    map_progress = None
    username = None
    data_valid_time = 0

    # default data valid time is set to 1800 seconds
    def __init__(self, username=None, valid_time=1800):
        self.username = username
        self.set_data_valid_time(valid_time)
        self.rackdata = RackData(self.data_valid_time)
        self.rackwork = RackWork(self.username)

    # get/set data valid time in mongo db
    def get_data_valid_time(self):
        return self.data_valid_time

    def set_data_valid_time(self, valid_time):
        self.data_valid_time = valid_time if valid_time > 0 else 0

    # start async call to refresh racks
    def start_async_refresh(self, type, rack_name, server):
        if type == self.rackdata.TEMPERATURE_NAME:
            self.rackdata.mydebug(
                "start_async_refresh, BEGIN delay start server {2} of {1}-{0}".format(type, rack_name, server))
            temperature.apply_async((server, rack_name, 'C'), queue='rack')
            self.rackdata.mydebug(
                "start_async_refresh, END delay start server {2} of {1}-{0}".format(type, rack_name, server))
        elif type == self.rackdata.SERVICE_NAME:
            self.rackdata.mydebug(
                "start_async_refresh, BEGIN delay start pbs_service of {1}-{0}".format(type, rack_name))
            pbs_service.apply_async([rack_name], queue='rack')
            self.rackdata.mydebug(
                "start_async_refresh, END delay start pbs_service of {1}-{0}".format(type, rack_name))
        else:
            log.debug(
                "NOT Supported to refresh {0} status of {1}".format(type, rack_name))

    # refresh rack status data
    def refresh_rack_data(self, type, rack_name):
        self.rackdata.mydebug(
            "enter into refresh_rack_data of {0}-{1}".format(rack_name, type))
        # check the status of 'rack_status'
        refresh_dict = self.rackdata.can_start_refresh(type, rack_name)
        self.map_progress.set_check_refresh_condition()
        if refresh_dict is None:
            return False

        total_hosts = {}
        if type == self.rackdata.TEMPERATURE_NAME:
            for rack_name in refresh_dict:
                if refresh_dict[rack_name]:
                    total_hosts[rack_name] = {
                        "total": 0, "updated": 0, "ratio": 0}
                    # change the status of 'rack_status' to 'refresh'
                    self.rackdata.set_status_start_refresh(type, rack_name)
                    hosts = self.rackdata.inventory.hostlist(rack_name)
                    total_hosts[rack_name]["total"] = len(hosts)
                    self.map_progress.update_data(
                        "temperature_data", {rack_name: total_hosts[rack_name]})
                    # fetch data for each host
                    for server in hosts:
                        self.start_async_refresh(type, rack_name, server)
        elif type == self.rackdata.SERVICE_NAME:
            if reduce(lambda x, y: x or y, [refresh_dict[name] for name in refresh_dict], False):
                for rack_name in refresh_dict:
                    total_hosts[rack_name] = {
                        "total": 0, "updated": 0, "ratio": 0}
                    # change the status of 'rack_status' to 'refresh'
                    self.rackdata.set_status_start_refresh(type, rack_name)
                    hosts = self.rackdata.inventory.hostlist(rack_name)
                    total_hosts[rack_name]["total"] = len(hosts)
                self.map_progress.update_data("service_data", total_hosts)
                # service refresh operation can update all rack ONLY once
                self.start_async_refresh(type, rack_name, None)

        self.rackdata.mydebug(
            "exit from refresh_rack_data of {0}-{1} with refresh data {2}".format(rack_name, type, refresh_dict))

        return True

    # refresh rack temperature
    def refresh_rack_temperature(self, rack_name):
        return self.refresh_rack_data(self.rackdata.TEMPERATURE_NAME, rack_name)

    # refresh rack service
    def refresh_rack_service(self, rack_name):
        return self.refresh_rack_data(self.rackdata.SERVICE_NAME, rack_name)

    # API of generate map
    def start_gen_map(self, service, rack_name):
        t = threading.Thread(
            target=self.gen_map_thread, args=[service, rack_name])
        t.start()
        return True

    # API of refresh map
    # return True means start refresh process
    #        False means NOT start refresh process, "fresh" gives the reason
    #               if "fresh" is True, that means the data in db is fresh, does NOT need a refresh
    #                             Flase, means ERROR occured in db
    def start_refresh_map(self, service, rack_name):
        result = False
        flag_fresh = False
        refresh_dict = self.rackdata.can_start_refresh(service, rack_name)
        if refresh_dict:
            result = reduce(
                lambda x, y: x or y, [refresh_dict[name] for name in refresh_dict], False)
            if result:
                t = threading.Thread(
                    target=self.refresh_map_thread, args=[service, rack_name])
                t.start()
            else:
                flag_fresh = True

        return {"result": result, "fresh": flag_fresh}

    # refresh map thread
    def refresh_map_thread(self, service, rack_name):
        self.get_map_progress(service)
        # self.map_progress.set_refresh_map()
        flag_data_ready = False
        if self.refresh_rack_data(service, rack_name):
            flag_data_ready = self.check_rack_refresh_status(
                service, rack_name)

        if flag_data_ready:
            self.rackwork.generate_map(service, rack_name, True)
        else:
            # refresh error, return to user
            self.map_progress.set_error_status()

    # generate map thread
    def gen_map_thread(self, service, rack_name):
        self.get_map_progress(service)

        flag_read_refresh_data = False
        flag_data_ready = False

        if self.rackdata.is_rack_data_ready(service, rack_name):
            flag_data_ready = True
        else:
            self.map_progress.set_load_refresh_map()
            if self.refresh_rack_data(service, rack_name):
                flag_read_refresh_data = True
                flag_data_ready = self.check_rack_refresh_status(
                    service, rack_name)

        if flag_data_ready:
            self.rackwork.generate_map(
                service, rack_name, flag_read_refresh_data)
        else:
            # read db error, return to user
            self.map_progress.set_error_status()

    # update the status of async  data refresh
    def update_data_refresh_status(self, service):
        data_dict = self.map_progress.get_data("{0}_data".format(service))
        total_count = 0
        total_updated = 0
        for rack_name in data_dict:
            if data_dict[rack_name]["updated"] < data_dict[rack_name]["total"]:
                # query db to get recent update status
                query_dict = self.rackdata.get_rack_query_dict(
                    service, rack_name, self.rackdata.LOCATION_TEMP)
                result_dict = self.rackdata.partly_query(
                    query_dict[rack_name], {"updated_node": 1})
                data_dict[rack_name]["updated"] = result_dict["updated_node"]
            total_count += data_dict[rack_name]["total"]
            total_updated += data_dict[rack_name]["updated"]
        ratio = total_updated * 1.0 / total_count
        self.map_progress.set_async_refresh(round(ratio, 2))

    # check mongo db refresh status
    # default interval time is 200ms, and the max check count is 10000
    def check_rack_refresh_status(self, service, rack_name, interval=0.2, max_count=10000):
        result = False
        curr_count = 1
        while True:
            sleep(interval)  # default is 200 ms
            # check and update async data refresh status
            self.update_data_refresh_status(service)
            if self.rackdata.is_refresh_rack_data_ready(service, rack_name):
                self.map_progress.set_async_refresh()
                result = True
                break
            curr_count += 1
            if curr_count > max_count:
                break
        return result

    def get_map_progress(self, service):
        if service == self.rackdata.TEMPERATURE_NAME:
            self.map_progress = get_temperature_progress(self.username)
        elif service == self.rackdata.SERVICE_NAME:
            self.map_progress = get_service_progress(self.username)

        return self.map_progress


# debug
if __name__ == "__main__":
    config = cm_config()
    mytest = FetchClusterInfo()
    #data = mytest.fetch_temperature_ipmi()
    # print "=" * 30
    # print data
    # print "-" * 30
    mytest.refresh_rack_temperature("echo")

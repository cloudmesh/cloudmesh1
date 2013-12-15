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

from cloudmesh.util.logger import LOGGER


log = LOGGER(__file__)



class FetchClusterInfo:

    map_progress = None

    def __init__(self):
        self.rackdata = RackData()
        self.rackwork = RackWork()
        
    
    # start async call to refresh racks
    def start_async_refresh(self, type, rack_name, server):
        if type == self.rackdata.TEMPERATURE_NAME:
            self.rackdata.mydebug("start_async_refresh, BEGIN delay start server {0} of {1}-{2}".format(server, rack_name, type))
            temperature.apply_async((server, rack_name, 'C'), queue='rack')
            self.rackdata.mydebug("start_async_refresh, END delay start server {0} of {1}-{2}".format(server, rack_name, type))
        elif type == self.rackdata.SERVICE_NAME:
            self.rackdata.mydebug("start_async_refresh, BEGIN delay start server {0} of {1}-{2}".format(server, rack_name, type))
            pbs_service.apply_async([rack_name], queue='rack')
            self.rackdata.mydebug("start_async_refresh, END delay start server {0} of {1}-{2}".format(server, rack_name, type))
        else:
            log.debug("NOT Supported to refresh {0} status of {1}".format(type, rack_name))
    
    
    # refresh rack status data
    def refresh_rack_data(self, type, rack_name, interval_time=1800):
        self.rackdata.mydebug("enter into refresh_rack_data of {0}-{1}".format(rack_name, type))
        # check the status of 'rack_status'
        refresh_dict = self.rackdata.can_start_refresh(type, rack_name, interval_time)
        self.map_progress.set_check_refresh_condition()
        if refresh_dict is None:
            return False
        
        total_hosts = {}
        if type == self.rackdata.TEMPERATURE_NAME:
            for rack_name in refresh_dict:
                if refresh_dict[rack_name]:
                    total_hosts[rack_name] = {"total": 0, "updated": 0, "ratio": 0}
                    # change the status of 'rack_status' to 'refresh'
                    self.rackdata.set_status_start_refresh(type, rack_name)
                    hosts = self.rackdata.inventory.hostlist(rack_name)
                    total_hosts[rack_name]["total"] = len(hosts)
                    self.map_progress.update_data("temperature_data", {rack_name: total_hosts[rack_name]})
                    # fetch data for each host
                    for server in hosts:
                        self.start_async_refresh(type, rack_name, server)
        elif type == self.rackdata.SERVICE_NAME:
            for rack_name in refresh_dict:
                total_hosts[rack_name] = {"total": 0, "updated": 0, "ratio": 0}
                # change the status of 'rack_status' to 'refresh'
                self.rackdata.set_status_start_refresh(type, rack_name)
                hosts = self.rackdata.inventory.hostlist(rack_name)
                total_hosts[rack_name]["total"] = len(hosts)
            self.map_progress.update_data("service_data", total_hosts)
            # service refresh operation can update all rack ONLY once
            self.start_async_refresh(type, rack_name, None)
        
        self.rackdata.mydebug("exit from refresh_rack_data of {0}-{1} with refresh data {2}".format(rack_name, type, refresh_dict))
        
        return True
    
    
    # refresh rack temperature
    def refresh_rack_temperature(self, rack_name, interval_time=1800):
        self.map_progress = get_temperature_progress()
        return self.refresh_rack_data(self.rackdata.TEMPERATURE_NAME, rack_name, interval_time)


    # refresh rack service
    def refresh_rack_service(self, rack_name, interval_time=1800):
        self.map_progress = get_service_progress()
        return self.refresh_rack_data(self.rackdata.SERVICE_NAME, rack_name, interval_time)
    
    
    # API of generate map
    def start_gen_map(self, service, rack_name):
        t = threading.Thread(target=self.gen_map_thread, args=[service, rack_name])
        t.start()
        return True
    
    
    # API of refresh map
    def start_refresh_map(self, service, rack_name):
        result = False
        if self.rackdata.can_start_refresh(service, rack_name):
            t = threading.Thread(target=self.refresh_map_thread, args=[service, rack_name])
            t.start()
            result = True
            
        return result
    
    
    # refresh map thread
    def refresh_map_thread(self, service, rack_name):
        self.get_map_progress(service)
        #self.map_progress.set_refresh_map()
        if self.refresh_rack_data(service, rack_name):
            while True:
                sleep(0.2)  # 200 ms
                if (self.rackdata.is_refresh_rack_data_ready(service, rack_name)):
                    self.map_progress.set_async_refresh()
                    break;
            self.rackwork.generate_map(service, rack_name, True)
        else:
            pass   # process the situation of refresh fail
    
    
    # generate map thread
    def gen_map_thread(self, service, rack_name):
        self.get_map_progress(service)
        
        flag_read_refresh_data = False
        if not self.rackdata.is_rack_data_ready(service, rack_name):
            self.map_progress.set_load_refresh_map()
            if self.refresh_rack_data(service, rack_name):
                flag_read_refresh_data = True
                while True:
                    sleep(0.2)  # 200 ms
                    if (self.rackdata.is_refresh_rack_data_ready(service, rack_name)):
                        self.map_progress.set_async_refresh()
                        break;
        self.rackwork.generate_map(service, rack_name, flag_read_refresh_data)


    def get_map_progress(self, service):
        if service == self.rackdata.TEMPERATURE_NAME:
            self.map_progress = get_temperature_progress()
        elif service == self.rackdata.SERVICE_NAME:
            self.map_progress = get_service_progress()
        
        return self.map_progress
    

# debug
if __name__ == "__main__":
    config = cm_config()
    mytest = FetchClusterInfo()
    #data = mytest.fetch_temperature_ipmi()
    #print "=" * 30
    #print data
    #print "-" * 30
    mytest.refresh_rack_temperature("echo")

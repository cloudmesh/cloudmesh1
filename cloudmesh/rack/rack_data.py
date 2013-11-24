from cloudmesh.inventory import Inventory

from cloudmesh.util.logger import LOGGER
from datetime import datetime, timedelta

log = LOGGER(__file__)

class rack_data:
    # ONLY for debug test
    MY_DEBUG_FLAG       = True
    
    inventory = None
    
    TEMPERATURE_NAME    = "temperature"
    SERVICE_NAME        = "service"
    LOCATION_TEMP       = "temp"
    
    # three status of server refresh
    STATUS_NOT_READY    = "not_ready"
    STATUS_REFRESH      = "refresh"
    STATUS_READY        = "ready"
    
    
    def __init__(self):
        self.inventory = Inventory()
    
    
    def mydebug(self, msg):
        if self.MY_DEBUG_FLAG:
            log.debug(msg)
    
    
    # change refresh status
    def set_status_start_refresh(self, service_type, rack_name):
        self.mydebug("set status start refresh for {0}-{1}".format(rack_name, service_type))
        query_dict = self.get_rack_query_dict(service_type, rack_name, self.LOCATION_TEMP)
        rack_info_dict = self.get_rack_info(query_dict)
        element = {
                     "rack_status"  : self.STATUS_REFRESH,
                     "updated_node" : 0,
                     "cm_refresh"   : datetime.now(),
                   }
        racks = self.inventory.get_clusters(rack_name)
        element['data'] = dict((h, None) for h in racks[0]['cm_value'])
        self.partly_update(query_dict[rack_name], {"$set": element})
    
    
    # get valid list of rack name
    # result: if rack_name is 'all', then ['india', 'echo', ...]
    #         else if rack_name is a valid rack name, then ['rack_name.lower()']
    #         else None
    def get_rack_name_list(self, rack_name):
        self.mydebug("enter into get_rack_name_list of {0}".format(rack_name))
        racks = self.inventory.get_clusters()
        rack_name_list = [rack['cm_cluster'] for rack in racks]
        rack_name_lower = rack_name.lower()
        if rack_name_lower != 'all':
            rack_name_list = [rack_name_lower] if rack_name_lower in rack_name_list else None
        
        self.mydebug("exit from get_rack_name_list {0}".format(rack_name_list))
        return rack_name_list
    
    
    # generate a query dict to query the rack table in inventory
    # location: 'temp' means cm_key is 'rack_temp_*' which is a temporary status table
    #           None means cm_key is 'rack_*', which is a permanent status table
    # result: if rack_name is 'all', then {"india": {query ...}, "echo": {query ...}, ... }
    #         else if rack_name is valid then {"rack_name": {query ...}}
    #         else None
    def get_rack_query_dict(self, service_type, rack_name, location=None):
        rack_name_list = self.get_rack_name_list(rack_name)
        if rack_name_list is None:
            return None
        
        query_dict = {}
        for rack_name in rack_name_list:
            query = {
                       "cm_type" : "inventory",
                       "cm_kind" : "rack",
                       "cm_id"   : rack_name
                    }
            if location:
                query["cm_key"] = "rack_{0}_{1}".format(location, service_type)
            else:
                query["cm_key"] = "rack_{0}".format(service_type)
            
            query_dict[rack_name] = query
        
        self.mydebug("get_rack_query_dict of {0}".format(query_dict))
        return query_dict
    
    
    def get_rack_info(self, query_dict):
        if query_dict is None:
            return None
        
        rack_info_dict = {}
        for rack_name in query_dict:
            rack_info_dict[rack_name] = self.inventory.find_one(query_dict[rack_name])
        
        self.mydebug("get_rack_info of {0}".format(rack_info_dict.keys()))
        return rack_info_dict
    
    # result: {'rack_name': True, 'rack_name': False, ...}
    def can_start_refresh(self, service_type, rack_name, interval_time=1800):
        self.mydebug("enter into can_start_refresh og {0}-{1}".format(rack_name, service_type))
        query_dict = self.get_rack_query_dict(service_type, rack_name, self.LOCATION_TEMP)
        rack_info_dict = self.get_rack_info(query_dict)
        if rack_info_dict is None:
            return None
        
        refresh_dict = {}
        for rack_name in rack_info_dict:
            flag_refresh = False
            rack_info = rack_info_dict[rack_name]
            status = rack_info['rack_status']
            if status == self.STATUS_NOT_READY:
                flag_refresh = True
            elif status == self.STATUS_READY:
                time_now = datetime.now()
                prev_refresh_time = rack_info['cm_refresh']
                time_interval = timedelta(seconds=interval_time)
                if (time_now > prev_refresh_time + time_interval):
                    flag_refresh = True
            refresh_dict[rack_name] = flag_refresh
        
        self.mydebug("can_start_refresh of {0}".format(refresh_dict))
        return refresh_dict
    
    # update a part of document in database
    def partly_update(self, query, value, flag_upsert=False, flag_multi=False):
        if not value:
            return self.inventory.update(query)
        
        return self.inventory.db_inventory.update(query, value, upsert=flag_upsert, multi=flag_multi)
    
    
    # NOT support to update 'all'
    # The update of 'all' MUST be divided into serveral updates of each independent rack of 'all'
    # update the information of a server
    def server_refresh_update_data(self, service_type, rack_name, server, data):
        self.mydebug("enter into server_refresh_update_data update server {0} for {1}-{2}".format(server, rack_name, service_type))
        flag_refresh_success = False
        query_dict = self.get_rack_query_dict(service_type, rack_name, self.LOCATION_TEMP)
        rack_info_dict = self.get_rack_info(query_dict)
        rack_info = None
        if rack_info_dict:
            rack_info = rack_info_dict[rack_name]
        
        if rack_info:
            time_now = datetime.now()
            element = {}
            element['cm_refresh'] = time_now
            element['data.{0}'.format(server)] = data
            # atomic update
            update_result = self.inventory.db_inventory.find_and_modify(query=query_dict[rack_name], update={'$inc': {'updated_node': 1}, '$set': element}, new=True, fields={'updated_node': 1})
            if update_result['updated_node'] == rack_info['max_node']:
                self.partly_update(query_dict[rack_name], {'$set': {'rack_status': self.STATUS_READY}})
                flag_refresh_success = True
            
            # update the normal record, which provides information to WEB page
            # After data of all servers in this rack are collected
            if flag_refresh_success:
                query_dict = self.get_rack_query_dict(service_type, rack_name)
                element = {}
                element['rack_status'] = self.STATUS_READY
                element['cm_refresh'] = time_now
                rack_info['data'][server] = data
                element['data'] = rack_info['data']
                self.mydebug("server_refresh_update_data, update rack {0} with data".format(rack_name))
                self.partly_update(query_dict[rack_name], {'$set': element})
            
        return flag_refresh_success
    
    
    # update the temperature of a server
    def server_refresh_update_temperature(self, rack_name, server, data):
        self.server_refresh_update_data(self.TEMPERATURE_NAME, rack_name, server, data)
    
    
    # update the service of a server
    def server_refresh_update_service(self, rack_name, server, data):
        self.server_refresh_update_data(self.SERVICE_NAME, rack_name, server, data)
    
    
    # get data of a rack
    def get_rack_status_data(self, service_type, rack_name):
        rack_info_dict = self.get_rack_info(self.get_rack_query_dict(service_type, rack_name))
        if rack_info_dict is None:
            return None
        
        dict_result = {}
        for rack_name in rack_info_dict:
            dict_result[rack_name] = rack_info_dict[rack_name]["data"]
        
        self.mydebug("exit from get_rack_status_data {0}-{1} with data".format(rack_name, service_type))
        return dict_result
    
    # get temperature data of a rack
    def get_rack_temperature_data(self, rack_name):
        return self.get_rack_status_data(self.TEMPERATURE_NAME, rack_name)
    
    # get service data of a rack
    def get_rack_service_data(self, rack_name):
        return self.get_rack_status_data(self.SERVICE_NAME, rack_name)
    
    # whether the data of a rack is ready or not
    def is_rack_data_ready(self, service_type, rack_name):
        rack_info_dict = self.get_rack_info(self.get_rack_query_dict(service_type, rack_name))
        if rack_info_dict is None:
            return False
        
        flag_ready = True
        for rack_name in rack_info_dict:
            if rack_info_dict[rack_name]['rack_status'] != self.STATUS_READY:
                flag_ready = False
                break;
            
        return flag_ready
    
    
    # whether the temperature data of a rack is ready or not
    def is_rack_temperature_ready(self, rack_name):
        return self.is_rack_data_ready(self.TEMPERATURE_NAME, rack_name)
    
    # whether the service data of a rack is ready or not
    def is_rack_service_ready(self, rack_name):
        return self.is_rack_data_ready(self.SERVICE_NAME, rack_name)
    
    
    
    
if __name__ == '__main__':
    rackdata = rack_data()
    rack_name = 'echo'
    #bready = rackdata.is_rack_temperature_ready(rack_name)
    #rackdata.mydebug("{0} is ready or not: {1}".format(rack_name, bready))
    #bready = rackdata.can_start_refresh("temperature", rack_name)
    #rackdata.mydebug("{0} can start refresh: {1}".format(rack_name, bready))
    bready = rackdata.set_status_start_refresh("temperature", rack_name)
    rackdata.mydebug("{0} can start refresh: {1}".format(rack_name, bready))

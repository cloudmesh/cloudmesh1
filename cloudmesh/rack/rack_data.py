from cloudmesh.inventory import Inventory
from datetime import datetime, timedelta

from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)


class RackData:
    # ONLY for debug test
    MY_DEBUG_FLAG = False

    # data valid time, unit second
    data_valid_time = 0

    inventory = None

    TEMPERATURE_NAME = "temperature"
    SERVICE_NAME = "service"
    LOCATION_TEMP = "temp"

    # three status of server refresh
    STATUS_NOT_READY = "not_ready"
    STATUS_REFRESH = "refresh"
    STATUS_READY = "ready"

    # default data valid time is set to 1800 seconds
    def __init__(self, valid_time=1800):
        self.data_valid_time = valid_time
        self.inventory = Inventory()

    def mydebug(self, msg):
        if self.MY_DEBUG_FLAG:
            log.debug(msg)

    # get/set data valid time in mongo db
    def get_data_valid_time(self):
        return self.data_valid_time

    def set_data_valid_time(self, valid_time):
        self.data_valid_time = valid_time if valid_time > 0 else 0

    # change refresh status
    def set_status_start_refresh(self, service_type, rack_name):
        self.mydebug(
            "set status start refresh for {0}-{1}".format(rack_name, service_type))
        query_dict = self.get_rack_query_dict(
            service_type, rack_name, self.LOCATION_TEMP)
        curr_time = datetime.now()
        element = {
            "rack_status": self.STATUS_REFRESH,
            "updated_node": 0,
            "cm_refresh": curr_time,
        }
        racks = {}
        for rack_name in query_dict:
            self.mydebug(
                "set_status_start_refresh rackname is: {0} ".format(rack_name))
            tmp_racks = self.inventory.get_clusters(rack_name)
            racks[rack_name] = tmp_racks[0]
            #self.mydebug("set_status_start_refresh racks[{0}] is: {1}".format(rack_name, racks[rack_name]))
            element['data'] = dict((h, None)
                                   for h in racks[rack_name]['cm_value'])
            self.partly_update(query_dict[rack_name], {"$set": element})

        self.mydebug(
            "Exit from status start refresh for {0}-{1}".format(rack_name, service_type))

    # get valid list of rack name
    # result: if rack_name is 'all', then ['india', 'echo', ...]
    #         else if rack_name is a valid rack name, then ['rack_name.lower()']
    #         else None
    def get_rack_name_list(self, rack_name="all"):
        self.mydebug("enter into get_rack_name_list of {0}".format(rack_name))
        racks = self.inventory.get_clusters()
        rack_name_list = [rack['cm_cluster'] for rack in racks]
        rack_name_lower = rack_name.lower()
        if rack_name_lower != 'all':
            rack_name_list = [
                rack_name_lower] if rack_name_lower in rack_name_list else None

        #self.mydebug("exit from get_rack_name_list {0}".format(rack_name_list))
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
                "cm_type": "inventory",
                "cm_kind": "rack",
                "cm_id": rack_name
            }
            if location:
                query["cm_key"] = "rack_{1}_{0}".format(service_type, location)
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
            rack_info_dict[rack_name] = self.inventory.find_one(
                query_dict[rack_name])
        #self.mydebug("get_rack_info of {0}".format(rack_info_dict.keys()))
        return rack_info_dict

    # result: {'rack_name': True, 'rack_name': False, ...}
    def can_start_refresh(self, service_type, rack_name):
        self.mydebug(
            "enter into can_start_refresh og {0}-{1}".format(rack_name, service_type))
        query_dict = self.get_rack_query_dict(
            service_type, rack_name, self.LOCATION_TEMP)
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
            elif status == self.STATUS_READY or status == self.STATUS_REFRESH:
                flag_refresh = self.is_db_data_expired(rack_info['cm_refresh'])
            refresh_dict[rack_name] = flag_refresh

        self.mydebug("can_start_refresh of {0}".format(refresh_dict))
        return refresh_dict

    # projection query
    def partly_query(self, query, partly_view):
        if partly_view:
            return self.inventory.db_inventory.find_one(query, partly_view)
        return self.inventory.find_one(query)

    # update a part of document in database
    def partly_update(self, query, value, flag_upsert=False, flag_multi=False):
        if not value:
            return self.inventory.update(query)

        return self.inventory.db_inventory.update(query, value, upsert=flag_upsert, multi=flag_multi)

    # Usually called in a different process
    # update the temperature of a server
    # NOT support to update 'all'
    # The update of 'all' MUST be divided into serveral updates of each independent rack of 'all'
    # update the information of a server
    def server_refresh_update_temperature(self, rack_name, server, data):
        self.mydebug("enter into server_refresh_update_temperature update server {0} for {1}".format(
            server, rack_name))
        service_type = self.TEMPERATURE_NAME
        flag_refresh_success = False
        query_dict = self.get_rack_query_dict(
            service_type, rack_name, self.LOCATION_TEMP)
        rack_info_dict = self.get_rack_info(query_dict)
        rack_info = None
        if rack_info_dict:
            rack_info = rack_info_dict[rack_name]
            time_now = datetime.now()
            element = {}
            element['cm_refresh'] = time_now
            element['data.{0}'.format(server)] = data
            # atomic update
            update_result = self.inventory.db_inventory.find_and_modify(query=query_dict[rack_name], update={
                                                                        '$inc': {'updated_node': 1}, '$set': element}, new=True, fields={'updated_node': 1})

            if update_result['updated_node'] == rack_info['max_node']:
                self.partly_update(
                    query_dict[rack_name], {'$set': {'rack_status': self.STATUS_READY}})
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
                self.mydebug(
                    "server_refresh_update_data, update rack {0} with data".format(rack_name))
                self.partly_update(query_dict[rack_name], {'$set': element})

        return flag_refresh_success

    # Usually called in a different process
    # update the service of a server
    def server_refresh_update_service(self, rack_name, data):
        self.mydebug(
            "enter into server_refresh_update_service update rack {0}".format(rack_name))
        service_type = self.SERVICE_NAME
        flag_refresh_success = False
        query_dict = {}
        for rack_name in data:
            tmp_result = self.get_rack_query_dict(
                service_type, rack_name, self.LOCATION_TEMP)
            query_dict[rack_name] = tmp_result[rack_name]
        rack_info_dict = self.get_rack_info(query_dict)
        if rack_info_dict is None:
            return flag_refresh_success

        for rack_name in rack_info_dict:
            rack_info = rack_info_dict[rack_name]
            time_now = datetime.now()
            element = {}
            element['cm_refresh'] = time_now
            element['updated_node'] = rack_info['max_node']
            element['rack_status'] = self.STATUS_READY
            element['data'] = data[rack_name]
            self.partly_update(query_dict[rack_name], {'$set': element})
            flag_refresh_success = True

            # update the normal record, which provides information to WEB page
            # After data of all servers in this rack are collected
            if flag_refresh_success:
                temp_query_dict = self.get_rack_query_dict(
                    service_type, rack_name)
                element = {}
                element['rack_status'] = self.STATUS_READY
                element['cm_refresh'] = time_now
                element['data'] = data[rack_name]
                self.mydebug(
                    "server_refresh_update_data, update rack {0} with data".format(rack_name))
                self.partly_update(
                    temp_query_dict[rack_name], {'$set': element})

        return flag_refresh_success

    # get data of a rack
    def get_rack_status_data(self, service_type, rack_name):
        rack_info_dict = self.get_rack_info(
            self.get_rack_query_dict(service_type, rack_name))
        if rack_info_dict is None:
            return None

        dict_result = {}
        for rack_name in rack_info_dict:
            dict_result[rack_name] = rack_info_dict[rack_name]["data"]

        self.mydebug(
            "exit from get_rack_status_data {0}-{1} with data".format(rack_name, service_type))
        return dict_result

    # get temperature data of a rack
    def get_rack_temperature_data(self, rack_name):
        return self.get_rack_status_data(self.TEMPERATURE_NAME, rack_name)

    # get service data of a rack
    def get_rack_service_data(self, rack_name):
        return self.get_rack_status_data(self.SERVICE_NAME, rack_name)

    # whether the data of a rack is ready or not
    def is_rack_data_ready(self, service_type, rack_name, refresh_flag=False):
        location = self.LOCATION_TEMP if refresh_flag else None
        query_dict = self.get_rack_query_dict(
            service_type, rack_name, location)
        rack_info_dict = self.get_rack_info(query_dict)
        if rack_info_dict is None:
            return False

        flag_ready = False
        for rack_name in rack_info_dict:
            #self.mydebug("{0} data is {1}".format(rack_name, rack_info_dict[rack_name]))
            rack_info = rack_info_dict[rack_name]

            if rack_info['rack_status'] == self.STATUS_READY:
                flag_ready = not self.is_db_data_expired(
                    rack_info["cm_refresh"])
            if not flag_ready:
                break
        return flag_ready

    # check data is ready or not in temp refresh db
    def is_refresh_rack_data_ready(self, service_type, rack_name):
        return self.is_rack_data_ready(service_type, rack_name, True)

    # whether the temperature data of a rack is ready or not
    def is_rack_temperature_ready(self, rack_name):
        return self.is_rack_data_ready(self.TEMPERATURE_NAME)

    # whether the service data of a rack is ready or not
    def is_rack_service_ready(self, rack_name):
        return self.is_rack_data_ready(self.SERVICE_NAME, rack_name)

    # check data in mongo db expired or not
    def is_db_data_expired(self, db_time):
        flag_expired = False
        time_interval = timedelta(seconds=self.data_valid_time)
        if (datetime.now() > db_time + time_interval):
            flag_expired = True
        return flag_expired


if __name__ == '__main__':
    rackdata = RackData()
    rack_name = 'echo'
    #bready = rackdata.is_rack_temperature_ready(rack_name)
    #rackdata.mydebug("{0} is ready or not: {1}".format(rack_name, bready))
    #bready = rackdata.can_start_refresh("temperature", rack_name)
    #rackdata.mydebug("{0} can start refresh: {1}".format(rack_name, bready))
    bready = rackdata.set_status_start_refresh("temperature", rack_name)
    rackdata.mydebug("{0} can start refresh: {1}".format(rack_name, bready))

"""
    Status Progress of rack map load/refresh/load_refresh
"""
from base_progress import BaseProgress


class RackMapProgress(BaseProgress):
    # progress type
    TYPE_LOAD_MAP = "load_map"

    TYPE_REFRESH_MAP = "refresh_map"

    TYPE_LOAD_REFRESH_MAP = "load_refresh_map"

    STATUS_SEND_HTTP_REQUEST = "send http request"

    STATUS_READ_DATA_FROM_DB = "read data from db"

    STATUS_CHECK_REFRESH_CONDITION = "check refresh condition"

    STATUS_ASYNC_REFRESH = "async refresh data"

    STATUS_READ_REFRESH_DATA = "read refresh data"

    STATUS_PROCESS_DATA = "process map data"

    STATUS_PLOT_MAP = "plot map"

    STATUS_PLOT_LEGEND = "plot legend"

    STATUS_LOADING_MAP = "loading map"
    # var
    map_progress_type = None

    # all possible status of map loading progress
    all_status_list = [
        STATUS_SEND_HTTP_REQUEST,
        STATUS_READ_DATA_FROM_DB,
        STATUS_CHECK_REFRESH_CONDITION,
        STATUS_ASYNC_REFRESH,
        STATUS_READ_REFRESH_DATA,
        STATUS_PROCESS_DATA,
        STATUS_PLOT_MAP,
        STATUS_PLOT_LEGEND,
        STATUS_LOADING_MAP,
    ]

    # (x, y), x means the index in all_status_list; y means the value of this status
    value_list_dict = {
        TYPE_LOAD_MAP:  [
            (0, 5),
            (1, 20),
            (5, 20),
            (6, 25),
            (7, 15),
            (8, 15),
        ],
        TYPE_REFRESH_MAP: [
            (0, 5),
            (2, 5),
            (3, 45),
            (4, 5),
            (5, 10),
            (6, 10),
            (7, 5),
            (8, 15),
        ],
        TYPE_LOAD_REFRESH_MAP: [
            (0, 5),
            (1, 5),
            (2, 5),
            (3, 40),
            (4, 5),
            (5, 10),
            (6, 10),
            (7, 5),
            (8, 15),
        ],
    }

    # status data dict
    # {status_text: {"begin": value_begin, "range": value_range, "next": next_status}, ...}
    status_data_dict = {}
    """
        load_map including: 1) 5%, send http request,
                            2) 20%, read data from db,
                            3) 20%, process data,
                            4) 25%, plot map,
                            5) 15%, plot legend,
                            6) 15%, loading map, receive http response

        refresh_map including:  1) 5%, send http request,
                                2) 5%, check refresh condition,
                                3) 45%, async send refresh,
                                4) 5%, read data from db,
                                5) 10%, process data,
                                6) 10%, plot map,
                                7) 5%, plot legend,
                                8) 15%, loading map, receive http response
        load_refresh_map including:
                            1) 5%, send http request,
                            2) 5%, read data from db,
                            3) 5%, check refresh condition,
                            4) 40%, async send refresh,
                            5) 5%, read data from db,
                            6) 10%, process data,
                            7) 10%, plot map,
                            8) 5%, plot legend,
                            9) 15%, loading map, receive http response
    """

    def __init__(self, vldist=None, status_list=None):
        BaseProgress.__init__(self)
        if status_list and type(status_list) is list:
            self.all_status_list = status_list
        if vldist and type(vldist) is dict:
            for type_name in self.value_list_dict:
                if type_name not in vldist:
                    self.init_status_data(
                        type_name, self.value_list_dict[type_name])
            for type_name in vldist:
                self.init_status_data(type_name, vldict[type_name])
        else:
            for type_name in self.value_list_dict:
                self.init_status_data(
                    type_name, self.value_list_dict[type_name])

    # init status_data_dict with value_list
    def init_status_data(self, type_name, value_list):
        self.status_data_dict[type_name] = {}
        value_begin = 0
        prev_status = None
        for (value_index, value_range) in value_list:
            status_text = self.all_status_list[value_index]
            self.status_data_dict[type_name][status_text] = {"begin": value_begin,
                                                             "range": value_range,
                                                             "next": "",
                                                             }
            if prev_status:
                prev_status["next"] = status_text
            prev_status = self.status_data_dict[type_name][status_text]
            value_begin += value_range

    # load map ?
    def is_load_map(self):
        return self.is_load_or_refresh_map(self.TYPE_LOAD_MAP)

    # refresh map ?
    def is_refresh_map(self):
        return self.is_load_or_refresh_map(self.TYPE_REFRESH_MAP)

    # load failed then refresh map ?
    def is_load_refresh_map(self):
        return self.is_load_or_refresh_map(self.TYPE_LOAD_REFRESH_MAP)

    def is_load_or_refresh_map(self, str_type):
        result = False
        if self.map_progress_type == str_type:
            result = True
        return result

    # set status to load map.
    def set_load_map(self):
        self.map_progress_type = self.TYPE_LOAD_MAP
        self.clear_status()

    # set status to refresh map
    def set_refresh_map(self):
        self.map_progress_type = self.TYPE_REFRESH_MAP
        self.clear_status()

    # set status to load failed then refresh map
    def set_load_refresh_map(self):
        self.map_progress_type = self.TYPE_LOAD_REFRESH_MAP
        self.set_map_progress_status(self.status_text)

    def set_map_progress_status(self, status, factor=1):
        #print("map_progress_type is: {0}, status is: {1}".format(self.map_progress_type, status))
        curr_status = self.status_data_dict[self.map_progress_type][status]
        if factor == 1:
            value = curr_status["begin"] + curr_status["range"]
        else:
            value = curr_status["begin"] + \
                int(round(curr_status["range"] * factor))
        #print("process status, status: '{0}', value: '{1}'".format(status, value))
        next_status = curr_status["next"] if factor == 1 else status
        self.set_status(status, value, next_status)

    def set_send_http_request(self, factor=1):
        self.set_map_progress_status(self.STATUS_SEND_HTTP_REQUEST, factor)

    def set_read_data_from_db(self, factor=1):
        self.set_map_progress_status(self.STATUS_READ_DATA_FROM_DB, factor)

    def set_check_refresh_condition(self, factor=1):
        self.set_map_progress_status(
            self.STATUS_CHECK_REFRESH_CONDITION, factor)

    def set_async_refresh(self, factor=1):
        self.set_map_progress_status(self.STATUS_ASYNC_REFRESH, factor)

    def set_read_refresh_data(self, factor=1):
        self.set_map_progress_status(self.STATUS_READ_REFRESH_DATA, factor)

    def set_process_data(self, factor=1):
        self.set_map_progress_status(self.STATUS_PROCESS_DATA, factor)

    def set_plot_map(self, factor=1):
        self.set_map_progress_status(self.STATUS_PLOT_MAP, factor)

    def set_plot_legend(self, factor=1):
        self.set_map_progress_status(self.STATUS_PLOT_LEGEND, factor)

    def set_receive_http_response(self, factor=1):
        self.set_map_progress_status(self.STATUS_LOADING_MAP, factor)


class HeatMapProgress(RackMapProgress):

    def __init__(self):
        RackMapProgress.__init__(self, None)


class ServiceMapProgress(RackMapProgress):

    def __init__(self):
        RackMapProgress.__init__(self, None)

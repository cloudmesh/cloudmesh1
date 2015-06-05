from cloudmesh.pbs.pbs import PBS
from cloudmesh.inventory import Inventory
from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh.rack.rack_progress import get_temperature_progress, get_service_progress
from cloudmesh.rack.cluster_map_heat import HeatClusterMap
from cloudmesh.rack.cluster_map_service import ServiceClusterMap
from cloudmesh.rack.rack_data import RackData
from cloudmesh.temperature.cm_temperature import cm_temperature
from cloudmesh_base.Shell import Shell
import time
from cloudmesh_base.logger import LOGGER
from cloudmesh_base.locations import config_file

log = LOGGER(__file__)


class RackWork:
    map_progress = None
    username = None

    def __init__(self, username=None):
        self.username = username
        self.temperature_ipmi = cm_temperature()
        self.rackdata = RackData(self.username)

    # thread
    def generate_map(self, service, rack_name, refresh_flag=False):
        # the following begin to generate map
        # class name means the specific class to generate map for different service type
        # method name means the specific method to fetch real data of different service type,
        #     the methods are defined in class FetchClusterInfo
        service_options = {
            "temperature": {
                "class": HeatClusterMap,
                "method": "read_temperature_mongo",
            },
            "service": {
                "class": ServiceClusterMap,
                "method": "read_service_mongo",
            },
        }
        # update progress satus
        self.get_map_progress(service)

        # get location of configuration file, input diag, output image
        dir_base = config_file("")

        server_config = cm_config_server()
        relative_dir_diag = server_config.get("cloudmesh.server.rack.input")
        relative_dir_image = server_config.get(
            "cloudmesh.server.rack.diagrams.{0}".format(service))
        # log.debug("relative dir image, {0}".format(relative_dir_image))
        flask_dir = "static"
        # guess absolute path of cloudmesh_web
        rack_py_dir = Shell.pwd().strip().split("/")
        cloudmesh_web_dir = rack_py_dir
        # log.debug("cloudmesh_web dir, {0}".format(cloudmesh_web_dir))
        list_image_dir = [flask_dir] + relative_dir_image.strip().split("/")
        abs_dir_image = "/".join(cloudmesh_web_dir + list_image_dir)
        abs_dir_diag = dir_base + "/" + relative_dir_diag
        # dynamic generate image
        map_class = service_options[service]["class"](
            self.username, rack_name, dir_base, abs_dir_diag, abs_dir_image)
        # get cluster server data
        dict_data = None
        if False:
            dict_data = map_class.genRandomValues()
        else:
            # flag_filter = None if rack_name == "all" else rack_name
            # If user want to customize the action, user can set optional param here
            # by calling map_class.set_optional_param(value)
            # optional param
            aparam = map_class.get_optional_param()
            dict_data = getattr(self, service_options[service]["method"])(
                rack_name, aparam, refresh_flag)

        # update data
        map_class.update(dict_data)
        # plot map
        map_class.plot()

        # get image names
        filename_image = map_class.getImageFilename()
        filename_legend = map_class.getLegendFilename()
        image_size = map_class.getImageSize()
        legend_size = map_class.getImageLegendSize()
        # log.debug("legend size is: {0}".format(legend_size))
        abs_web_path_image = "/".join([""] + list_image_dir + [filename_image])
        abs_web_path_legend = "/".join([""] +
                                       list_image_dir + [filename_legend])
        img_flag = "?" + str(time.time())

        map_data = {
            "map_width": image_size["width"],
            "map_height": image_size["height"],
            "legend_width": legend_size["width"],
            "legend_height": legend_size["height"],
            "map_url": abs_web_path_image + img_flag,
            "legend_url": abs_web_path_legend + img_flag,
        }
        self.map_progress.update_data("map_data", map_data)

    # celery task
    def pbs_service(self, rack_name=None):
        config = cm_config()
        username = config.get("cloudmesh.hpc.username")
        pbs = PBS(username, "india.futuregrid.org")
        dict_pbs_info = pbs.pbsnodes()
        dict_data = {}
        inventory = Inventory()
        racks = inventory.get_clusters()
        for rack in racks:
            rack_name = rack["cm_cluster"]
            dict_data[rack_name] = {}
            hosts = rack["cm_value"]
            for host in hosts:
                (hid, hlabel) = inventory.get_host_id_label(host, "public")
                utype = "unknown"
                if hlabel in dict_pbs_info:
                    server = dict_pbs_info[hlabel]
                    if "note" in server.keys():
                        note_value = server["note"]
                        # to compatible with the future change
                        if type(note_value) is dict:
                            utype = note_value["service"]
                        else:   # currently is a literal string for note
                            utype = note_value
                dict_data[rack_name][hid] = utype
        return dict_data

    # fetch cluster temperature from mongo db
    # params:
    # flag_filter, None or one item in list ['india', 'bravo', 'echo',
    # 'delta']
    def read_temperature_mongo(self, rack_name=None, unit='C', refresh_flag=False):
        # read data from mongo db
        rack_data_dict = self.rackdata.get_rack_temperature_data(rack_name)

        if refresh_flag:
            self.map_progress.set_read_refresh_data(0.7)
        else:
            self.map_progress.set_read_data_from_db(0.7)

        dict_data = {}
        for rack_name in rack_data_dict:
            for host in rack_data_dict[rack_name]:
                result = self.temperature_ipmi.parse_max_temp(
                    rack_data_dict[rack_name][host], unit)
                dict_data[host] = result["value"]

        if refresh_flag:
            self.map_progress.set_read_refresh_data()
        else:
            self.map_progress.set_read_data_from_db()

        return dict_data

    # fetch cluster service from mongo db
    # params:
    # flag_filter, None or one item in list ['india', 'bravo', 'echo',
    # 'delta']
    def read_service_mongo(self, rack_name=None, unit=None, refresh_flag=False):
        # read data from mongo db
        rack_data_dict = self.rackdata.get_rack_service_data(rack_name)

        if refresh_flag:
            self.map_progress.set_read_refresh_data(0.7)
        else:
            self.map_progress.set_read_data_from_db(0.7)

        dict_data = {}
        for rack_name in rack_data_dict:
            for host in rack_data_dict[rack_name]:
                dict_data[host] = rack_data_dict[rack_name][host]

        if refresh_flag:
            self.map_progress.set_read_refresh_data()
        else:
            self.map_progress.set_read_data_from_db()

        return dict_data

    def get_map_progress(self, service):
        if service == self.rackdata.TEMPERATURE_NAME:
            self.map_progress = get_temperature_progress(self.username)
        elif service == self.rackdata.SERVICE_NAME:
            self.map_progress = get_service_progress(self.username)
        return self.map_progress


# usage
if __name__ == "__main__":
    rackwork = RackWork("username")
    map_progress = rackwork.get_map_progress("temperature")

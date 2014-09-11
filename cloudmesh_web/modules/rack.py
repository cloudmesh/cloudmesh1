from cloudmesh_install import config_file
from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh.rack.cluster_map_heat import HeatClusterMap
from cloudmesh.rack.cluster_map_service import ServiceClusterMap
from cloudmesh.rack.fetch_cluster_info import FetchClusterInfo
from flask import Blueprint, g, render_template, request, redirect, url_for
from flask.ext.login import login_required  # @UnresolvedImport
from flask.ext.wtf import Form  # @UnresolvedImport
from pprint import pprint
from sh import pwd  # @UnresolvedImport
from wtforms import SelectField
from flask.ext.principal import Permission, RoleNeed
import time
from cloudmesh.rack.rack_progress import get_temperature_progress, get_service_progress
import json
import sys
from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)


rack_module = Blueprint('rack_module', __name__)

admin_permission = Permission(RoleNeed('admin'))

#
# ROUTE: rack
#


class RackForm(Form):
    # MUST create an unique selector for each different service
    service_rack = SelectField()
    temperature_rack = SelectField()

    all_racks_dict = {
        "all": ('all', 'All Clusters'),
        "india": ('india', 'India Cluster'),
        "echo": ('echo', 'Echo Cluster'),
        "delta": ('delta', 'Delta Cluster'),
        "bravo": ('bravo', 'Bravo Cluster'),
    }
    # all possible service provided
    all_services_list = ["service", "temperature", ]

    # content of each service, including label, and range of clusters
    # 'clusters' means the specific service can be used on some different clusters
    # 'select' means one attribute name of SelectField, typical name is "{service name}_rack"
    all_services_dict = {
        "service": {
            "label": "Service Map",
            "clusters": ["all", "india", "echo", "delta", "bravo", ],
            "select": "service_rack",
        },
        "temperature": {
            "label": 'Heat Map',
            "clusters": ["echo", ],
            "select": "temperature_rack",
        },
    }

    # a dict that holds all selector
    selector_dict = {}

    def initForm(self):
        for service in self.all_services_list:
            service_dict = {}
            service_dict["name"] = service
            service_dict["label"] = self.all_services_dict[service]["label"]
            service_dict["select"] = getattr(
                self, self.all_services_dict[service]["select"])
            rack_list = []
            for rack in self.all_services_dict[service]["clusters"]:
                rack_list.append(self.all_racks_dict[rack])

            service_dict["select"].choices = rack_list
            self.selector_dict[service] = service_dict

    def validate_on_submit(self):
        return True


@rack_module.route('/inventory/rack')
@login_required
def display_rack_home():
    rack_form = RackForm()
    if rack_form.validate_on_submit():
        rack_form.initForm()
        return render_template("mesh/rack/rack.html", form=rack_form, flag_home=True)


@rack_module.route('/inventory/rack/mapcontainer', methods=['POST'])
@login_required
def display_rack_map_container():
    # rack denote the rack that user selected
    # service denote the service user selected on the specific rack
    rack = request.form['select_rack']
    service = request.form['select_service']

    # double check to make sure rack can provide the specific service
    rack_form = RackForm()
    if rack not in rack_form.all_services_dict[service]["clusters"]:
        log.error("Someone try to hack the service [service: '{0}' on rack: '{1}'] provided by Rack Diagram. Just ignore it.".format(
            service, rack))
        return redirect("/inventory/rack")

    return render_template(
        "mesh/rack/map_container.html",
        rack=rack,
        service=service,
    )


@rack_module.route('/inventory/rack/genmap', methods=['GET', 'POST'])
@login_required
def gen_rack_map():
    service = request.args.get("service")
    rack = request.args.get("rack")
    # double check to make sure rack can provide the specific service
    rack_form = RackForm()
    if rack not in rack_form.all_services_dict[service]["clusters"]:
        log.error("Someone try to hack the service [service: '{0}' on rack: '{1}'] provided by Rack Diagram. Just ignore it.".format(
            service, rack))
        return redirect("/inventory/rack")

    myfetch = FetchClusterInfo(g.user.id)
    map_progress = myfetch.get_map_progress(service)
    map_progress.set_load_map()
    map_progress.set_send_http_request()
    result = {"result": "failure", "reason": {
        "status": "failure", "text": "Read DB Error"}}
    if myfetch.start_gen_map(service, rack):
        result["result"] = "success"
    return json.dumps(result)


@rack_module.route('/inventory/rack/refreshmap', methods=['GET', 'POST'])
@login_required
def refresh_rack_map():
    service = request.args.get("service")
    rack = request.args.get("rack")
    # double check to make sure rack can provide the specific service
    rack_form = RackForm()
    if rack not in rack_form.all_services_dict[service]["clusters"]:
        log.error("Someone try to hack the service [service: '{0}' on rack: '{1}'] provided by Rack Diagram. Just ignore it.".format(
            service, rack))
        return redirect("/inventory/rack")

    myfetch = FetchClusterInfo(g.user.id)
    map_progress = myfetch.get_map_progress(service)
    map_progress.set_refresh_map()
    map_progress.set_send_http_request()
    result = {"result": "failure", "reason": {
        "status": "failure", "text": "Read DB Error"}}
    result_dict = myfetch.start_refresh_map(service, rack)
    if result_dict["result"]:
        result["result"] = "success"
    elif result_dict["fresh"]:
        result["reason"]["status"] = "success"
        result["reason"]["text"] = "Data is already newest"

    return json.dumps(result)


@rack_module.route('/inventory/rack/mapprogress', methods=['GET', 'POST'])
@login_required
def rack_map_progress_status():
    service = request.args.get("service")
    result = {"text": "", "value": 0, "next": ""}

    myfetch = FetchClusterInfo(g.user.id)
    map_progress = myfetch.get_map_progress(service)
    if map_progress:
        result = map_progress.get_status()
        # log.debug("progress status: {0}".format(result))
        if result["next"] == "loading map":
            result["data"] = map_progress.get_data("map_data")

    return json.dumps(result)


@rack_module.route('/inventory/rack/map', methods=['POST'])
@login_required
def display_rack_map():

    ####
    #
    #  Flag of debug, True means generate fake data with random generator
    #                 False means fetch the real data from server
    ####
    flag_debug = False

    # class name means the specific class to generate map for different service type
    # method name means the specific method to fetch real data of different service type,
    #     the methods are defined in class FetchClusterInfo
    service_options = {
        "temperature": {
            "class": HeatClusterMap,
            "method": "fetch_temperature_ipmi",
        },
        "service": {
            "class": ServiceClusterMap,
            "method": "fetch_service_type",
        },
    }

    # rack denote the rack user selected
    # service denote the service user selected on the specific rack
    rack = request.form['select_rack']
    service = request.form['select_service']

    # double check to make sure rack can provide the specific service
    rack_form = RackForm()
    if rack not in rack_form.all_services_dict[service]["clusters"]:
        log.error("Someone try to hack the service [service: '{0}' on rack: '{1}'] provided by Rack Diagram. Just ignore it.".format(
            service, rack))
        return redirect("/inventory/rack")

    # get location of configuration file, input diag, output image
    dir_base = config_file("")
    server_config = cm_config_server()
    relative_dir_diag = server_config.get("cloudmesh.server.rack.input")
    relative_dir_image = server_config.get(
        "cloudmesh.server.rack.diagrams.{0}".format(service))
    # log.debug("relative dir image, {0}".format(relative_dir_image))
    flask_dir = "static"
    # guess absolute path of cloudmesh_web
    rack_py_dir = pwd().strip().split("/")
    cloudmesh_web_dir = rack_py_dir  # [:-1]
    # log.debug("cloudmesh_web dir, {0}".format(cloudmesh_web_dir))
    list_image_dir = [flask_dir] + relative_dir_image.strip().split("/")
    abs_dir_image = "/".join(cloudmesh_web_dir + list_image_dir)
    abs_dir_diag = dir_base + "/" + relative_dir_diag
    # dynamic generate image
    map_class = service_options[service]["class"](
        rack, dir_base, abs_dir_diag, abs_dir_image)
    # get cluster server data
    dict_data = None
    if flag_debug:
        dict_data = map_class.genRandomValues()
    else:
        # fetch the real data ....
        # TODO cloudmesh.hpc.proxyserver
        # should we add a field in cloudmesh.yaml for the proxy server to run
        # pbsnodes ???
        config = cm_config()
        user = config.get("cloudmesh.hpc.username")
        myfetch = FetchClusterInfo(user, "india.futuregrid.org")
        flag_filter = None if rack == "all" else rack
        # If user want to customize the action, user can set optional param here
        # by calling map_class.set_optional_param(value)
        # optional param
        aparam = map_class.get_optional_param()
        dict_data = getattr(myfetch, service_options[service]["method"])(
            flag_filter, aparam)

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
    abs_web_path_legend = "/".join([""] + list_image_dir + [filename_legend])
    img_flag = "?" + str(time.time())
    return render_template("mesh/rack/rack.html",
                           flag_home=False,
                           rack=rack,
                           imageWidth=image_size["width"],
                           imageHeight=image_size["height"],
                           legendWidth=legend_size["width"],
                           legendHeight=legend_size["height"],
                           service=service,
                           imageFilename=abs_web_path_image + img_flag,
                           legendFilename=abs_web_path_legend + img_flag
                           )

from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh.rack.cluster_map_heat import HeatClusterMap
from cloudmesh.rack.cluster_map_service import ServiceClusterMap
from cloudmesh.rack.fetch_cluster_info import FetchClusterInfo
from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import login_required  # @UnresolvedImport
from flask.ext.wtf import Form  # @UnresolvedImport
from pprint import pprint
from sh import pwd  # @UnresolvedImport
from wtforms import SelectField
from flask.ext.principal import Permission, RoleNeed

from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

# from cloudmesh.config.cm_rack import cm_keys



rack_module = Blueprint('rack_module', __name__)

admin_permission = Permission(RoleNeed('admin'))

#
# ROUTE: rack
#

class RackForm(Form):
    # MUST create an unique selector for each different service
    service_rack        = SelectField()
    temperature_rack    = SelectField()

    all_racks_dict = {
                       "all":   ('all', 'All Clusters'),
                       "india": ('india', 'India Cluster'),
                       "echo":  ('echo', 'Echo Cluster'),
                       "delta": ('delta', 'Delta Cluster'),
                       "bravo": ('bravo', 'Bravo Cluster'),
                     }
    # all possible service provided
    all_services_list = ["service", "temperature",]
    
    # content of each service, including label, and range of clusters
    # 'clusters' means the specific service can be used on some different clusters
    # 'select' means one attribute name of SelectField, typical name is "{service name}_rack"
    all_services_dict = {
                          "service":     {
                                            "label": "Service Map",
                                            "clusters": ["all", "india", "echo", "delta", "bravo",],
                                            "select":   "service_rack",
                                          },
                          "temperature": {
                                            "label": 'Heat Map',
                                            "clusters": ["echo",],
                                            "select":   "temperature_rack",
                                          },
                        }
    
    # a dict that holds all selector
    selector_dict = {}
    
    
    def initForm(self):
        for service in self.all_services_list:
            service_dict = {}
            service_dict["name"] = service
            service_dict["label"] = self.all_services_dict[service]["label"]
            service_dict["select"] = getattr(self, self.all_services_dict[service]["select"])
            rack_list = []
            for rack in self.all_services_dict[service]["clusters"]:
                rack_list.append(self.all_racks_dict[rack])
            
            #print "rack list: ", rack_list
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



@rack_module.route('/inventory/rack/map', methods=['POST'])
@login_required
def display_rack_map():

    ####
    #
    #  Flag of debug
    #
    ####
    flag_debug = False

    # class name means the specific class to generate map for different service type
    # method name means the specific method to fetch real data of different service type, 
    #     the methods are defined in class FetchClusterInfo
    service_options = {"temperature": {"class": HeatClusterMap,
                                       "method": "fetch_temperature_ipmi",
                                       },
                       "service": {"class": ServiceClusterMap,
                                   "method": "fetch_service_type",
                                   },
                       }
    
    rack = request.form['select_rack']
    service = request.form['select_service']
    
    # double check to make sure cluster can provide the specific service
    rack_form = RackForm()
    if rack not in rack_form.all_services_dict[service]["clusters"]:
        log.error("Someone try to hack the service provided by Rack Diagram. Just ignore it.")
        return redirect("/inventory/rack")
    
    # get location of configuration file, input diag, output image
    dir_base = "~/.futuregrid"
    server_config = cm_config_server()
    relative_dir_diag = server_config.get("cloudmesh.server.rack.input")
    relative_dir_image = server_config.get("cloudmesh.server.rack.diagrams.{0}".format(service))
    print "relative dir image, ", relative_dir_image
    flask_dir = "static"
    # guess absolute path of webui
    rack_py_dir = pwd().strip().split("/")
    # print "rack_py_dir dir,,,,", rack_py_dir
    webui_dir = rack_py_dir  # [:-1]
    # print "webui dir,,,,", webui_dir
    list_image_dir = [ flask_dir ] + relative_dir_image.strip().split("/");
    abs_dir_image = "/".join(webui_dir + list_image_dir)
    abs_dir_diag = dir_base + "/" + relative_dir_diag
    # dynamic generate image
    map_class = service_options[service]["class"](rack, dir_base, abs_dir_diag, abs_dir_image)
    # get cluster server data
    dict_data = None
    if flag_debug:
        dict_data = map_class.genRandomValues()
    else:
        # fetch the real data ....
        # to do ...
        config = cm_config()
        user = config.get("cloudmesh.hpc.username")
        myfetch = FetchClusterInfo(user, "india.futuregrid.org")
        flag_filter = None if rack == "all" else rack
        dict_data = getattr(myfetch, service_options[service]["method"])(flag_filter)
        #dict_data = myfetch.fetch_service_type(flag_filter)
    # update data
    map_class.update(dict_data)
    # plot map
    map_class.plot()

    # get image names
    filename_image = map_class.getImageFilename()
    filename_legend = map_class.getLegendFilename()
    image_size = map_class.getImageSize()
    legend_size = map_class.getImageLegendSize()
    print "legend size is: ", legend_size
    abs_web_path_image = "/".join([""] + list_image_dir + [filename_image])
    abs_web_path_legend = "/".join([""] + list_image_dir + [filename_legend])

    return render_template("mesh/rack/rack.html",
                            flag_home=False,
                            rack=rack,
                            imageWidth=image_size["width"],
                            imageHeight=image_size["height"],
                            legendWidth=legend_size["width"],
                            legendHeight=legend_size["height"],
                            service=service,
                            imageFilename=abs_web_path_image,
                            legendFilename=abs_web_path_legend
                            )




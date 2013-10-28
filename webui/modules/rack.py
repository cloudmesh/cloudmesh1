from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh.rack.cluster_map_heat import HeatClusterMap
from cloudmesh.rack.cluster_map_service import ServiceClusterMap
from cloudmesh.rack.fetch_cluster_info import FetchClusterInfo
from flask import Blueprint, render_template, request, redirect
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
    select_rack = SelectField()
    select_service = SelectField()

    rack_list = [ ('all', 'All Clusters'),
                  ('india', 'India Cluster'),
                  ('echo', 'Echo Cluster'),
                  ('delta', 'Delta Cluster'),
                  ('bravo', 'Bravo Cluster'),
                 ]

    service_list = [
        ('service', 'Service Map'),
        ('temperature', 'Heat Map'),
    ]

    def initForm(self):
        self.select_rack.choices = self.rack_list
        self.select_service.choices = self.service_list

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




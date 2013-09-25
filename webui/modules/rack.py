from flask import Blueprint
from flask import render_template, request, redirect
#from cloudmesh.util.util import path_expand
from cloudmesh.config.cm_config import cm_config_server

# from cloudmesh.config.cm_rack import cm_keys

from cloudmesh.rack.cluster_map_heat import HeatClusterMap
from cloudmesh.rack.cluster_map_service import ServiceClusterMap

from sh import pwd  # @UnresolvedImport
from flask.ext.wtf import Form  # @UnresolvedImport
from wtforms import SelectField
from flask.ext.login import login_required  # @UnresolvedImport

rack_module = Blueprint('rack_module', __name__)

#
# ROUTE: rack
#

class RackForm(Form):
	select_rack = SelectField()
	select_service = SelectField()
	
	rack_list = [ ('india', 'India Cluster'),
				  ('echo',  'Echo Cluster'),
				  ('delta', 'Delta Cluster'), 
				  ('bravo', 'Bravo Cluster'), 
				  ('all',   'All Clusters')
				]
	
	service_list = [ ('temperature', 'Heat Map'), 
				     ('service', 'Service Map')
				   ]
	
	def initForm(self):
		self.select_rack.choices=self.rack_list
		self.select_rack.data = "bravo"
		
		self.select_service.choices=self.service_list
		self.select_service.data = 'temperature'
		
	def validate_on_submit(self):
		return True
	

@rack_module.route('/inventory/rack')
def display_rack_home():
	rack_form = RackForm()
	if rack_form.validate_on_submit():
		rack_form.initForm()
		return render_template("rack.html", form=rack_form, flag_home=True)


@rack_module.route('/inventory/rack/map', methods=['POST'])
def display_rack_map():
	
	####
	#
	#  Flag of debug
	#
	####
	flag_debug = True
	
	rack = request.form['select_rack']
	service = request.form['select_service']
	# get location of configuration file, input diag, output image
	dir_base = "~/.futuregrid"
	server_config = cm_config_server()
	relative_dir_diag = server_config.get("rack.input")
	relative_dir_image = server_config.get("rack.diagrams." + service)
	print "relative dir image, ", relative_dir_image
	flask_dir = "static"
	# guess absolute path of webui
	rack_py_dir = pwd().strip().split("/")
	#print "rack_py_dir dir,,,,", rack_py_dir
	webui_dir = rack_py_dir	#[:-1]
	#print "webui dir,,,,", webui_dir
	list_image_dir = [ flask_dir ] + relative_dir_image.strip().split("/");
	abs_dir_image = "/".join(webui_dir + list_image_dir)
	abs_dir_diag = dir_base + "/" + relative_dir_diag
	# dynamic generate image
	map_class = None
	if service == "temperature":
		map_class = HeatClusterMap(rack, dir_base, abs_dir_diag, abs_dir_image)
	elif service == "service":
		map_class = ServiceClusterMap(rack, dir_base, abs_dir_diag, abs_dir_image)
	# get cluster server data
	dict_data = None
	if flag_debug:
		dict_data = map_class.genRandomValues()
	else:
		# fetch the real data ....
		# to do ...
		pass
	# update data
	map_class.update(dict_data)
	# plot map
	map_class.plot()
	
	# get image names
	filename_image = map_class.getImageFilename()
	filename_legend = map_class.getLegendFilename()
	abs_web_path_image = "/".join([""] + list_image_dir + [filename_image])
	abs_web_path_legend = "/".join([""] + list_image_dir + [filename_legend])
	
	return render_template( "rack.html", 
							flag_home=False, 
							rack=rack,
							imageWidth=300 * map_class.getRackCount(), 
							service=service,
							imageFilename=abs_web_path_image,
							legendFilename=abs_web_path_legend
							)



@rack_module.route('/inventory/rack/old')
def display_all_racks():


	# dir = path_expand(cm_config_server().get("rack.path"))

	# not so nice cludge, ask for location of statcic instead

	# web_pwd = pwd().strip()
	# basename = "/static/{0}/{1}".format(dir, filename)

	rack = None

	return render_template('rack.html',
						   name="india",
						   rack=rack)


@rack_module.route('/inventory/rack/<name>')
@rack_module.route('/inventory/rack/<name>/<service>')
def display_rack(name, service=None):


	if service is None:
		service = "temperature"
	print "test begin/...."
	basename = None
	# diag_dir = path_expand(cm_config_server().get("rack.input"))
	# output_dir = path_expand(cm_config_server().get("rack.diagramms.{0}".format(service)))
	

	# not so nice cludge, ask for location of statcic instead

	# web_pwd = pwd().strip()
	# basename = "/static/{0}/{1}".format(output_dir, name)

	#  /static/racks/diagrams/india
	# .svg
	# .png
	# -legend.png


	#
	# CREATE YOU IMAGES NOW
	#

	# if service == "temperature":
	#	do this
	# else:
	#	do that

	rack = name

	return render_template('rack.html',
						   service=service,
						   basename=basename,
						   name=name,
						   rack=rack)

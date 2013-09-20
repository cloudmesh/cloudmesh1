"""
Service map of cluster servers, use HSV color space
"""
import math
from copy import deepcopy
from cloudmesh.rack.base_cluster_map import BaseClusterMap

class ServiceClusterMap(BaseClusterMap):
	
	# maximum h, 240/360 = 2/3
	h_max = 2.0 / 3.0
	
	# section name of service list
	service_section_name = "service"
	
	# service dict
	dict_services = None
	
	# ascending sorted service list
	list_services = None
	
	# mapping dict
	# map a type of service to a tuple RGB color
	# the key of dict is the different service got from cluster servers
	# formation is: {hpc:(255, 3, 5), openstack:(34, 50, 200), ...}
	dict_mapping = {} 
	
	
	def __init__(self, name):
		# call parent init function
		BaseClusterMap.__init__(self, name)
		
	
	# get the RGB according to a specific h param
	# there are only limited serveral colors according to the total services 
	def getRGB(self, h):
		return self.getRGBWithH(h)
	
	
	# init mapping dict
	def initMappingDict(self):
		len_arr = len(self.list_services)
		if len_arr < 1:
			return
		
		step = self.h_max / len_arr
		h_current = 0
		# update the first and last service type with #FF0000 and #0000FF
		self.dict_mapping.update({self.list_services[0]: (255, 0, 0)})
		if len_arr > 1:
			self.dict_mapping.update({self.list_services[-1]: (0, 0, 255)})
			
		# update other services RGB
		for i in range(1, len_arr-1):
			h_current += step
			self.dict_mapping.update({self.list_services[i]: self.getRGB(h_current)})
		
	
	# default service for cluster servers
	#    default value is the first type in ascending order
	def getDefaultService(self):
		return self.list_services[0]
		
	
	# ======================================
	#           abstract function
	#         sub-class MUST override
	# ======================================
	#
	# get default value for dict_servers
	def getServersDefaultValue(self):
		# get service list 
		self.dict_services = self.dict_rack_config[self.service_section_name]
		self.list_services = sorted(self.dict_services.keys())
		self.initMappingDict()
		
		return self.getDefaultService()
		
	
	
	# ======================================
	#           abstract function
	#         sub-class MUST override
	# ======================================
	#
	# get corresponding mapping dict, from specific value to RGB value
	# the formation of RGB is: (R, G, B)
	# for example: {1:(255, 0, 16), 2:(25, 20, 16), ...} 
	def getMappingDict(self):
		return deepcopy(self.dict_mapping)
	
	
	# ======================================
	#           abstract function
	#         sub-class MUST override
	# ======================================
	# 
	# get the current status of servers
	def update(self):
		if self.flag_debug:
			print "Update servers with DEBUG random data ..."
			#self.generateRandomService()
			self.generateContinousService()
			return
		
		# to do ....
		# grab real data from mongo db
		# ...
	
	
	# ======================================
	#           abstract function
	#         sub-class MUST override
	# ======================================
	# 
	# plot the legend of cluster map
	# param, ax is an instance of matplotlib.axes.Axes
	# return value is the filename of legend image file
	def drawLegendContent(self, ax, xylim):
		xcount = len(self.list_services) + 1
		xstep = xylim[0] / float(xcount)
		xstart = 0.5 * xstep
		xwidth = 0.6 * xstep
		ycount = 3.0 
		ystep = xylim[1] / ycount
		ystart = 0.5 * ystep
		yheight = 0.6 * ystep
		
		for service in self.list_services:
			rect = self.genDefaultRect()
			lb_x = xstart
			lb_y = ystart + ystep
			rect.update({"verts":{"lb":(lb_x, lb_y), "rt":(lb_x + xwidth, lb_y + yheight)}})
			rcolor = self.convertRGB2Hex(self.dict_mapping[service])
			rect.update({"facecolor_rect":rcolor, "edgecolor_rect":rcolor})
			rect.update({"label":{"lb":(lb_x, ystart), "text": service}})
			xstart += xstep
			
			self.drawRectangle(ax, rect)
	
	
	# only for test
	# generate random service for cluster servers
	def generateRandomService(self):
		# init the seed of random function
		self.getRandom(True)
		
		for server in self.dict_servers:
			temp_rand = self.getRandom()
			temp = int(round(temp_rand * len(self.list_services))) - 1
			
			self.dict_servers[server] = self.list_services[temp]
		
	
	# only for test, especially continuous colors
	def generateContinousService(self):
		arr = sorted(self.dict_servers.keys())
		len_arr = len(arr)
		# found a unknown cluster
		if len_arr == 0:
			return
		len_service = len(self.list_services)
		count = 0
		for server in arr:
			self.dict_servers[server] = self.list_services[count % len_service]
			count += 1
	
	
# test
if __name__ == "__main__":
	mytest = ServiceClusterMap("india")
	mytest.plot()

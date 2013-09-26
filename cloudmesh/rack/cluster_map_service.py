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
	
	# already know service list, read from 'default_rack_yaml' file
	list_services_known = None
	
	# service found in current clusters
	list_services_found = []
	
	# unknown service list had found
	list_unknown_services_found = []
	
	# unknown service
	unknown_service = "unknown"
	
	# mapping dict
	# map a type of service to a tuple RGB color
	# the key of dict is the different service got from cluster servers
	# formation is: {hpc:(255, 3, 5), openstack:(34, 50, 200), ...}
	dict_mapping = {} 
	
	
	def __init__(self, name, dir_yaml=None, dir_diag=None, dir_output=None, img_type=None):
		# call parent init function
		BaseClusterMap.__init__(self, name, "service", dir_yaml, dir_diag, dir_output, img_type)
		
	
	# get the RGB according to a specific h param
	# there are only limited serveral colors according to the total services 
	def getRGB(self, h):
		return self.getRGBWithH(h)
	
	
	# get proper service
	def getProperService(self, value):
		lvalue = value.lower()
		# check 'value' is a service in known service list or not
		# if not, assign it to a unknown servcie, and print warning message
		if lvalue not in self.list_services_known:
			if lvalue not in self.list_unknown_services_found:
				print "[Warning] '{0}' is NOT a known service, assign its status to 'unknown'.".format(value)
				self.list_unknown_services_found.append(lvalue)
				
			lvalue = self.unknown_service
		# update current service list
		# service_found will NOT include unknown service 
		elif lvalue not in self.list_services_found:
			self.list_services_found.append(lvalue)
			
		return lvalue
	
	
	# default service for cluster servers
	#    default value is "unknown"
	def getDefaultService(self):
		return self.getProperService(self.unknown_service)
		
	
	# ======================================
	#           abstract function
	#         sub-class MUST override
	# ======================================
	#
	# get default value for dict_servers
	def getServersDefaultValue(self):
		# get service list by reading 'default_rack_yaml' file
		self.dict_services = self.dict_rack_config[self.service_section_name]
		self.list_services_known = map(lambda x:x.lower(), self.dict_services.keys())
		
		print "services known", self.list_services_known
		
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
		# update the last/unknown type with #FF0000
		self.dict_mapping.update({self.unknown_service: (255, 0, 0)})
		
		len_found = len(self.list_services_found)
		if len_found >= 1:
			list_found_sorted = sorted(self.list_services_found)
			# the first service type with #0000FF
			self.dict_mapping.update({list_found_sorted[0]: (0, 0, 255)})
		
			# update other services RGB
			step = self.h_max / len_found
			for i in range(len_found):
				h_current = step * (len_found - i)
				self.dict_mapping.update({list_found_sorted[i]: self.getRGB(h_current)})
				
		return deepcopy(self.dict_mapping)
	
	
	# ======================================
	#		   abstract function
	#		 sub-class MUST override
	# ======================================
	#
	# get the current status of servers
	# params: dict_values means the data get from each server
	# this function MUST be called before plot to refresh status of servers in memory
	def update(self, dict_values):
		if dict_values is None:
			return
		
		self.dict_mapping.clear()
		self.resetDictServers(self.getDefaultService())
		# update servce with proper service 
		for server in dict_values:
			value = self.getProperService(dict_values[server])
			self.updateServer(server, value)


	# ======================================
	#           abstract function
	#         sub-class MUST override
	# ======================================
	# 
	# plot the legend of cluster map
	# param, ax is an instance of matplotlib.axes.Axes
	# return value is the filename of legend image file
	def drawLegendContent(self, ax, xylim):
		xcount = len(self.list_services_found) + 1 + 1
		xstep = xylim[0] / float(xcount)
		xstart = 0.5 * xstep
		xwidth = 0.6 * xstep
		ycount = 3.0 
		ystep = xylim[1] / ycount
		ystart = 0.5 * ystep
		yheight = 0.6 * ystep
		
		# we always arrange the display location of the 'unknown service' to the last 
		for service in sorted(self.list_services_found) + [self.unknown_service]:
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
	def genRandomValues(self, flag_continue=True):
		if flag_continue:
			return self.generateContinousService()
		else:
			return self.generateRandomService()
	
	
	# only for test
	# generate random service for cluster servers
	def generateRandomService(self):
		# init the seed of random function
		self.getRandom(True)
		
		dict_data = {}
		arr_services = self.list_services_known + [self.unknown_service]
		len_services = len(arr_services)
		for server in self.dict_servers:
			temp_rand = self.getRandom()
			temp = int(round(temp_rand * len_services)) - 1
			dict_data[server] = self.getProperService(arr_services[temp])
			
		return dict_data
		
	
	# only for test, especially continuous colors
	def generateContinousService(self):
		arr_servers = sorted(self.dict_servers.keys())
		len_servers = len(arr_servers)
		
		dict_data = {}
		arr_services = sorted(self.list_services_known) + [self.unknown_service]
		len_services = len(arr_services)
		count = 0
		for server in arr_servers:
			dict_data[server] = self.getProperService(arr_services[count % len_services])
			count += 1
			
		return dict_data
	
	
# test
if __name__ == "__main__":
	mytest = ServiceClusterMap("all")
	mytest.update(mytest.genRandomValues())
	mytest.plot()
	#print mytest.genRandomValues()

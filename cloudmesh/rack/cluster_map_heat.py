"""
Heat map of cluster servers, use HSV color space
"""
import math
from copy import deepcopy
from cloudmesh.rack.base_cluster_map import BaseClusterMap


class HeatClusterMap(BaseClusterMap):

    
	# maximum h, 240/360 = 2/3
	h_max = 2.0 / 3.0
	
	# minimum temperature user defined
	temperature_min = 0
	
	# maximum temperature user defined
	temperature_max = 100
	
	# mapping dict
	# map the value of a temperature to a tuple RGB color
	# the key of dict is the different temperature got from cluster servers
	# the precise of the key is 0.1
	# formation is: {10.2:(255, 3, 5), 25.3:(34, 50, 200), ...}
	dict_mapping = {} 
	
	# color table, NOT used, 
	#
	# instead of using a fixed color table, we use a dynamic color table from #0000FF to #FF0000
	# With the dynamic color table, we can have 240 different colors rather than 100
	# If possilbe, we can change the 240 colors to 2M (240 * 100 * 100) colors according to the HSV color space
	# But, I think it is enough for us to denote the different status of clusters with 240 colors
	
	def __init__(self, name, min_temp=0, max_temp=100):
		self.temperature_min = float(min_temp if min_temp > 0 else 0)
		self.temperature_max = float(max_temp)
		# call parent init function
		BaseClusterMap.__init__(self, name)
		
	
	# get the RGB according to a specific temperature
	# the MAX different colors is 240, from #0000FF to #FF0000 with temperature ascending
	def getRGB(self, temp):
		rate = (self.temperature_max - temp) / (self.temperature_max - self.temperature_min)
		h = rate * self.h_max
		return self.getRGBWithH(h)
	
	
	# get proper temperature for cluster server
	# formation is XXX.X, the precise is 0.1
	def getProperTemperature(self, temp):
		return round(temp, 1)
	
	
	# default temperature for cluster servers
	def getDefaultTemperature(self):
		temp_default = self.temperature_min + (self.temperature_max - self.temperature_min)/3.0
		return self.getProperTemperature(temp_default)
		
	
	# ======================================
	#           abstract function
	#         sub-class MUST override
	# ======================================
	#
	# get default value for dict_servers
	def getServersDefaultValue(self):
		temp_default = self.getProperTemperature(self.getDefaultTemperature())
		temp_rgb = self.getRGB(temp_default)
		# update mapping dict with {temp_default:temp_rgb}
		self.dict_mapping.update({temp_default:temp_rgb})
		
		return temp_default
		
	
	
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
			#self.generateRandomTemperature()
			self.generateContinousTemperature()
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
		# step of temperature marker
		marker_step = int(round(self.temperature_max - self.temperature_min)) / 10
		marker_step_half = 0.5 * marker_step
		marker_list = [1, 2, 5, 10, 25, 50]
		
		prev_value = 1
		for value in marker_list:
			if marker_step < value:
				marker_step = prev_value
				break;
			prev_value = value;
		# start temperature on marker
		marker_start = int(round(self.temperature_min / marker_step)) * marker_step
		while marker_start < self.temperature_min + marker_step_half:
			marker_start += marker_step
		
		marker_end = int(round(self.temperature_max / marker_step)) * marker_step
		while marker_end > self.temperature_max - marker_step_half:
			marker_end -= marker_step
			
		marker_count = (marker_end - marker_start) / marker_step + 1
		#color_bar_count = xylim[0]
		color_bar_count = 240
		
		xcount = color_bar_count + 20
		xstep = xylim[0] / float(xcount)
		xstart = 10 * xstep
		xwidth = xstep
		ycount = 3.0 
		ystep = xylim[1] / ycount
		ystart = 0.5 * ystep
		yheight = 0.8 * ystep
		
		hstep = self.h_max / color_bar_count
		tstep_half = 0.5 * (self.temperature_max - self.temperature_min) / color_bar_count
		tstep = 2 * tstep_half
		
		# the first and last color bar
		color_bar_first = {"color": "#0000FF", "temp": self.temperature_min}
		color_bar_last = {"color": "#FF0000", "temp": self.temperature_max}
		
		temp_current = self.temperature_min
		marker_current = marker_start
		for i in range(0, color_bar_count+1):
			rect = self.genDefaultRect()
			lb_x = xstart
			lb_y = ystart + ystep
			rect.update({"verts":{"lb":(lb_x, lb_y), "rt":(lb_x + xwidth, lb_y + yheight)}})
			# color
			if i == 0:
				rcolor = color_bar_first["color"]
			elif i == color_bar_count:
				rcolor = color_bar_last["color"]
			else:
				h = (color_bar_count - i) * hstep
				rcolor = self.convertRGB2Hex(self.getRGBWithH(h))
			
			rect.update({"facecolor_rect":rcolor, "edgecolor_rect":rcolor})
			
			# label
			lb_x -= xstep
			if i == 0:
				rect.update({"label":{"lb":(lb_x-0.5*xstep, ystart), "text": self.temperature_min}})
			elif i == color_bar_count:
				rect.update({"label":{"lb":(lb_x, ystart), "text": self.temperature_max}})
			# marker
			elif abs(temp_current - marker_current) < tstep_half:
				rect.update({"label":{"lb":(lb_x, ystart), "text": marker_current}})
				rect.update({"marker": True})
				marker_current += marker_step
				
			xstart += xstep
			temp_current += tstep
			
			self.drawRectangle(ax, rect)
		
		
	
	# only for test
	# generate random temperature for cluster servers
	def generateRandomTemperature(self):
		# init the seed of random function
		self.getRandom(True)
		
		for server in self.dict_servers:
			temp_rand = self.getRandom()
			temp = self.getProperTemperature(self.temperature_min + temp_rand * (self.temperature_max - self.temperature_min))
			rgb = self.getRGB(temp)
			# update mapping dict
			self.dict_mapping.update({temp:rgb})
			
			self.dict_servers[server] = temp
		
	# only for test, especially continuous colors
	def generateContinousTemperature(self):
		arr = sorted(self.dict_servers.keys())
		len_arr = len(arr)
		# found a unknown cluster
		if len_arr == 0:
			return
		
		step = (self.temperature_max - self.temperature_min)/len_arr
		temp_current = self.temperature_min
		
		for server in arr:
			temp = self.getProperTemperature(temp_current)
			rgb = self.getRGB(temp)
			self.dict_mapping.update({temp:rgb})
			temp_current += step
			
			self.dict_servers[server] = temp
	
	
# test
if __name__ == "__main__":
	mytest = HeatClusterMap("india", 43, 349)
	mytest.plot()

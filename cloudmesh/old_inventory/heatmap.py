from jinja2 import Template
from sh import rackdiag
from hostlist import expand_hostlist
import time
import random
from os import path
import sys
import re


class MyTempMap:


    #
    # Filename of server.diag
    #
    diag_filename = ""
    
    #
    # type of image
    #
    image_type = "svg"
    
    #
    # filename of image
    #
    image_filename = ""
    
    # content of diag file
    diag_content = ""
    
    # temporary diag file
    diag_temp_filename = ""
    
    #
    # Array of sever names
    # This array is always a double array
    # the 1st array is related to a rack
    # the 2nd items is a server in the specific rack
    # the 3rd is the data of the corresponding server (name, code of template)
    # 
    arr_servers = []
    
    #
    # color substitute dict 
    #
    dict_colors = {}
    
    
    #
    # static regex pattern for parsing rackXXX.diag file
    #
    
    # racklist, a group of rack
    patt_racklist = re.compile("rackdiag\s*?\{", re.I)
    
    # rack, a group of server
    patt_rack = re.compile("rack\s*?\{", re.I)
    
    # description // .... 
    patt_desc = re.compile("^//", re.I)
    
    # total server units, e.g., 48U
    patt_total_u = re.compile("^\d+?u", re.I)
    
    # a record of normal server 
    # 5: gravel01 [2U] {{gravel01}}
    # 5: gravel01 {{gravel01}}
    # 5: {{gravel01}}
    patt_server_normal = re.compile("(^\d+?):((?:\s*?\w+?)?(?:\s*?\[\w+?\])?)\s*?\{\{(\w+?)\}\}", re.I)
    
    # already rendered record of server
    #  5: gravel01 [2U] [color=XXXX]
    #  5: gravel01 [color=XXXX]
    #  5: [color=XXXX]
    patt_server_render = re.compile("(^\d+?):((?:\s*?\w+?)?(?:\s*?\[\w+?\])?)\s*?\[color\s*?=\s*?(\w+?)\]", re.I)
    
        
    #
    # the image file locates in the same directory with the input filename
    # param: filename is the input filename of a rackXXX.diag
    # 
    def __init__(self, filename, type):
    	fullname = path.abspath(filename)
    	self.diag_filename = fullname.lower()
    	
    	basename = path.basename(self.diag_filename)
    	dirname = path.dirname(self.diag_filename)
    	
    	# check extension of input filename
    	if not basename.endswith(".diag"):
    		print "Warning: ONLY .diag file is supported. Exit immediately!"
    		sys.exit(-1)
    	
    	# set diag temporary filename
    	self.diag_temp_filename = self.diag_filename[0:-5] + "-temp.diag"
    	
    	# set image file to the default svg format
    	self.set_image_format(self.image_type)
    	    	
    
    # set image type
    # change the extension of image filename
    def set_image_format(self, type):
    	if not type:
    		print "You must set a non-empty type."
    		exit
    	
    	# lower string of type
    	ltype = type.lower()
    	if self.image_filename:
    		stype = "." + ltype
    		if self.image_filename.endswith(stype):
    			print "The default or previous image type already is {0}".format(type)
    			return
    	if ltype in ["svg", "png"]:
    		self.image_type = ltype
    	else:
    		print "Image type {0} is NOT supported currently!".format(type)
    		print "Use svg to replace ."
    		self.image_type = "svg"
    	
    	# filename, diag filename ends with ".diag"
    	# image filename ends with "." + a valid lower image type 
    	self.image_filename = self.diag_filename[0:-4] + self.image_type


        # bug use    (name, ending) = self.image_filename.split(".",-1) 
        # http://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    	print "image filename is: " + self.image_filename

    
	# update server color code to a real color in RGB space
    def update_server_color(self, scode, scolor):
    	if scode in self.dict_colors:
    		print "update dict_colors with [{0}, {1}]".format(scode, scolor)
    		self.dict_colors.update({scode: scolor})
    	else:
    		print "[Error] code {0} does NOT exist in dict_colors.".format(scode) 
    
    
    # add color to color_dict
    def append_server_color(self, scode):
		if scode in self.dict_colors:
			print "Find a same color code among different server. \n Please check the origial rackXXX.diag file."
		else:
			self.dict_colors[scode] = scode
    
    
    #
    # ONLY used when a rack embed in the racklist
    # IF there is only one rack, this function should NOT be called
    # 
    # add one server record into 3-dimension array data structure
    # 	
    def addRackListServer(self, rackIndex, numIndex, sname, scolor):
    	print "into add server info ..."
    	
    	arr_record = (numIndex, sname, scolor)
    	print arr_record
    	
    	self.arr_servers[rackIndex].append(arr_record)
    	
    	# add color to color_dict
    	self.append_server_color(scolor)
    	
    	
    	
    # ONLY has a rack in rackXXX.diag file
    # It will be a 2-dimension array, containing ONLY one rack
    def addRackServer(self, numIndex, sname, scolor):
    	print "into add server info [rack] ..."
    	
    	arr_record = (numIndex, sname, scolor)
    	print arr_record
    	
    	self.arr_servers.append(arr_record)
    	
    	# add color to color_dict
    	self.append_server_color(scolor)
    
    

    #
    # read information from the diag file
    #
    def readDiagInfo(self):
    	print "Ready to read DIAG info from {0} ...".format(self.diag_filename)
        rf = open(self.diag_filename, "r")
        
        print rf
        
        rackindex = -2;
        for aline in rf:
        	print aline
        	
        	# keep the file content in memory
        	# add line string to diag_content
        	self.diag_content += aline
        	self.diag_content += "\n"
        	
        	line = aline.strip()
        	# normal server
        	m = self.patt_server_normal.match(line)
        	if m:
        		print "find normal server..."
        		sindex = m.group(1).strip()
        		sname = m.group(2).strip()
        		scolor = m.group(3).strip()
        		if rackindex < 0:
        			print "ONLY a SINGLE rack exist..."
        			self.addRackServer(sindex, sname, scolor)
        		else:
        			self.addRackListServer(rackindex, sindex, sname, scolor)
        		
        		continue
        	
        	# rendered server
        	m = self.patt_server_render.match(line)
        	if m:
        		print "find rendered server..."
        		sindex = m.group(1).strip()
        		sname = m.group(2).strip()
        		scolor = m.group(3).strip()
        		if rackindex < 0:
        			print "ONLY a SINGLE rack exist..."
        		
        		print "RENDERED Info: index={0}, name={1}, color={2}".format(sindex, sname, scolor)
        		continue
        	
        	# description
        	m = self.patt_desc.match(line)
        	if m:
        		print "find description..."
        		continue
        		
        	# rack
        	m = self.patt_rack.match(line)
        	if m:
        		print "find rack..."
        		self.arr_servers.append([]);
        		rackindex += 1
        		continue
        	
        	# total U
        	m = self.patt_total_u.match(line)
        	if m:
        		print "find total u.."
        		continue
        	
        	# racklist
        	m = self.patt_racklist.match(line)
        	if m:
        		print "find racklist.."
        		rackindex += 1
        		continue
        	
        	# currently, ignore all unmatched items/lines
        	# To do...	
        	
        # Finally, close file
        rf.close()
    
    #
    # generate a new diag file with random temperature or color
    # 
    def writeTempDiagInfo(self):
    	arr = {}
    	for k in self.dict_colors.keys():
    		vcolor = '[color="{0}"];'.format(self.dict_colors[k])
    		arr[k] = vcolor
    		
    	wf = open(self.diag_temp_filename, "w")
    	template = Template(self.diag_content)
    	scontent = template.render(arr)
    	wf.write(scontent)
    	wf.close()
    	
    
    #
    # generate an image with the tool of rackdiag
    #
    def gen_rack_image(self):
    	# step 1. write temporary diag file to disk
    	self.writeTempDiagInfo()
    	
    	# step 2. call rackdiag to make a image
    	self.plot_rackdiag()
        
    
    
    def convertNumToRGB_2(self, value):
        h = [
            (0, 0, 255),
            (0, 1, 255),
            (0, 2, 255),
            (0, 4, 255),
            (0, 5, 255),
            (0, 7, 255),
            (0, 9, 255),
            (0, 11, 255),
            (0, 13, 255),
            (0, 15, 255),
            (0, 18, 253),
            (0, 21, 251),
            (0, 24, 250),
            (0, 27, 248),
            (0, 30, 245),
            (0, 34, 243),
            (0, 37, 240),
            (0, 41, 237),
            (0, 45, 234),
            (0, 49, 230),
            (0, 53, 226),
            (0, 57, 222),
            (0, 62, 218),
            (0, 67, 214),
            (0, 71, 209),
            (0, 76, 204),
            (0, 82, 199),
            (0, 87, 193),
            (0, 93, 188),
            (0, 98, 182),
            (0, 104, 175),
            (0, 110, 169),
            (0, 116, 162),
            (7, 123, 155),
            (21, 129, 148),
            (34, 136, 141),
            (47, 142, 133),
            (60, 149, 125),
            (71, 157, 117),
            (83, 164, 109),
            (93, 171, 100),
            (104, 179, 91),
            (113, 187, 92),
            (123, 195, 73),
            (132, 203, 63),
            (140, 211, 53),
            (148, 220, 43),
            (156, 228, 33),
            (163, 237, 22),
            (170, 246, 11),
            (176, 255, 0),
            (183, 248, 0),
            (188, 241, 0),
            (194, 234, 0),
            (199, 227, 0),
            (204, 220, 0),
            (209, 214, 0),
            (213, 207, 0),
            (217, 200, 0),
            (221, 194, 0),
            (224, 188, 0),
            (227, 181, 0),
            (230, 175, 0),
            (233, 169, 0),
            (236, 163, 0),
            (238, 157, 0),
            (240, 151, 0),
            (243, 145, 0),
            (244, 140, 0),
            (246, 134, 0),
            (248, 129, 0),
            (249, 123, 0),
            (250, 118, 0),
            (251, 112, 0),
            (252, 107, 0),
            (253, 102, 0),
            (254, 97, 0),
            (255, 92, 0),
            (255, 87, 0),
            (255, 82, 0),
            (255, 78, 0),
            (255, 73, 0),
            (255, 68, 0),
            (255, 64, 0),
            (255, 59, 0),
            (255, 55, 0),
            (255, 51, 0),
            (255, 47, 0),
            (255, 43, 0),
            (255, 39, 0),
            (255, 35, 0),
            (255, 31, 0),
            (255, 27, 0),
            (255, 23, 0),
            (255, 20, 0),
            (255, 16, 0),
            (255, 13, 0),
            (255, 10, 0),
            (255, 8, 0),
            (255, 3, 0)]
        
        i = int(value * 100)


        (r, g, b) = h[i]
        print "INDEX", value, i, r, g, b

        return "#{0:02X}{1:02X}{2:02X}".format(r, g, b)


    # 
    # convert a number between 0.00 and 1.00 to a RGB value represented by Hex value
    #
    def convertNumToRGB(self, value):
    	# y = mx + b
        # m = 4
        # x = value
        # y = RGB__
        if (0 <= value and value <= 1 / 8) :
            RGB_R = 0
            RGB_G = 0
            RGB_B = 4 * value + .5  # .5 - 1 # b = 1/2
        elif (1 / 8 < value and value <= 3 / 8) :
            RGB_R = 0
            RGB_G = 4 * value - .5  # 0 - 1 # b = - 1/2
            RGB_B = 0
        elif (3 / 8 < value and value <= 5 / 8) :
            RGB_R = 4 * value - 1.5  # 0 - 1 # b = - 3/2
            RGB_G = 1
            RGB_B = -4 * value + 2.5  # 1 - 0 # b = 5/2
        elif (5 / 8 < value and value <= 7 / 8) :
            RGB_R = 1
            RGB_G = -4 * value + 3.5  # 1 - 0 # b = 7/2
            RGB_B = 0
        elif (7 / 8 < value and value <= 1) :
            RGB_R = -4 * value + 4.5  # 1 - .5 # b = 9/2
            RGB_G = 0
            RGB_B = 0
        else :  # should never happen - value > 1
            RGB_R = .5
            RGB_G = 0
            RGB_B = 0


        # scale for hex conversion
        RGB_R *= 15
        RGB_G *= 15
        RGB_B *= 15

        shexRGB = "#{0:02X}{1:02X}{2:02X}".format(int(round(RGB_R)), int(round(RGB_G)), int(round(RGB_B)))

        return shexRGB
    

    
    # generate random temperature for all possilbe server with color code
    # just do this in dict_colors data structure
    def gen_random_temperature(self):
    	self.get_random(True)
    	for scode in self.dict_colors.keys():
    		rtemp = self.get_random(False);
    		rcolor = self.convertNumToRGB_2(rtemp)
    		self.update_server_color(scode, rcolor)
    
    # set a specific temperature for a server
    # this method MUST call after gen_random_temperature
    def set_server_temperature(self, scode, stemp):
    	if stemp < 0.0 or stemp > 1.0:
    		print "[Error]Temperature MUST in range 0.0 -- 1.0, "
    		return
    	
    	if scode in self.dict_colors:
    		print "Find server {0}".format(scode)
    		rtemp = self.convertNumToRGB_2(stemp)
    		self.dict_colors.update({scode:rtemp})
    	else:
    		print "Cannot find server {0} in server list".format(scode)
    
    
    # get random number
    # range is 0.00 ~ 0.99
    # params:
    #   bResetSeed, a Boolean value. True means the seed of Random will be set,
    #                Flase, do not touch the seed of Random
    def get_random(self, bResetSeed=True):
        if bResetSeed:
            rseed = time.time()
            random.seed(100)
        
        rand = random.random()
        # ivalue = int(rand * 100)
        # fvalue = float(ivalue / 100.0)
        return rand
    
    #
    # call rackdiag to make a image
    #
    def plot_rackdiag(self):
    	# write temporary diag file to disk
    	self.writeTempDiagInfo()
    	
    	# call rackdiag to plot
    	r = rackdiag("-T{0}".format(self.image_type),
                    "-o", self.image_filename, self.diag_temp_filename)
        
    # plot_rackdiag(type, input_filename, output_filename)
    
    # only for testing ....
    # t = get_random_temperature()
    # print t

# main
if  __name__ == '__main__':

    arg_len = len(sys.argv)
    print "Number of arguments: ", arg_len, " ."
    if arg_len < 2:
        # usage
        # python chmap [type] diag_filename
        print "Usage:"
        print "\t python chmap [image_type] diag_filename"
        print "\t\t image_type ONLY support 'svg' and 'png' currently."
        print ""
        print "Example:"
        print "\t python chmap svg india-color.diag"
        print "\t or"
        print "\t python chmap india-color.diag"
        print ""    
        exit(-1)

    diag_file = sys.argv[arg_len - 1]
    print "input filename is ", diag_file 
    t = MyTempMap(diag_file, "svg")
    t.readDiagInfo()
    
    """
    print "server info..."
    print t.arr_servers
    print "dict colors..."
    print t.dict_colors
    t.gen_random_temperature()
    print "updated colors"
    print t.dict_colors
    t.set_server_temperature("india001", 2)
    print "call set server temperature, 2 "
    print t.dict_colors
    t.set_server_temperature("india001", -2)
    print "call set server temperature, -2"
    print t.dict_colors
    t.set_server_temperature("india001", 0.5)
    print "call set server temperature, 0.5"
    print t.dict_colors
    print "plot..."
    t.plot_rackdiag()
    print "plot ok"
    """


    d = {}
    temp = t.get_random(True)
    for spec in ['echo[01-16]', 'india[001-136]', 'delta[01-16]']:
        servers = expand_hostlist(spec)
        for server in servers:
            temp = t.get_random(False)
            t.set_server_temperature(server, temp)
    t.plot_rackdiag()


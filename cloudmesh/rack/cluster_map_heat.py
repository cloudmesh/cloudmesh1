"""
Heat map of cluster servers, use HSV color space
"""
from copy import deepcopy
from cloudmesh.rack.base_cluster_map import BaseClusterMap

from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)


class HeatClusterMap(BaseClusterMap):

    # maximum h, 240/360 = 2/3
    h_max = 2.0 / 3.0

    # unit of temperature 'C' or 'F'
    temperature_unit = 'C'

    # minimum temperature user defined
    temperature_min = 0

    # maximum temperature user defined
    temperature_max = 100

    # default temperature
    temperature_default = 0

    # RGB for unknown temperature of host
    rgb_unknown_temperature = (211, 211, 211)

    # mapping dict
    # map the value of a temperature to a tuple RGB color
    # the key of dict is the different temperature got from cluster servers
    # the precise of the key is 0.1
    # formation is: {10.2:(255, 3, 5), 25.3:(34, 50, 200), ...}
    dict_mapping = {}

    # temperature marker dict
    dict_marker = {"min": None,  # minimum temperature displayed on color bar, <= temperature_min
                   # maximum temperature displayed on color bar, >=
                   # temperature_max
                   "max": None,
                   "start": None,  # marker start displayed on color bar
                   "end": None,  # marker end displayed on color bar
                   "step": None,  # marker step
                   "round": None,  # temperarture precise
                   "range": None  # marker_max - marker_min
                   }

    # color table, NOT used,
    #
    # instead of using a fixed color table, we use a dynamic color table from #0000FF to #FF0000
    # With the dynamic color table, we can have 240 different colors rather than 100
    # If possilbe, we can change the 240 colors to 2M (240 * 100 * 100) colors according to the HSV color space
    # But, I think it is enough for us to denote the different status of
    # clusters with 240 colors

    def __init__(self, username, name,
                 dir_yaml=None, dir_diag=None, dir_output=None, img_type=None,
                 min_temp=0, max_temp=100):
        self.setTemperatureMinMax(min_temp, max_temp)
        # call parent init function
        BaseClusterMap.__init__(
            self, username, name, "temperature", dir_yaml, dir_diag, dir_output, img_type)

    def get_temperature_unit(self):
        return self.temperature_unit

    def set_temperature_unit(self, unit):
        upper_unit = "C" if not unit else unit.upper()
        if upper_unit in ['C', 'F']:
            self.temperature_unit = upper_unit

    def set_optional_param(self, aparam):
        self.set_temperature_unit(aparam)

    def get_optional_param(self):
        return self.get_temperature_unit()

    # set min/max temperature
    # adjust min/max and marker on color bar
    #
    def setTemperatureMinMax(self, tmin, tmax):
        self.temperature_min = float(tmin if tmin > 0 else 0)
        self.temperature_max = float(
            tmax if self.temperature_min < tmax else self.temperature_min + 1)

        # step of temperature marker
        marker_step = round(self.temperature_max - self.temperature_min) / 10
        # marker_step_half = 0.5 * marker_step
        marker_list = [
            0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 25, 50, 100, 200, 500]
        marker_round_list = [
            0.01, 0.01, 0.01, 0.01, 0.1, 0.1, 0.1, 1, 1, 2, 5, 10, 20, 50, 100]
        temp_round_list = [3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]
        # guess the perfect step of color bar marker
        prev_index = 0
        for value in marker_list:
            if marker_step < value:
                marker_step = marker_list[prev_index]
                marker_round = marker_round_list[prev_index]
                temp_round_precise = temp_round_list[prev_index]
                break
            prev_index += 1
        # marker start/end on color bar marker
        marker_start = int(
            round(self.temperature_min / marker_step)) * marker_step
        marker_end = int(
            round(self.temperature_max / marker_step)) * marker_step
        # min/max temperature on color bar
        marker_min = marker_start
        while marker_min > self.temperature_min:
            marker_min -= marker_round
        if marker_min < 0:
            marker_min = 0
        marker_max = marker_end
        while marker_max < self.temperature_max:
            marker_max += marker_round
        # re-evaluate marker start/end
        if marker_start == marker_min:
            marker_start += marker_step
        while marker_start - marker_step > marker_min:
            marker_start -= marker_step

        if marker_end == marker_max:
            marker_end -= marker_step
        while marker_end + marker_step < marker_max:
            marker_end += marker_step
        # save the property of marker
        self.dict_marker.update({"min": marker_min,
                                 "max": marker_max,
                                 "start": marker_start,
                                 "end": marker_end,
                                 "step": marker_step,
                                 "round": temp_round_precise,
                                 "range": marker_max - marker_min
                                 })

    # get the RGB according to a specific temperature
    # the MAX different colors is 240, from #0000FF to #FF0000 with
    # temperature ascending
    def getRGB(self, temp):
        rate = (self.dict_marker["max"] - temp) / self.dict_marker["range"]
        h = rate * self.h_max
        return self.getRGBWithH(h)

    # get proper temperature for cluster server
    # formation is XXX.YYY, the precise (YYY) is controlled by
    # self.dict_marker["round"]
    def getProperTemperature(self, temp):
        # temperature unknown
        round_temp = -1 if temp == - \
            1 else round(temp, self.dict_marker["round"])
        if round_temp not in self.dict_mapping.keys():
            temp_rgb = self.getRGB(round_temp)
            self.dict_mapping.update({round_temp: temp_rgb})

        return round_temp

    # default temperature for cluster servers
    def getDefaultTemperature(self):
        temp_default = self.temperature_min + \
            (self.temperature_max - self.temperature_min) / 3.0
        return self.getProperTemperature(temp_default)

    # ======================================
    #           abstract function
    #         sub-class MUST override
    # ======================================
    #
    # get default value for dict_servers
    def getServersDefaultValue(self):
        self.temperature_default = self.getDefaultTemperature()
        return self.temperature_default

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
    # params: dict_values means the data get from each server
    # this function MUST be called before plot to refresh status of servers in
    # memory
    def update(self, dict_values):
        if dict_values is None:
            return

        self.dict_mapping.clear()
        # unknow temperature of host
        self.dict_mapping.update({-1: self.rgb_unknown_temperature})
        arr_values = [
            value for value in sorted(dict_values.values()) if value >= 0]
        self.setTemperatureMinMax(arr_values[0], arr_values[-1])
        self.resetDictServers(self.getServersDefaultValue())

        for server in dict_values:
            value = self.getProperTemperature(dict_values[server])
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
        marker_min = self.dict_marker["min"]
        marker_max = self.dict_marker["max"]
        marker_start = self.dict_marker["start"]
        # marker_end = self.dict_marker["end"]
        marker_step = self.dict_marker["step"]

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
        tstep_half = 0.5 * (marker_max - marker_min) / color_bar_count
        tstep = 2 * tstep_half

        temp_current = marker_min
        marker_current = marker_start
        for i in range(0, color_bar_count + 1):
            rect = self.genDefaultRect()
            lb_x = xstart
            lb_y = ystart + ystep
            rect.update(
                {"verts": {"lb": (lb_x, lb_y), "rt": (lb_x + xwidth, lb_y + yheight)}})
            # color
            if i == 0:
                rcolor = "#0000FF"
            elif i == color_bar_count:
                rcolor = "#FF0000"
            else:
                h = (color_bar_count - i) * hstep
                rcolor = self.convertRGB2Hex(self.getRGBWithH(h))

            rect.update({"facecolor_rect": rcolor, "edgecolor_rect": rcolor})

            # label
            lb_x -= xstep
            if i == 0:
                rect.update(
                    {"label": {"lb": (lb_x - 0.5 * xstep, ystart), "text": marker_min}})
            elif i == color_bar_count:
                rect.update(
                    {"label": {"lb": (lb_x, ystart), "text": marker_max}})
            # marker
            elif abs(temp_current - marker_current) < tstep_half:
                rect.update(
                    {"label": {"lb": (lb_x, ystart), "text": marker_current}})
                rect.update({"marker": True})
                marker_current += marker_step

            xstart += xstep
            temp_current += tstep

            self.drawRectangle(ax, rect)
        # temperature unit
        pos_unit = (xstart * 0.4, 0)
        options = {
            "C": "Celsius",
            "F": "Fahrenheit",
        }
        self.drawText(ax, pos_unit, "( Temperature unit: {0} )".format(
            options[self.temperature_unit]))

    # only for test
    def genRandomValues(self, flag_continue=True):
        if flag_continue:
            return self.generateContinousTemperature()
        else:
            return self.generateRandomTemperature()

    # only for test
    # generate random temperature for cluster servers
    def generateRandomTemperature(self):
        # init the seed of random function
        self.getRandom(True)

        dict_data = {}
        for server in self.dict_servers:
            temp_rand = self.getRandom()
            temp = self.getProperTemperature(
                self.temperature_min + temp_rand * (self.temperature_max - self.temperature_min))
            dict_data[server] = temp

        return dict_data

    # only for test, especially continuous colors
    def generateContinousTemperature(self):
        arr = sorted(self.dict_servers.keys())
        len_arr = len(arr)
        # found a unknown cluster
        if len_arr == 0:
            return

        step = (self.temperature_max - self.temperature_min) / len_arr
        temp_current = self.temperature_min

        dict_data = {}
        for server in arr:
            dict_data[server] = self.getProperTemperature(temp_current)
            temp_current += step

        return dict_data


# test
if __name__ == "__main__":
    mytest = HeatClusterMap("echo")
    ddata = {'e010': 43.0, 'e016': 53.0, 'e011': 43.0, 'e012': 43.0, 'e003': 43.0, 'e002': 43.0, 'e001': 43.0, 'e013':
             51.0, 'e007': 43.0, 'e006': 43.0, 'e005': 43.0, 'e004': 43.0, 'e014': 43.0, 'e009': 43.0, 'e008': 43.0, 'e015': 43.0}
    # mytest.update(mytest.genRandomValues())
    legend_size = mytest.getImageLegendSize()
    print "legend size: ", legend_size
    mytest.update(ddata)
    mytest.plot()

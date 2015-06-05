from __future__ import print_function
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.inventory import Inventory
from pprint import pprint
from cloudmesh_base.Shell import Shell
import re

from cloudmesh_base.logger import LOGGER

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)


class cm_temperature:

    # instance of cm_config_server
    config_server = None

    # instance of Inventory
    inventory = None

    # pattern of temperature, such as "30 degrees C"
    patt = re.compile("([0-9+.-]+?)\s+degrees\s+([A-Z])", re.I)

    def __init__(self):
        self.config_server = cm_config_server().get(
            "cloudmesh.server.clusters")
        self.inventory = Inventory()

    # get sensor temperature with ipmitool
    # param: hostname is a uniform hostname as the following
    #    india cluster: i001, i010, i100
    #    echo cluster: e001, e010
    #    delta cluster: d001, d010
    #    bravo cluster: b001, b010
    #
    # return: a dict with the following style:
    #                         {
    #                            "name": "Domain A FP Temp",
    #                            "address": "44h",
    #                            "status": "ok",
    #                            "entity": "7.1",
    #                            "value": "24"
    #                            "unit": "C"
    #                          }
    def get_ipmi_temperature(self, hostname):

        (hostaddr, data) = self.inventory.ipadr_cluster(hostname, "bmc")
        clustername = data["cm_cluster"]
        config = self.config_server[clustername]['bmc']
        # username and password to access ipmitool
        password = config['password']
        username = config['user']

        command = "ipmitool -I lanplus -H {0} -U {1} -P {2} sdr type temperature".format(
            hostaddr, username, password)
        # access ipmitool need a proxy server
        proxyaddr = config['proxy']['ip']
        proxyusername = config['proxy']['user']

        log.debug("Get temperature for host '{2}' via proxy server '{0}@{1}'".format(
            proxyusername, proxyaddr, hostname))

        try:
            result = Shell.ssh("{0}@{1}".format(proxyusername, proxyaddr), command)
        except:
            result = ""

        dict_result = None
        if result == "":
            log.warning(
                "Cannot access to host '{0}' OR ipmitool failed on host '{0}'".format(hostname))
        else:
            log.debug(
                "Temperature data retrieved from host '{0}' successfully.".format(hostname))
            dict_result = {}
            lines = result.split("\n")
            for line in lines:
                fields = map(lambda x: x.strip(), line.split("|"))
                name = fields[0]
                # test and ignore the blank line in the last output
                if name == "":
                    continue
                value = "-1"
                unit = "C"
                m = self.patt.match(fields[4])
                if m:
                    value = m.group(1)
                    unit = m.group(2)
                dict_result[name] = {"name": fields[0],
                                     "address": fields[1],
                                     "status": fields[2],
                                     "entity": fields[3],
                                     "value": value,
                                     "unit": unit
                                     }
        return dict_result

    # get the max temperature on a server
    # params: tdict is the result from get_ipmi_temperature
    #         unit is a temperature unit either 'C' or 'F'
    # return: a dictary
    def parse_max_temp(self, tdict, unit):
        unit_upper = unit.upper()
        max_temp = -1
        options = {
            "C": "convert_temp_C2F",
            "F": "convert_temp_F2C",
        }
        if tdict is not None:
            for name in tdict:
                if tdict[name]["status"].lower() == "ok":
                    value = round(float(tdict[name]["value"]), 1)
                    if unit_upper != tdict[name]["unit"].upper():
                        value = getattr(self, options[unit_upper])(value)
                    if value > max_temp:
                        max_temp = value

        return {"unit": unit_upper, "value": max_temp}

    # convert temperature from Fahrenheit (F) to Celsius (C)
    def convert_temp_C2F(self, cvalue):
        return round(cvalue * 1.8 + 32, 1)

    # convert temperature from Celsius (C) to Fahrenheit (F)
    def convert_temp_F2C(self, fvalue):
        return round((fvalue - 32) / 1.8, 1)

# debug test
if __name__ == "__main__":
    hostname = "e005"
    ct = cm_temperature()
    arrdict = {}
    # pprint (ct.get_ipmi_temperature(hostname))
    # echo clusters
    arrname = ["e001", "e002", "e003", "e004", "e005", "e006", "e007",
               "e008", "e009", "e010", "e011", "e012", "e013", "e014", "e015", "e016"]
    for name in arrname:
        arrdict[name] = ct.get_ipmi_temperature(name)

    # output information
    for name in arrname:
        print("host [{0}] information:".format(name))
        if arrdict[name] is None:
            print("Cannot access host {0}".format(name))
        else:
            pprint(arrdict[name])
        print("-" * 40)

from cloudmesh.util.config import read_yaml_config
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.provisioner.baremetal_status import BaremetalStatus
import requests
import json
from time import sleep
import threading
from cloudmesh_common.logger import LOGGER
#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)


class CobblerRestAPI:

    """Cobbler REST Service API
    This class provide the access to cobbler provision API via REST service. 
    """

    def __init__(self):
        self.server_url = self.get_server_url()
        self.bm_status = BaremetalStatus()

    def get_cobbler_distro_list(self):
        """
        shortcut for get cobbler distro list
        """
        return self.get_cobbler_object_list("distro")

    def get_cobbler_profile_list(self):
        """
        shortcut for get cobbler profile list
        """
        return self.get_cobbler_object_list("profile")

    def get_cobbler_system_list(self):
        """
        shortcut for get cobbler system list
        """
        return self.get_cobbler_object_list("system")

    def get_cobbler_kickstart_list(self):
        """
        shortcut for get cobbler kickstart list
        """
        return self.get_cobbler_object_list("kickstart")

    def get_cobbler_iso_list(self):
        """
        shortcut for get cobbler iso file list
        """
        return self.get_cobbler_object_list("iso")

    def get_cobbler_object_list(self, cobbler_object):
        """list the cobbler objects.
        :param string cobbler_object: one of the cobbler objects, currently support four objects, 'distro', 'profile', 'system', 'kickstart'
        :return: a list with the formation ['name1', 'name2', ] of corresponding objects if cobbler_object is a valid object, otherwise None
        :rtype: list 
        """
        url = "/cm/v1/cobbler/{0}s".format(cobbler_object)
        rest_data = self.request_rest_api("get", url)
        return rest_data["data"] if rest_data["result"] else None

    def get_cobbler_distro_children(self, name):
        """
        shortcut for get cobbler children of distro *name*
        """
        return self.get_cobbler_object_children("distro", name)

    def get_cobbler_profile_children(self, name):
        """
        shortcut for get cobbler children of profile *name*
        """
        return self.get_cobbler_object_children("profile", name)

    def get_cobbler_object_children(self, cobbler_object, name):
        """list the children of cobbler objects.
        :param string cobbler_object: one of the cobbler objects, currently support four objects, 'distro', 'profile',
        :return: a list with the formation ['name1', 'name2', ] of corresponding objects if cobbler_object is a valid object, otherwise None
        :rtype: list 
        """
        if cobbler_object in ["distro", "profile"]:
            url = "/cm/v1/cobbler/{0}s/{1}/child".format(cobbler_object, name)
            rest_data = self.request_rest_api("get", url)
            return rest_data["data"] if rest_data["result"] else None
        return None

    def get_cobbler_profile_based_kickstart(self, ks_filename):
        """
        get cobbler profile defined with the kickstart filename *ks_filename*
        """
        url = "/cm/v1/cobbler/kickstarts/{0}/profile".format(ks_filename)
        rest_data = self.request_rest_api("get", url)
        return rest_data["data"] if rest_data["result"] else None

    def get_cobbler_distro_report(self, name):
        """
        shortcut for get cobbler distro report
        """
        return self.get_cobbler_object_report("distro", name)

    def get_cobbler_profile_report(self, name):
        """
        shortcut for get cobbler profile report
        """
        return self.get_cobbler_object_report("profile", name)

    def get_cobbler_system_report(self, name):
        """
        shortcut for get cobbler system report
        """
        return self.get_cobbler_object_report("system", name)

    def get_cobbler_kickstart_report(self, name):
        """shortcut for get cobbler kickstart report
        :param string name: the filename of kickstart file, it supports UNIX wildcard
        :return: a list of the format [{"name": "full name", "contents": [lines...]}, {}]
        """
        return self.get_cobbler_object_report("kickstart", name)

    def get_cobbler_object_report(self, cobbler_object, name):
        """get the detail report of cobbler object
        :param string cobbler_object: one of the cobbler objects, currently support four objects, 'distro', 'profile', 'system', 'kickstart'
        :param string name: the name of the cobbler object. It supports UNIX wildcards
        :return: a list of corresponding object with full name if cobbler_object is a valid object and named object exists, otherwise None
        The formation of result is: [{"name": "full_name", "field1": "value1",}, {}]
        """
        url = "/cm/v1/cobbler/{0}s/{1}".format(cobbler_object, name)
        rest_data = self.request_rest_api("get", url)
        return [v["data"] for v in rest_data["data"]] if rest_data["result"] else None

    def add_cobbler_distro(self, data):
        """add a distribution to cobbler.
        :param dict data: a json data structure. The formation is {"name": "your distro name", "url": "full url of iso"}
        :return: a dict {"distro": "name", "profile": "name"} means add distro operation success, otherwise None means failed
        """
        return self.add_cobbler_object("distro", data, flag_return_data=True)

    def add_cobbler_profile(self, data):
        """add a profile to cobbler.
        :param dict data: a json data structure. The formation is {"name": "your profile name", "distro": "distro", "kickstart": "kickstart.file",}
        :return: True means add profile operation success, otherwise Failed
        """
        return self.add_cobbler_object("profile", data)

    def add_cobbler_system(self, data):
        """add a system to cobbler.
        :param dict data: a json data structure. The formation is {"name": "your system name", "profile": "profile", "power": {}, "interfaces": [{}, {},]}
        :return: True means add system operation success, otherwise Failed
        """
        return self.add_cobbler_object("system", data)

    def add_cobbler_kickstart(self, data):
        """add a kickstart to cobbler.
        :param dict data: a json data structure. The formation is {"name": "your kickstart filename", "contents": [line, line,...]}
        :return: True means add kickstart operation success, otherwise Failed
        """
        return self.add_cobbler_object("kickstart", data)

    def add_cobbler_object(self, cobbler_object, data, flag_return_data=False):
        """add a specific object to cobbler.
        :param string cobbler_object: one of the cobbler objects, currently support four objects, 'distro', 'profile', 'system', 'kickstart'
        :param dict data: a json data structure. The formation is {"name": "your object name", ...}
        :return: True means add an object operation success, otherwise Failed
        """
        url = "/cm/v1/cobbler/{0}s/{1}".format(cobbler_object, data["name"])
        rest_data = self.request_rest_api("post", url, data)
        if flag_return_data:
            return rest_data["data"] if rest_data["result"] else None
        return rest_data["result"]

    def update_cobbler_distro(self, data):
        """update a distro to cobbler. 
        :param dict data: a json data structure. The formation is {"name": "your distro name", "comment": "your comment", "owners": "specified owners",}
        :return: True means update distro operation success, otherwise Failed
        """
        return self.update_cobbler_object("distro", data)

    def update_cobbler_profile(self, data):
        """update a profile to cobbler. 
        :param dict data: a json data structure. The formation is {"name": "your profile name", "distro": "distro", "kickstart": "kickstart.file", "comment": "your comment", "owners": "specified owners",}
        :return: True means update profile operation success, otherwise Failed
        """
        return self.update_cobbler_object("profile", data)

    def update_cobbler_system(self, data):
        """update a system to cobbler.
        :param dict data: a json data structure. The formation is {"name": "your system name", "profile": "profile", "comment": "your comment", "owners": "specified owners", "power": {}, "interfaces": [{}, {},]}
        :return: True means update system operation success, otherwise Failed
        """
        return self.update_cobbler_object("system", data)

    def update_cobbler_kickstart(self, data):
        """update a kickstart to cobbler.
        :param dict data: a json data structure. The formation is {"name": "your kickstart filename", "contents": [line, line,...]}
        :return: True means update kickstart operation success, otherwise Failed
        """
        return self.update_cobbler_object("kickstart", data)

    def update_cobbler_object(self, cobbler_object, data):
        """update a specific object to cobbler.
        :param string cobbler_object: one of the cobbler objects, currently support THREE objects, 'profile', 'system', 'kickstart'
        :param dict data: a json data structure. The formation is {"name": "your object name", ...}
        :return: True means update an object operation success, otherwise Failed
        """
        url = "/cm/v1/cobbler/{0}s/{1}".format(cobbler_object, data["name"])
        rest_data = self.request_rest_api("put", url, data)
        return rest_data["result"]

    def remove_cobbler_distro(self, name):
        """
        shortcut for remove cobbler distro item `name`
        """
        return self.remove_cobbler_object("distro", name)

    def remove_cobbler_profile(self, name):
        """
        shortcut for remove cobbler profile  item `name`
        """
        return self.remove_cobbler_object("profile", name)

    def remove_cobbler_system(self, name):
        """
        shortcut for get cobbler system  item `name`
        """
        return self.remove_cobbler_object("system", name)

    def remove_cobbler_kickstart(self, name):
        """
        shortcut for get cobbler kickstart  item `name`
        """
        return self.remove_cobbler_object("kickstart", name)

    def remove_cobbler_object(self, cobbler_object, name):
        """remove a specific object to cobbler.
        :param string cobbler_object: one of the cobbler objects, currently support FOUR objects, 'distro', 'profile', 'system', 'kickstart'
        :param string name: the name of the cobbler object.
        :return: True means remove an object operation success, otherwise Failed
        """
        url = "/cm/v1/cobbler/{0}s/{1}".format(cobbler_object, name)
        rest_data = self.request_rest_api("delete", url)
        return rest_data["result"]

    def remove_cobbler_system_interface(self, system_name, if_name):
        """remove a specific interface *if_name* from the cobbler system *system_name*.
        :param string system_name: the name of a cobbler system
        :param string if_name: the name of an interface on the cobbler system.
        :return: True means remove an interface operation success, otherwise Failed
        """
        url = "/cm/v1/cobbler/systems/{0}/{1}".format(system_name, if_name)
        rest_data = self.request_rest_api("delete", url)
        return rest_data["result"]

    def monitor_cobbler_system(self, name):
        """monitor the status of baremetal system *name* via ping service.
        :param string name: the name of a cobbler system or host
        :return: True means system is ON, otherwise OFF.
        """
        url = "/cm/v1/cobbler/baremetal/{0}".format(name)
        rest_data = self.request_rest_api("get", url)
        return rest_data["result"]

    def deploy_cobbler_system(self, name):
        """deploy baremetal system *name*. 
        The cycle of deply system status is False(OFF) --> True(ON) --> False(OFF).
        :param string name: the name of a cobbler system or host
        :return: Always return True, which ONLY means has sent deploy command through IPMI. You MUST call `monitor_cobbler_system` to get the status of the system `name`.
        """
        # init deploy status
        self.bm_status.init_deploy_status(name)
        # call deploy REST
        url = "/cm/v1/cobbler/baremetal/{0}".format(name)
        rest_data = self.request_rest_api("post", url)
        # save deploy command result to mongodb
        self.bm_status.update_deploy_command_result(name, rest_data["result"])
        if rest_data["result"]:
            # monitor status
            self.monitor_deploy_power_status(name, "deploy")
        return rest_data["result"]

    def power_cobbler_system(self, name, flag_on=True):
        """power ON/OFF baremetal system *name*. 
        The system is ON/OFF must be call **monitor_cobbler_system** and its result is True(ON)/False(OFF)
        :param string name: the name of a cobbler system or host
        :param boolean flag_on: a boolean value. True means to power on the system, False means power off.
        :return: Always return True, which ONLY means has sent deploy command through IPMI. You MUST call `monitor_cobbler_system` to get the status of the system `name`.
        """
        # init power status
        self.bm_status.init_power_status(name, flag_on)
        # call power REST
        url = "/cm/v1/cobbler/baremetal/{0}".format(name)
        data = {"power_on": flag_on, }
        rest_data = self.request_rest_api("put", url, data)
        if rest_data["result"]:
            # monitor status
            self.monitor_deploy_power_status(name, "power", flag_on)
        return rest_data["result"]

    def monitor_deploy_power_status(self, name, action, flag_on=True):
        """monitor the deploy/power ON/OFF status of host name. 
        :param string name: the unique ID of host
        :param string action: action of "deploy" or "power"
        :param boolean flag_on: ONLY valid when action is power, True means power ON, False means OFF
        """
        data = {"cm_id": name,
                "action": action,
                "flag_on": flag_on,
                "time": 10,  # 10 seconds
                }
        t = threading.Thread(target=self.monitor_status_thread, args=[data])
        t.start()

    def monitor_status_thread(self, data):
        result = True
        host = data["cm_id"]
        while result:
            status = "ON" if self.monitor_cobbler_system(host) else "OFF"
            if data["action"] == "deploy":
                result = self.bm_status.update_deploy_status(host, status)
                if result:
                    progress = self.bm_status.get_deploy_progress(host)
            elif data["action"] == "power":
                result = self.bm_status.update_power_status(
                    host, status, data["flag_on"])
                if result:
                    progress = self.bm_status.get_power_progress(
                        host, data["flag_on"])
            if progress >= 100:
                break
            if progress < 0:
                # error
                log.error("Error when getting the progress of host {0} on {1}.".format(
                    host, data["action"]))
                break
            sleep(data["time"])

    def get_server_url(self,):
        """
        get the BASE URL of the cobbler service
        """
        server_config = cm_config_server()
        cobbler_config = server_config.get("cloudmesh.server.cobbler")
        return "{0}://{1}:{2}".format(cobbler_config["prot"], cobbler_config["host"], cobbler_config["port"])

    def request_rest_api(self, method, url, data=None):
        """
        Request a REST service through requests library.
        :param string method: the operation in REST service, valid value in [get, post, put, delete]
        :return: a dict with the formation {"result":True|False, "data": data}
        """
        method = method.lower()
        headers = {"content-type": "application/json",
                   "accept": "application/json", }
        req_api = getattr(requests, method)
        req_url = self.server_url + url
        if method == "get":
            r = req_api(req_url)
        else:
            if data:
                data["user_token"] = ""
            else:
                data = {"user_token": ""}
            r = req_api(req_url, data=json.dumps(data), headers=headers)
        return r.json()["cmrest"]["data"] if r.status_code == 200 else {"result": False}

if __name__ == "__main__":
    bmc = CobblerRestAPI()
    #"""
    # get distros list
    result = bmc.get_cobbler_iso_list()
    #"""
    """
    # get cobbler report
    result = bmc.get_cobbler_object_report("kickstart", "*")
    """
    """
    # add a distro, CentOS-6.5-x86_64-bin-DVD1.iso
    data = {"name": "test_centos_1405023", "url": "http://mirrors.usc.edu/pub/linux/distributions/centos/6.5/isos/x86_64/CentOS-6.5-x86_64-bin-DVD1.iso"}
    result = bmc.add_cobbler_distro(data)
    """
    """
    # add a profile, 
    data = {"name": "test_profile_1405023", "distro": "test_centos_1405023-x86_64", "kickstart":"sample.ks",}
    result = bmc.add_cobbler_profile(data)
    """
    """
    # add a system
    data = {"name": "test_system_1405023", "profile": "test_profile_1405023", 
            "power": {"power-address": "1.2.3.4",
                      "power-user": "onlytest",
                      "power-pass": "onlytest",
                      "power-type": "ipmilan",
                      "power-id": 1,
                      },
            "interfaces": [
                 {
                   "name": "ee1",
                   "ip-address": "192.168.11.23",
                   "mac-address": "aa:11:cc:dd:ee:ff",
                   "static": True,
                   "netmask": "255.255.255.0"
                 },
                {
                   "name": "ee2",
                   "ip-address": "192.168.11.123",
                   "mac-address": "aa:11:cc:dd:ff:ff",
                   "static": True,
                   "netmask": "255.255.255.0"
                 },
                ]
            }
    result = bmc.add_cobbler_system(data)
    """
    """
    # update a profile
    data = {"name": "test_profile_1405023", "kickstart": "default.ks",}
    result = bmc.update_cobbler_profile(data)
    """
    """
    # update a system
    data = {"name": "test_system_1405023", "power": {"power-user": "hellouser"}}
    result = bmc.update_cobbler_system(data)
    """
    """
    # remove a interface of system
    system_name="test_system_1405023"
    if_name = "ee2"
    result = bmc.remove_cobbler_system_interface(system_name, if_name)
    """
    """
    # remove system
    system_name="test_system_1405023"
    result = bmc.remove_cobbler_system(system_name)
    """
    """
    # remove a profile
    profile_name="test_profile_1405023"
    result = bmc.remove_cobbler_profile(profile_name)
    """
    """
    # remove a distro
    distro_name="test_centos_1405023-x86_64"
    # MUST delete the default profile firstly
    result = bmc.remove_cobbler_profile(distro_name)
    result = bmc.remove_cobbler_distro(distro_name)
    """
    result = bmc.get_cobbler_profile_based_kickstart("a.seed")
    print "result is: ", result

from dbhelper import DBHelper
from cloudmesh.util.config import read_yaml_config
from cloudmesh.config.cm_config import cm_config_server
from baremetal_status import BaremetalStatus
from hostlist import expand_hostlist
import requests
import json
from time import sleep
import threading
from copy import deepcopy
from cloudmesh.util.logger import LOGGER
#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)

class BaremetalComputer:
    """Baremetal computer class.
    First, this class provide the access to cobbler provision API via REST service. 
    Second, this class also provide a easy API to initialize the cobbler baremetal computers in mongodb, e.g., mac and power info,
    Third, this class have an API through which user can get the detail information to provision a cobbler baremetal computer 
    """
    def __init__(self):
        coll_name = "inventory"
        self.yaml_file = "~/.futuregrid/cloudmesh_mac.yaml"
        self.db_client = DBHelper(coll_name)
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
    
    def get_cobbler_object_list(self, cobbler_object):
        """list the cobbler objects.
        :param string cobbler_object: one of the cobbler objects, currently support four objects, 'distro', 'profile', 'system', 'kickstart'
        :return: a list with the formation ['name1', 'name2', ] of corresponding objects if cobbler_object is a valid object, otherwise None
        :rtype: list 
        """
        url = "/cm/v1/cobbler/{0}s".format(cobbler_object)
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
        :return: True means add distro operation success, otherwise Failed
        """
        return self.add_cobbler_object("distro", data)
    
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
        
    def add_cobbler_object(self, cobbler_object, data):
        """add a specific object to cobbler.
        :param string cobbler_object: one of the cobbler objects, currently support four objects, 'distro', 'profile', 'system', 'kickstart'
        :param dict data: a json data structure. The formation is {"name": "your object name", ...}
        :return: True means add an object operation success, otherwise Failed
        """
        url = "/cm/v1/cobbler/{0}s/{1}".format(cobbler_object, data["name"])
        rest_data = self.request_rest_api("post", url, data)
        return rest_data["result"]
    
    def update_cobbler_distro(self, data):
        """update a distro to cobbler. 
        :param dict data: a json data structure. The formation is {"name": "your distro name", "comment": "your comment", "owners": "specified owners",}
        :return: True means update distro operation success, otherwise Failed
        """
        return self.update_cobbler_object("profile", data)
    
    def update_cobbler_profile(self, data):
        """update a profile to cobbler. 
        :param dict data: a json data structure. The formation is {"name": "your profile name", "distro": "distro", "kickstart": "kickstart.file", }
        :return: True means update profile operation success, otherwise Failed
        """
        return self.update_cobbler_object("profile", data)
    
    def update_cobbler_system(self, data):
        """update a system to cobbler.
        :param dict data: a json data structure. The formation is {"name": "your system name", "profile": "profile", "power": {}, "interfaces": [{}, {},]}
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
        url = "/cm/v1/cobbler/baremetal/{0}".format(name)
        rest_data = self.request_rest_api("post", url)
        # init deploy status
        self.bm_status.init_deploy_status(name)
        # monitor status
        monitor_deploy_power_status(name, "deploy")
        return rest_data["result"]
    
    def power_cobbler_system(self, name, flag_on=True):
        """power ON/OFF baremetal system *name*. 
        The system is ON/OFF must be call **monitor_cobbler_system** and its result is True(ON)/False(OFF)
        :param string name: the name of a cobbler system or host
        :param boolean flag_on: a boolean value. True means to power on the system, False means power off.
        :return: Always return True, which ONLY means has sent deploy command through IPMI. You MUST call `monitor_cobbler_system` to get the status of the system `name`.
        """
        url = "/cm/v1/cobbler/baremetal/{0}".format(name)
        data = {"power_on": flag_on, }
        rest_data = self.request_rest_api("put", url, data)
        # init power status
        self.bm_status.init_power_status(name, flag_on)
        # monitor status
        monitor_deploy_power_status(name, "power", flag_on)
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
                result = self.bm_status.update_power_status(host, status, data["flag_on"])
                if result:
                    progress = self.bm_status.get_power_progress(host, data["flag_on"])
            if progress >= 100:
                break
            if progress < 0:
                # error
                log.error("Error when getting the progress of host {0} on {1}.".format(host, data["action"]))
                break
            sleep(data["time"])
    
    
    def get_default_query(self):
        """
        query helper function.
        :return: the default query field.
        """
        return { "cm_type": "inventory",
                 "cm_kind": "server",
                 "cm_attribute": "network",
                 "cm_key": "server",
                }
    
    def get_full_query(self, query_elem=None):
        """
        merge the default query and user defined query.
        :return: the full query dict
        """
        result = self.get_default_query()
        if query_elem:
            result.update(query_elem)
        return result
    
    def read_data_from_yaml(self):
        """
        read mac address and bmc configuration information from **mac.yaml** file.
        """
        data = read_yaml_config(self.yaml_file)
        result = None
        if data:
            result = {}
            data = data["inventory"]
            for cluster in data:
                cluster_data = data[cluster]
                if "bmc" in cluster_data and "common" in cluster_data["bmc"]:
                    # process the common bmc data in cluster
                    common_bmc_data = cluster_data["bmc"]["common"]
                    host_range = common_bmc_data.pop("range", None)
                    hosts = expand_hostlist(host_range)
                mac_data = cluster_data["macaddr"]
                for host in mac_data:
                    if host in hosts:
                        temp_common_bmc_data = deepcopy(common_bmc_data)
                        if "bmc" in mac_data[host]:
                            # bmc config in individual host have a high priority than common config
                            temp_common_bmc_data.update(mac_data[host]["bmc"])
                        mac_data[host]["bmc"] = temp_common_bmc_data
                result[cluster] = mac_data
        return result
    
    def insert_mac_data_to_inventory(self):
        """
        Insert the mac address information including power config into inventory. 
        This API should be called **BEFORE** baremetal provision.
        Currently, this API is called by **fab mongo.inventory**
        """
        data = self.read_data_from_yaml()
        result = False
        if data and len(data) > 0:
            result = self.update_mac_address(data)
        return result
    
    def update_mac_address(self, mac_dict):
        """
        update *inventory* db with mac address information.
        :param dict mac_dict: a dict with the following formation. *label_name* is the *cm_id* defined in inventory.
        *internal* or *public* is the type defined in inventory. 
        {"cluster_name":{
          "label_name": {"internal": {"name":"eth0", "macaddr": "aa:aa:aa:aa:aa:aa"}, 
                         "public": {"name":"eth1", "macaddr": "aa:aa:aa:aa:aa:ab"},
                         "bmc": {"user": "user_name", "pass": "password", "type": "type",},}
        }
        :return: True means all the mac address in mac_dict updated successfully; False means failed.
        """
        result = True
        if mac_dict:
            for cluster in mac_dict:  # cluster
                cluster_data = mac_dict[cluster]
                for host_id in cluster_data:  # host
                    host_data = cluster_data[host_id]
                    for network_type in host_data: # network
                        network_data = host_data[network_type]
                        query_elem = {"cm_id": host_id, "type": network_type, "cm_cluster": cluster,}
                        if network_type in ["bmc"]: # power config information
                            update_elem = network_data
                        else:
                            update_elem = {"ifname": network_data["name"],
                                           "macaddr":network_data["macaddr"],
                                           }
                        update_result = self.db_client.atom_update(self.get_full_query(query_elem), 
                                                                   {"$set": update_elem}, False)
                        if not update_result["result"]:
                            result = False
                            break
                    if not result:
                        break
                if not result:
                    break
        return result
    
    def get_host_info(self, host_id, info_format="cobbler"):
        """
        get the required host info for baremetal computer.
        :param string host_id: the unique name/id of a node in cloudmesh
        :param string info_format: the dest info format of general host info. To support a new formation, such as *xtest*, the API get_host_info_xtest MUST be provided. 
        :return: a dict with the following formation if info_format is None, otherwise return the use specified formation conerted from the default one.
        {
          "id": "unique ID",
          "power": {"ipaddr": ipaddr, "power_user": user, "power_pass": pass, "power_type": type,},
          "interfaces": [{"name": "eth0", "ipaddr": ipaddr, "macaddr": macaddr,}],
        }
        """
        query_elem = {"cm_id": host_id}
        full_query_elem = self.get_full_query(query_elem)
        find_result = self.db_client.find(full_query_elem)
        result = None
        if find_result["result"]:
            result = {"id": host_id, "power":{}}
            data = find_result["data"]
            interface_list = []
            cluster_id = None
            for record in data:
                if "macaddr" in record:  # general network interface
                    interface_list.append({"name": record["ifname"], 
                                           "ipaddr": record["ipaddr"],
                                           "macaddr": record["macaddr"],
                                           })
                    if record["type"] == "public":
                        result["hostname"] = record["label"]
                        cluster_id = record["cm_cluster"]
                elif "power_user" in record:  # ipmi network interface
                    power_key_list = ["ipaddr", "power_user", "power_pass", "power_type",]
                    for key in power_key_list:
                        result["power"][key] = record[key]
            # sort the inteface with ascending order
            result["interfaces"] = sorted(interface_list, key=lambda k: k["name"])
            if cluster_id:
                # try to find name server for the servers in this cluster
                name_servers = self.get_cluster_name_server(cluster_id)
                if name_servers:
                    result["name_servers"] = name_servers
            if info_format:
                getattr(self, "get_host_info_{0}".format(info_format))(result)
        return result
    
    def get_cluster_name_server(self, cluster_id):
        """find the name servers for a cluster
        :param string cluster_id: the unique ID of a cluster
        :return: None if not exist a name server for the cluster, otherwise a string represents the one or more name servers
        """
        query_elem = {"cm_id": cluster_id, "cm_key": "nameserver", "cm_attribute": "variable"}
        full_query_elem = self.get_full_query(query_elem)
        find_result = self.db_client.find(full_query_elem)
        result = []
        if find_result["result"]:
            data = find_result["data"]
            for record in data:
                result.append(record["cm_value"])
        return None if len(result) < 1 else " ".join(result)
    
    def change_dict_key(self, data_dict, fields):
        """
        change the key in dict from old_key to new_key.
        :param dict fields: the projection from old_key to new_key. {"old_key": "new_key"}
        """
        for key in fields:
            if key in data_dict:
                data_dict[fields[key]] = data_dict.pop(key)
    
    def fill_dict_default_key(self, data_dict, fields):
        """
        fill the dict with default key-value pair.
        :param dict fields: the default key-value pair. {"key": "default"}
        """
        for key in fields:
            if key not in data_dict:
                data_dict[key] = fields[key]
    
    
    def get_host_info_cobbler(self, host_dict):
        """
        convert general host info dict to the formation of cobbler host formation
        """
        # section 1, general fields
        general_fields = {"id": "name", "name_servers": "name-servers",}
        self.change_dict_key(host_dict, general_fields)
        # section 2, power fields
        power_fields = {"ipaddr": "power-address", 
                        "power_user": "power-user",
                        "power_pass": "power-pass",
                        "power_type": "power-type",
                        }
        power_default = {"power-id": 1,
                         }
        self.change_dict_key(host_dict["power"], power_fields)
        self.fill_dict_default_key(host_dict["power"], power_default)
        # section 3, interface fields
        interface_fields = {"ipaddr": "ip-address",
                            "macaddr": "mac-address",
                            }
        interface_default = {"netmask": "255.255.255.0",
                             "static": True,
                             }
        for one_interface in host_dict["interfaces"]:
            self.change_dict_key(one_interface, interface_fields)
            self.fill_dict_default_key(one_interface, interface_default)
    
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
        headers = {"content-type": "application/json", "accept": "application/json", }
        req_api = getattr(requests, method)
        req_url = self.get_server_url() + url
        if method == "get":
            r = req_api(req_url)
        else:
            if data:
                data["user_token"] = ""
            else:
                data = {"user_token": ""}
            r = req_api(req_url, data=json.dumps(data), headers=headers)
        return r.json()["cmrest"]["data"] if r.status_code == 200 else {"result": False}

    
# test
if __name__ == "__main__":
    from pprint import pprint
    bmc = BaremetalComputer()
    """
    data = bmc.insert_mac_data_to_inventory()
    print data
    for host in ["???", "???", "???"]:
        data = bmc.get_host_info(host)
        pprint(data)
    """
    """
    # get distros list
    result = bmc.get_cobbler_distro_list()
    """
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
    result = bmc.get_host_info("i080")
    pprint(result)
    
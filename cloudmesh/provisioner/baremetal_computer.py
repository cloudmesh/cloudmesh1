from dbhelper import DBHelper
from baremetal_status import BaremetalStatus
from cloudmesh_base.hostlist import Parameter
from copy import deepcopy
from cloudmesh.util.config import read_yaml_config
from cloudmesh_base.logger import LOGGER
from cloudmesh_base.locations import config_file
#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)


class BaremetalComputer:
    """Baremetal computer class.
    First, this class also provide a easy API to initialize the cobbler baremetal computers in mongodb, e.g., mac and power info,
    Second, this class have an API through which user can get the detail information to provision a cobbler baremetal computer
    """

    def __init__(self):
        coll_name = "inventory"
        self.yaml_file = config_file("/cloudmesh_mac.yaml")
        self.db_client = DBHelper(coll_name)
        self.bm_status = BaremetalStatus()

    def get_default_query(self):
        """
        query helper function.
        :return: the default query field.
        """
        return {"cm_type": "inventory",
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
                    hosts = Parameter.expand(host_range)
                mac_data = cluster_data["macaddr"]
                for host in mac_data:
                    if host in hosts:
                        temp_common_bmc_data = deepcopy(common_bmc_data)
                        if "bmc" in mac_data[host]:
                            # bmc config in individual host have a high
                            # priority than common config
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
        # insert a document of baremetal computers list
        self.insert_blank_baremetal_list()
        # insert mac data
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
                    for network_type in host_data:  # network
                        network_data = host_data[network_type]
                        query_elem = {
                            "cm_id": host_id, "type": network_type, "cm_cluster": cluster, }
                        if network_type in ["bmc"]:  # power config information
                            update_elem = network_data
                        else:
                            update_elem = {"ifname": network_data["name"],
                                           "macaddr": network_data["macaddr"],
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
            result = {"id": host_id, "power": {}}
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
                    power_key_list = [
                        "ipaddr", "power_user", "power_pass", "power_type", ]
                    for key in power_key_list:
                        result["power"][key] = record[key]
            # sort the inteface with ascending order
            result["interfaces"] = sorted(
                interface_list, key=lambda k: k["name"])
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
        query_elem = {
            "cm_id": cluster_id, "cm_key": "nameserver", "cm_attribute": "variable"}
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
        general_fields = {"id": "name", "name_servers": "name-servers", }
        self.change_dict_key(host_dict, general_fields)
        # section 2, power fields
        power_fields = {"ipaddr": "power-address",
                        "power_user": "power-user",
                        "power_pass": "power-pass",
                        "power_type": "power-type",
                        }
        power_default = {"power-id": 2,
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

    def insert_blank_baremetal_list(self):
        """insert a blank document of baremetal computers list into mongodb
        ONLY called ONCE by **fab mongo.inventory**
        """
        elem = {"cm_kind": "baremetal", "cm_type": "bm_list_inventory", }
        result = self.db_client.find_one(elem)
        flag_insert = True
        if result["result"] and result["data"]:
            flag_insert = False
        if not flag_insert:
            return True
        result = self.db_client.insert(elem)
        return result["result"]

    def enable_baremetal_computers(self, hosts):
        """add the list of *hosts* to be baremetal computers
        :param list hosts: the list of hosts with the formation ["host1", "host2",]
        :return: True means enabled successfully, otherwise False
        """
        if hosts:
            query_elem = {
                "cm_kind": "baremetal", "cm_type": "bm_list_inventory", }
            update_elem = {"$addToSet": {"data": {"$each": hosts}}}
            result = self.db_client.atom_update(query_elem, update_elem)
            return result["result"]
        return True

    def disable_baremetal_computers(self, hosts):
        """remove the list of *hosts* from baremetal computers
        :param list hosts: the list of hosts with the formation ["host1", "host2",]
        :return: True means disabled successfully, otherwise False
        """
        if hosts:
            query_elem = {
                "cm_kind": "baremetal", "cm_type": "bm_list_inventory", }
            update_elem = {"$pull": {"data": {"$in": hosts}}}
            result = self.db_client.atom_update(query_elem, update_elem)
            return result["result"]
        return True

    def get_baremetal_computers(self):
        """get the list of baremetal computers
        :return: the list of hosts with the formation ["host1", "host2",] or None if failed
        """
        query_elem = {"cm_kind": "baremetal", "cm_type": "bm_list_inventory", }
        result = self.db_client.find_one(query_elem)
        if result["result"]:
            return result["data"]["data"] if "data" in result["data"] else []
        return None


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
    # result = bmc.get_host_info("i080")
    # result = bmc.insert_blank_baremetal_list()
    # result = bmc.enable_baremetal_computers(["i001", "i003", "i007", "i189"])
    # result = bmc.disable_baremetal_computers(["i001", "i007",])
    result = bmc.get_baremetal_computers()
    pprint(result)

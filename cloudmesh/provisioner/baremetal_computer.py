from dbhelper import DBHelper
from cloudmesh.util.config import read_yaml_config
from cloudmesh.util.logger import LOGGER
#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)

class BaremetalComputer:
    def __init__(self):
        coll_name = "inventory"
        self.yaml_file = "~/.futuregrid/mac.yaml"
        self.db_client = DBHelper(coll_name)
    
    def get_default_query(self):
        """
        query helper function.
        return the default query field.
        """
        return { "cm_type": "inventory",
                 "cm_kind": "server",
                 "cm_attribute": "network",
                 "cm_key": "server",
                }
    
    def get_full_query(self, query_elem=None):
        """
        merge the default query and user defined query.
        return the full query dict
        """
        result = self.get_default_query()
        if query_elem:
            result.update(query_elem)
        return result
    
    def read_data_from_yaml(self):
        """
        read mac address information from yaml file.
        """
        data = read_yaml_config(self.yaml_file)
        result = None
        if data:
            result = data["inventory"]["macaddr"]
        return result
    
    def insert_mac_data_to_inventory(self):
        """
        Insert the mac address information into inventory. 
        This API should be called **BEFORE** baremetal provision.
        """
        data = self.read_data_from_yaml()
        result = False
        if data and len(data) > 0:
            result = self.update_mac_address(data)
        return result
    
    def update_mac_address(self, mac_dict):
        """
        update `inventory` db with mac address information.
        param mac_dict a dict with the following formation. `label_name` is the `cm_id` defined in inventory.
        `internal` or `public` is the type defined in inventory. 
        {
          "label_name": {"internal": {"name":"eth0", "macaddr": "aa:aa:aa:aa:aa:aa"}, 
                         "public": {"name":"eth1", "macaddr": "aa:aa:aa:aa:aa:ab"}
        }
        return True means all the mac address in mac_dict updated successfully; False means failed.
        """
        result = True
        if mac_dict:
            for label_name in mac_dict:
                for network_type in mac_dict[label_name]:
                    query_elem = {"cm_id": label_name, "type": network_type,}
                    update_elem = {"ifname": mac_dict[label_name][network_type]["name"],
                                   "macaddr":mac_dict[label_name][network_type]["macaddr"],
                                   }
                    update_result = self.db_client.atom_update(self.get_full_query(query_elem), 
                                                               {"$set": update_elem}, False)
                    if not update_result["result"]:
                        result = False
                        break
                if not result:
                    break
        return result
    
    def get_host_info(self, host_id):
        """
        get the required host info for baremetal computer.
        return a dict with the following formation.
        {
          "id": "unique ID",
          "interfaces": {"eth0": {"ipaddr": ipaddr, "macaddr": macaddr, "type": type,}}
        }
        """
        query_elem = {"cm_id": host_id}
        full_query_elem = self.get_full_query(query_elem)
        find_result = self.db_client.find(full_query_elem)
        result = None
        if find_result["result"]:
            result = {"id": host_id, "interfaces": {}}
            data = find_result["data"]
            for record in data:
                if "macaddr" in record:
                    result["interfaces"][record["ifname"]] = {"ipaddr": record["ipaddr"],
                                                              "macaddr": record["macaddr"],
                                                              "type": record["type"],
                                                              }
        return result
    
# test
if __name__ == "__main__":
    bmc = BaremetalComputer()
    data = bmc.insert_mac_data_to_inventory()
    print data
    for host in ["???", "???", "???"]:
        data = bmc.get_host_info(host)
        print data
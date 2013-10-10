from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.inventory import Inventory
from pprint import pprint
from sh import ssh 

# class cm_temperature:

hostname = "i066"

config_server = cm_config_server().get("cloudmesh.server.clusters")

inventory = Inventory()

def get_ipmi_temperature(host):

    (hostaddr, data) =  inventory.ipadr_cluster (hostname, "bmc")
    clustername = data["cm_cluster"]
    config = config_server[clustername]['bmc']
    password = config['password']
    username = config['user']

    command = "ipmitool -I lanplus -U {0} -P {1} -E -H {2} sdr type temperature".format(username,password,hostaddr)
    
    proxyaddr = config['proxy']['ip']
    proxyusername = config['proxy']['user']

    result = ssh("{0}@{1}".format(proxyusername, proxyaddr), command)

    return result

print get_ipmi_temperature(hostname)

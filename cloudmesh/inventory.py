from cloudmesh.config.cm_config import cm_config_server
from cloudmesh_install import config_file
from cloudmesh_common.logger import LOGGER
from hostlist import expand_hostlist
from pprint import pprint
import sys
from cloudmesh_install.util import path_expand as cm_path_expand
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.config.cm_config import get_mongo_db
from cloudmesh.config.ConfigDict import ConfigDict
from datetime import datetime, timedelta
from cloudmesh.provisioner.baremetal_db import BaremetalDB
from cloudmesh.provisioner.baremetal_computer import BaremetalComputer
from copy import deepcopy

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)


class Inventory:

    server_config = None

    CONFIG_FILE = config_file("/cloudmesh_cluster.yaml")

    def __init__(self):
        # read the host file definition from cloudmesh_cluster.yaml
        self.server_config = cm_config_server()

        self.config = ConfigDict(filename=self.CONFIG_FILE)

        collection = "inventory"
        self.db_inventory = get_mongo_db(collection)

    def get_attribute(self, host_label, attribute):

        try:
            value = self.find({"cm_id": host_label,
                               'cm_attribute': 'variable',
                               'cm_key': attribute})[0]
        except:
            value = None
        return value

    def get(self, cm_kind, id_kind, name):
        host = None
        if id_kind == 'cm_id':
            host = self.find_one({'cm_type': "inventory",
                                  'cm_key': 'server',
                                  'cm_kind': cm_kind,
                                  'cm_id': name})
        elif id_kind == "label":
            host = self.find_one({'cm_type': "inventory",
                                  'cm_key': 'server',
                                  'cm_kind': cm_kind,
                                  'label': name})

        else:
            log.error("Wrong type {0} {1} {2}".format(cm_kind, id_kind, name))
            sys.exit()
        return host

    # added by HC on Nov. 15, 2013
    # to simplify the procedure of finding host information from Inventory
    # the param 'id_label' can be a valid cm_id or a valid real label
    # network_type can be a valid 'public', 'internal', 'bmc'

    # find one host record information
    # cm_id: i001; real label: i1
    # BEGIN host info
    def get_host_info(self, id_label, network_type=None):
        query = {
            '$or': [
                {'cm_id': id_label},
                {'label': id_label},
            ],
            'cm_type': 'inventory',
            'cm_key': 'server',
            'cm_kind': 'server',
        }
        if network_type:
            query["type"] = network_type
        host = self.find_one(query)
        if host is None:
            if network_type:
                raise NameError("Wrong cm_id or label '{0}' of network '{1}', Cannot find host info from Inventory.".format(
                    id_label, network_type))
            else:
                raise NameError(
                    "Wrong cm_id or label '{0}', Cannot find host info from Inventory.".format(id_label))

        return host

    # get cm_id and real lable of host
    # cm_id is an unique label of clusters
    # label is the real name of host in the configuration, /etc/hosts
    # for example, valid cm_id: i100, b010, d001
    #              valid label: i100, b10,  d1
    def get_host_id_label(self, id_label, network_type=None):
        sresult = None
        try:
            host = self.get_host_info(id_label, network_type)
            sresult = (host["cm_id"], host["label"])
        except NameError, ne:
            log.error(str(ne))

        return sresult

    # END host info

    def set_attribute(self, host_label, attribute, value, time=None):
        print "SETTING", host_label, attribute, value

        if time is None:
            time = datetime.now()

        # get the cluster from the host_label
        try:
            host = self.find_one({"cm_id": host_label,
                                  "cm_attribute": "network"})["cm_cluster"]
        except:
            log.error("could not find host with the label:{0}".format(host_label))
            sys.exit()

        cursor = self.update({"cm_id": host_label,
                              'cm_attribute': 'variable',
                              'cm_key': attribute},
                             {"$set": {attribute: value,
                                       'cm_cluster': host,
                                       'cm_type': "inventory",
                                       'cm_kind': 'server',
                                       'cm_key': attribute,
                                       'cm_value': value,
                                       'cm_attribute': 'variable',
                                       'cm_refresh': time,
                                       }
                              })

    def update(self, query, values=None):
        '''
        executes a query and updates the results from mongo db.
        :param query:
        '''
        if values is None:
            return self.db_inventory.update(query, upsert=True)
        else:
            # log.info("Query {0} {1}".format(query, values))
            return self.db_inventory.update(query, values, upsert=True)

    def insert(self, element):
        self.db_inventory.insert(element)

    def clear(self):
        self.db_inventory.remove({"cm_type": "inventory"})

    def find(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_inventory.find(query)

    def find_one(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_inventory.find_one(query)

    def _generate_globals(self):

        for name in self.config.get("cloudmesh.inventory"):

            cluster = self.config.get("cloudmesh.inventory")[name]
            keys = cluster.keys()

            element = dict({'cm_cluster': name,
                            'cm_id': name,
                            'cm_type': "inventory",
                            'cm_kind': 'server',
                            'cm_key': 'range',
                            'cm_value': expand_hostlist(cluster["id"]),
                            'cm_hostlist': cluster["id"],
                            'cm_attribute': 'variable'
                            })
            self.insert(element)

            for key in keys:
                if (type(cluster[key]) is str) and \
                        (not key in ["id", "network"]):
                    element = dict({'cm_cluster': name,
                                    'cm_id': name,
                                    'cm_type': "inventory",
                                    'cm_kind': 'server',
                                    'cm_key': key,
                                    'cm_value': cluster[key],
                                    'cm_attribute': 'variable'
                                    })
                    self.insert(element)
                elif key == "publickeys":
                    publickeys = cluster[key]
                    for k in publickeys:
                        element = dict({'cm_cluster': name,
                                        'cm_id': name,
                                        'cm_type': "inventory",
                                        'cm_kind': 'publickey',
                                        'cm_key': k['name'],
                                        'cm_name': cm_path_expand(k['path']),
                                        'cm_value': cluster[key],
                                        'cm_attribute': 'variable'
                                        })
                        self.insert(element)

    def generate(self):
        self._generate_globals()

        clusters = self.config.get("cloudmesh.inventory")

        for cluster_name in clusters:
            cluster = clusters[cluster_name]
            names = expand_hostlist(cluster["id"])
            net_id = 0
            for network in cluster["network"]:

                n_index = expand_hostlist(network["id"])
                n_label = expand_hostlist(network["label"])
                n_range = expand_hostlist(network["range"])
                n_name = network["name"]

                for i in range(0, len(names)):
                    name = n_index[i]
                    element = dict(network)
                    del element['range']
                    element.update({'cm_type': "inventory",
                                    'cm_key': 'server',
                                    'cm_kind': 'server',
                                    'cm_id': name,
                                    'cm_cluster': cluster_name,
                                    'id': name,
                                    'label': n_label[i],
                                    'network_name': n_name,
                                    'cm_network_id': net_id,
                                    'ipaddr': n_range[i],
                                    'cm_attribute': 'network'}
                                   )
                    self.insert(element)
                net_id += 1

        # added by HC
        # init rack status
        self.generate_rack_status()
        # init baremetal computer managemnt, maybe will be deprecated later
        bdb = BaremetalDB()
        bdb.init_base_document_structure()
        # insert necessary mac info of baremetal computers to inventory
        bmc = BaremetalComputer()
        bmc.insert_mac_data_to_inventory()

    def cluster(self, name):
        """returns cluster data in dict"""
        name = "NOT IMPLEMENTED"
        raise RuntimeError("Not Implemented")

    def info(self):
        '''
        print some elementary overview information
        '''
        clusters = self.find({'cm_type': 'inventory',
                              'cm_key': 'range',
                              'cm_kind': 'server'})
        servers = self.find({'cm_type': 'inventory',
                             'cm_key': 'server',
                             'cm_kind': 'server'})
        services = self.find({'cm_type': 'inventory',
                              'cm_key': 'image',
                              'cm_kind': 'image'})

        # print "%15s:" % "dbname", self.inventory_name
        print "%15s:" % "clusters", clusters.count(), "->", ', '.join([c['cm_cluster'] for c in clusters])
        print "%15s:" % "services", services.count()
        print "%15s:" % "servers", servers.count()
        print

        print "Clusters"
        print 30 * "="
        for host in clusters:
            print "    ", host['cm_cluster'], "->", host['cm_hostlist']

        print

    def hostlist(self, name):
        # print "NAME", name
        hosts = self.find({"cm_cluster": name, 'cm_key': 'range'})[
            0]['cm_value']
        # print "===================", self.find_one({"cm_cluster": name,
        # 'cm_key': 'range' })
        return hosts

    def host(self, index, auth=True):
        cursor = self.find({"cm_id": index,
                            'cm_attribute': 'network'})

        # print "CCCC", cursor[0]

        data = {}

        data['cm_cluster'] = cursor[0]['cm_cluster']
        data['cm_type'] = cursor[0]['cm_type']
        data['cm_id'] = cursor[0]['cm_id']

        # pprint (cursor[0]['cm_cluster'])

        c2 = self.find({"cm_attribute": 'variable'})

        # DEBUG
        # for e in c2:
        #    print "EEE", e
        #    print

        cursor_attributes = self.find(
            {"cm_id": index, 'cm_attribute': 'variable'})
        for element in cursor_attributes:
            data[element['cm_key']] = element['cm_value']

        data['network'] = {}
        for result in cursor:

            # DEBUG
            # print 70 * "R"
            # pprint(result)
            # print 70 * "S"

            n_id = result["cm_network_id"]
            n_name = result["network_name"]
            n_ipaddr = result["ipaddr"]
            data['network'][n_name] = dict(result)
            # del data["network"][name]["_id"]

        cluster_name = data['cm_cluster']
        cluster_auth = self.server_config.get(
            "cloudmesh.server.clusters")[cluster_name]

        for name in cluster_auth:
            network = data["network"][name]
            d = dict(cluster_auth[name])
            network.update(d)

        excludes = ['user', 'password']

        for name in data["network"]:
            del data["network"][name]["_id"]
            if not auth:
                for exclude in excludes:
                    if exclude in data["network"][name]:
                        del data["network"][name][exclude]

        return data

    def ipadr(self, index, iptype):
        return self.find({"cm_id": index,
                          "type": iptype})[0]['ipaddr']

    def ipadr_cluster(self, index, iptype):
        data = self.find({"cm_id": index,
                          "type": iptype})[0]
        return (data['ipaddr'], data)

    # added by HC on Nov. 18
    # Append the service type and temperature of racks into Inventory
    # BEGIN rack inventory
    def get_clusters(self, rack_name=None):
        query = {
            'cm_key': 'range',
            'cm_type': 'inventory',
            'cm_kind': 'server',
        }
        if rack_name:
            query['cm_id'] = rack_name

        return self.find(query)

    def generate_rack_status(self):
        service_list = [
            'temperature',
            'service',
        ]

        racks = self.get_clusters()
        for rack in racks:
            log.info(
                "Adding the initial status of rack {0}".format(rack["cm_cluster"]))
            for service_type in service_list:
                self.init_rack_status(service_type, rack)
                self.init_rack_temp_status(service_type, rack)

    # init a type of status of a rack
    # two status: 'not_ready' means the init of the record
    #             'ready' means the record contains useful data
    def init_rack_status(self, service_type, rack):
        query = {
            "cm_key": "rack_{0}".format(service_type),
            "cm_type": "inventory",
            "cm_kind": "rack",
            "cm_label": rack["cm_cluster"],
            "cm_id": rack["cm_cluster"],
            "id": rack["cm_cluster"],
            "label": rack["cm_cluster"],
        }

        element = deepcopy(query)
        element['rack_status'] = 'not_ready'
        element['cm_refresh'] = None
        element['data'] = dict((h, None) for h in rack['cm_value'])

        self.update(query, element)

    # init a type of temporary refreshing status of a rack
    # three status: 'not_ready' means the init of the record
    #               'refresh' mean the status data is updating
    #               'ready' means the record contains useful data
    def init_rack_temp_status(self, service_type, rack, status='not_ready'):
        query = {
            "cm_key": "rack_temp_{0}".format(service_type),
            "cm_type": "inventory",
            "cm_kind": "rack",
            "cm_label": rack["cm_cluster"],
            "cm_id": rack["cm_cluster"],
            "id": rack["cm_cluster"],
            "label": rack["cm_cluster"],
        }

        element = deepcopy(query)
        element['rack_status'] = status
        # the start time of refresh
        element[
            'cm_refresh'] = None if status == 'not_ready' else datetime.now()
        element['updated_node'] = 0
        element['max_node'] = len(rack['cm_value'])
        element['data'] = dict((h, None) for h in rack['cm_value'])

        self.update(query, element)

    # END rack inventory


def main():
    inventory = Inventory()

    r = inventory.find({})
    for e in r:
        print e

    print r.count()

    name = "b010"
    data = inventory.host(name)
    pprint(data)

    print inventory.ipadr(name, "public")
    print inventory.ipadr(name, "internal")

    inventory.info()

if __name__ == '__main__':
    main()

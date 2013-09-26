from cloudmesh.config.cm_config import cm_config_server

from cloudmesh.util.logger import LOGGER
from hostlist import expand_hostlist
from pprint import pprint
import sys
from cloudmesh.util.util import path_expand as cm_path_expand
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.config.cm_config import get_mongo_db
from cloudmesh.config.ConfigDict import ConfigDict
from datetime import datetime

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)


class Inventory:

    server_config = None

    CONFIG_FILE = "~/.futuregrid/cloudmesh_cluster.yaml"
    BOOTSPEC_FILE = "~/.futuregrid/cloudmesh_bootspec.yaml"

    def __init__(self):
		# read the host file definition from cloudmesh_cludter.yaml
		self.server_config = cm_config_server()

		self.config = ConfigDict(filename=self.CONFIG_FILE)

		self.bootspec_config = ConfigDict(filename=self.BOOTSPEC_FILE)
		
		collection = "inventory"
		self.db_inventory = get_mongo_db(collection)

    def get_attribute(self, host_label, attribute):

        try:
            value = self.find ({"cm_id" : host_label,
                                'cm_attribute' : 'variable',
                                'cm_key' : attribute})[0]
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
            print "ERROR Wrong type"
            print cm_kind, id_kind, name
            sys.exit()
        return host

    def set_attribute(self, host_label, attribute, value, time=None):
        print "SETTING", host_label, attribute, value

        if time is None:
            time = datetime.now()

        # get the cluster from the host_label
        try:
            host = self.find_one({"cm_id": host_label,
                                  "cm_attribute": "network"})["cm_cluster"]
        except:
            print "could not find host with the label", host_label
            sys.exit()


        cursor = self.update ({"cm_id" : host_label,
                               'cm_attribute' : 'variable',
                               'cm_key' : attribute},
                                  { "$set": { attribute: value,
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
            print query
            print values
            return self.db_inventory.update(query, values, upsert=True)

    def insert(self, element):
        self.db_inventory.insert(element)

    def clear(self):
        self.db_inventory.remove({"cm_type" : "inventory"})

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

        for name in self.config["clusters"]:

            cluster = self.config["clusters"][name]
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
        self.generate_bootspec()
        self._generate_globals()



        clusters = self.config["clusters"]

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
                                     'label' : n_label[i],
                                     'network_name': n_name,
                                     'cm_network_id': net_id,
                                     'ipaddr': n_range[i],
                                     'cm_attribute': 'network'}
                    )
                    self.insert(element)
                net_id += 1

    def cluster (self, name):
        """returns cluster data in dict"""
        name = "NOT IMPLEMENTED"
        raise RuntimeError("Not Implemented")

    def info(self):
        '''
        print some elementary overview information 
        '''
        clusters = self.find({'cm_type' : 'inventory',
                              'cm_key' : 'range',
                              'cm_kind' : 'server'})
        servers = self.find({'cm_type' : 'inventory',
                             'cm_key' : 'server',
                             'cm_kind' : 'server'})
        services = self.find({'cm_type' : 'inventory',
                              'cm_key' : 'image',
                              'cm_kind' : 'image'})
        images = self.find({'cm_key' : 'bootspec'})
        print "IIII", images.count()


        # print "%15s:" % "dbname", self.inventory_name
        print "%15s:" % "clusters", clusters.count(), "->", ', '.join([c['cm_cluster'] for c in clusters])
        print "%15s:" % "services", services.count()
        print "%15s:" % "servers", servers.count()
        print "%15s:" % "images", images.count() , "->", ', '.join([c['cm_label'] for c in images])
        print

        print clusters.count()

        print "Clusters"
        print 30 * "="
        for host in clusters:
            print "    ", host['cm_cluster'], "->", host['cm_hostlist']

        print

    def hostlist (self, name):
        print "NAME", name
        hosts = self.find ({"cm_cluster": name, 'cm_key': 'range' })[0]['cm_value']
        #print "===================", self.find_one({"cm_cluster": name, 'cm_key': 'range' })
        return hosts

    def host (self, index, auth=True):
        cursor = self.find ({"cm_id" : index,
                             'cm_attribute' : 'network'})

        print "CCCC", cursor[0]


        data = {}

        data['cm_cluster'] = cursor[0]['cm_cluster']
        data['cm_type'] = cursor[0]['cm_type']
        data['cm_id'] = cursor[0]['cm_id']

        pprint (cursor[0]['cm_cluster'])

        c2 = self.find({"cm_attribute": 'variable'})

        for e in c2:
            print "EEE", e
            print

        cursor_attributes = self.find ({"cm_id" : index, 'cm_attribute' : 'variable'})
        for element in cursor_attributes:
            data[element['cm_key']] = element['cm_value']


        data['network'] = {}
        for result in cursor:
            print 70 * "R"
            pprint(result)
            print 70 * "S"

            n_id = result["cm_network_id"]
            n_name = result["network_name"]
            n_ipaddr = result["ipaddr"]
            data['network'][n_name] = dict(result)
            # del data["network"][name]["_id"]


        cluster_name = data['cm_cluster']
        cluster_auth = self.server_config["clusters"][cluster_name]

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

    def ipadr (self, index, iptype):
        return self.find ({"cm_id": index,
                           "type": iptype})[0]['ipaddr']

    def generate_bootspec(self):
		print self.bootspec_config

		bootspecs =  self.bootspec_config['bootspec']
		for name in bootspecs:
			
			print "Adding to inventory bootspec", name
			description = bootspecs[name]
			print "DDD", description
			self.add_bootspec(name, description)

    def add_bootspec(self, name, description):
        '''
        cm_type: inventory
        cm_kind: bootspec
        cm_key: bootspec
        
        cm_id: name
        label: name
        cm_refresh: now
        
        osimage: '/backup/snapshot/india_openstack-2013-07-01.squashfs'
        os: 'ubuntu12'
        extension: 'squashfs'
        partition_scheme: 'gpt'
        fstab_append: False
        method: 'put'
        boot:
           kernel_type: kernel
           bootloader: 'grub2'
        rootpass: False
        disk:
           device: '/dev/sda'
           partitions:
               swap:
                   size: '2'
               system:
                   size: '100'
                   mount: '/'
                   type: 'ext4'
               data:
                   size: '-1'
                   mount: '/var/lib/nova'
                   type: 'xfs'
        '''
        print "IAM IN", name, description
        time = datetime.now()
        print "TYPE", type(description)
        element = dict(description)
        print "ELEMENT", element
        element.update({'cm_type': "inventory",
                        'cm_key': 'bootspec',
                        'cm_kind': 'bootspec',
                        'cm_label': name,
                        'cm_id': name,
                        'id': name,
                        'label' : name,
                        'cm_refresh': time})
        self.update({'cm_key': 'bootspec', 'id': name}, element)

    def get_bootspec (self, name):
        spec = self.find_one ({'cm_type': "inventory",
                               'cm_key': 'bootspec',
                               'cm_kind': 'bootspec',
                               'cm_id': name})
        return spec


def main():
    inventory = Inventory()


    r = inventory.find ({})
    for e in r:
        print e

    print r.count()

    name = "b010"
    data = inventory.host(name)
    pprint(data)

    print inventory.ipadr (name, "public")
    print inventory.ipadr (name, "internal")


if  __name__ == '__main__':
    main()


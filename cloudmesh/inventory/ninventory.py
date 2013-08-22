from cloudmesh.config.cm_config import cm_config_server

from cloudmesh.util.logger import LOGGER
from hostlist import expand_hostlist
from pprint import pprint
from pymongo import MongoClient
from jinja2 import Template
import sys
from cloudmesh.util.util import path_expand as cm_path_expand
from cloudmesh.config.cm_config import cm_config_server
import yaml
import json
# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER('cm_mongo')

 
class ninventory:
            
    server_config = None
    
    def __init__(self):         
        self.server_config = cm_config_server().config
        location = cm_path_expand("~/.futuregrid/cloudmesh_cluster.yaml")
        result = open(location, 'r').read()
        template = Template(result)
        self.config = yaml.load(template.render(self.server_config))
        self._connect_to_mongo()
        self.generate()

    def _connect_to_mongo(self):
        db_name = "new-inventory"
        collection = "inventory"
        self.client = MongoClient()    
        self.db = self.client[db_name]          
        self.db_inventory = self.db[collection]    


    def insert(self,element):
        self.db_inventory.insert(element)

    def _generate_globals(self):
        for name in self.config["clusters"]:
            cluster = self.config["clusters"][name]
            keys = cluster.keys()
            for key in keys: 
                if (type(cluster[key]) is str) and (not key in ["id","network"]):
                  element = {'cm_id': name,
                             'cm_type': "inventory",
                             'cm_kind': 'server',
                             'cm_key': key,
                             'cm_value': cluster[key]
                             }
                  self.insert(element)
                elif key == "publickeys":
                      publickeys = cluster[key]
                      for k in publickeys:
                         element = {'cm_id': name,
                                    'cm_type': "inventory",
                                    'cm_kind': 'publickey',
                                    'cm_key': k['name'],
                                    'cm_name': cm_path_expand(k['path']), 
                                    'cm_value': cluster[key]
                                    }
                         self.insert(element)

        
    def generate(self):    
        self.clear()
        self._generate_globals()
        clusters = self.config["clusters"]
        
        data = {}
        
        for cluster_name in clusters:
            cluster = clusters[cluster_name]
            names = expand_hostlist(cluster["id"])
            net_id = 0    
            for network in cluster["network"]:
                
                n_index = expand_hostlist(network["id"])
                n_label = expand_hostlist(network["label"])
                n_range = expand_hostlist(network["range"])
                n_name = network["name"]
                
                for i in range(0,len(names)):
                    name = n_index[i]
                    element = dict(network)
                    del element['range']
                    element.update({'cm_type': "inventory",
                                     'cm_kind': 'server',
                                     'cm_id': name,
                                     'cluster': cluster_name, 
                                     'id': name, 
                                     'label' : n_label[i], 
                                     'network_name': n_name, 
                                     'network_id': net_id, 
                                     'ipaddr': n_range[i]})
                    self.insert(element)
                net_id +=1
                    
    def clear(self):
        self.db_inventory.remove({"cm_type" : "inventory"})
        
    def find(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_inventory.find(query) 
       
    def host (self, index):
        cursor = self.find ({"cm_id" : index})
        
        data = {}
        
        data['cluster'] = cursor[0]['cluster']
        data['cm_type'] = cursor[0]['cm_type']  
        data['cm_id'] = cursor[0]['cm_id']  
        data['label'] = cursor[0]['label']  
        
        data['network']={}
        for result in cursor:
            n_id = result["network_id"]
            n_name = result["network_name"]
            n_ipaddr = result["ipaddr"]
            data['network'][n_name] = dict(result)
            #del data["network"][name]["_id"]

        
        cluster_name = data["cluster"]
        cluster_auth = self.server_config["clusters"][cluster_name]

        for name in cluster_auth:
            network = data["network"][name]
            network.update(cluster_auth[name])
  
        for name in data["network"]:
            del data["network"][name]["_id"]
        
        return data
                
    def ipadr (self, index, type):
        return self.find ({"cm_id": index, "type": type})[0]['ipaddr']
            
def main():
    inventory = ninventory()


    r = inventory.find ({})
    for e in r:
        print e

    print r.count()

    name = "b010"
    data = inventory.host(name)
    pprint(data)
    
    print inventory.ipadr (name, "public")
    print inventory.ipadr (name, "internal")

    
if  __name__ =='__main__':
    main()
 

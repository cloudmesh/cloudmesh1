from cloudmesh.config.cm_config import cm_config_server

from cloudmesh.util.logger import LOGGER
from hostlist import expand_hostlist
from pprint import pprint
from pymongo import MongoClient
# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER('cm_mongo')

 
class ninventory:
            
    def __init__(self):         
        self.elements = []
        self.config = cm_config_server("~/.futuregrid/cloudmesh_cluster.yaml")
        self._connect_to_mongo()

    def _connect_to_mongo(self):
        db_name = "new-inventory"
        collection = "inventory"
        self.client = MongoClient()    
        self.db = self.client[db_name]          
        self.db_inventory = self.db[collection]    

    def add(self,element):
        self.elements.append(element)
        
    def generate(self):    
        clusters = self.config.get()["clusters"]
        
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
                
                element = {}
                for i in range(0,len(names)):
                    name = n_index[i]
                    element[name] = {'cm_type': "inventory",
                                     'cm_kind': 'server',
                                     'cm_id': name,
                                     'cluster': cluster_name, 
                                     'id': name, 
                                     'label' : n_label[i], 
                                     'network_name': n_name, 
                                     'network_id': net_id, 
                                     'ipaddr': n_range[i]}
                    self.add(element[name])
                net_id +=1
                    
    def dump(self):
        for e in self.elements: 
            print e

    def upload(self):
        self.db_inventory.remove({"cm_type" : "inventory"})
        
        for e in self.elements: 
            self.db_inventory.insert(e)

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
        
        data['network']=[]
        for result in cursor:
            n_id = result["network_id"]
            n_name = result["network_name"]
            n_ipaddr = result["ipaddr"]
            data['network'].append({"name": n_name, "ipaddr" : n_ipaddr})
        
        return data
        

def main():
    inventory = ninventory()
    inventory.generate()
    inventory.dump()
    inventory.upload()
    
    r = inventory.find ({})

    print r.count()
    pprint (inventory.host("d010"))
    
if  __name__ =='__main__':
    main()
 

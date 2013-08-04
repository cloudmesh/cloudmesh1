import pymongo
from pymongo import MongoClient
from pbs import PBS
from pprint import pprint
from bson.objectid import ObjectId

class pbs_mongo:

    hosts = {}
    db_qstat = None
    db_pbsnodes = None
    client = None
    pbs_client = None
    
    def __init__(self, collections=["qstat","pbsnodes"]):
        self.client = MongoClient()    
        self.db = self.client["cm-pbs"]          
        self.db_qstat = self.db[collections[0]]    
        self.db_pbsnodes = self.db[collections[1]]    
            
    def activate(self,host,user):
        """activates a specific host to be queried"""
        
        self.pbs_client = PBS(user,host)
        self.hosts[host] = self.pbs_client
    
    def refresh(self, host, type):
        """refreshes the specified data from the given host"""
        data = None
        if type.startswith("q"): 
           data = self.refresh_qstat(host)
        elif type.startswith("n"):
            data = self.refresh_pbsnodes(host)
        else:
            print "type not suported"
        return data
        
    def refresh_qstat(self, host):
        data =  self.hosts[host].qstat(refresh=True)
        for name in data:
            print "mongo: add {0}, {1}, {2}".format(host, 
                                                    data[name]['Job_Id'], 
                                                    data[name]['Job_Owner'], 
                                                    data[name]['Job_Name'])  

            id = "{0}-{1}".format(host,name).replace(".","-")
            data[name]["pbs_host"] = host
            data[name]["cm_id"] = id
            self.db_qstat.remove({"cm_id": id}, safe=True)
            self.db_qstat.insert(data[name])
    
    def get_qstat(self, host):
        data = self.db_qstat.find({"pbs_host": host})
        return data
        
    def refresh_pbsnodes(self, host):
        data = self.hosts[host].pbsnodes(refresh=True)
        for name in data:
            print "mongo: add {0}, {1}".format(host, 
                                               name) 
            
            id = "{0}-{1}".format(host,name).replace(".","-")
            data[name]["pbs_host"] = host
            data[name]["cm_id"] = id
            self.db_pbsnodes.remove({"cm_id": id}, safe=True)
            self.db_pbsnodes.insert(data[name])

    def get_pbsnodes(self, host):
        data = self.db_pbsnodes.find({"pbs_host": host})
        return data
    
    def delete_qstat(self,host):
        pass
    
    def delete_pbsnodes(self,host):
        pass
    
    def clear(self):
        """deletes the data in the collection"""
        
def main():
    
    host = "alamo.futuregrid.org"
    pbs = pbs_mongo()
    pbs.activate(host,"gvonlasz")
    print pbs.hosts
    
    # d = pbs.refresh_qstat(host)
    """
    d = pbs.get_qstat(host)
    for e in d:
        pprint(e) 
    """
    
    d = pbs.refresh_pbsnodes(host)
    d = pbs.get_pbsnodes(host)
    for e in d:
        pprint(e) 
    
if __name__ == "__main__":
    main()
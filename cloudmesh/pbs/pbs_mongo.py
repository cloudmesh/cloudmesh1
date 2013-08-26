import pymongo
from pbs import PBS
from pprint import pprint
from bson.objectid import ObjectId
from cloudmesh.util.util import path_expand
import yaml
from cloudmesh.config.cm_config import get_mongo_db
from datetime import datetime

class pbs_mongo:

    hosts = {}
    db_qstat = None
    db_pbsnodes = None
    client = None
    pbs_client = None
    
    
    config = None
    

    def __init__(self, collections=["qstat","pbsnodes"]):
        
        self.db_qstat = get_mongo_db(collections[0])
        self.db_pbsnodes = get_mongo_db(collections[1])  
            
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
        '''
        obtains a refreshed qstat data set from the specified host. The result is written into the mongo db.
        :param host: The host on which to execute qstat
        '''
        time_now = datetime.now()
        data =  dict(self.hosts[host].qstat(refresh=True))
        print "DDDD"
        pprint (data)
        self.db_qstat.remove({"cm_host": host, "cm_kind" : "qstat"}, safe=True)
        print "EEEE"
        pprint (data)
        for name in data:
            
            
            print "mongo: add {0}, {1}, {2}".format(host, 
                                                    data[name]['Job_Id'], 
                                                    data[name]['Job_Owner'], 
                                                    data[name]['Job_Name'])  

            id = "{0}-{1}-qstat".format(host,name).replace(".","-")
            data[name]["cm_host"] = host
            data[name]["cm_kind"] = "qstat"
            data[name]["cm_id"] = id
            data[name]["cm_refresh"] = time_now

            print "mongo: add {0}, {1}, {2}".format(host, 
                                                    data[name]['Job_Id'], 
                                                    data[name]['Job_Owner'], 
                                                    data[name]['Job_Name'])  

            print "IIIIII"
            pprint(data)
            self.db_qstat.insert(data[name])
    
    def get(self, host, type):
        """refreshes the specified data from the given host"""
        data = None
        if type.startswith("q"): 
           data = self.get_qstat(host)
        elif type.startswith("n"):
            data = self.get_pbsnodes(host)
        else:
            print "type not suported"
        return data
        
    def get_qstat(self, host=None):
        '''
        returns the qstat data from the mongo db. The data can be put into the mongo db via refresh
        :param host:
        '''
        if host is None:
            data = self.db_qstat.find({"cm_kind": "qstat"})
        else:
            data = self.db_qstat.find({"cm_host": host, "cm_kind": "qstat"})
        print "COUNT", data.count()
        return data
        
    def refresh_pbsnodes(self, host):
        '''
        retrieves the qstat data from the host and puts it into mongodb
        :param host:
        '''
        time_now = datetime.now()
        data = self.hosts[host].pbsnodes(refresh=True)
        for name in data:
            print "mongo: add {0}, {1}".format(host, 
                                               name) 
            
            id = "{0}-{1}".format(host,name).replace(".","-")
            data[name]["cm_host"] = host
            data[name]["cm_id"] = id
            data[name]["cm_kind"] = "pbsnodes"    
            data[name]["cm_refresh"] = time_now
            self.db_pbsnodes.remove({"cm_id": id}, safe=True)
            self.db_pbsnodes.insert(data[name])

    def get_pbsnodes(self, host=None):
        '''
        retrieves the pbsnodes data for the ost from mongodb. the data can be put with a refresh method into mongo db.
        :param host:
        '''
        if host is None:
            data = self.db_pbsnodes.find({"cm_kind": "pbsnodes"})
        else:
            data = self.db_pbsnodes.find({"cm_host": host, "cm_kind": "pbsnodes"})
        return data
    
    def delete_qstat(self,host):
        '''
        NOT IMPLEMENTED .deletes the qstat information from mongodb
        :param host:
        '''
    
    def delete_pbsnodes(self,host):
        '''
        NOT IMPLEMENTED. deletes the pbsnodes information from mongodb
        :param host:
        '''
    
    def clear(self):
        '''
        NOT IMPLEMENTED. clears the mongo db data for pbs and qstat
        '''
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
"""
Fetch cluster's information, for example: temperature, service type and etc.
Currently, FetchCluster only knows existing cluster,
that is ['india', 'bravo', 'echo', 'delta']
If more cluster are added later, this class MUST be modified carefully
"""
from cloudmesh.pbs.pbs import PBS
from cloudmesh.config.ConfigDict import ConfigDict
from hostlist import expand_hostlist
from cloudmesh.rack.tasks import task_sensors

class FetchClusterInfo:
    
    username = None
    
    hostname = None
    
    def __init__(self, user, host):
        self.username = user
        self.hostname = host
    
    # fetch cluster service type with "ssh user@host pbsnodes -a"
    # params: 
    #    flag_filter, None or one item in list ['india', 'bravo', 'echo', 'delta']
    def fetch_service_type(self, flag_filter=None):
        pbs = PBS(self.username, self.hostname)
        dict_pbs_info = pbs.pbsnodes()
        dict_data = {}
        for key in dict_pbs_info.keys():
            server = dict_pbs_info[key]
            ukey = self.getUniformFromRealLabel(server["name"])
            if flag_filter is None or flag_filter[0] == ukey[0]:
                utype = "unknown"
                if "note" in server.keys():
                    utype = server["note"]
                dict_data[ukey] = utype
        return dict_data
    
    
    # fetch cluster temperature from mongo db
    # params: 
    #    flag_filter, None or one item in list ['india', 'bravo', 'echo', 'delta']
    def fetch_temperature_mongo(self, flag_filter=None):
        # read data from mongo db
        pass
    
    
    # refresh cluster temperature to mongo db
    # file_yaml: the absolute path of cloudmesh_cluster.yaml
    def update_temperature_mongo(self, file_yaml):
        # read cloudmesh_cluster.yaml configuration
        clusters_config = ConfigDict(filename=file_yaml)
        dict_config = clusters_config["clusters"]
        dict_cluster = {}
        for key in dict_config.keys():
            dict_cluster[key] = {}
            # get the information of "label", "IP address"
            list_networks = dict_config[key]["network"]
            for network in list_networks:
                dict_cluster[key][network["name"]] = network
        
        # construct a dict 
        dict_idip = {}
        for key in dict_cluster.keys():
            dict_idip[key] = {}
            # only proceed network whose name is "internal" or 0
            # I think name is 0 is also an internal network
            if "internal" in dict_cluster[key].keys():
                network = dict_cluster[key]["internal"]
            else:
                network = dict_cluster[key][0]
            idlist = expand_hostlist(network["id"])
            iplist = expand_hostlist(network["range"])
            for uid, ip in zip(idlist, iplist):
                dict_idip[key][uid] = ip
        
        # call async service/task to get real temperature
        # the async service will update the mongo db after success
        task_sensors(dict_idip)
    
    
    #
    # mapping between the uniform label and the real label
    # india: i001  <--> i1; i010 <--> i10, i100 <--> i100
    # bravo: b001i <--> b001
    # delta: d001i <--> d001, deltai <--> d000
    # echo: echo15i <--> e015
    #
    # # get real label of unique cluster server name from the uniform label
    def getRealLabelFromUniform(self, ulabel):
        if ulabel == "d000":
            return "deltai"
        
        lchar = list(ulabel)
        if lchar[0] == 'b'or lchar[0] == 'd':
            return ulabel + "i"
        else:
            snum = "".join(lchar[1:])
            rsnum = str(int(snum))
            if lchar[0] == 'e':
                return "echo" + rsnum + "i"
            elif lchar[0] == 'i':
                return "i" + rsnum
        
        # don't know anymore, just return
        return ulabel

    # get uniform label from real label of cluster name
    def getUniformFromRealLabel(self, rlabel):
        if rlabel == "deltai":
            return "d000"
        
        lchar = list(rlabel)
        lzero = list("000")
        lresult = []
        if lchar[0] == 'b'or lchar[0] == 'd':
            lresult = lchar[:-1]
        elif lchar[0] == 'e':
            lzero.extend(lchar[4:-1])
            lresult.append('e')
            lresult.extend(lzero[-3:])
        elif lchar[0] == 'i':
            lzero.extend(lchar[1:])
            lresult.append('i')
            lresult.extend(lzero[-3:])
        else:
            return rlabel
            
        return "".join(lresult)

# debug
if __name__ == "__main__":
    mytest = FetchClusterInfo("hengchen", "india.futuregrid.org")
    #data = mytest.fetch_service_type()
    print "=" * 30
    print data
    print "-" * 30
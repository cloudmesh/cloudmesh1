"""
Fetch cluster's information, for example: temperature, service type and etc.
Currently, FetchCluster only knows existing cluster,
that is ['india', 'bravo', 'echo', 'delta']
If more cluster are added later, this class MUST be modified carefully
"""
from cloudmesh.pbs.pbs import PBS
from cloudmesh.config.ConfigDict import ConfigDict
from hostlist import expand_hostlist
from cloudmesh.rack.queue.tasks import temperature
from cloudmesh.config.ConfigDict import ConfigDict


from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class FetchClusterInfo:

    CLUSTER_CONFIG_FILE = "~/.futuregrid/cloudmesh_cluster.yaml"

    username = None

    hostname = None

    cluster_config = None

    def __init__(self, user, host):
        self.username = user
        self.hostname = host
        self.cluster_config = ConfigDict(filename=self.CLUSTER_CONFIG_FILE)

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
                    note_value = server["note"]
                    if type(note_value) is dict:
                        utype = note_value["service"]
                    else:
                         utype = note_value

                dict_data[ukey] = utype
        return dict_data


    # fetch cluster temperature from mongo db
    # params:
    #    flag_filter, None or one item in list ['india', 'bravo', 'echo', 'delta']
    def fetch_temperature_mongo(self, flag_filter=None):
        # read data from mongo db
        pass


    # fetch cluster temperature from ipmitools
    # params:
    #    flag_filter, None or one item in list ['india', 'bravo', 'echo', 'delta']
    #    unit: temperature unit, its value is C or F
    # return: {"i002": 45.0, "i123": 55.1, ...}
    def fetch_temperature_ipmi(self, flag_filter=None, unit='C'):
        default_list_cluster = self.cluster_config.get("cloudmesh.inventory").keys()
        list_id_ranges = []
        if flag_filter is None:
            for cluster in default_list_cluster:
                list_id_ranges.append(self.cluster_config.get("cloudmesh.inventory.{0}.id".format(cluster)))
        elif flag_filter in default_list_cluster:
            list_id_ranges.append(self.cluster_config.get("cloudmesh.inventory.{0}.id".format(flag_filter)))
        else:
            log.error("A invalid cluster name {0} in fetch_temperature_ipmi".format(flag_filter))
        list_hosts = []
        for id_range in list_id_ranges:
            list_hosts += expand_hostlist(id_range)
        dict_data = {}
        for host in list_hosts:
            result = temperature(host, unit)
            # temperature value -1 means the destination host is not reachable
            dict_data[host] = -1 if result is None else result["value"]

        # log.debug("fetch dict data: {0}".format(dict_data))

        return dict_data



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
    data = mytest.fetch_temperature_ipmi()
    print "=" * 30
    print data
    print "-" * 30

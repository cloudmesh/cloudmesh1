# with open ("pbs_nodes_data.txt", "r") as myfile:
#    pbs_nodes_data=myfile.readlines()

from ast import literal_eval
from collections import Counter
from hostlist import expand_hostlist
from pprint import pprint
from sh import ssh, ssh
from xml.dom import minidom
import yaml
import sys

class PBS:

    user = None
    host = None
    pbs_qstat_data = None
    pbs_nodes_data = None
    pbs_qinfo_data = None

    cluster_queues = None

    def __init__(self, user, host):
        self.user = user
        self.host = host

        #
        # hard codd for now should be in yaml file
        #
        if host.startswith("india"):
            self.cluster_queues = {
                                   'india.futuregrid.org': [
                                                            'ib',
                                                            'fg40',
                                                            'batch',
                                                            'long',
                                                            'provision',
                                                            'b534',
                                                            'systest',
                                                            'reserved',
                                                            'interactive'],
                                   'delta.futuregrid.org': [
                                                            'delta',
                                                            'delta-long'],
                                   'echo.futuregrid.org': ['echo'],
                                   'bravo.futuregrid.org': ['bravo', 'bravo-long'],
                                   }

    def requister_joint_queues(self, cluster_queues):
        """allows the registration of queues for multiple clusters managed through the same queuing server
        
                
        cluster_queues = {
            'india.futuregrid.org': ['ib','fg40', 'batch', 'long', 'provision', 'b534', 'systest', 'reserved', 'interactive'],
            'delta.futuregrid.org': ['delta', 'delta-long'],
            'echo.futuregrid.org': ['echo'],
            'bravo.futuregrid.org': ['bravo', 'bravo-long'],
        }
        """
        self.cluster_queues = cluster_queues


    def qinfo(self, refresh=True):
        """returns qstat -Q -f in dict format"""

        if self.pbs_qstat_data is None or refresh:
            try:
                result = ssh("{0}@{1}".format(self.user, self.host), "qstat -Q -f")
            except:
                raise RuntimeError("can not execute pbs qstat via ssh")

            d = {}

            # sanitize block

            result = result.replace("\n\t", "")

            result = result.replace('resources_assigned.', 'resources_assigned_')
            result = result.replace('resources_default.', 'resources_default_')
            result = result.replace('resources_max.', 'resources_max_')


            for block in result.split("\n\n")[:-1]:
                block = [x.replace(" =", ":", 1) for x in block.split("\n")]
                block[0] = block[0].replace("Queue: ", "") + ":"
                queue = block[0][:-1]

                block = '\n'.join(block)

                block_yaml = yaml.safe_load(block)
                d[queue] = block_yaml[queue]

                d[queue]['queue'] = queue
                # end sanitize

                if 'state_count' in d[queue]:
                    values = [x.split(":") for x in d[queue]['state_count'].split(" ")]
                    d[queue]['state_count'] = {}
                    for value in values:
                        d[queue]['state_count'][value[0]] = value[1]

                if 'acl_hosts' in d[queue]:
                    print d[queue]['acl_hosts']
                    d[queue]['acl_hosts'] = d[queue]['acl_hosts'].split("+")

        self.pbs_qinfo_data = d

        if self.cluster_queues is None:
            return {self.host: self.pbs_qinfo_data}
        else:
            return self.qinfo_extract(self.cluster_queues, self.pbs_qinfo_data)


    def qinfo_extract(self, cluster_queues, qinfo_data):


        # initialize the queues
        queues = {}
        for q in cluster_queues:
            queues[q] = {}

        # separate the queues
        for cluster in cluster_queues:
            for q in cluster_queues[cluster]:
                queues[cluster][q] = qinfo_data[q]

        return queues


    def pbsnodes(self, refresh=True):
        """returns the pbs node infor from an pbs_nodes_raw_data is a string see above for example"""

        if self.pbs_nodes_data is None or refresh:
            try:
                result = ssh("{0}@{1}".format(self.user, self.host), "pbsnodes", "-a")
            except:
                raise RuntimeError("can not execute pbs nodes via ssh")
            pbsinfo = {}
            nodes = result.split("\n\n")
            for node in nodes:
                pbs_data = node.split("\n")
                pbs_data = [e.strip()  for e in pbs_data]
                name = pbs_data[0]
                if name != "":
                    pbsinfo[name] = {u'name': name}
                    for element in pbs_data[1:]:
                        try:
                            (attribute, value) = element.split (" = ")
                            if attribute == 'status':
                                status_elements = value.split(",")
                                pbsinfo[name][attribute] = {}
                                for e in status_elements:
                                    (a, v) = e.split("=")
                                    pbsinfo[name][attribute][a] = v
                            elif attribute == 'jobs':
                                pbsinfo[name][attribute] = value.split(',')
                            elif attribute == 'note' and (value.strip().startswith("{") or value.strip().startswith("[")):
                                pbsinfo[name][attribute] = literal_eval(value)
                            else:
                                pbsinfo[name][attribute] = value
                        except:
                            pass
            self.pbs_nodes_data = pbsinfo

        return self.pbs_nodes_data

    def exists(self, host):
        """ prints true if the host is in the node list """
        return host in self.pbs_nodes_data

    def set(self, spec, attribute):
        """add an attribute for the specified hosts in the format
        i[1-20]. which would set the attribute for all hosts in i1 to
        i20"""
        hosts = expand_hostlist(spec)
        for host in hosts:
            self._set(host, attribute)

    def _set(self, host, attribute):
        """add an attribute for the specified hosts"""
        print "TODO: ALLAN"


    def qstat(self, refresh=True):
        if self.pbs_qstat_data is None or refresh:
            try:
                xmldata = str(ssh("{0}@{1}".format(self.user, self.host), "qstat", "-x"))
            except:
                raise RuntimeError("can not execute pbs qstat via ssh")
            info = {}

            try:
                xmldoc = minidom.parseString(xmldata)

                itemlist = xmldoc.getElementsByTagName('Job')
                for item in itemlist:
                    job = {}
                    for attribute in item.childNodes:
                        if len(attribute.childNodes) == 1:
                            job[attribute.nodeName] = attribute.firstChild.nodeValue
                        else:
                            job[attribute.nodeName] = {}
                            for subchild in attribute.childNodes:
                                job[attribute.nodeName][subchild.nodeName] = subchild.firstChild.nodeValue

                    info[job['Job_Id']] = job
            except:
                pass
            self.pbs_qstat_data = info
        return self.pbs_qstat_data

    def service_distribution(self, simple=True):
        """prints the distribution of services"""

        def pbsnodes_data(host):

            result = str(ssh("{0}@{1}".format(self.user, host), "pbsnodes", "-l", "-n"))[:-1]
            return result

        empty = ["", "", ""]
        x = [x.split() for x in pbsnodes_data(self.host).split("\n")]

        # Fill missing values

        r = []
        for line in x:
            new = ["unkown", "unkown", "unkown"]
            for i in range(0, len(line)):
                try:
                    new[i] = line[i]
                except:
                    pass
            r.append(new)

        # just taking column 2

        x = [x[2] for x in r]



        print "GFKHFJH ", x
        cnt = Counter(x)

        print "COUNT",

        return dict(cnt)

    """
    def _namemap(self,"0000"):
        result = (str(ssh(host, "pbsnodes", "-l", "-n"))[:-1]).split("\n")
        names = [x.split()[0] for x in result]

        #
        #
        #  s1 -> s0001
        #  i11 -> i0011
        #  deltai -> delta   ???
        #  d012i  -> d0012
        #  b011i  -> d0011
        #
    """

if __name__ == "__main__":


    pbs = PBS("gvonlasz", "alamo")
    pprint (pbs.qinfo())


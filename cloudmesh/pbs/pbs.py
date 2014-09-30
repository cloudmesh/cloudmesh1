# with open ("pbs_nodes_data.txt", "r") as myfile:
#    pbs_nodes_data=myfile.readlines()

from ast import literal_eval
from collections import Counter
from hostlist import expand_hostlist
from pprint import pprint
from sh import ssh
from xml.dom import minidom
import yaml
import sys
import re

from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)


class PBS:

    user = None
    host = None
    pbs_qstat_data = None
    pbs_nodes_data = None
    pbs_qinfo_data = None
    pbs_qinfo_default_data = None

    cluster_queues = None

    def __init__(self, user, host):
        self.user = user
        self.host = host

        #
        # hard coded for now should be in yaml file
        #
        if host.startswith("india"):
            self.cluster_queues = {
                'india.futuregrid.org': [
                    'batch',
                    'long',
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
            'india.futuregrid.org': ['batch', 'long', 'b534', 'systest', 'reserved', 'interactive'],
            'delta.futuregrid.org': ['delta', 'delta-long'],
            'echo.futuregrid.org': ['echo'],
            'bravo.futuregrid.org': ['bravo', 'bravo-long'],
        }
        """
        self.cluster_queues = cluster_queues

    def qinfo_user(self, refresh=True):
        """Return the number of user from qstat

            example line is:
            873664.i136 ...549.sh xcguser  0   Q long
            $3 indicates an user id
        """
        if self.pbs_qinfo_default_data is None or refresh:
            try:
                result = ssh("{0}@{1}".format(self.user, self.host), "qstat")
            except:
                raise RuntimeError(
                    "can not execute pbs qstat on host {0}".format(self.host))

            # sanitize block
            data = self.convert_into_json(result)
            merged_data = self.merge_queues(self.cluster_queues, data)
            self.pbs_qinfo_default_data = merged_data
        else:
            merged_data = self.pbs_qinfo_default_data

        return merged_data

    def merge_queues(self, machines, data):
        res = {}
        for row in data:
            if not machines:
                try:
                    res[self.host].append(row)
                except:
                    res[self.host] = [row]
            else:
                for machine in machines:
                    queues = machines[machine]
                    if row['Use'] in queues:
                        try:
                            res[machine].append(row)
                        except:
                            res[machine] = [row]
        return res

    def convert_into_json(self, qstat):

        list_qstat = qstat.split("\n")
        try:
                # delete a delimiter line between a header and contents looks
                # like '-------- --- ---'
            del(list_qstat[1])
        except:
            pass
        pattern = re.compile(r'\s+')
        tmp = []
        for row in list_qstat:
            tmp.append(re.sub(pattern, ',', row))

        res = csv.DictReader(tmp, skipinitialspace=True)
        return res

    def qinfo(self, refresh=True):
        """returns qstat -Q -f in dict format"""

        if self.pbs_qinfo_data is None or refresh:
            try:
                result = ssh(
                    "{0}@{1}".format(self.user, self.host), "qstat -Q -f")
            except:
                raise RuntimeError(
                    "can not execute pbs qstat on host {0}".format(self.host))

            d = {}

            # sanitize block

            result = result.replace("\n\t", "")

            result = result.replace(
                'resources_assigned.', 'resources_assigned_')
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
                    values = [x.split(":")
                              for x in d[queue]['state_count'].split(" ")]
                    d[queue]['state_count'] = {}
                    for value in values:
                        d[queue]['state_count'][value[0]] = value[1]

                if 'acl_hosts' in d[queue]:
                    # print d[queue]['acl_hosts']
                    d[queue]['acl_hosts'] = d[queue]['acl_hosts'].split("+")

        self.pbs_qinfo_data = d

        #pprint(self.qinfo_extract(self.cluster_queues, self.pbs_qinfo_data))

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
                try:
                    queues[cluster][q] = qinfo_data[q]
                except:
                    log.error("no data found for {0}".format(q))
        return queues

    def _qmgr(self, command):
        result = None
        try:
            result = ssh("{0}@{1}".format(self.user, self.host), command)
        except:
            raise RuntimeError(
                "can not execute qmgr on host {0}, command:".format(self.host, command))
        return result

    def create_node(self, name):
        """create node"""
        result = self._qmgr("create node {0}".format(name))
        return result

    def set_np(self, name, np):
        """set node %name np %np | qmgr"""
        result = self._qmgr("set node {0} np {1}".format(name, np))
        return result

    def set_properties(self, name, properties):
        """set node % properties %"""
        result = self._qmgr("set node {0} properties {1}".format(name, properties))

    def set_note(self, name, note):
        """set node % note %"""
        result = self._qmgr("set node {0} note {1}".format(name, note))

    def pbsnodes(self, refresh=True):
        """returns the pbs node infor from an pbs_nodes_raw_data is a string see above for example"""

        if self.pbs_nodes_data is None or refresh:
            try:
                result = ssh(
                    "{0}@{1}".format(self.user, self.host), "pbsnodes", "-a")
            except:
                raise RuntimeError(
                    "can not execute pbs nodes on host {0}".format(self.host))
            pbsinfo = {}
            nodes = result.split("\n\n")
            for node in nodes:
                pbs_data = node.split("\n")
                pbs_data = [e.strip() for e in pbs_data]
                name = pbs_data[0]
                if name != "":
                    pbsinfo[name] = {u'name': name}
                    for element in pbs_data[1:]:
                        try:
                            (attribute, value) = element.split(" = ")
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
                xmldata = str(
                    ssh("{0}@{1}".format(self.user, self.host), "qstat", "-x"))
            except:
                raise RuntimeError(
                    "can not execute pbs qstat on host {0}".format(self.host))
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
                                job[attribute.nodeName][
                                    subchild.nodeName] = subchild.firstChild.nodeValue

                    info[job['Job_Id']] = job
            except:
                pass
            self.pbs_qstat_data = info
        # return self.pbs_qstat_data

        #pprint (self.pbs_qstat_data)

        if self.cluster_queues is None:
            return {self.host: self.pbs_qstat_data}
        else:
            return self.qstat_extract(self.cluster_queues, self.pbs_qstat_data)

    def qstat_extract(self, cluster_queues, qstat_data):

        # initialize the queues
        queues = {}
        for q in cluster_queues:
            queues[q] = {}

        # separate the queues
        for job in qstat_data:
            queue = qstat_data[job]['queue']

            for cluster in cluster_queues:
                if queue in cluster_queues[cluster]:
                    queues[cluster][job] = qstat_data[job]
            # log.error("no data found for {0}".format(q))
        return queues

    def get_uniq_users(self, refresh=False):
        if self.pbs_qstat_data is None or refresh:
            self.qstat()

        data = self.pbs_qstat_data
        job_owner = {}
        for job in data:
            queue_name = data[job]['queue']
            server_name = self.get_machine_name(queue_name)
            ownerid = (data[job]['Job_Owner']).split("@")[0]
            try:
                job_owner[server_name].add(ownerid)
            except:
                job_owner[server_name] = set([ownerid])

        return job_owner

    def get_machine_name(self, qname):
        machines = self.cluster_queues
        if not machines:
            return qname
        for machine in machines:
            queues = machines[machine]
            if qname in queues:
                return machine

        return qname

    def service_distribution(self, simple=True):
        """prints the distribution of services"""

        def pbsnodes_data(host):

            result = str(
                ssh("{0}@{1}".format(self.user, host), "pbsnodes", "-l", "-n"))[:-1]
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

        # print "GFKHFJH ", x
        cnt = Counter(x)

        # print "COUNT",

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

    pbs = PBS("gvonlasz", "echo.futuregrid.org")
    #pprint (pbs.qinfo())
    pprint(pbs.qstat())


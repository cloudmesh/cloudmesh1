#with open ("data.txt", "r") as myfile:
#    data=myfile.readlines()

from sh import ssh
from pprint import pprint
from ast import literal_eval

data= """i51
     state = down,job-exclusive
     np = 8
     properties = compute
     ntype = cluster
     jobs = 0/594490.i136, 1/594490.i136, 2/594490.i136, 3/594490.i136, 4/594490.i136, 5/594490.i136, 6/594490.i136, 7/594490.i136
     note = {'service': 'hpc', 'project': 'fg82', 'owner': 'gvonlasz', 'type': 'reserved', 'provisioner': 'teefaa'}
     gpus = 0

i52
     state = down,job-exclusive
     np = 8
     properties = compute
     ntype = cluster
     jobs = 0/594490.i136, 1/594490.i136, 2/594490.i136, 3/594490.i136, 4/594490.i136, 5/594490.i136, 6/594490.i136, 7/594490.i136
     status = rectime=1375095999,varattr=,jobs=,state=free,netload=1261133500,gres=,loadave=0.00,ncpus=8,physmem=24659396kb,availmem=26474592kb,totmem=26763868kb,idletime=1605207,nusers=0,nsessions=? 0,sessions=? 0,uname=Linux i52 2.6.18-348.6.1.el5 #1 SMP Fri Apr 26 09:21:26 EDT 2013 x86_64,opsys=statefulrhels5,arch=x86_64
     gpus = 0

i53
     state = down,job-exclusive
     np = 8
     properties = compute
     ntype = cluster
     jobs = 0/594490.i136, 1/594490.i136, 2/594490.i136, 3/594490.i136, 4/594490.i136, 5/594490.i136, 6/594490.i136, 7/594490.i136
     status = rectime=1375096495,varattr=,jobs=,state=free,netload=1253604666,gres=,loadave=0.00,ncpus=8,physmem=24659396kb,availmem=26474128kb,totmem=26763868kb,idletime=1605707,nusers=0,nsessions=? 0,sessions=? 0,uname=Linux i53 2.6.18-348.6.1.el5 #1 SMP Fri Apr 26 09:21:26 EDT 2013 x86_64,opsys=statefulrhels5,arch=x86_64
     gpus = 0

i54
     state = down,job-exclusive
     np = 8
     properties = compute
     ntype = cluster
     jobs = 0/594490.i136, 1/594490.i136, 2/594490.i136, 3/594490.i136, 4/594490.i136, 5/594490.i136, 6/594490.i136, 7/594490.i136
     status = rectime=1375096494,varattr=,jobs=,state=free,netload=1239414644,gres=,loadave=0.00,ncpus=8,physmem=24659396kb,availmem=26473364kb,totmem=26763868kb,idletime=1605666,nusers=0,nsessions=? 0,sessions=? 0,uname=Linux i54 2.6.18-348.6.1.el5 #1 SMP Fri Apr 26 09:21:26 EDT 2013 x86_64,opsys=statefulrhels5,arch=x86_64
     gpus = 0

i70
     state = down,offline,job-exclusive
     np = 8
     properties = provision
     ntype = cluster
     jobs = 0/594490.i136, 1/594490.i136, 2/594490.i136, 3/594490.i136, 4/594490.i136, 5/594490.i136, 6/594490.i136, 7/594490.i136
     gpus = 0

i71
     state = down
     np = 8
     properties = compute
     ntype = cluster
     status = rectime=1375097304,varattr=,jobs=,state=free,netload=2783777877,gres=,loadave=0.00,ncpus=8,physmem=24659396kb,availmem=26461836kb,totmem=26763868kb,idletime=1606519,nusers=0,nsessions=? 0,sessions=? 0,uname=Linux i71 2.6.18-348.6.1.el5 #1 SMP Fri Apr 26 09:21:26 EDT 2013 x86_64,opsys=statefulrhels5,arch=x86_64
     gpus = 0

i72
     state = down
     np = 8
     properties = provision
     ntype = cluster
     gpus = 0
"""

#print data

class PBS:

    user = None
    host = None
    pbs_data = None
    
    
    def __init__(self,user, host):
        self.user = user
        self.host = host
    
    def refresh(self):
        """fetches the pbs nodes info"""
        self.pbs_data = ssh("{0}@{1}".format(self.user,self.host), "pbsnodes", "-a")

    @property
    def info(self):
        """returns the pbs node infor from an pbs_data is a string see above for example"""
        pbsinfo = {}
        if self.pbs_data is None:
            self.refresh()
            
        nodes = self.pbs_data.split("\n\n")
        for node in nodes:
            pbs_data = node.split("\n")
            pbs_data = [e.strip()  for e in pbs_data]
            name = pbs_data[0]
            pbsinfo[name] = {}
            for element in pbs_data[1:]:
                try:
                    (attribute, value) = element.split (" = ")
                    if attribute == 'status':
                        status_elements = value.split(",")
                        pbsinfo[name][attribute] = {}
                        for e in status_elements:
                            (a,v) = e.split("=")
                            pbsinfo[name][attribute][a] = v
                    elif attribute == 'jobs':
                        pbsinfo[name][attribute] = value.split(',')
                    elif attribute == 'note':
                        pbsinfo[name][attribute] = literal_eval(value)
                    else:
                        pbsinfo[name][attribute] = value
                except:
                    pass
        self.data = pbsinfo
        return self.data

    def exists(self, host):
        """ prints true if the host is in the node list """
        return host in self.data

    def __str__(self)
        return str(self.data)
    
    def get(self, host):
        """returns just the info for the specified host as dict"""
        if self.exists(host):
            return self.data[host]
        else:
            return None

    def set(self, hosts, attribute):
        """add an attribute for the specified hosts"""
        for host in hosts:
            self._set(host, attribute):
            
    def _set(self, host, attribute):
        """add an attribute for the specified hosts"""
        print "TODO: ALLAN"
            

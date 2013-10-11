"""
A wrap python class of 'pbsnodes -N "note" node' command
The purpose of this class is to provide a simple API 
to write some attribute and its value pairs to note attribute of cluster nodes.
"""

from sh import ssh
from ast import literal_eval
from types import *
from cloudmesh.pbs.pbs import PBS

class PbsNoteBuilder:

    userName = None
    hostName = None
    pbs_nodes_info = None
    
    def __init__(self, user, host):
        self.userName = user
        self.hostName = host
        self.fetchPbsNodesInfo()
    
    # get recent pbsnodes info
    def fetchPbsNodesInfo(self):
        pbs = PBS(self.userName, self.hostName)
        self.pbs_nodes_info = pbs.pbsnodes()
    
    # node is the server name, e.g., i129, i15
    # note is a dict, {"attr1": "value1", "attr2": "value2"}
    # setNote doesn't check the correctness of the attribute-value pair

    def setNote(self, node, note):
        if node not in self.pbs_nodes_info.keys():
            print "[Warning] PbsNoteBuilder: ", node, " is NOT a valid/existed node according to PBS.pbsnodes"
            return

        # ["note"] ONLY has two type: dict or string
        prev_note = self.pbs_nodes_info[node]["note"]
        flag_dict = False
        if type(prev_note) is DictType:
            flag_dict = True
        
        # assume the default note is for 'service'
        if not flag_dict:
            self.pbs_nodes_info[node]["note"] = {"service": prev_note}
            prev_note = self.pbs_nodes_info[node]["note"]
        
        # now prev_note already is a dict
        # to keep consistency, the keys in note should be lower
        map(lambda x:str(x).lower(), note.keys())
        prev_note.update(note)

        # convert the dict to a unique string
        # e.g., "'other': 'test', 'temperature': '10.2', 'service': 'hpc'"
        kvpair_list = ", ".join([": ".join(map(lambda x: "'".join(["", str(x), ""]), [key, prev_note[key]])) for key in sorted(prev_note.keys())])
        snote = "".join(['{', kvpair_list, '}'])
        sshnote = '"'.join(["", snote, ""])

        # debug, try reverse to dict
        #print "snote is: ", snote
        #print "sshnote is: ", sshnote
        #dnote = literal_eval(snote)
        #print "dnote is: ", dnote
        # update the note attribute in memory to real node
        command = " ".join(["pbsnodes -N", sshnote, node])
        str_ssh = "@".join([self.userName, self.hostName])
        print "[DEBUG] PbsNoteBuilder: command ready to execute is: \n  > ssh {0} {1}\n".format(str_ssh, command)

        #ssh(str_ssh, command)
    
    
    # set server's temperature
    # a shortcut of setNote
    def setTemperatureNote(self, node, temp):
        self.setNote(node, {"temperature": temp})
        
    
    # set server's service type
    # a shortcut of setNote
    def setServiceNote(self, node, service):
        self.setNote(node, {"service": service})
        
        
# test only
if __name__ == "__main__":
    pbsnote = PbsNoteBuilder("hengchen", "india")
    # test temperature
    pbsnote.setTemperatureNote("i129", 99.2)
    # test service type
    pbsnote.setServiceNote("i129", "down")
    # test setNote
    note = {"service": "down, offline", "temperature": "-100.12", "test": "debug", 0:12}
    pbsnote.setNote("i129", note)

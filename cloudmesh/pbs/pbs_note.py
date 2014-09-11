"""
A wrap python class of 'pbsnodes -N "note" node' command
The purpose of this class is to provide a simple API 
to write some attribute and its value pairs to note attribute of cluster nodes.
"""

from sh import ssh
from ast import literal_eval
from types import *
from copy import deepcopy
from cloudmesh.pbs.pbs import PBS
from cloudmesh.inventory import Inventory
import json
from cloudmesh_common.logger import LOGGER

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)


class pbs_note_builder:

    def __init__(self, user, host):
        self.username = user
        self.hostname = host
        self.inventory = Inventory()
        self.fetch_pbs_nodes_info()

    # get recent pbsnodes info
    def fetch_pbs_nodes_info(self):
        pbs = PBS(self.username, self.hostname)
        self.pbs_nodes_info = pbs.pbsnodes()
        # print self.pbs_nodes_info

    def check_node_validation(self, node):
        node_id_label = self.inventory.get_host_id_label(node)
        berror = False
        if node_id_label is None:
            berror = True
        else:
            (node_id, node_label) = node_id_label

        if not berror:
            if node_label not in self.pbs_nodes_info.keys():
                berror = True

        if berror:
            raise NameError(
                "pbs_note_builder: '{0}' is NOT a valid or existed node.".format(node))

        return node_id_label

    def get_note(self, node):
        (node_id, node_label) = self.check_node_validation(node)
        print "{0}-note: {1}".format(node_id, self.pbs_nodes_info[node_label]["note"])

    # node is the server name, e.g., i129, i15
    # note is a dict, {"attr1": "value1", "attr2": "value2"}
    # setNote doesn't check the correctness of the attribute-value pair
    def set_note(self, node, note):
        (node_id, node_label) = self.check_node_validation(node)

        # ["note"] ONLY has two type: dict or string
        prev_note = self.pbs_nodes_info[node_label]["note"]
        if type(prev_note) is dict:
            curr_note = deepcopy(prev_note)
        else:
            # assume the default note is for 'service'
            curr_note = {"service": deepcopy(prev_note)}

        # now curr_note already is a dict
        # to keep consistency, the keys in note should be lower
        map(lambda x: str(x).lower(), note.keys())
        curr_note.update(note)

        # convert the dict to a unique string
        # e.g., "'other': 'test', 'temperature': '10.2', 'service': 'hpc'"
        #kvpair_list = ", ".join([": ".join(map(lambda x: "'".join(["", str(x), ""]), [key, prev_note[key]])) for key in sorted(prev_note.keys())])
        #snote = "".join(['{', kvpair_list, '}'])
        #sshnote = '"'.join(["", snote, ""])

        # try get the dict string with json dumps
        sshnote = json.dumps(curr_note)

        # update the note attribute in memory to real node
        command = " ".join(["pbsnodes -N", sshnote, node_label])
        str_ssh = "@".join([self.username, self.hostname])
        log.debug("pbs_note_builder: command ready to execute is: \n  > ssh {0} {1}\n".format(
            str_ssh, command))

        # This operation NEED authorization ...
        #ssh(str_ssh, command)

    # set server's temperature
    # a shortcut of set_note
    def set_temperature_note(self, node, temp):
        self.set_one_note(node, "temperature", temp)

    # set server's service type
    # a shortcut of set_note
    def set_service_note(self, node, service):
        self.set_one_note(node, "service", service)

    def set_one_note(self, node, attr, value):
        self.set_note(node, {attr: value})

# test only
if __name__ == "__main__":
    # only used for test
    username = "change me"
    hostname = "change me"
    pbsnote = pbs_note_builder(username, "india")
    try:
        pbsnote.get_note(hostname)
        # test temperature
        pbsnote.set_temperature_note(hostname, 99.2)
        # test service type
        pbsnote.set_service_note(hostname, "down")
        # test setNote
        note = {"service": "down, offline",
                "temperature": "-100.12", "test": "debug", 0: 12}
        pbsnote.set_note(hostname, note)
    except NameError, ne:
        print "My exception info: "
        print str(ne)

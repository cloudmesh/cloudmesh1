import os
import sh
import json

class ssh_config(object):

    def __init__(self, filename=None):
        if filename is not None:
            #load
            pass
        else:
            filename = "~/.ssh/config"

        self.filename = os.path.expanduser(filename)
        self.load()
        
    def load(self):
        """list the hosts defined in the ssh config file"""
        with open(self.filename) as f:
            content = f.readlines()
        content = [" ".join(x.split()) .strip('\n').lstrip().split(' ', 1) for x in content] 
        # removes duplicated spaces, and splits in two fields, removes leading spaces
        hosts = {}
        host = "NA"
        for line in content:
            if line[0].startswith('#') or line[0] is '':
                pass # ignore line
            else:
                attribute = line[0]
                value = line[1]
                if attribute in ['Host']:
                    host = value
                    hosts[host] = {'host': host}
                else:
                    hosts[host][attribute] = value
                    pass
        self.hosts = hosts

    def list(self):
        return self.hosts.keys()

    def __str__(self):
        return json.dumps(self.hosts, indent=4)
        
    def status(self):
        """executes a test with the given ssh config if a login is possible"""

if __name__ == "__main__":
    config = ssh_config()
    print config.list()
    print config    


class ClusterExistsError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Clusters(object):

    def __init__(self):
        self.config = cm_config()
        self.mongodb = cm_mongo()
        self.user = self.config.username()
        pass

    def defaults(self, default_dict):
        """setes image, cloud, flavor, key, username, ..."""
        pass

    def list(self):
        """ returns the list of the clusters in json format. This includes the status"""
        return None

    def vms(self, name):
        """returns in json the information about the vms of the named cluster"""
        return None

    def ips(self, name):
        """returns a list of ips belonging to the named cluster"""
        return None
    
    def names(self, name):
        """returns a lsit of names of the vms belonging to the cluster"""
        return None
    
    def group(self, name):
        """returns the group belonging to the cluster"""
        return None
                
    def delete(self, name):
        """deletes the named cluster"""
        
    def info(self, name):
        """returns a simplified information about the cluster in json format"""
        """each vm contains the ips and the name, as well as the status of the vm"""
        return None
    
    def create(self, name, n):
        """creates a cluster with the given name and the number of vms.
        If the cluster exists an exception is thrown. Returns the json of the cluster."""

        # raise ClusterExistsError('Cluster ' + name + ' exists')
        
                

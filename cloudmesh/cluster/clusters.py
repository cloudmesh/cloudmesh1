from cloudmesh.experiment.group import GroupManagement

class ClusterExistsError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Clusters(object):

    def __init__(self):
        self.config = cm_config()
        self.mongodb = cm_mongo()
        self.username = self.config.username()
        pass

    def defaults(self, default_dict):
        """setes image, cloud, flavor, key, username, ...
        
        TODO:: cloud select
               cloud on
               key default
               label
               default image
               default flavor
        """
        pass

    def list(self):
        """ returns the list of the clusters in json format. This includes the status"""
        return None

    def vms(self, name):
        """
        returns in json the information about the vms of the named cluster
        
        TODO:: vm list --group=name --format=json
        """
        return None

    def ips(self, name):
        """
        returns a list of ips belonging to the named cluster
        
        TODO:: vm ip show --group=name --format=json
        """
        return None
    
    def names(self, name):
        """
        returns a lsit of names of the vms belonging to the cluster
        
        TODO:: group show name vm --format=json
        """
        return None
    
    def group(self, name):
        """
        returns the group belonging to the cluster
        
        return a list of group names
        """
        GroupManage = GroupManagement(self.username)
        groups = GroupManage.get_groups()
        res = []
        for group in groups:
            if "cluster" in group.tags:
                res.append(group.name)
        return res
                
    def delete(self, name):
        """
        deletes the named cluster
        
        TODO:: vm delete --group=name --force
               maybe delete the group too: group remove name
        """
        
    def info(self, name):
        """returns a simplified information about the cluster in json format"""
        """each vm contains the ips and the name, as well as the status of the vm"""
        return None
    
    def create(self, name, n):
        """creates a cluster with the given name and the number of vms.
        If the cluster exists an exception is thrown. Returns the json of the cluster."""

        # raise ClusterExistsError('Cluster ' + name + ' exists')
        
                

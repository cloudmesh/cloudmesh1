from cloudmesh.experiment.group import GroupManagement
from cloudmesh.config.cm_config import cm_config
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh import banner
import time

from pprint import pprint


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
        self.GroupManage = GroupManagement(self.username)
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

    def list_clusters(self):
        """ returns the list of the clusters in json format. This includes the status"""
        groups = self.GroupManage.get_groups()
        res = {}
        for group in groups:
            if self.check_group_is_a_cluster(group):
                res[group.name] = {}
                vms_info = self.vms(group.name)[group.name]
                res[group.name]['num_of_nodes'] = len(vms_info)
                num_of_active_nodes = 0
                for key, value in vms_info.iteritems():
                    if 'status' in value and value['status'].upper() == 'ACTIVE':
                        num_of_active_nodes = num_of_active_nodes + 1
                res[group.name]['num_of_active_nodes'] = num_of_active_nodes

        return res

    def group(self, name):
        """
        returns the group belonging to the cluster according to cluster name
        TODO:: this is similar as function vms
        """
        return None

    def ips(self, name):
        """
        returns a list of ips belonging to the named cluster
        """
        return None

    def names(self, name):
        """
        returns a lsit of names of the vms belonging to the cluster
        
        TODO:: group show name vm --format=json
        """
        return None

    def vms(self, name, refresh=True):
        """
        returns in json the information about the vms of the named cluster
        this includes cluster name and its detailed VMs information
        """
        group_ = self.GroupManage.get_groups(groupname=name)
        if self.check_group_is_a_cluster(group_):
            VM_name_list = self.GroupManage.list_items_of_group(
                name,
                _type="VM")["VM"]
            if refresh:
                self.mongodb.activate(cm_user_id=self.username)
                self.mongodb.refresh(cm_user_id=self.username, types=['servers'])

            VM_dict = self.mongodb.servers(cm_user_id=self.username)
            res = {}
            res[name] = {}
            for cloud, value_0 in VM_dict.iteritems():
                for id_, value_1 in value_0.iteritems():
                    if value_1['name'] in VM_name_list:
                        res[name][value_1['name']] = value_1
                        if '_id' in res[name][value_1['name']]:
                            del res[name][value_1['name']]['_id']
            return res
        else:
            raise Exception("group '{0}' is not a cluster group".format(name))

    def delete(self, name, grouponly=False):
        """
        deletes the named cluster
        
        ::param grouponly: in default, when deleting a cluster, the group object along
                           with its VMs will be deleted, if grouponly=True, then the 
                           VMs will be preserved
        """
        from cloudmesh.experiment.group_usage import remove_vm_from_group_while_deleting

        vms = self.vms(name)[name]
        if not grouponly:
            clouds = []
            for vmname, value in vms.iteritems():
                cloudname = value['cm_cloud']
                id_ = value['id']
                banner("Deleting vm->{0} on cloud->{1}".format(vmname, cloudname))
                result = self.mongodb.vm_delete(cloudname, id_, self.username)
                print(result)
                if cloudname not in clouds:
                    clouds.append(cloudname)
                remove_vm_from_group_while_deleting(self.username, vmname)
            time.sleep(5)
            for cloud in clouds:
                self.mongodb.release_unused_public_ips(cloud, self.username)
            self.mongodb.refresh(cm_user_id=self.username, types=['servers'])
        banner("Deleting group->{0}".format(name))
        self.GroupManage.delete_group(name)

    def info(self, name):
        """returns a simplified information about the cluster in json format"""
        """each vm contains the ips and the name, as well as the status of the vm"""
        return None

    def create_with_existence_check(self, name, n):
        """
        creates a cluster with the given name and the number of vms.
        If the cluster exists an exception is thrown. Returns the json of the cluster.
        """
        pass
        # raise ClusterExistsError('Cluster ' + name + ' exists')

    def create(self, name, n):
        """
        creates a cluster with the given name and the number of vms.
        
        NOTICE: this function doesn't check the existence of a cluster(a 
        cluster us identified by group name), if the cluster already exists,
        this function will add number n VMs to the cluster instead of create 
        a new one
        """
        pass

    def check_group_is_a_cluster(self, groupobj):
        """
        a cluster group object shoud have a 'cluster' tag in its tags
        
        ::param groupobj: group object
        return True if a group contains the tag, otherwise return False
        """
        if "cluster" in groupobj.tags:
            return True
        else:
            return False


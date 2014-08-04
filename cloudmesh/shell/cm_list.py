from cloudmesh.config.cm_config import cm_config
from cloudmesh.iaas.cm_cloud import CloudManage
from cloudmesh_common.logger import LOGGER
from tabulate import tabulate




log = LOGGER(__file__)

def shell_command_list(arguments):
    """
    Usage:
        list flavor [CLOUD|--all] [--refresh]
        list server [CLOUD|--all] [--refresh]
        list image [CLOUD|--all] [--refresh]
        list project
        list cloud

    Arguments:

        CLOUD    the name of the cloud

    Options:

        -v         verbose mode
        --all      list information of all active clouds
        --refresh  refresh data before list

    Description:
        
        List clouds and projects information, if CLOUD argument is not given,
        default or selected cloud will be used, you may use command 'cloud select' 
        to select the cloud to work with.
    
        list flavor [CLOUD|--all] [--refresh]
            list the flavors
        list server [CLOUD|--all] [--refresh]
            list the vms
        list image [CLOUD|--all] [--refresh]
            list the images
        list project
            list the projects
        list cloud
            list active clouds
        
    """
    call = ListInfo(arguments)
    call.call_procedure()
    
    
class ListInfo(object):
    cloudmanage = CloudManage()
    try:
        config = cm_config()
    except:
        log.error("There is a problem with the configuration yaml files")
    
    username = config['cloudmesh']['profile']['username']
    
    def __init__(self, args):
        self.args = args
        
        
    def _list_flavor(self):
        clouds = self.get_working_cloud_name()
        if clouds:
            itemkeys = [
                         ['id', 'id'],
                         ['name', 'name'],
                         ['vcpus', 'vcpus'],
                         ['ram', 'ram'],
                         ['disk', 'disk'],
                         ['refresh time', 'cm_refresh']
                       ]
            if self.args['--refresh']:
                self.cloudmanage.mongo.activate(cm_user_id=self.username, names=clouds)
                self.cloudmanage.mongo.refresh(cm_user_id=self.username, names=clouds, types=['flavors'])
            for cloud in clouds:
                self.cloudmanage.print_cloud_flavors(username=self.username, cloudname=cloud.encode("ascii"), itemkeys=itemkeys, refresh=False, output=False)
        
        else:
            return
        
        
    def _list_image(self):
        clouds = self.get_working_cloud_name()
        if clouds:
            itemkeys = {"openstack":
                        [
                            # [ "Metadata", "metadata"],
                            [ "name" , "name"],
                            [ "status" , "status"],
                            [ "id", "id"],
                            [ "type_id" , "metadata", "instance_type_id"],
                            [ "iname" , "metadata", "instance_type_name"],
                            [ "location" , "metadata", "image_location"],
                            [ "state" , "metadata", "image_state"],
                            [ "updated" , "updated"],
                            #[ "minDisk" , "minDisk"],
                            [ "memory_mb" , "metadata", 'instance_type_memory_mb'],
                            [ "fid" , "metadata", "instance_type_flavorid"],
                            [ "vcpus" , "metadata", "instance_type_vcpus"],
                            #[ "user_id" , "metadata", "user_id"],
                            #[ "owner_id" , "metadata", "owner_id"],
                            #[ "gb" , "metadata", "instance_type_root_gb"],
                            #[ "arch", ""]
                        ],
                      "ec2":
                        [
                            # [ "Metadata", "metadata"],
                            [ "state" , "extra", "state"],
                            [ "name" , "name"],
                            [ "id" , "id"],
                            [ "public" , "extra", "is_public"],
                            [ "ownerid" , "extra", "owner_id"],
                            [ "imagetype" , "extra", "image_type"]
                        ],
                      "azure":
                        [
                            [ "name", "label"],
                            [ "category", "category"],
                            [ "id", "id"],
                            [ "size", "logical_size_in_gb" ],
                            [ "os", "os" ]
                        ],
                      "aws":
                        [
                            [ "state", "extra", "state"],
                            [ "name" , "name"],
                            [ "id" , "id"],
                            [ "public" , "extra", "ispublic"],
                            [ "ownerid" , "extra", "ownerid"],
                            [ "imagetype" , "extra", "imagetype"]
                        ]
                     }
            if self.args['--refresh']:
                self.cloudmanage.mongo.activate(cm_user_id=self.username, names=clouds)
                self.cloudmanage.mongo.refresh(cm_user_id=self.username, names=clouds, types=['images'])
            for cloud in clouds:
                self.cloudmanage.print_cloud_images(username=self.username, cloudname=cloud.encode("ascii"), itemkeys=itemkeys, refresh=False, output=False)
        
        else:
            return
        
        
    def _list_server(self):
        clouds = self.get_working_cloud_name()
        if clouds:
            itemkeys = {"openstack":
                      [
                          ['name','name'],
                          ['status','status'],
                          ['addresses','addresses'],
                          ['flavor', 'flavor','id'],
                          ['id','id'],
                          ['image','image','id'],
                          ['user_id', 'user_id'],
                          ['metadata','metadata'],
                          ['key_name','key_name'],
                          ['created','created'],
                      ],
                      "ec2":
                      [
                          ["name", "id"],
                          ["status", "extra", "status"],
                          ["addresses", "public_ips"],
                          ["flavor", "extra", "instance_type"],
                          ['id','id'],
                          ['image','extra', 'imageId'],
                          ["user_id", 'user_id'],
                          ["metadata", "metadata"],
                          ["key_name", "extra", "key_name"],
                          ["created", "extra", "launch_time"]
                      ],
                      "aws":
                      [
                          ["name", "name"],
                          ["status", "extra", "status"],
                          ["addresses", "public_ips"],
                          ["flavor", "extra", "instance_type"],
                          ['id','id'],
                          ['image','extra', 'image_id'],
                          ["user_id","user_id"],
                          ["metadata", "metadata"],
                          ["key_name", "extra", "key_name"],
                          ["created", "extra", "launch_time"]
                      ],
                      "azure":
                      [
                          ['name','name'],
                          ['status','status'],
                          ['addresses','vip'],
                          ['flavor', 'flavor','id'],
                          ['id','id'],
                          ['image','image','id'],
                          ['user_id', 'user_id'],
                          ['metadata','metadata'],
                          ['key_name','key_name'],
                          ['created','created'],
                      ]
                     }
            if self.args['--refresh']:
                self.cloudmanage.mongo.activate(cm_user_id=self.username, names=clouds)
                self.cloudmanage.mongo.refresh(cm_user_id=self.username, names=clouds, types=['servers'])
            for cloud in clouds:
                self.cloudmanage.print_cloud_servers(username=self.username, cloudname=cloud.encode("ascii"), itemkeys=itemkeys, refresh=False, output=False)
        
        else:
            return
        
        
    def _list_project(self):
        selected_project = None
        try:
            selected_project = self.cloudmanage.mongo.db_defaults.find_one({'cm_user_id': self.username})['project']
        except:
            log.error("clould not find selected project in the database")
        
        print tabulate([[selected_project]], ["selected project"], tablefmt="simple")
        print "\n"
        
        active_projects = None
        try:
            active_projects = self.cloudmanage.mongo.db_user.find_one({'cm_user_id': self.username})['projects']['active']
        except:
            log.error("clould not find active projects in the database")
        to_print = []
        if active_projects == None:
            to_print = [None]
        else:
            for project in active_projects:
                to_print.append([str(project)])
        print tabulate(to_print, ["active projects"], tablefmt="simple")
        print "\n"
        
        completed_projects = None
        try:
            completed_projects = self.cloudmanage.mongo.db_user.find_one({'cm_user_id': self.username})['projects']['completed']
        except:
            log.error("clould not find completed projects in the database")
        to_print = []
        if completed_projects == None:
            to_print = [None]
        else:
            for project in completed_projects:
                to_print.append([str(project)])
        print tabulate(to_print, ["completed projects"], tablefmt="simple")
        print "\n"
        
        
    def _list_cloud(self):
        active_clouds = []
        other_clouds = []
        activeclouds = self.cloudmanage.mongo.active_clouds(self.username)
        clouds = self.cloudmanage.get_clouds(self.username)
        clouds = clouds.sort([('cm_cloud', 1)])
        for cloud in clouds:
            name = cloud['cm_cloud']
            if name in activeclouds:
                active_clouds.append([str(name)])
            else:
                other_clouds.append([str(name)])
        if active_clouds == []: active_clouds = [None]
        if other_clouds == []: other_clouds = [None]
        print tabulate(active_clouds, ["active clouds"], tablefmt="simple")
        print "\n"
        print tabulate(other_clouds, ["other clouds"], tablefmt="simple")
        print "\n"
            
    
    # --------------------------------------------------------------------------
    def get_working_cloud_name(self):
        '''
        get the name of a cloud to be work on, if CLOUD not given, will pick the
        slected cloud, is --all, will return a list of active clouds
        '''
        activeclouds = None
        try:
            activeclouds = self.cloudmanage.mongo.active_clouds(self.username)
        except:
            pass
        if self.args['--all']:
            if activeclouds == None:
                print "no active cloud, please activate a cloud by 'cloud on [CLOUD]'"
                return False
            return activeclouds
        else:
            if self.args['CLOUD']:
                name = self.args['CLOUD']
            else:
                name = self.cloudmanage.get_selected_cloud(self.username)
            if self.cloudmanage.get_clouds(self.username, getone=True, cloudname=name) == None:
                log.error("no cloud information of '{0}' in database".format(name))
                return False
            if name not in activeclouds:
                log.error("cloud '{0} is active, please activate a cloud by 'cloud on [CLOUD]'".format(name))
                return False
            return [name]
        
        
    def call_procedure(self):
        if self.args['flavor'] == True:
            call = 'flavor'
        elif self.args['server'] == True:
            call = 'server'
        elif self.args['image'] == True:
            call = 'image'
        elif self.args['project'] == True:
            call = 'project'
        elif self.args['cloud'] == True:
            call = 'cloud'
        func = getattr(self, "_list_" + call)
        func()
        
        
        
        
        
        
        

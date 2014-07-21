from cloudmesh_common.tables import column_table
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from collections import OrderedDict
from pprint import pprint



def shell_command_list(arguments):
    """
    Usage:
        list flavor [CLOUD]
        list server [CLOUD]
        list image [CLOUD]
        list project
        list cloud
        list

    Arguments:

        CLOUD    the name of the cloud, input 'all' instead to show requested
                 information for all active clouds

    Options:

        -v       verbose mode

    Description:
        
        List clouds and projects information, if CLOUD argument is not given,
        default or selected cloud will be used, please use command 'cloud select' 
        to select the cloud to work with.([NOT IMPLEMENTED]for now, selected 
        cloud information is not in the mongo)
    
        list flavor [CLOUD]
            list the flavors
        list server [CLOUD]
            list the vms
        list image [CLOUD]
            list the images
        list project
            list the projects
        list cloud
            list active clouds
        
    """
    call = ListInfo(arguments)
    call.call_procedure()
    
    
class ListInfo(object):
    config = cm_config()
    mongo = cm_mongo()
    
    
    def __init__(self, args):
        self.args = args
        self.cloud = self.args['CLOUD'].lower()
        self.username = self.config.username()
        self.active_clouds = None
    

    def clouds_to_show(self):
        self.active_clouds = self.mongo.active_clouds(self.username)
        if self.active_clouds == []:
            print "ERROR: no active cloud"
            clouds = None
        else:
            if self.cloud == None:
                #- --------------------------------------------------------
                #bug: should select default cloud or selected cloud from db
                #- --------------------------------------------------------
                clouds = self.active_clouds[0]
            elif self.cloud == 'all':
                clouds = self.active_clouds
            else:
                if self.cloud not in self.active_clouds:
                    print "ERROR: cloud '{0}' is not activated".format(self.cloud)
                    clouds = None
                else:
                    clouds = self.cloud
        return clouds
                
    
    def _list_flavor(self):
        clouds = self.clouds_to_show()
        if clouds == None: return
        flavors_dict = self.mongo.flavors(clouds=clouds, cm_user_id=self.username)
        pprint(flavors_dict)
        
    
    def _list_server(self):
        clouds = self.clouds_to_show()
        if clouds == None: return
        servers_dict = self.mongo.servers(cm_user_id=username, clouds=clouds)
        pprint(servers_dict)

    
    def _list_image(self):
        clouds = self.clouds_to_show()
        if clouds == None: return
        images_dict = self.mongo.images(cm_user_id=username, clouds=clouds)
        pprint(images_dict)
    
    def _list_project(self):
        projects = self.mongo.active_project(self.username)
        col = OrderedDict([('active projects', projects)])
        print column_table(col)
        count = len(projects)
        print "count: {0}".format(count)
    
    def _list_cloud(self):
        self.active_clouds = self.mongo.active_clouds(self.username)
        col = OrderedDict([('active clouds', self.active_clouds)])
        print column_table(col)
        count = len(self.active_clouds)
        print "count: {0}".format(count)
    
    
    
    
    def call_procedure(self):
        cmds = self.get_commands()
        vals = cmds.values()
        if True not in vals:
            self._list_cloud()
        else:
            for cmd, tof in cmds.iteritems():
                if tof:
                    func = getattr(self, "_list_" + cmd)
                    func()
                    break

    def get_commands(self):
        '''Return commands only except options start with '--' from docopt
        arguments
        
        Example:
            get_commands({"info": True, "--count":None})
            returns
            {"info": True} 
        '''
        args = self.args
        result = {}
        for k,v in args.iteritems():
            if k.startswith('--'):
                continue
            result[k] = v
        return result
    

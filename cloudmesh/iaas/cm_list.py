from cloudmesh_common.tables import column_table
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from collections import OrderedDict
from pprint import pprint
from tabulate import tabulate



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
        self.cloud = self.args['CLOUD']
        if self.cloud != None: self.cloud = self.cloud.lower()
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
                clouds = [self.active_clouds[0]]
            elif self.cloud == 'all':
                clouds = self.active_clouds
            else:
                if self.cloud not in self.active_clouds:
                    print "ERROR: cloud '{0}' is not activated".format(self.cloud)
                    clouds = None
                else:
                    clouds = [self.cloud]
        return clouds
                
    
    def _list_flavor(self):
        clouds = self.clouds_to_show()
        if clouds == None: return
        flavors_dict = self.mongo.flavors(clouds=clouds, cm_user_id=self.username)
        #pprint(flavors_dict)
        your_keys = [
                     'id',
                     'name',
                     'vcpus',
                     'ram',
                     'disk',
                     'cm_refresh',
                     ]
        
        def _select_flavors(data, keys):
            res = [keys]
            for key, item in data.iteritems():
                values = []
                for name in keys:
                    try:
                        values.append(item[name])
                    except:
                        values.append(' ')
                res.append(values)
            return res
                
        for key, item in flavors_dict.iteritems():
            count = len(item)
            ls = _select_flavors(item, your_keys)
            sentence =  "flavors of cloud '{0}'".format(key)
            print "+"+"-"*(len(sentence)-2)+"+"
            print sentence
            _display(ls)
            print "count: {0}\n".format(count)
            
    
    def _list_server(self):
        clouds = self.clouds_to_show()
        if clouds == None: return
        servers_dict = self.mongo.servers(cm_user_id=self.username, clouds=clouds)
        your_keys = {"openstack":
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
        
        for key, item in servers_dict.iteritems():
            count = len(item)
            ls = _select_items(item, your_keys)
            sentence =  "vms of cloud '{0}'".format(key)
            print "+"+"-"*(len(sentence)-2)+"+"
            print sentence
            _display(ls)
            print "count: {0}\n".format(count)

    
    def _list_image(self):
        clouds = self.clouds_to_show()
        if clouds == None: return
        images_dict = self.mongo.images(cm_user_id=self.username, clouds=clouds)
        #pprint(images_dict)
        your_keys = {"openstack":
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
                            [ "minDisk" , "minDisk"],
                            [ "memory_mb" , "metadata", 'instance_type_memory_mb'],
                            [ "fid" , "metadata", "instance_type_flavorid"],
                            [ "vcpus" , "metadata", "instance_type_vcpus"],
                            [ "user_id" , "metadata", "user_id"],
                            [ "owner_id" , "metadata", "owner_id"],
                            [ "gb" , "metadata", "instance_type_root_gb"],
                            [ "arch", ""]
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
        
        for key, item in images_dict.iteritems():
            count = len(item)
            ls = _select_items(item, your_keys)
            sentence =  "images of cloud '{0}'".format(key)
            print "+"+"-"*(len(sentence)-2)+"+"
            print sentence
            _display(ls)
            print "count: {0}\n".format(count)
        
    
    def _list_project(self):
        # --------------------------------
        # bug: should list all projects
        # --------------------------------
        project = [self.mongo.active_project(self.username)]
        col = OrderedDict([('selected project', project)])
        print column_table(col)
        #count = len(project)
        #print "count: {0}".format(count)
    
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
                if tof == True:
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
    
    
    
def _display(json_data, headers="firstrow", tablefmt="orgtbl"):
    table = tabulate(json_data, headers, tablefmt)
    try:
        separator = table.split("\n")[1].replace("|", "+")
    except:
        separator = "-" * 50
    print separator
    print table
    print separator
    

def _select_items(data, selected_keys):
    res = []
    keys = []
        
    def _getFromDict(dataDict, mapList):
        '''Get values of dataDict by mapList
        mapList is a list of keys to find values in dict.
        dataDict is a nested dict and will be searched by the list.
        
        e.g.  Access to the value 5 in dataDict
        
        dataDict = { "abc": {
                        "def": 5 
                        } 
                    }
        mapList = [ "abc", "def" ]
        
        _getFromDict(dataDict, mapList) returns 5
        
        ref: http://stackoverflow.com/questions/14692690/access-python-nested-dictionary-items-via-a-list-of-keys
        '''
        return reduce(lambda d, k: d[k], mapList, dataDict)
            
    for i, v in data.iteritems():
        values = []
        # cm_type is required to use a selected_keys for the cm_type
        cm_type = v['cm_type']
        for k in selected_keys[cm_type]:
            keys.append(k[0])
            try:
                values.append(str(_getFromDict(v, k[1:])))
            except:
                #print sys.exc_info()
                values.append(None)
        res.append(values)
    headers = [keys]
    return headers + res
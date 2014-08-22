from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.user.cm_user import cm_user
from cloudmesh_common.logger import LOGGER
from cloudmesh.iaas.cm_cloud import CloudManage
from cloudmesh.config.cm_config import cm_config
from pprint import pprint
from cloudmesh_common.util import banner
from cloudmesh_common.bootstrap_util import yn_choice

log = LOGGER(__file__)

def shell_command_vm(arguments):
    """
        ::
        
            Usage:
                vm start [NAME]
                         [--count=<count>]
                         [--cloud=<CloudName>]
                         [--image=<imgName>|--imageid=<imgId>]
                         [--flavor=<flavorName>|--flavorid=<flavorId>]
                         [--group=<group>]                    
                vm delete [NAME|--id=<id>]
                          [--group=<group>]
                          [--cloud=<CloudName>]
                          [--prefix=<prefix>] 
                          [--range=<range>]
                                    
            Arguments:
            
            Options:
            
            Description:
            
            Examples:   
                          
    """
    
    call = VMcommand(arguments)
    call.call_procedure()
    
  

    
class VMcommand(object):
    try:
        config = cm_config()
    except:
        log.error("There is a problem with the configuration yaml files")
        
    username = config['cloudmesh']['profile']['username']
    
    
    def __init__(self, arguments):
        self.arguments = arguments
        print self.arguments ########
    
    def _vm_create(self):
        # ------------------------- 
        # check input
        count = 1
        if self.arguments['--count']:
            try:
                count = int(self.arguments['--count'])
            except:
                log.warning("ERROR: --count must be assigned with an integer")
                return
            if count < 1:
                log.warning("ERROR: --count must be assigned with an integer greater than 0")
                return
            import time
            watch = time.time()
        # ------------------------- 
        # select cloud
        cloudobj = CloudManage()
        if self.arguments['--cloud']:
            cloud = cloudobj.get_clouds(self.username, getone=True, cloudname=self.arguments['--cloud'])
            if cloud == None:
                print "ERROR: could not find cloud '{0}'".format(self.arguments['--cloud'])
                return
            else:
                cloudname = self.arguments['--cloud']
        else:
            cloudname = cloudobj.get_selected_cloud(self.username)
        # ------------------------- 
        # starting vm
        start_vm(self.username, 
                 cloudname,
                 count=count,
                 flavorname=self.arguments['--flavor'], 
                 flavorid=self.arguments['--flavorid'], 
                 imagename=self.arguments['--image'],
                 imageid=self.arguments['--imageid'],
                 groupname=self.arguments['--group'],
                 servername=self.arguments['NAME'])
        # ------------------------- 
       
        if self.arguments['--count']:
            watch = time.time() - watch
            print ("time consumed: %.2f" % watch), "s"
            
        print "to check realtime vm status: list vm --refresh"

        
        
    def _vm_delete(self):
        # ------------------------- 
        # check input
        if self.arguments['NAME'] == None and\
           self.arguments['--id'] == None and\
           self.arguments['--group'] == None and\
           self.arguments['--cloud'] == None and\
           self.arguments['--prefix'] == None and\
           self.arguments['--range'] == None:
            print "Please specify at least one option, to get more information: vm help"
            return
        
        rangestart = None
        rangeend = None
        if self.arguments['--range']:
            ranges = [x.strip() for x in self.arguments["--range"].split(',')]
            error = False
            if len(ranges) != 2:
                error = True
            else:
                try:
                    if ranges[0] != '':
                        rangestart = int(ranges[0])
                    if ranges[1] != '':
                        rangeend = int(ranges[1])
                except:
                    error = True
            if error:
                print "ERROR: range option must be given as --range=int,int, for example:\
                       --range=1,3"
                return
            if rangestart and rangeend:
                if rangestart > rangeend:
                    print "ERROR: first number of range must be no greater than the second one,\
                          for example: --range=1,3"
                    return
        # ------------------------- 
        # select cloud
        deleteAllCloudVMs = False
        cloudobj = CloudManage()
        if self.arguments['--cloud']:
            cloud = cloudobj.get_clouds(self.username, getone=True, cloudname=self.arguments['--cloud'])
            if cloud == None:
                print "ERROR: could not find cloud '{0}'".format(self.arguments['--cloud'])
                return
            else:
                cloudname = self.arguments['--cloud']
                deleteAllCloudVMs = True
        else:
            cloudname = cloudobj.get_selected_cloud(self.username)
        # ------------------------- 
        delete_vm(self.username,
                  cloudname,
                  servername=self.arguments['NAME'],
                  serverid=self.arguments['--id'],
                  groupname=self.arguments['--group'],
                  prefix=self.arguments['--prefix'],
                  rangestart=rangestart,
                  rangeend=rangeend,
                  deleteAllCloudVMs=deleteAllCloudVMs,
                  preview=True)
        
    
    # --------------------------------------------------------------------------
    def call_procedure(self):
        if self.arguments['start'] == True:
            call = 'create'
        elif self.arguments['delete'] == True:
            call = 'delete'
            
        func = getattr(self, "_vm_" + call)
        func()
    # --------------------------------------------------------------------------
        
# ------------------------------------------------------------------------
# supporting functions 
# ------------------------------------------------------------------------
  
def start_vm(username, 
             cloudname, 
             count=1,
             flavorname=None, 
             flavorid=None, 
             imagename=None,
             imageid=None,
             groupname=None,
             servername=None):
    '''
    create a vm of a cloud of a user
    will check flavor, image existence if provided
    user can specify groupname which will be written in metadata, servername which 
    will replace prefix+index as the vm name
    :param username: string
    :param cloudname: string
    :param count: number of vms to start
    :return 
    
    TODO: what if fail, how to acknowledge it; no return now as using celery
          input key 
          missing security group
    '''

    mongo = cm_mongo()
    userobj = cm_user()
    cloudobj = CloudManage()
    mongo.activate(cm_user_id = username, names=[cloudname])
    userinfo = userobj.info(username)
    key = None
    vm_image_id = None
    vm_flavor_id = None
    
    error = ''
        
    # ------------------------- 
    # refresh flavor or image
    to_refresh = []

    if flavorname != None or flavorid != None:
        to_refresh.append("flavors")
    if imagename != None or imageid != None:
        to_refresh.append("images")
    if to_refresh != []:
        mongo.refresh(username, names=[cloudname], types=to_refresh)
    
    # -------------------------
    # flavor handler
    if flavorname != None or flavorid != None:
        flavordata = mongo.flavors(clouds=[cloudname], cm_user_id=username)[cloudname]
        same_name_count = 0
        for k, v in flavordata.iteritems():
            if flavorname != None:
                if flavorname == v['name']:
                    vm_flavor_id = k
                    same_name_count = same_name_count + 1
            else:
                if flavorid == k:
                    vm_flavor_id = k
                    break
        if vm_flavor_id == None:
            error = error + "The flavor you provide doesn't exist. "
        if same_name_count > 1:
            error = error + "There are more than one flavor with the name you provide \
                            please use flavorid instead or select one by command cloud \
                            set flavor [CLOUD]. "
    else:
        try:
            vm_flavor_id = userinfo["defaults"]["flavors"][cloudname]
        except:
            error = error + "Please specify a default flavor(command: cloud set flavor [CLOUD]). "
    
        if vm_flavor_id in [None, 'none']:
            error = error + "Please specify a default flavor(command: cloud set flavor [CLOUD]). "
    # -------------------------
    # image handler
    if imagename != None or imageid != None:
        imagedata = mongo.images(clouds=[cloudname], cm_user_id=username)[cloudname]
        same_name_count = 0
        for k, v in imagedata.iteritems():
            if imagename != None:
                if imagename == v['name']:
                    vm_image_id = k
                    same_name_count = same_name_count + 1
            else:
                if imageid == k:
                    vm_image_id = k
                    break
        if vm_image_id == None:
            error = error + "The image you provide doesn't exist. "
        if same_name_count > 1:
            error = error + "There are more than one image with the name you provide \
                            please use imageid instead or select one by command cloud \
                            set image [CLOUD]. "
    else:
        try:
            vm_image_id = userinfo["defaults"]["images"][cloudname]
        except:
            error = error + "Please specify a default image. "
        
        if vm_image_id in [None, 'none']:
            error = error + "Please specify a default image. "
    
    # -------------------------
    # key handler
    if "key" in userinfo["defaults"]:
        key = userinfo["defaults"]["key"]
    elif len(userinfo["keys"]["keylist"].keys()) > 0:
        key = userinfo["keys"]["keylist"].keys()[0]
        
    if key:
        keycontent = userinfo["keys"]["keylist"][key]
        if keycontent.startswith('key '):
            keycontent = keycontent[4:]
        check_register_key(username, cloudname, key, keycontent)
        keynamenew = _keyname_sanitation(username, key)
    else:
        error = error + "No sshkey found. Please <a href='https://portal.futuregrid.org/my/ssh-keys'>Upload one</a>"
    # -------------------------
    
    if error != '':
        log.error(error)
        return False
    # -------------------------
    metadata = {'cm_owner': username}
    if groupname:
        metadata['cm_group'] = groupname
    
    tmpnamefl = cloudobj.get_flavors(cloudname=cloudname, getone=True, id=vm_flavor_id)['name']
    tmpnameim = cloudobj.get_images(cloudname=cloudname, getone=True, id=vm_image_id)['name']
    
    while count > 0:
        userinfo = userobj.info(username)
        if servername:
            prefix = ''
            index = ''
            givenvmname = servername
            tmpnameser = servername
        else:
            prefix = userinfo["defaults"]["prefix"]
            index = userinfo["defaults"]["index"]
            givenvmname = None
            tmpnameser = prefix+'_'+str(index)
        # ------------------------
        # vm start procedure
        
        banner("Starting vm->{0} on cloud->{1} using image->{2}, flavor->{3}, key->{4}"\
               .format(tmpnameser, cloudname, tmpnamefl, tmpnameim, keynamenew))
        #result = mongo.vm_create(
        #using celery, to disable, call vm_create
        result = mongo.vm_create_queue(
            cloudname,
            prefix,
            index,
            vm_flavor_id,
            vm_image_id,
            keynamenew,
            meta=metadata,
            cm_user_id=username,
            givenvmname=givenvmname)
        # ------------------------
        # increase index if it is used
        if not servername:
            userobj.set_default_attribute(username, "index", int(index) + 1)
        # ------------------------
        
        #pprint(result) 
        #print result.failed()
        print "job status:", result.state
        #print result.traceback
        count = count - 1
    
    
    
def delete_vm(username,
              cloudname,
              servername=None,
              serverid=None,
              groupname=None,
              prefix=None,
              rangestart=None,
              rangeend=None,
              deleteAllCloudVMs=False,
              preview=False):
    '''
    delete vms of a cloud of a user, this function provides several ways to find and 
    delete vms
    :param deleteAllCloudVMs: True to enable condition that find all vms of the cloud
    :param preview: True if the user wants to preview and confirm before start to delete
    
    TODO: what if fail, how to acknowledge it
          range search: now if prefix not given, all vms whose index are in the range will
          be deleted, regardless of its prefix
    '''
    # -------------------------
    # simple input check
    if servername and serverid:
        print "ERROR: server name and server id can't be both provided"
        return False
    if rangestart and rangeend:
        if rangestart > rangeend:
            print "ERROR: rangestart > rangeend"
            return False
    # -------------------------
    mongo = cm_mongo()
    mongo.activate(cm_user_id = username, names=[cloudname])
    mongo.refresh(username, names=[cloudname], types=['servers'])
    serverdata = mongo.servers(clouds=[cloudname], cm_user_id=username)[cloudname]
    #pprint(serverdata)  ##########
    # -------------------------
    # search for qualified vms for each critera
    ls =[
           [], #0 servername
           [], #1 serverid
           [], #2 groupname
           [], #3 prefix
           [], #4 rangestart
           [], #5 rangeend
           []  #6 deleteAllCloudVMs
        ]
    for k, v in serverdata.iteritems():
        if servername:
            if servername == v['name']:
                ls[0].append(k)
        if serverid:
            if serverid == k:
                ls[1].append(k)
        if groupname:
            grouptemp = None
            try:
                grouptemp = v['metadata']['cm_group']
            except:
                pass
            if groupname == grouptemp:
                ls[2].append(k)
        if prefix or rangestart or rangeend:
            nametemp = server_name_analyzer(v['name'])
        if prefix:
            if prefix == nametemp[0]:
                ls[3].append(k)
        if rangestart:
            if nametemp[1]:
                if rangestart <= nametemp[1]:
                    ls[4].append(k)
        if rangeend:
            if nametemp[1]:
                if rangeend >= nametemp[1]:
                    ls[5].append(k)  
        if deleteAllCloudVMs:
            if v['cm_cloud'] == cloudname:
                ls[6].append(k)
    # -------------------------
    # intersect the results
    ls = [x for x in ls if x != []]
    l = len(ls)
    if l == 0:
        res = []
    elif l == 1:
        res = ls[0]
    else:
        res = ls[0]
        del ls[0]
        for i in ls:
            res = set(res)&set(i)
        res = list(res)
    # -------------------------
    # preview and confirm
    confirm_deletion = True
    if preview:
        if res == []:
            print "no vm meets the condition"
        else:
            resserverdata = {}
            for i in res:
                resserverdata[i] = serverdata[i]
            cloudobj = CloudManage()
            itemkeys = {"openstack":
                      [
                          ['name','name'],
                          ['status','status'],
                          ['addresses','addresses'],
                          ['id','id'],
                          ['flavor', 'flavor','id'],
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
            cloudobj.print_cloud_servers(username=username,
                                         cloudname=cloudname,
                                         itemkeys=itemkeys,
                                         refresh=False,
                                         output=False,
                                         serverdata=resserverdata)
            if yn_choice("confirm to delete these vms?", default = 'n', tries = 3):
                pass
            else:
                confirm_deletion = False
                
    # -------------------------
    # deleting
    if confirm_deletion:
        if res == []:
            return
        else:
            for i in res:
                tempservername = serverdata[i]['name'].encode("ascii")
                banner("Deleting vm->{0} on cloud->{1}".format(tempservername, cloudname))
                result = mongo.vm_delete(cloudname, i, username)
                pprint(result) 
            mongo.release_unused_public_ips(cloudname, username)
            mongo.refresh(username, names=[cloudname], types=['servers'])
            

    
# ========================================================================   
def _keyname_sanitation(username, keyname):
    keynamenew = "%s_%s" % (username, keyname.replace('.', '_').replace('@', '_'))
    return keynamenew


def check_register_key(username, cloudname, keyname, keycontent):
    mongo = cm_mongo()
    mongo.activate(cm_user_id=username, names=[cloudname])
    cloudmanager = mongo.clouds[username][cloudname]['manager']
    
    keynamenew = _keyname_sanitation(username, keyname)
    keysRegistered = cloudmanager.keypair_list()
    registered = False
    # Openstack & Eucalyptus
    if 'keypairs' in keysRegistered:
        keypairsRegistered = keysRegistered["keypairs"]
        for akeypair in keypairsRegistered:
            if keynamenew == akeypair['keypair']['name']:
                registered = True
                break
    else:
        if keynamenew in keysRegistered:
            registered = True
    
    if not registered:
        cloudmanager.keypair_add(keynamenew, keycontent)
        log.info("Automatically registered the default key <%s> for user <%s>" % (keyname, username))


def server_name_analyzer(name):
    '''
    standard vm name, unless user gives the name, is prefix_index such as abc_11, this
    function returns vm name's prefix and index [prefix, index], if the name is not in 
    standard form, returns [input, None]
    '''
    res = [x for x in name.split('_')]
    l = len(res)
    if l == 1:
        return [name, None]
    
    index = None
    try:
        index = int(res[-1])
    except:
        pass
    if index == None:
        return [name, None]
    
    prefix = None
    if l > 2:
        del res[-1]
        prefix = "_".join(res)
    else:
        prefix = res[0]
        return [prefix, index]



# ========================================================================

# ------------------------------------------------------------------------


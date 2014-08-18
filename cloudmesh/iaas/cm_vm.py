from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.user.cm_user import cm_user
from cloudmesh_common.logger import LOGGER
from cloudmesh.iaas.cm_cloud import CloudManage
from cloudmesh.config.cm_config import cm_config
from pprint import pprint
from cloudmesh_common.util import banner

log = LOGGER(__file__)

def shell_command_vm(arguments):
    """
        ::
        
            Usage:
                vm start [NAME|--count=<count>]
                         [--cloud=<CloudName>]
                         [--image=<imgName>|--imageid=<imgId>]
                         [--flavor=<flavorName>|--flavorid=<flavorId>]
                         [--group=<group>]
                vm delete NAME
                vm delete --group=<group>
                vm delete --cloud=<CloudName>
                vm delete --range=<range>
                vm list [CLOUD|--all]
                       
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
        print self.arguments
    
    def _vm_create(self):
        # ------------------------- 
        # check input
        if self.arguments['--count']:
            count = None
            try:
                count = int(self.arguments['--count'])
            except:
                log.warning("ERROR: --count must be assigned with an integer")
                return
            if count < 1:
                log.warning("ERROR: --count must be assigned with an integer greater than 0")
                return
        # ------------------------- 
        # select cloud
        cloudobj = CloudManage()
        if self.arguments['--cloud']:
            cloud = cloudobj.get_clouds(self.username, getone=True, cloudname=self.arguments['--cloud'])
            if cloud == None:
                log.warning("ERROR: could not find cloud '{0}'".format(self.arguments['--cloud']))
                return
            else:
                cloudname = self.arguments['--cloud']
        else:
            cloudname = cloudobj.get_selected_cloud(self.username)
        # ------------------------- 
        # starting vm
        start_vm(self.username, 
                 cloudname,
                 refresh=True,
                 flavorname=self.arguments['--flavor'], 
                 flavorid=self.arguments['--flavorid'], 
                 imagename=self.arguments['--image'],
                 imageid=self.arguments['--imageid'],
                 groupname=self.arguments['--group'],
                 servername=self.arguments['NAME'])
        # ------------------------- 
        # starting mutiple vms
        if self.arguments['--count'] and count > 1:
            while count > 1:
                start_vm(self.username, 
                         cloudname,
                         refresh=False,
                         flavorname=self.arguments['--flavor'], 
                         flavorid=self.arguments['--flavorid'], 
                         imagename=self.arguments['--image'],
                         imageid=self.arguments['--imageid'],
                         groupname=self.arguments['--group'],
                         servername=None)
                count = count - 1
        
        
        
        
    def _vm_delete(self):
        pass
    
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
             refresh=True,
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
    :param refresh: boolean, designed for starting more than one vm on a cloud, avoid
    unnescessary refresh
    :return 
    
    TODO: what if fail, how to acknowledge it;
          input key 
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
    # refresh flavor or image if needed
    to_refresh = []
    if refresh:
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
    tmpnamefl = cloudobj.get_flavors(cloudname=cloudname, getone=True, id=vm_flavor_id)['name']
    tmpnameim = cloudobj.get_images(cloudname=cloudname, getone=True, id=vm_image_id)['name']
    banner("Starting vm->{0} on cloud->{1} using image->{2}, flavor->{3}, key->{4}"\
           .format(tmpnameser, cloudname, tmpnamefl, tmpnameim, keynamenew))
    result = mongo.vm_create(
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
    
    #pprint(result) #################
    
    
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
# ========================================================================

# ------------------------------------------------------------------------


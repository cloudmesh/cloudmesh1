from cloudmesh_common.logger import LOGGER
from cloudmesh.config.cm_config import cm_config
from cloudmesh.cm_mongo import cm_mongo
from tabulate import tabulate
from cloudmesh_common.util import banner, dict_uni_to_ascii
from pprint import pprint
from cloudmesh.util.menu import menu_return_num
from cloudmesh_common.bootstrap_util import yn_choice
import sys

log = LOGGER(__file__)

def shell_command_cloud(arguments):
    """
        ::

            Usage:
                cloud
                cloud list [--column=COLUMN]
                cloud info [CLOUD|--all]
                cloud alias <name> [CLOUD]
                cloud select [CLOUD]
                cloud on [CLOUD]
                cloud off [CLOUD]
                cloud add CLOUDFILE [--force]
                cloud remove [CLOUD]
                cloud default [CLOUD] [--flavorset|--imageset]
                cloud default --all

            Arguments:

              CLOUD          the name of a cloud to work on
              CLOUDFILE      a yaml file contains cloud information
              name           new cloud name to set

            Options:

               -v                verbose model
               --column=COLUMN   specify what information to display. For
                                 example, --column=active,label. Available
                                 columns are active, label, host, type/version,
                                 type, heading, user, credentials, defaults
                                 (all to diplay all, semiall to display all
                                 except credentials and defaults)
               --flavorset       set the default flavor of a cloud
               --imageset        set the image flavor of a cloud
               --all             provide information of all clouds
               --force           if same cloud exists in database, it will be 
                                 overwritten

            Description:
                the place to manage clouds

                cloud list [--column=COLUMN]
                    lists the stored clouds, optionally, specify columns for more
                    cloud information. For example, --column=active,label

                cloud info [CLOUD|--all]  
                    provides the available information about the cloud in dict format 
                    options: specify CLOUD to display it, --all to display all,
                             otherwise selected cloud will be used

                cloud alias <name> [CLOUD]
                    sets a new name for a cloud
                    options: specify CLOUD to work with, otherwise selected cloud 
                             will be used

                cloud select [CLOUD]
                    selects a cloud to work with from a list of clouds if CLOUD is
                    not given

                cloud on [CLOUD]
                cloud off [CLOUD]
                    activates or deactivates a cloud, if CLOUD is not given, 
                    selected cloud will be activated or deactivated

                cloud add CLOUDFILE [--force]
                    adds cloud information to database. CLOUDFILE is a yaml file with 
                    full file path. Inside the yaml, clouds should be written in the
                    form: 
                    cloudmesh: clouds: cloud1...
                                       cloud2...
                    please check ~/.futuregrid/cloudmesh.yaml
                    options: --force, by default, existing cloud in database can't be
                             overwirtten, enable --force to overwrite if same cloud 
                             name encountered

                cloud remove [CLOUD]
                    remove a cloud from mongo, if CLOUD is not given, selected cloud 
                    will be reomved.
                    CAUTION: remove all is enabled(remove all)
                    
                cloud default [CLOUD] [--flavorset|--imageset]
                cloud default --all
                    view or manage cloud's default flavor and image
                    options: CLOUD, specify a cloud to work on, otherwise selected 
                             cloud will be used, --all to display all clouds defaults
                             --setflavor, set default flaovr
                             --setimage, set default image

    """
    call = CloudCommand(arguments)
    call.call_procedure()
    
    
class CloudManage(object):
    try:
        config = cm_config()
    except:
        log.error("There is a problem with the configuration yaml files")
        
    try:
        mongo = cm_mongo()
    except:
        log.error("There is a problem with the mongo server")
    
    username = config['cloudmesh']['profile']['username']
    
    def get_clouds(self, username, admin=False, getone=False, cloudname=None):
        if getone:
            return self.mongo.db_clouds.find_one({'cm_kind': 'cloud', 'cm_user_id': username, 'cm_cloud': cloudname})
        if admin: 
            return self.mongo.db_clouds.find({'cm_kind': 'cloud'})
        else:
            return self.mongo.db_clouds.find({'cm_kind': 'cloud', 'cm_user_id': username})
        
    def get_selected_cloud(self, username):
        user = self.mongo.db_user.find_one({'cm_user_id': username})
        try:
            cloud = user['selected_cloud']
        except:
            defaults = self.mongo.db_defaults.find_one({'cm_user_id': username})
            try:
                cloud = defaults['cloud']
            except:
                log.warning("no selected cloud and no default cloud is setup, please use command 'cloud select [CLOUD]' to select a cloud")
                sys.exit()
            self.mongo.db_user.update({'cm_user_id': username}, {'$set': {'selected_cloud': cloud}})
        
        return cloud
    
    def update_selected_cloud(self, username, cloudname):
        self.mongo.db_user.update({'cm_user_id': username}, {'$set': {'selected_cloud': cloudname}})
    
    def update_default_cloud(self, username, cloudname):
        self.mongo.db_defaults.update({'cm_user_id': username}, {'$set': {'cloud': cloudname}})
    
    def update_cloud_name(self, username, cloudname, newname):
        '''
        change the cloud name in db
        before use this function, check whether cloud exists in db_clouds
        '''
        self.mongo.db_clouds.update({'cm_kind': 'cloud', 'cm_user_id': username, 'cm_cloud': cloudname}, {'$set': {'cm_cloud': newname}})
        try:
            if cloudname == self.mongo.db_user.find_one({'cm_user_id': username})['selected_cloud']:
                self.update_selected_cloud(username, newname)
        except:
            pass
        try:
            if cloudname == self.mongo.db_defaults.find_one({'cm_user_id': username})['cloud']:
                self.update_default_cloud(username, newname)
        except:
            pass    
        
    def activate_cloud(self, username, cloudname):
        '''
        activate a cloud 
        '''
        cloud = self.mongo.get_cloud(cm_user_id=username, cloud_name=cloudname, force=True)
        if cloud == None:
            return 0
        else: 
            defaults = self.mongo.db_defaults.find_one({'cm_user_id': username})
            if cloudname not in defaults['registered_clouds']:
                defaults['registered_clouds'].append(cloudname)
            if cloudname not in defaults['activeclouds']:
                defaults['activeclouds'].append(cloudname)
            self.mongo.db_defaults.update({'cm_user_id': username}, defaults, upsert=True)
            return 1
    
    def deactivate_cloud(self, username, cloudname):
        '''
        deactivate a cloud
        simply delete the cloud name from activecloud in db_defaults
        '''
        defaults = self.mongo.db_defaults.find_one({'cm_user_id': username})
        if cloudname in defaults['activeclouds']:
            defaults['activeclouds'].remove(cloudname)
        self.mongo.db_defaults.update({'cm_user_id': username}, defaults, upsert=True)
        
    #########doubt######################
    def add(self, d):
        if d['cm_type'] in ['openstack']:
            if d['credentials']['OS_USERNAME']:
                del d['credentials']['OS_USERNAME']
            if d['credentials']['OS_PASSWORD']:
                del d['credentials']['OS_PASSWORD']
            if d['credentials']['OS_TENANT_NAME']:
                del d['credentials']['OS_TENANT_NAME']
        elif d['cm_type'] in ['ec2', 'aws']:
            if d['credentials']['EC2_ACCESS_KEY']:
                del d['credentials']['EC2_ACCESS_KEY']
            if d['credentials']['EC2_SECRET_KEY']:
                del d['credentials']['EC2_SECRET_KEY']
        elif d['cm_type'] in ['azure']:
            if d['credentials']['subscriptionid']:
                del d['credentials']['subscriptionid']
        self.db_clouds.insert(d)


    def remove(self, cloudname):
        self.db_clouds.remove({'cm_kind': 'cloud', 'cm_cloud': cloudname})
    ####################################
    
class CloudCommand(CloudManage):
    def __init__(self, args):
        self.args = args
        
    def _cloud_list(self):
        if self.args["--column"]:
            if self.args["--column"] == 'all':
                col_option = ['active', 'user', 'label', 'host', 'type/version', 'type', 'heading', 'credentials', 'defaults']
            elif self.args["--column"] == 'semiall':
                col_option = ['active', 'user', 'label', 'host', 'type/version', 'type', 'heading']
            else:
                col_option = [x.strip() for x in self.args["--column"].split(',')]

            if not set(col_option).issubset(set(['active', 'label', 'host', 'type/version', 'type', 'heading', 'user', 'credentials', 'defaults'])):
                log.warning("ERROR: one or more column type doesn't exist, available columns are: active,label,host,type/version,type,heading,user,credentials,defaults  ('all' to diplay all, 'semiall' to display all except credentials and defauts)")
                return       
        else:
            col_option = ['active']
        headers = ['cloud'] + col_option
        standard_headers = []
        
        def attribute_name_map(name):
            if name == "cloud":
                return "cm_cloud"
            elif name == "label":
                return "cm_label"
            elif name == "host":
                return "cm_host"
            elif name == "type/version":
                return "cm_type_version"
            elif name == "type":
                return "cm_type"
            elif name == "heading":
                return "cm_heading"
            elif name == "user":
                return "cm_user_id"
            elif name == "credentials":
                return "credentials"
            elif name == "defaults":
                return "default"
            else:
                return name
        
        for item in headers:
            standard_headers.append(attribute_name_map(item))
            
        clouds = self.get_clouds(self.username)
        clouds = clouds.sort([('cm_cloud', 1)])
        activeclouds = self.mongo.active_clouds(self.username)
        
        to_print = []
        
        for cloud in clouds:
            res = []
            for key in standard_headers:
                if key == "active":
                    if cloud['cm_cloud'] in activeclouds:
                        res.append('True')
                    else:
                        res.append(' ')
                else:
                    try:
                        res.append(str(cloud[key]))
                    except:
                        res.append(' ')
            to_print.append(res)
            
        print tabulate(to_print, headers, tablefmt="grid")
        
        if clouds.count() == 0:
            log.info("no cloud in database, please import cloud information by 'cloud add CLOUDFILE'")
        
        
    def _cloud_info(self):
        def printing(cloud):
            cloud = dict_uni_to_ascii(cloud)
            banner(cloud['cm_cloud'])
            pprint(cloud)
            print "#", 70 * "-"
            if cloud['cm_cloud'] in self.mongo.active_clouds(self.username):
                print "active: True"
            else:
                print "active: False"
            print "#", 70 * "#", "\n"
            
        if self.args['CLOUD']:
            cloud = self.get_clouds(self.username, getone=True, cloudname=self.args['CLOUD'])
            if cloud == None:
                log.warning("ERROR: could not find cloud '{0}'".format(self.args['CLOUD']))
            else:
                printing(cloud)
        elif self.args['--all']:
            clouds = self.get_clouds(self.username)
            clouds = clouds.sort([('cm_cloud', 1)])
            if clouds.count() == 0:
                log.info("no cloud in database, please import cloud information by 'cloud add CLOUDFILE'")
                return
            for cloud in clouds:
                printing(cloud)
        else:
            selected_cloud = self.get_selected_cloud(self.username)  
            cloud = self.get_clouds(self.username, getone=True, cloudname=selected_cloud)
            if cloud == None:
                log.warning("no cloud information of '{0}' in database".format(selected_cloud))
                return
            printing(cloud)
        
        
    def _cloud_select(self):
        if self.args['CLOUD']:
            cloud = self.get_clouds(self.username, getone=True, cloudname=self.args['CLOUD'])
            if cloud == None:
                log.warning("no cloud information of '{0}' in database, please import it by 'cloud add CLOUDFILE'".format(self.args['CLOUD']))
                return
            self.update_selected_cloud(self.username, self.args['CLOUD'])
            log.info("cloud '{0}' is selected".format(self.args['CLOUD']))
        else:
            clouds = self.get_clouds(self.username)
            cloud_names = []
            for cloud in clouds:
                cloud_names.append(cloud['cm_cloud'].encode("ascii"))
            cloud_names.sort()
            res = menu_return_num(title="select a cloud", menu_list=cloud_names, tries=3)
            if res == 'q': return
            self.update_selected_cloud(self.username, cloud_names[res])
            log.info("cloud '{0}' is selected".format(cloud_names[res]))
            
    def _cloud_alias(self):
        if self.args['CLOUD']:
            name = self.args['CLOUD']
        else:
            name = self.get_selected_cloud(self.username)
        if self.get_clouds(self.username, getone=True, cloudname=name) == None:
            log.error("no cloud information of '{0}' in database".format(name))
            return
        if yn_choice("rename cloud '{0}' to '{1}'?".format(name, self.args['<name>']), default = 'n', tries = 3):
            self.update_cloud_name(self.username, name, self.args['<name>'])
        else:
            return
                
    def _cloud_activate(self):
        if self.args['CLOUD']:
            name = self.args['CLOUD']
        else:
            name = self.get_selected_cloud(self.username)
        if self.get_clouds(self.username, getone=True, cloudname=name) == None:
            log.error("no cloud information of '{0}' in database".format(name))
            return
        if yn_choice("activate cloud '{0}'?".format(name), default = 'n', tries = 3):
            res = self.activate_cloud(self.username, name)
            if res == 0:
                return
            elif res == 1:
                print "cloud '{0}' activated.".format(name)
        else:
            return
        
    def _cloud_deactivate(self):
        if self.args['CLOUD']:
            name = self.args['CLOUD']
        else:
            name = self.get_selected_cloud(self.username)
        if self.get_clouds(self.username, getone=True, cloudname=name) == None:
            log.error("no cloud information of '{0}' in database".format(name))
            return
        if yn_choice("activate cloud '{0}'?".format(name), default = 'n', tries = 3):
            self.deactivate_cloud(self.username, name)
            print "cloud '{0}' deactivated.".format(name)
        else:
            return
        
        
    def _cloud_remove(self):
        '''
        remove selected_cloud value if such cloud is removed
        '''
        pass
        


    def call_procedure(self):
        if self.args['list'] == True:
            call = 'list'
        elif self.args['info'] == True:
            call = 'info'
        elif self.args['alias'] == True:
            call = 'alias'
        elif self.args['select'] == True:
            call = 'select'
        elif self.args['on'] == True:
            call = 'activate'
        elif self.args['off'] == True:
            call = 'deactivate'
        elif self.args['add'] == True:
            pass
        elif self.args['remove'] == True:
            pass
        elif self.args['default'] == True:
            pass
        else:
            call = 'list'
        func = getattr(self, "_cloud_" + call)
        func()
    
    
    
    
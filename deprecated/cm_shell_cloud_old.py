from cloudmesh_common.logger import LOGGER
import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from collections import OrderedDict
from cloudmesh.cm_mongo import cm_mongo
from cmd3.shell import command
from cloudmesh_common.tables import column_table
from cloudmesh_common.bootstrap_util import yn_choice
from pprint import pprint
from cloudmesh_common.util import banner, dict_uni_to_ascii
from cloudmesh.util.menu import menu_return_num
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh_common.bootstrap_util import path_expand

log = LOGGER(__file__)


class cm_shell_cloud:

    """opt_example class"""

    # For now, initial selected cloud is just a randomly picked cloud in the db
    # [default: india], once you restart cm, previous
    # selection will be erased, later on we may choose default cloud as the
    # initial selected cloud
    
    
    # ----------------------------------------------------------------------------------------
    # bug: active clouds should be read from default db, cloud info shouldn't keep active info
    # ----------------------------------------------------------------------------------------
    
    selected_cloud = None
    clouds = None
    
    
    def activate_cm_shell_cloud(self):
        self.register_command_topic('cloud', 'cloud')
        self._db_loaded = False
        self._requery = True
        self._cloud_selected = False
        pass
    
        
        
        

    def _load_mongodb(self):
        if not self._db_loaded:
            try:
                self.cloudsinfo = cm_mongo()
                self._db_loaded = True
            except:
                print "ERROR: Could not load db, did you start mongo?"
                      
    def _requery_db(self):
        if self._requery:
            self.clouds = self.cloudsinfo.get_clouds()
            self.clouds = self.clouds.sort([('cm_cloud', 1)])
            self._requery = False
        else:
            return
        
    def _check_empty(self):
        if self.clouds.count() == 0:
            return True
        else:
            return False
        
        
        
    def _get_selected_cloud(self):
        if self._cloud_selected:
            return self.selected_cloud
        else:
            self._load_mongodb()
            self._requery_db()
            if self._check_empty():
                print "ERROR: no cloud to select in database"
                return None
            else:
                for cloud in self.clouds:
                    if cloud['cm_cloud'] == 'india':
                        self.selected_cloud = cloud
                        self._cloud_selected = True
                        self.clouds.rewind()
                        return self.selected_cloud
                self.clouds.rewind()
                self.selected_cloud = self.clouds.__getitem__(0)
                self.clouds.rewind()
                self._cloud_selected = True
                return self.selected_cloud
        
        

    @command
    def do_cloud(self, args, arguments):
        """
        ::

            Usage:
                cloud list [--column=COLUMN]
                cloud info [NAME] 
                cloud set NAME
                cloud select [NAME]
                cloud on [NAME]
                cloud off [NAME]
                cloud add CLOUD
                cloud remove [NAME]
                cloud

            Manages the clouds

            Arguments:

              NAME           the name of a service or server
              CLOUD          a yaml file contains cloud information

            Options:

               -v       verbose model
               --column=COLUMN   specify what information to display. For
                                 example, --column=active,label. Available
                                 columns are active, label, host, type/version,
                                 type, heading, user, credentials, defaults
                                 (all to diplay all, semiall to display all
                                 except credentials and defaults)

            Description:

                cloud list [--column=COLUMN]
                    lists the cloud names, optionally, specify columns for more
                    cloud information

                cloud info [NAME] 
                    provides the available information about cloud and its status 
                    in dict format. If no NAME is given, default or selected cloud
                    is used. If the name all is used, all clouds are displayed

                cloud set NAME
                    sets a new name for selected or default cloud, please select a
                    cloud to work with first, otherwise the default cloud will be 
                    used

                cloud select [NAME]
                    selects a cloud to work with from a list of clouds if NAME 
                    not given

                cloud on [NAME]
                cloud off [NAME]
                    activates or deactivates a cloud, if name is not given, 
                    default or selected cloud will be activated or deactivated

                cloud add CLOUD
                    adds cloud information to database. CLOUD is a yaml file with 
                    full file path. Inside yaml, clouds should be written in the
                    form: 
                    cloudmesh: clouds: cloud1...
                                       cloud2...

                cloud remove [NAME]
                    remove a cloud from mongo, if name is not given, default or 
                    selected cloud will be reomved.
                    CAUTION: remove all is enabled

        """

        #log.info(arguments)
        #print "<", args, ">"

        if arguments["list"] or args=="":
            self._load_mongodb()
            self._requery_db()
            if self._check_empty():
                print "Can't preceed, no cloud in database"
                return
            else:
                col = OrderedDict([('cloud', [])])
                if arguments["--column"]:
                    if arguments["--column"] == 'all':
                        col_option = ['active', 'user', 'label', 'host', 'type/version', 'type', 'heading', 'credentials', 'defaults']
                    elif arguments["--column"] == 'semiall':
                        col_option = ['active', 'user', 'label', 'host', 'type/version', 'type', 'heading']
                    else:
                        col_option = [x.strip() for x in arguments["--column"].split(',')]

                    if set(col_option).issubset(set(['active', 'label', 'host', 'type/version', 'type', 'heading', 'user', 'credentials', 'defaults'])):
                        
                        for co in col_option:
                            col[co] = []
                    else:
                        print "ERROR: one or more column type doesn't exist, available columns are: active,label,host,type/version,type,heading,user,credentials,defaults  ('all' to diplay all, 'semiall' to display all except credentials and defauts)"
                        return
                else:
                    col['active'] = []

                for cloud in self.clouds:
                    for key in col.keys():
                        db_key = self.cloudsinfo.db_name_map(key)
                        try:
                            val = cloud[db_key]
                        except:
                            val = " "
                            pass
                        if val != " ":
                            try:
                                val = val.encode("ascii")
                            except:
                                if isinstance(val, dict):
                                    val = dict_uni_to_ascii(val)
                                pass
                        col[key].append(val)
                self.clouds.rewind()     
                print column_table(col)
             

        if arguments["info"]:
            self._load_mongodb()
            def printing(cloud):
                cloud = dict_uni_to_ascii(cloud)
                banner(cloud['cm_cloud'])
                pprint(cloud)
                print "#", 70 * "#", "\n"
                
            if not arguments["NAME"]:
                cloud = self._get_selected_cloud()
                if cloud == None: return
                else: printing(cloud)
            else:
                if arguments["NAME"] == 'all':
                    self._requery_db()
                    if self._check_empty():
                        print "Can't preceed, no cloud in database"
                        return
                    else:
                        for cloud in self.clouds:
                            printing(cloud)
                        self.clouds.rewind()
                else:
                    self._requery_db()
                    res = None
                    for cloud in self.clouds:
                        if cloud['cm_cloud'] == arguments["NAME"]:
                            res = cloud
                    self.clouds.rewind() 
                    if res == None:
                        print "ERROR: could not find cloud '{0}'".format(arguments["NAME"])
                    else:
                        printing(res)
                        
        if arguments["set"] and arguments["NAME"]:
            self._load_mongodb()
            cloud = self._get_selected_cloud()
            if cloud == None: return
            if yn_choice("rename cloud '{0}' to '{1}'?".format(cloud['cm_cloud'], arguments["NAME"]), default = 'n', tries = 3):
                self.cloudsinfo.set_name(cloud['cm_cloud'], arguments["NAME"])
                self.selected_cloud['cm_cloud'] = arguments["NAME"]
            else:
                return
            
            
        if arguments["select"]:
            self._load_mongodb()
            if arguments["NAME"]:
                def selecting(cloud):
                    if cloud == None:
                        print "'{0}' is not in the database".format(arguments["NAME"])
                        return
                    else:
                        self.selected_cloud = cloud
                        self._cloud_selected = True
                        print "cloud '{0}' is selected".format(arguments["NAME"])
                if self._requery:
                    cloud = self.cloudsinfo.get_one_cloud(arguments["NAME"])
                    selecting(cloud)
                else:
                    res = None
                    for cloud in self.clouds:
                        if cloud['cm_cloud'] == arguments["NAME"]:
                            res = cloud
                    self.clouds.rewind()
                    selecting(res)
            else:
                current_selected = self._get_selected_cloud()
                if current_selected == None: return
                current_selected = current_selected['cm_cloud'].encode("ascii")
                self._requery_db()
                cloud_names = []
                for cloud in self.clouds:
                    cloud_names.append(cloud['cm_cloud'].encode("ascii"))
                self.clouds.rewind()
                cloud_names.sort()
                res = menu_return_num(title="select a cloud (current selected: {0})".format(current_selected), menu_list=cloud_names, tries=3)
                if res == 'q': return
                name = cloud_names[res]
                res = None
                for cloud in self.clouds:
                    if cloud['cm_cloud'] == name:
                        res = cloud
                self.clouds.rewind()
                self.selected_cloud = res
                self._cloud_selected = True
                print "cloud '{0}' is selected".format(name)
            
            
        if arguments["on"]:
            self._load_mongodb()
            if not arguments["NAME"]:
                current_selected = self._get_selected_cloud()
                if current_selected == None: return
                current_selected = current_selected['cm_cloud'].encode("ascii")
                res = self.cloudsinfo.activate_one_cloud(current_selected)
                self._cloud_selected = False
                if res == 0:
                    return
                elif res == 1:
                    print "cloud '{0}' activated.".format(current_selected)
            else:
                def activating(cloud):
                    if cloud == None:
                        print "ERROR: Could not find '{0}' in database.".format(arguments["NAME"])
                        return
                    cloudname = cloud['cm_cloud'].encode("ascii")
                    res = self.cloudsinfo.activate_one_cloud(cloudname)
                    self._cloud_selected = False
                    if res == 0:
                        return
                    elif res == 1:
                        print "cloud '{0}' activated.".format(cloudname)
                        
                if self._requery:
                    cloud = self.cloudsinfo.get_one_cloud(arguments["NAME"])
                    activating(cloud)
                else:
                    res = None
                    for cloud in self.clouds:
                        if cloud['cm_cloud'] == arguments["NAME"]:
                            res = cloud
                    self.clouds.rewind()
                    activating(res)
            
        

        if arguments["off"]:
            self._load_mongodb()
            if not arguments["NAME"]:
                current_selected = self._get_selected_cloud()
                if current_selected == None: return
                current_selected = current_selected['cm_cloud'].encode("ascii")
                self.cloudsinfo.deactivate_one_cloud(current_selected)
                self._cloud_selected = False
                print "cloud '{0}' deactivated.".format(current_selected)
            else:
                def deactivating(cloud):
                    if cloud == None:
                        print "ERROR: Could not find '{0}' in database.".format(arguments["NAME"])
                        return
                    cloudname = cloud['cm_cloud'].encode("ascii")
                    self.cloudsinfo.deactivate_one_cloud(cloudname)
                    self._cloud_selected = False
                    print "cloud '{0}' deactivated.".format(cloudname)
                        
                if self._requery:
                    cloud = self.cloudsinfo.get_one_cloud(arguments["NAME"])
                    deactivating(cloud)
                else:
                    res = None
                    for cloud in self.clouds:
                        if cloud['cm_cloud'] == arguments["NAME"]:
                            res = cloud
                    self.clouds.rewind()
                    deactivating(res)


        if arguments["add"] and arguments["CLOUD"]:
            try:
                file = path_expand(arguments["CLOUD"])
                config = ConfigDict(filename=file)
            except:
                print "ERROR: could not load file, please check filename and its path"
                return
            try:
                cloudsdict = config.get("cloudmesh", "clouds")
            except:
                print "ERROR: could not get clouds information from yaml file, please check you yaml file, clouds information must be under 'cloudmesh' -> 'clouds' -> cloud1..."
                return
            '''
            #get cm_active information from yaml
            try:
                active = config.get("cloudmesh")['active'] 
            except:
                active = []
            '''
            try:
                user = config.get("cloudmesh")['profile']['username']
            except:
                user = ' '
            self._load_mongodb()
            self._requery_db()
            cloud_names = []
            for cloud in self.clouds:
                cloud_names.append(cloud['cm_cloud'].encode("ascii"))
            self.clouds.rewind()
            for key in cloudsdict:
                if key in cloud_names:
                    print "ERROR: cloud '{0}' exists in database, please remove it from database first".format(key)
                    continue
                cloudsdict[key]['cm_cloud']=key
                cloudsdict[key]['cm_kind']='cloud'
                cloudsdict[key]['cm_user_id']=user
                '''
                #get cm_active information from yaml
                if key in active:
                    cloudsdict[key]['cm_active']=True
                else:
                    cloudsdict[key]['cm_active']=False
                '''
                cloudsdict[key]['cm_active']=False
                try:
                    self.cloudsinfo.add(cloudsdict[key])
                except:
                    print "ERROR: failed to add cloud '{0}' into database, please check".format(key)
                    continue
                print "cloud '{0}' added.".format(key)
            self._requery = True
            
            
        if arguments["remove"]:
            self._load_mongodb()
            self._requery_db()
            if not arguments["NAME"]:
                current_selected = self._get_selected_cloud()
                if current_selected == None: return
                current_selected = current_selected['cm_cloud'].encode("ascii")
                ans = yn_choice("Remove cloud '{0}' from database?".format(current_selected), default ='n', tries=3)
                if ans:
                    self.cloudsinfo.remove(current_selected)
                    print "cloud '{0}' removed.".format(current_selected)
                    self._requery = True
                    self._cloud_selected = False
            else:
                if arguments["NAME"] == 'all':
                    ans = yn_choice("!!!CAUTION!!! Remove all clouds from database?", default ='n', tries=3)
                    if ans:
                        for cloud in self.clouds:
                            self.cloudsinfo.remove(cloud['cm_cloud'])
                            print "cloud '{0}' removed.".format(cloud['cm_cloud'])
                        self._requery = True
                        self._cloud_selected = False
                    else: return
                else:
                    cloud_names = []
                    for cloud in self.clouds:
                        cloud_names.append(cloud['cm_cloud'].encode("ascii"))
                    self.clouds.rewind()
                    if arguments["NAME"] not in cloud_names:
                        print "ERROR: Could not find '{0}' in database".format(arguments["NAME"])
                        return
                    else:
                        ans = yn_choice("Remove cloud '{0}' from database?".format(arguments["NAME"]), default ='n', tries=3)
                        if ans:
                            self.cloudsinfo.remove(arguments["NAME"])
                            print "cloud '{0}' removed.".format(arguments["NAME"])
                            self._requery = True
                            self._cloud_selected = False
              
                        
       

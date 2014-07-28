from cloudmesh_common.logger import LOGGER
from cloudmesh.config.cm_config import cm_config

log = LOGGER(__file__)

def shell_command_cloud(arguments):
    """
        ::

            Usage:
                cloud
                cloud list [--column=COLUMN]
                cloud info [CLOUD|--all] 
                cloud set <name> [CLOUD]
                cloud select [CLOUD]
                cloud on [CLOUD]
                cloud off [CLOUD]
                cloud add CLOUDFILE
                cloud remove [CLOUD]
                cloud default [--setflavor|--setimage] [CLOUD|--all]

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
               --setflavor       set the default flavor of a cloud
               --serimage        set the image flavor of a cloud
               --all             provide information of all clouds

            Description:
                the place to manage clouds

                cloud list [--column=COLUMN]
                    lists the stored clouds, optionally, specify columns for more
                    cloud information. For example, --column=active,label

                cloud info [CLOUD|--all]  
                    provides the available information about the cloud in dict format 
                    options: specify CLOUD to display it, --all to display all,
                             otherwise selected cloud will be used

                cloud set <name> [CLOUD]
                    sets a new name for a cloud
                    options: specify CLOUD to work with, otherwise selected cloud 
                             will be used

                cloud select [CLOUD]
                    selects a cloud to work with from a list of clouds if CLOUD 
                    not given

                cloud on [CLOUD]
                cloud off [CLOUD]
                    activates or deactivates a cloud, if CLOUD is not given, 
                    selected cloud will be activated or deactivated

                cloud add CLOUDFILE
                    adds cloud information to database. CLOUDFILE is a yaml file with 
                    full file path. Inside the yaml, clouds should be written in the
                    form: 
                    cloudmesh: clouds: cloud1...
                                       cloud2...
                    please check ~/.futuregrid/cloudmesh.yaml

                cloud remove [CLOUD]
                    remove a cloud from mongo, if CLOUD is not given, selected cloud 
                    will be reomved.
                    CAUTION: remove all is enabled(remove all)
                    
                cloud default [--setflavor|--setimage] [CLOUD|--all]
                    view or manage cloud's default flavor and image
                    options: CLOUD, specify a cloud to work on, otherwise selected 
                             cloud will be used, --all to display all clouds defaults
                             --setflavor, set default flaovr
                             --setimage, set default image

    """
    call = CloudCommand(arguments)
    call.call_procedure()
    
    
class CloudManage(object):
    config = cm_config()
    
class CloudCommand(CloudManage):
    def __init__(self, args):
        self.args = args
        
        
        
    def call_procedure(self):
        print self.args
    '''
        cmds = self.get_commands()
        vals = cmds.values()
        if True not in vals:
            self._cloud_list()
        else:
            for cmd, tof in cmds.iteritems():
                if tof == True:
                    func = getattr(self, "_cloud_" + cmd)
                    func()
                    break
    '''

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
    
    
    
    
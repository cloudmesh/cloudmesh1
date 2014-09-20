from cmd3.shell import command
from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.util import CONSOLE
from cloudmesh_common.util import dotdict
from cloudmesh_common.tables import print_format_dict
from pprint import pprint

log = LOGGER(__file__)

class cm_shell_yaml:

    cm_config = cm_config()
    cm_config_server = cm_config_server()

    def activate_cm_shell_yaml(self):
        self.register_command_topic('cloud', 'yaml')
        self.register_command_topic('cloud', 'debug')
        self.register_command_topic('cloud', 'loglevel')

    @command
    def do_debug(self, args, arguments):
        """
        Usage:
            debug on
            debug off

            Turns the debug log level on and off.
        """
        if arguments['on']:
            key = "cloudmesh.server.loglevel"
            value = "DEBUG"
            self.cm_config_server._update(key, value)
            self.cm_config_server.write(format="yaml")
            print ("Debug mode is on.")
        elif arguments['off']:
            key = "cloudmesh.server.loglevel"
            value = "ERROR"
            self.cm_config_server._update(key, value)
            self.cm_config_server.write(format="yaml")
            print ("Debug mode is off.")
            
    
    @command
    def do_color(self, args, arguments):
        """
        Usage:
            color on
            color off
            
            Turns the shell color printing on or off
        """
        if arguments['on']:
            key = "cloudmesh.shell.color"
            value = True
            self.cm_config_server._update(key, value)
            self.cm_config_server.write(format="yaml")
            print ("color on.")
        elif arguments['off']:
            key = "cloudmesh.shell.color"
            value = False
            self.cm_config_server._update(key, value)
            self.cm_config_server.write(format="yaml")
            print ("color off.")
        
  

    @command
    def do_loglevel(self, args, arguments):
        """
        Usage:
            loglevel
            loglevel error
            loglevel warning
            loglevel debug
            loglevel info
            loglevel critical

            Shows current log level or changes it.
        """
        key = "cloudmesh.server.loglevel"
        if arguments['debug']:
            value = "DEBUG"
        elif arguments['error']:
            value = "ERROR"
        elif arguments['warning']:
            value = "WARNING"
        elif arguments['info']:
            value = "INFO"
        elif arguments['critical']:
            value = "CRITICAL"
        else:
            print self.cm_config_server.get(key)
            return

        self.cm_config_server._update(key, value)
        self.cm_config_server.write(format="yaml")
        log.info("{0} mode is set.".format(value))
        print ("{0} mode is set.".format(value))

    @command
    def do_yaml(self, args, arguments):
        """
        Usage:
            yaml KIND [KEY] [--filename=FILENAME] [--format=FORMAT]
            yaml KIND KEY VALUE [--filename=FILENAME] 

        Provides yaml information or updates yaml on a given replacement

        Arguments:
            KIND    The typye of the yaml file (server, user) 
            KEY     Key name of the nested dict e.g. cloudmesh.server.loglevel
            VALUE   Value to set on a given KEY
            FILENAME      cloudmesh.yaml or cloudmesh_server.yaml
            FORMAT         The format of the output (table, json, yaml)

        Options:
            
            --format=FORMAT      the format of the output [default: print]

        Description:

             Sets and gets values from a yaml configuration file
        """
        
        Console = CONSOLE()        
        #
        # use dot notation to make things better readable
        #
        arguments['value'] = arguments.pop('VALUE')                        
        arguments['kind'] = arguments.pop('KIND')                
        arguments['key'] = arguments.pop('KEY')        
        arguments['format'] = arguments.pop('--format')
        arguments['filename'] = arguments.pop('--filename')        
        arguments = dotdict(arguments)
        
        #
        # List functions
        #
        if arguments.kind not in ['user','server']:
            Console.error("the specified kind does not exist")
            return
        
        if arguments.kind == 'user':
            config = self.cm_config
        elif arguments.kind == 'server':
            config = self.cm_config_server

        arguments.filename = arguments.filename or config.filename
        config.load(arguments.filename)

        if not arguments.key and not arguments.value:
            if arguments.format == "print":
                print config.pprint()
            elif arguments.format == 'json':
                print config.json()
            elif arguments.format == 'yaml':
                print config.yaml()
            else:
                Console.error("format not supported")
            return
        elif arguments.key and not arguments.value:
            print config.get(arguments.key)
            return

        #
        # 
        #
        print "HERE"

        if arguments.kind == 'server':
            if not arguments.key:
                self.cm_config_server.pprint()
            else:
                print self.cm_config_server.get(arguments.key)
        elif arguments['user'] and arguments.key and arguments.value:
            self.cm_config._update(arguments.key, arguments['VALUE'])
            self.cm_config.write(format="yaml")
            self.cm_config.pprint() 
        elif arguments['server'] and arguments.key and arguments.value:
            self.cm_config_server._update(arguments.key, arguments.value)
            self.cm_config_server.write(format="yaml")
            self.cm_config_server.pprint() 

        '''

            project = arguments["NAME"]
            self.projects.default(project)
            # WRITE TO YAML
            self.projects.write()
            # UPDATE MONGO DB
            self.cm_user.set_default_attribute(self.username, 'project', project)
            self.cm_user.add_active_projects(self.username, project)
            self._load_projects()

            msg = '{0} project is a default project now'.format(project)
            log.info(msg)
            print msg
            return

        elif arguments["active"] and arguments['NAME']:
            log.info("Sets the active project")
            project = arguments["NAME"]
            self.projects.add(project)
            self.projects.write()
            self.cm_user.add_active_projects(self.username, project)
            self._load_projects()

            msg = '{0} project is an active project(s) now'.format(project)
            log.info(msg)
            print msg
            return

        elif arguments['delete'] and arguments['NAME']:
            log.info('Deletes the project')
            project = arguments['NAME']
            try:
                self.projects.delete(project,'active')
            except ValueError, e:
                log.info('Skipped deleting the project {0} in the active \
                         list:{1}'.format(project, e))
            try:
                self.projects.delete(project,'completed')
            except ValueError, e:
                log.info('Skipped deleting the project {0} in the completed\
                         list:{1}'.format(project, e))
            try: 
                self.projects.delete(project,'default')
            except ValueError, e:
                log.info('Skipped deleting the project {0} in the default\
                         list:{1}'.format(project, e))
            self.projects.write()
            self.cm_user.delete_projects(self.username, project)
            self._load_projects()

            msg = '{0} project is deleted'.format(project)
            log.info(msg)
            print msg
            return

        elif arguments['completed'] and arguments['NAME']:
            log.info('Sets a completed project')
            project = arguments['NAME']
            self.projects.delete(project,'active')
            self.projects.add(project,'completed')
            self.projects.delete(project,'default')
            self.projects.write()
            self.cm_user.delete_projects(self.username, project)
            self.cm_user.add_completed_projects(self.username, project)
            self._load_projects()

            msg = '{0} project is in a completed project(s)'.format(project)
            log.info(msg)
            print msg
            return
        else: 
            #elif arguments["info"]:


            # log.info ("project info for all")
            if arguments["--json"]:
                print self.projects.dump()
                return
            else:
                print
                print "Project Information"
                print "-------------------"
                print
                if self.projects.names("default") is not "" and not []:
                    print "%10s:" % "default", self.projects.names("default")
                else:
                    print "%10s:" % "default ", \
                          "default is not set, please set it"
                if len(self.projects.names("active")) > 0:
                    print "%10s:" % "projects", \
                        ', '.join(self.projects.names("active"))

                if len(self.projects.names("completed")) > 0:
                    print "%10s:" % "completed", \
                        ', '.join(self.projects.names("completed"))
                print
            return
        '''

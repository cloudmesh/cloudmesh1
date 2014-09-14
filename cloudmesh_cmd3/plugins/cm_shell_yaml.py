from cmd3.shell import command
from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_yaml:

    cm_config = cm_config()
    cm_config_server = cm_config_server()

    @command
    def do_debug(self, args, arguments):
        """
        Usage:
            debug on
            debug off
        """
        print arguments

    @command
    def do_loglevel(self, args, arguments):
        """
        Usage:
            loglevel
            loglevel error
            loglevel debug
            loglevel info
        """
        print arguments

    @command
    def do_yaml(self, args, arguments):
        """
        Usage:
            yaml [KEY] [--filename=FILENAME]
            yaml info [KEY] [--filename=FILENAME]
            yaml info-server [KEY]
            yaml replace KEY VALUE [--filename=FILENAME] 
            yaml replace-server KEY VALUE

        Provides yaml information or updates yaml on a given replacement

        Arguments:
            KEY     Key name of the nested dict e.g. cloudmesh.server.loglevel
            VALUE   Value to set on a given KEY
            FILENAME      cloudmesh.yaml or cloudmesh_server.yaml

        """

        if arguments['info']:
            self.cm_config.load(arguments['--filename'] or
                                self.cm_config.filename)
            if not arguments['KEY']:
                self.cm_config.pprint()
            else:
                print self.cm_config.get(arguments['KEY'])
        elif arguments['info-server']:
            if not arguments['KEY']:
                self.cm_config_server.pprint()
            else:
                print self.cm_config_server.get(arguments['KEY'])
        elif arguments['replace-server']:
            self.cm_config_server._update(arguments['KEY'], arguments['VALUE'])
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

from cmd3.shell import command
from cloudmesh.user.cm_user import cm_user
from cloudmesh.config.cm_projects import cm_projects
from cloudmesh_install import config_file

from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)

class cm_shell_project:

    """opt_example class"""

    def _load_projects(self):
        if not self.cm_shell_project_loaded:
            filename = config_file("/cloudmesh.yaml")
            self.projects = cm_projects(filename)
            if self.echo:
                log.info(
                    "Reading project information from -> {0}".format(filename))
            self.cm_shell_project_loaded = True

    def activate_shell_project(self):
        self.register_command_topic('cloud', 'project')
        #
        # BUG this should be done outside of the activate
        #
        self.cm_shell_project_loaded = False
        pass

    @command
    def do_project(self, args, arguments):
        """
        Usage:
               project
               project info [--json]
               project default NAME
               project active NAME
               project delete NAME
               project completed NAME

        Manages the project

        Arguments:

          NAME           The project id

        Options:

           -v       verbose mode

        """

        if arguments["default"] and arguments["NAME"]:
            log.info("sets the default project")

            self._load_projects()
            project = arguments["NAME"]
            self.projects.default(project)
            # WRITE TO YAML
            self.projects.write()
            # UPDATE MONGO DB
            self.cm_user = cm_user()
            username = self.projects.config['cloudmesh']['profile']['username']
            self.cm_user.set_default_attribute(username, 'project', project)
            self._load_projects()

            msg = '{0} project is a default project now'.format(project)
            log.info(msg)
            print msg
            return

        elif arguments["active"] and arguments['NAME']:
            log.info("Sets the active project")
            self._load_projects()
            project = arguments["NAME"]
            self.projects.add(project)
            self.projects.write()
            self._load_projects()

            msg = '{0} project is an active project(s) now'.format(project)
            log.info(msg)
            print msg
            return

        elif arguments['delete'] and arguments['NAME']:
            log.info('Deletes the project')
            self._load_projects()
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
            self._load_projects()

            msg = '{0} project is deleted'.format(project)
            log.info(msg)
            print msg
            return

        elif arguments['completed'] and arguments['NAME']:
            log.info('Sets a completed project')
            self._load_projects()
            project = arguments['NAME']
            self.projects.delete(project,'active')
            self.projects.add(project,'completed')
            self.projects.delete(project,'default')
            self.projects.write()
            self._load_projects()

            msg = '{0} project is in a completed project(s)'.format(project)
            log.info(msg)
            print msg
            return
        else: 
            #elif arguments["info"]:

            self._load_projects()

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

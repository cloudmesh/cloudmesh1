from __future__ import print_function
from cmd3.shell import command
from cloudmesh.user.cm_user import cm_user
from cloudmesh.config.cm_projects import cm_projects
from cloudmesh_base.locations import config_file
from cloudmesh_common.tables import two_column_table, print_format_dict
from cloudmesh_base.logger import LOGGER
import json

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

    @command
    def do_project(self, args, arguments):
        """
        ::
        
          Usage:
              project
              project info [--format=FORMAT]
              project default NAME
              project active NAME
              project delete NAME
              project completed NAME

          Arguments:

              NAME           The project id
              FORMAT         The display format. (json, table)
            
          Description:
              Manages the user's projects
              
              project info
                  show project information
              project default
                  set the default project
              project active
                  set/add an active project, 
              project delete
                  delete the project
              project completed
                  set a completed project, this will remove the project
                  from active projects list and defalut project if it is
              

        """
        self._load_projects()
        self.cm_user = cm_user()
        self.username = self.projects.config['cloudmesh']['profile']['username']

        if arguments["default"] and arguments["NAME"]:
            log.info("sets the default project")

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
            print(msg)
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
            print(msg)
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
            print(msg)
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
            print(msg)
            return
        else: 
            # log.info ("project info for all")
            if arguments["--format"] == "json":
                a = json.loads(self.projects.dump())
                print(print_format_dict(a, kind='json'))
                return
            else:
                a = json.loads(self.projects.dump())
                print(two_column_table(a))
                '''
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
                '''
            return

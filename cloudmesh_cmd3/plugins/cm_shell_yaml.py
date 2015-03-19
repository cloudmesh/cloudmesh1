from __future__ import print_function
from cmd3.shell import command
from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh_base.logger import LOGGER
from cmd3.console import Console
from cloudmesh_base.dotdict import dotdict
from pprint import pprint

log = LOGGER(__file__)

class cm_shell_yaml:

    def activate_cm_shell_yaml(self):
        self.cm_config = cm_config()
        Console.color = self.cm_config.get("cloudmesh.shell.color")
        self.cm_config_server = cm_config_server()
        self.register_command_topic('cloud', 'yaml')

    @command
    def do_yaml(self, args, arguments):
        """
        ::

          Usage:
              yaml KIND [KEY] [--filename=FILENAME] [--format=FORMAT]
              yaml KIND KEY VALUE [--filename=FILENAME] 

          Provides yaml information or updates yaml on a given replacement

          Arguments:
              KIND        The type of the yaml file (server, user) 
              KEY         Key name of the nested dict e.g. cloudmesh.server.loglevel
              VALUE       Value to set on a given KEY
              FILENAME    cloudmesh.yaml or cloudmesh_server.yaml
              FORMAT      The format of the output (table, json, yaml)

          Options:

              --format=FORMAT      the format of the output [default: print]

          Description:

             Sets and gets values from a yaml configuration file
        """
        
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
        else:
            if arguments.kind == 'user':
                config = self.cm_config
            elif arguments.kind == 'server':
                config = self.cm_config_server
            arguments.filename = arguments.filename or config.filename
            config.load(arguments.filename)

        
        if not arguments.value:

            if not arguments.key and not arguments.value:
                if arguments.format == "print":
                    print(config.pprint())
                elif arguments.format == 'json':
                    print(config.json())
                elif arguments.format == 'yaml':
                    print(config.yaml())
                else:
                    Console.error("format not supported")
                return
            elif arguments.key and not arguments.value:
                print(config.get(arguments.key))

            return

        else:
        #
        # SETTING VALUES
        #

            config._update(arguments.key, arguments.value)
            # config.pprint()
            config['meta']['location'] = arguments.filename
            config.write(output="yaml")

            self.config = config

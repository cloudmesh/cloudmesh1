from __future__ import print_function
import os
import sys
from cmd3.shell import command
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.tables import row_table
from cmd3.console import Console

log = LOGGER(__file__)

class cm_shell_volume:

    """opt_example class"""

    def activate_cm_shell_volume(self):
        self.register_command_topic('cloud','volume')
        pass

    @command
    def do_volume(self, args, arguments):
        """
        Usage:
            volume list
            volume create <size>
                          [--snapshot-id=<snapshot-id>]
                          [--image-id=<image-id>]
                          [--display-name=<display-name>]
                          [--display-description=<display-description>]
                          [--volume-type=<volume-type>]
                          [--availability-zone=<availability-zone>]
            volume delete <volume>
            volume attach <server> <volume> <device>
            volume detach <server> <volume>
            volume show <volume>
            volume snapshot-list
            volume snapshot-create <volume-id>
                                   [--force]
                                   [--display-name=<display-name>]
                                   [--display-description=<display-description>]
            volume snapshot-delete <snapshot>
            volume snapshot-show <snapshot>
            volume help


        volume management

        Arguments:
            <size>            Size of volume in GB
            <volume>          Name or ID of the volume to delete
            <volume-id>       ID of the volume to snapshot
            <server>          Name or ID of server(VM).
            <device>          Name of the device e.g. /dev/vdb. Use "auto" for 
                              autoassign (if supported)
            <snapshot>        Name or ID of the snapshot

        Options:
            --snapshot-id <snapshot-id>
                                    Optional snapshot id to create the volume from.
                                    (Default=None)
            --image-id <image-id>
                                    Optional image id to create the volume from.
                                    (Default=None)
            --display-name <display-name>
                                    Optional volume name. (Default=None)
            --display-description <display-description>
                                    Optional volume description. (Default=None)
            --volume-type <volume-type>
                                    Optional volume type. (Default=None)
            --availability-zone <availability-zone>
                                    Optional Availability Zone for volume. (Default=None)
            --force                 Optional flag to indicate whether to snapshot a volume
                                    even if its attached to an instance. (Default=False)
                                    
        Description:
            volume list
                List all the volumes
            volume create <size> [options...]
                Add a new volume
            volume delete <volume>
                Remove a volume   
            volume attach <server> <volume> <device>
                Attach a volume to a server    
            volume-detach <server> <volume>
                Detach a volume from a server
            volume show <volume>        
                Show details about a volume
            volume snapshot-list
                List all the snapshots
            volume snapshot-create <volume-id> [options...]
                Add a new snapshot
            volume snapshot-delete <snapshot>
                Remove a snapshot
            volume-snapshot-show <snapshot>
                Show details about a snapshot
            volume help 
                Prints the nova manual

        """
        # log.info(arguments)
        
        keys = os.environ.keys()
        items = ['OS_USERNAME','OS_PASSWORD','OS_TENANT_NAME','OS_AUTH_URL']
        for item in items:
            if item not in keys:
                Console.warning("Please first update the environment variables from the cloud by: "
                                "nova set [CLOUD]")
                return

        if arguments["help"]:
            os.system("nova help")

        elif arguments['list']:
            os.system('nova volume-list')
            
        elif arguments['create']:
            command = "nova volume-create " + arguments['<size>']
            for item in ['--snapshot-id',
                         '--image-id',
                         '--display-name',
                         '--display-description',
                         '--volume-type',
                         '--availability-zone']:
                if arguments[item]:
                    command = command + " {0} {1}".format(item, arguments[item])
            os.system(command)
               
        elif arguments['delete']:
            os.system("nova volume-delete {0}".format(arguments['<volume>']))
            
        elif arguments['attach']:
            os.system("nova volume-attach {0} {1} {2}".format(arguments['<server>'],
                                                              arguments['<volume>'],
                                                              arguments['<device>']))
            
        elif arguments['detach']:
            os.system("nova volume-detach {0} {1}".format(arguments['<server>'],
                                                          arguments['<volume>']))
        
        elif arguments['show']:
            os.system("nova volume-show {0}".format(arguments['<volume>']))
            
        elif arguments['snapshot-create']:
            command = "nova volume-snapshot-create " + arguments['<volume-id>']
            for item in ['--display-name',
                         '--display-description']:
                if arguments[item]:
                    command = command + " {0} {1}".format(item, arguments[item])
            if arguments['--force']:
                command = command + " --force True"
            os.system(command)
        
        elif arguments['snapshot-delete']:
            os.system("nova volume-snapshot-delete {0}".format(arguments['<snapshot>']))
            
        elif arguments['snapshot-list']:
            os.system('nova volume-snapshot-list')
        
        elif arguments['snapshot-show']:
            os.system("nova volume-snapshot-show {0}".format(arguments['<snapshot>']))
            
        else:
            print(arguments)
            return


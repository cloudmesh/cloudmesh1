from __future__ import print_function
import os
from cloudmesh_common.tables import print_format_dict, two_column_table

from cmd3.console import Console
from cmd3.shell import command
import json
from cloudmesh.user.cm_user import cm_user
from cloudmesh.config.cm_config import cm_config
from pprint import pprint


class cm_shell_ssh:

    def activate_cm_shell_ssh(self):
        self.register_command_topic('ssh', 'ssh')
        userid = self.cm_config.username()
        print (userid)
        user = {'userid': userid}
        self.ssh_machines = {'bravo': 'ssh -t {userid}@india.futuregrid.org  "/opt/torque/bin/qsub -I -q bravo"'.format(**user),
                             'delta': 'ssh -t {userid}@india.futuregrid.org  "/opt/torque/bin/qsub -I -q delta"'.format(**user),
                             'echo': 'ssh -t {userid}@india.futuregrid.org  "/opt/torque/bin/qsub -I -q echo"'.format(**user)}
        pass

    @command
    def do_ssh(self, args, arguments):
        """
        ::

          Usage:
              ssh list [--format=json|yaml]
              ssh register NAME COMMANDS
              ssh NAME


          conducts a ssh login into a machine while using a set of
          registered commands under the name of the machine.

          Arguments:

            NAME      Name of the machine to log in
            list      Lists the machines that are registered and
                      the commands to login to them
            register  Register the commands to a name
            COMMANDS  The list of commands executed when issuing a name

          Options:

             -v       verbose mode

        """
        pprint(arguments)

        if arguments["list"]:
            if 'json' == arguments["--format"]:
                print (print_format_dict(self.ssh_machines, kind='json'))
            elif 'yaml' == arguments["--format"]:
                print (print_format_dict(self.ssh_machines, kind='yaml'))
            else:
                print (two_column_table(self.ssh_machines,  header=['Machines', 'Commands']))

        elif arguments["register"]:
            Console.error("NOT YET IMPLEMENTED")
        else:
            machine = arguments["NAME"]
            if machine in self.ssh_machines:
                commands = self.ssh_machines[machine]
                print (commands)
                Console.info ("login to " + machine)
                os.system(commands)
            else:
                Console.error("machine " + machine + " not found")
            
            
        # shell_command_open_ssh(arguments)
        pass

# if __name__ == '__main__':
#    command = cm_shell_ssh()
#    command.do_ssh("")

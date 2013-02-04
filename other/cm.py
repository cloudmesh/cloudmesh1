"""cm.

Usage:
  cm.py init --user <user> --pass <passphrase>
  cm.py log (<FILENAME> | --on | --off)
  cm.py project --list [<number>]
  cm.py project --info <number>
  cm.py project --activate <number>
  cm.py project --deactivate
  cm.py project --charge <amount>
  cm.py project --refund <amount>
  cm.py project --ballance
  cm.py project --cost <action>
  cm.py env
  cm.py list (resource | service | image | id)
  cm.py cloud --list
  cm.py cloud --activate --service (eucalyptus|openstack) --host (india|sierra|bravo|delta|alamo) 
  cm.py cloud --activate --service (azure|aws) --zone <zone>
  cm.py cloud --activate --service trystack 
  cm.py vm id <id> <label>
  cm.py vm create <label>
  cm.py vm destroy <label>
  cm.py vm terminate <label>
  cm.py vm info <label>
  cm.py vm status <label>
  cm.py -h | --help
  cm.py --version
  cm.py -cool <parameter>

Options:
  -h --help       Shows the help message.
  --version       Show the version.
  --cloud=<iaas>  Default IaaS CLoud set to OpenStack [default: openstack].
  --resouce=<resource> Default FG resource [default:india].

"""
from docopt import docopt
import warnings
import inspect

# class accounting managed in its own file and interfaces with gold. we want a gold and non gold provider
# non gold provider uses mongodb

def manage_project_commands(arguments):
    warnings.warn("Manage Project commands")
    if arguments["--list"]:
        print "list"
    elif arguments["--info"]:
        # check is number exists, if not error, if empty return all 
        number = arguments["<number>"]
        print number
        #account.list(number)
    elif arguments["--activate"]:
        print arguments["<number>"]
        #account.activate(user, number)
    elif arguments["--deactivate"]:
        print "deactivate"
        #account.deactivate()
    elif arguments["--charge"]:
        print arguments["<amount>"]
        #project must be activated previously
        # account.charge(user, project, amount)
    elif arguments["--refund"]:
        print arguments["<amount>"]
        #Users are not allowed to ask for refuds only the admin can do that or a system service
        #project must be activated previously
        # account.refund(user, project, amount)
    elif arguments["--ballance"]:
        print "ballance"
        #account.ballance()
    elif arguments["--cost"]:
        print arguments["<amount>"]
        #to be determined, suggests cost for certain actions
    else:
        warnings.warn("Problem parsing command")
    
def manage_list_commands(arguments):
    warnings.warn("Manage List commands")

def manage_log_commands(arguments):
    warnings.warn("Manage Log commands")
    if arguments["--on"]:
        warnings.warn("Log on")
    elif arguments["--off"]:
        warnings.warn("Log off")
    else:
        warnings.warn("Set Log File")
        filename = arguments["<FILENAME>"]
        print filename

def manage_env_commands(arguments):
    warnings.warn("Manage Env commands")

def manage_vm_commands(arguments):
    warnings.warn("Manage VM commands")
    label = arguments["<label>"]
    if arguments["id"]:
        warnings.warn("Manage VM id")
        id = arguments["<id>"]
        print label
        print id 
    elif arguments["create"]:
        warnings.warn("Manage VM create")
        print label
    elif arguments["destroy"]:
        warnings.warn("Manage VM destroy")
        print label
    elif arguments["terminate"]:
        warnings.warn("Manage VM terminate")
        print label
    elif arguments["info"]:
        warnings.warn("Manage VM info")
        print label
    elif arguments["status"]:
        warnings.warn("Manage VM status")
        print label


if __name__ == '__main__':
    arguments = docopt(__doc__, version='cm.py version 0.1')
    print(arguments)

    if arguments['list']:
        warnings.warn ('found list resource')
    elif arguments['log']:
        manage_log_commands(arguments)
    elif arguments['project']:
        manage_project_commands(arguments)
    elif arguments['env']:
        manage_env_commands(arguments)
    elif arguments['vm']:
        manage_vm_commands(arguments)
    elif arguments['cool']:
        manage_cool_commands(arguments)
    else:
        warnings.warn("command not found")


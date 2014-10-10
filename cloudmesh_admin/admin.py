"""cm-admin.

Usage:
  cm-admin server start
  cm-admin server stop
  cm-admin server status
 
Options:
  -h --help     Show this screen.
  --version     Show version.
 
"""

from fabfile.server import start, stop

from docopt import docopt
import cloudmesh

if __name__ == '__main__':
    arguments = docopt(__doc__, version=cloudmesh.__version__)
    print(arguments)

    if arguments['start']:
        print "start"
        start()
    elif arguments['stop']:
        print "stop"
        stop()
    elif arguments['status']:
        print "status"        

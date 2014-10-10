"""cm-admin.

Usage:
  cm-admin server start
  cm-admin server stop
  cm-admin server status
  cm-admin version
  
Options:
  -h --help     Show this screen.
  --version     Show version.
 
"""

from fabfile.server import start, stop, kill
from fabfile.queue import ls as queue_ls
from fabfile.mongo import info as mongo_info

from docopt import docopt
import cloudmesh

if __name__ == '__main__':
    arguments = docopt(__doc__, version=cloudmesh.__version__)
    print(arguments)

    if arguments['version']:
        print cloudmesh.__version__
    
    if arguments['start']:
        start()
    elif arguments['stop']:
        stop()
        kill()
    elif arguments['status']:
        print "status"
        queue_ls()
        mongo_info()

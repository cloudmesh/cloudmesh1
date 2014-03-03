from cherrypy import wsgiserver
from cm_wsapps import app
import os

d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
server = wsgiserver.CherryPyWSGIServer((os.environ["FG_HOSTING_IP"], 5001), d)

if __name__ == '__main__':
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
    except:
        server.stop()

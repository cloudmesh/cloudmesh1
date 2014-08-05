from cloudmesh_common.logger import LOGGER
from docopt import docopt
from cloudmesh.config.ConfigDict import ConfigDict
import os
import sys

log = LOGGER(__file__)

def shell_command_open_web(arguments):
    """
    Usage:
        web [LINK]

    Arguments:

        CLOUD    the link of the page to be opened

    Options:

        -v         verbose mode

    Description:
        
        Opens a web page with the specified link
        
    """
    
    link = arguments["LINK"]
    if link is None:
        link = ""
        
    try:

        web_browser = "firefox"

        if sys.platform == 'darwin':
            web_browser = "open"

        try:

            server_config = ConfigDict(filename="~/.futuregrid/cloudmesh_server.yaml")

            host = server_config.get("cloudmesh.server.webui.host")
            port = server_config.get("cloudmesh.server.webui.port")

        except Exception, e:

            print  "some error reading from the config file"
            print e   

        url_link = "http://{0}:{1}/{2}".format(host, port, link)

        os.system('%s "%s"' % (web_browser, url_link))
 
    except:
        raise Exception("ERROR: I could not view this page")

def main():
    arguments = docopt(shell_command_open_web.__doc__)
    shell_command_open_web(arguments)

if __name__ == '__main__':
    main()

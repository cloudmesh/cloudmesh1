from cloudmesh_common.logger import LOGGER
from docopt import docopt
from cloudmesh.config.ConfigDict import ConfigDict
import os
import sys
from cloudmesh_install import config_file

log = LOGGER(__file__)


def shell_command_open_web(arguments):
    """
    Usage:
        web [--fg|--cm] [LINK]

    Arguments:

        LINK    the link on the localhost cm server is opened.

    Options:

        -v         verbose mode
        --fg       opens a link on the FG portal
        --cm       opens a link on the CM portal

    Description:

        Opens a web page with the specified link

    """

    link = arguments["LINK"]
    if link is None or link == "/":
        link = ""

    web_browser = "firefox"
    if sys.platform == 'darwin':
        web_browser = "open"

    if arguments["--fg"]:
        location = "https://portal.futuregrid.org"
    elif arguments["--cm"]:
        location = "https://cloudmesh.futuregrid.org"
    else:
        try:
            filename = config_file("/cloudmesh_server.yaml")
            server_config = ConfigDict(filename=filename)

            host = server_config.get("cloudmesh.server.webui.host")
            port = server_config.get("cloudmesh.server.webui.port")
            location = "http://{0}:{1}".format(host, port)
        except Exception, e:
            print "ERROR: some error reading from the config file"
            print e
            return

    url_link = "{0}/{1}".format(location, link)
    print "opening", url_link

    try:
        os.system('%s "%s"' % (web_browser, url_link))
    except:
        raise Exception(
            "ERROR: I could not view this page {0} {1}".format(location, link))


def main():
    arguments = docopt(shell_command_open_web.__doc__)
    shell_command_open_web(arguments)

if __name__ == '__main__':
    main()

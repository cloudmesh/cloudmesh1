from __future__ import with_statement

import sys
from cloudmesh.util.logger import LOGGER

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)


# ----------------------------------------------------------------------
# TRY cloudmesh
# ----------------------------------------------------------------------

try:
   import cloudmesh
   # print "Version", cloudmesh.__version__
   # TODO: ful version does not work whne installed via setup.py install
   # thus we simply do not print for now.
   # print "Full Version", cloudmesh.__full_version__
except Exception, e:
    print "ERROR: could not find package\n\n   cloudmesh\n"
    print "please run first\n"
    print "     python setup.py install\n"
    print
    print "Exception"
    print e
    sys.exit()


from fabric.api import task, local, execute, hide, settings
from fabric.contrib.console import confirm
import os
import webbrowser
import platform

from cloudmesh.util.util import path_expand

__all__ = ['start', 'stop', 'kill', 'view', 'clean', 'cleanmongo', 'agent']

#
# SETTING THE BROWSER BASED ON PLATFORM
#
web_browser = "firefox"

if sys.platform == 'darwin':
    web_browser = "open"


#
# VERSION MANAGEMENT
#

#
# we are no longer doing version management with the VERSION.txt file,
# but instead including it in setup.py we need to change the code
# here, so do not use the version increment
#

# filename = "VERSION.txt"
# version = open(filename).read()

@task
def agent():
    # with settings(warn_only=True):
    #    local("killall ssh-agent")
    print 70 * "="
    print" PLEASE COPY THE FOLLOWING COMMNADS AND EXECUTE IN YOUR SHELL"
    print 70 * "="
    print ("eval `ssh-agent -s`")
    print("ssh-add")

@task
def stop(server="server"):
    """sma e as the kill command"""
    kill(server)

@task
def kill(server="server"):
    """kills all server processes """
    with settings(warn_only=True):
        with hide('output', 'running', 'warnings'):
            local("fab mongo.stop")
            result = local('ps -a | fgrep "python {0}.py" | fgrep -v fgrep'.format(server), capture=True).split("\n")
            for line in result:
                pid = line.split(" ")[0]
                local("kill -9 {0}".format(pid))

@task
def start(link="", server="server", port="5000", browser='yes'):
    """ starts in dir webgui the program server.py and displays a browser on the given port and link"""
    kill()
    local("python setup.py install")
    local("fab mongo.start")
    local("cd webui; python {0}.py &".format(server))
    if browser == 'yes':
        local("sleep 2; {0} http://127.0.0.1:{2}/{1}".format(web_browser, link, port))

@task
def view(link="inventory"):
    """run the browser"""
    local("sleep 1")
    local("%s http://localhost:5000/%s" % (web_browser, link))

@task
def clean():
    """clean the directory"""
    local("find . -name \"#*\" -exec rm {} \\;")
    local("find . -name \"*~\" -exec rm {} \\;")
    local("find . -name \"*.pyc\" -exec rm {} \\;")
    local("rm -rf build dist *.egg-info")
    local("rm -rf doc/build ")




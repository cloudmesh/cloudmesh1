from __future__ import with_statement

import sys
from cloudmesh_common.logger import LOGGER
from cloudmesh_install.util import banner
from cloudmesh_install import config_file
from cloudmesh_common.util import PROGRESS
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh_install.util import path_expand

from pprint import pprint

import fabric
from fabric.api import task, local, execute, hide, settings, run
from fabric.contrib.console import confirm
import os
import webbrowser
import platform

import queue
import mq
import progress
import mongo
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
    print
    print "     ./install cloudmesh\n"
    print
    print "Exception"
    print e
    sys.exit()


__all__ = ['start', 'stop', 'kill', 'view', 'clean', 'cleanmongo',
           'agent', 'quick', 'wsgi', 'web']

#
# SETTING THE BROWSER BASED ON PLATFORM
#
web_browser = "firefox"

debug = True
try:
    debug = cm_config_server().get("cloudmesh.server.debug")
except:
    pass

if debug:
    progress.off()
else:
    progress.on()

PROGRESS.set('Cloudmesh Services', 50)

if sys.platform == 'darwin':
    web_browser = "open"


def execute_command(msg, command, debug):
    _capture = not debug
    if debug:
        banner(msg, debug=debug)
    else:
        PROGRESS.next()
    local(command, capture=_capture)


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
def kill(server="server", debug=True):
    """kills all server processes """
    with settings(warn_only=True):
        execute_command("STOP MONGO", "fab mongo.stop", debug=debug)
        result = local(
            'ps -ax | fgrep "python {0}.py" | fgrep -v fgrep'.format(server), capture=True).split("\n")
        for line in result:
            if line is not '':
                pid = line.split(" ")[0]
                local("kill -9 {0}".format(pid))

        # local("fab queue.stop")


@task
def quick(server="server", browser='yes'):
    """ starts in dir webgui the program server.py and displays a browser on the given port and link"""

    banner("INSTALL CLOUDMESH")
    local("python setup.py install")

    banner("START WEB SERVER")
    local("cd cloudmesh_web; python {0}.py &".format(server))
    # view(link)


@task
def start(server="server", browser='yes', debug=False):
    """ starts in dir webgui the program server.py and displays a browser on the given port and link"""

    # pprint (fabric.state.output)

    """
        'aborts': True,
        'debug': False,
        'running': True,
        'status': True,
        'stderr': True,
        'stdout': True,
        'user': True,
        'warnings': True
        }
    """
    # banner(debug)

    banner("KILL THE SERVER", debug=debug)
    r = kill(debug=debug)
    if debug:
        print r
    else:
        PROGRESS.next()

    execute_command("INSTALL CLOUDMESH",
                    "python setup.py install",
                    debug=debug)

    mongo.start()
    # execute_command("START MONGO",
    #            "fab mongo.start",
    #            debug)

    queue.start()
    # execute_command("START RABITMQ",
    #        "fab queue.start", debug)

    queue.flower_server()
    # execute_command("START FLOWER",
    #        "fab queue.flower_server",
    #        debug)
    fabric.state.output.stdout = True
    fabric.state.output.stderr = True
    execute_command("START WEB SERVER",
                    "cd cloudmesh_web; python {0}.py &".format(server),
                    True)
    # view(link)
    PROGRESS.finish()
    # pprint (fabric.state.output)


@task
def web(server="server", browser='yes'):
    banner("START WEB SERVER")
    local("cd cloudmesh_web; python {0}.py &".format(server))
    # view(link)


@task
def view(link=""):
    """run the browser"""
    from cloudmesh.config.ConfigDict import ConfigDict

    server_config = ConfigDict(filename=config_file("/cloudmesh_server.yaml"))

    host = server_config.get("cloudmesh.server.webui.host")
    port = server_config.get("cloudmesh.server.webui.port")

    url_link = "http://{0}:{1}/{2}".format(host, port, link)

    local("%s %s" % (web_browser, url_link))
    # if browser == 'yes':
    #    local("sleep 2; {0} http://127.0.0.1:{2}/{1}".format(web_browser, link, port))


@task
def clean():
    """clean the directory"""
    local("find . -name \"#*\" -exec rm {} \\;")
    local("find . -name \"*~\" -exec rm {} \\;")
    local("find . -name \"*.pyc\" -exec rm {} \\;")
    local("rm -rf build dist *.egg-info")
    local("rm -rf doc/build ")


# For production server
@task
def wsgi(action="start"):
    pidfile = config_file("/uwsgi/cloudmesh_uwsgi.pid")
    logfile = config_file("/uwsgi/cloudmesh_uwsgi.log")
    command = False

    user_pidfile = os.path.expanduser(pidfile)
    user_logfile = os.path.expanduser(logfile)

    if action == "restart":
        wsgi("stop")
        action = "start"

    if action == "start":
        command = "uwsgi -s /tmp/cloudmesh.sock -M -p 2 -t 10 \
      --daemonize={0} \
      --pidfile={1} \
      --chown-socket=cloudmesh:www-data \
      --chdir=cloudmesh_web \
      --module=server \
      --callable=app".format(user_logfile, user_pidfile)
    elif (action == "stop" or action == "kill"):
        command = "kill -INT `cat {0}`".format(user_pidfile)
    elif (action == "reload"):
        command = "kill -HUP `cat {0}`".format(user_pidfile)
    if (command):
        local(command)

from __future__ import with_statement

import sys
from cloudmesh_base.logger import LOGGER
from cloudmesh_base.util import banner
from cloudmesh_base.Shell import Shell
from cloudmesh_base.locations import config_file
from cloudmesh_common.util import PROGRESS
from cloudmesh.config.cm_config import cm_config_server

import fabric
from fabric.api import task, local, settings
import os

import queue
import progress
import mongo
from build import cursor_on

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

__all__ = ['start', 'stop', 'kill', 'view', 'clean',
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
    # local("killall ssh-agent")
    print 70 * "="
    print" PLEASE COPY THE FOLLOWING COMMNADS AND EXECUTE IN YOUR SHELL"
    print 70 * "="
    print ("eval `ssh-agent -s`")
    print("ssh-add")


@task
def stop(server="server"):
    """sma e as the kill command"""
    kill(server)
    cursor_on()


@task
def kill(server="server", debug=True):
    """kills all server processes """
    with settings(warn_only=True):
        try:
            mongo.stop()
        except:
            print "ERROR: could not stop mongo"
        # execute_command("STOP MONGO", "fab mongo.stop", debug=debug)
        result = Shell.ps("-ax").split("\n")

        result = Shell.find_lines_with(result, "python {:}.py".format(server))
        result = Shell.remove_line_with(result, "fgrep")

        if result is None or len(result) == 0:
            print "ERROR: no process found to terminate"
        else:
            for line in result:
                if line is not '':
                    pid = line.split(" ")[0]
                    print "Killing process", pid
                    Shell.kill("-9", "{:}".format(pid))
                    # local("fab queue.stop")


@task
def quick(server="server", browser='yes'):
    """ starts in dir webgui the program server.py and displays a browser on the given port and link"""

    banner("INSTALL CLOUDMESH")
    os.system("python setup.py install")

    banner("START WEB SERVER")
    os.system("cd cloudmesh_web; python {0}.py &".format(server))
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
    kill(debug=debug)
    if not debug:
        PROGRESS.next()

    execute_command("INSTALL CLOUDMESH",
                    "python setup.py install",
                    debug=debug)

    mongo.start()
    # execute_command("START MONGO",
    # "fab mongo.start",
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
    os.system("cd cloudmesh_web; python {0}.py &".format(server))
    # view(link)


@task
def view(link=""):
    """run the browser"""
    from cloudmesh_base.ConfigDict import ConfigDict

    server_config = ConfigDict(filename=config_file("/cloudmesh_server.yaml"))

    host = server_config.get("cloudmesh.server.webui.host")
    port = server_config.get("cloudmesh.server.webui.port")

    url_link = "http://{0}:{1}/{2}".format(host, port, link)

    os.system("%s %s" % (web_browser, url_link))
    # if browser == 'yes':
    # local("sleep 2; {0} http://127.0.0.1:{2}/{1}".format(web_browser, link, port))


@task
def clean():
    """clean the directory"""
    commands='''
        find . -name \"#*\" -exec rm {} \\;
        find . -name \"*~\" -exec rm {} \\;
        find . -name \"*.pyc\" -exec rm {} \\;
        rm -rf build dist *.egg-info
        rm -rf doc/build
    '''
    for command in commands.split("\n"):
        print(command)
        os.system(command)

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
    elif action == "stop" or action == "kill":
        command = "kill -INT `cat {0}`".format(user_pidfile)
    elif action == "reload":
        command = "kill -HUP `cat {0}`".format(user_pidfile)
    if command:
        local(command)

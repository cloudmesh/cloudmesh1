from fabric.api import task, local, execute
import clean
import os
import sys
import platform
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.util.password import get_password, get_user, get_host
from cloudmesh.util.menu import ascii_menu
from cloudmesh_common.util import yn_choice, path_expand
from pprint import pprint
from sh import mkdir
from cloudmesh_common.util import PROGRESS
from cloudmesh_common.logger import LOGGER
log = LOGGER(__file__)

PROGRESS.set('Cloudmesh Services', 10)

rabbit_env = {
    'rabbitmq_server': "sudo rabbitmq-server",
    'rabbitmqctl': "sudo rabbitmqctl",
    'detached': ""
    }

def set_rabbitmq_env():

    global RABBITMQ_SERVER
    
    location = path_expand("~/.cloudmesh/rabbitm")
    
    if sys.platform == "darwin":
        mkdir("-p", location)
        rabbit_env["RABBITMQ_MNESIA_BASE"] = location
        rabbit_env["RABBITMQ_LOG_BASE"] = location        
        os.environ["RABBITMQ_MNESIA_BASE"] = location
        os.environ["RABBITMQ_LOG_BASE"] = location
        rabbit_env["rabbitmq_server"]="/usr/local/opt/rabbitmq/sbin/rabbitmq-server"
        rabbit_env["rabbitmqctl"]="/usr/local/opt/rabbitmq/sbin/rabbitmqctl"        
    elif sys.platform == "linux2":
        mkdir("-p", location)
        rabbit_env["RABBITMQ_MNESIA_BASE"] = location
        rabbit_env["RABBITMQ_LOG_BASE"] = location        
        os.environ["RABBITMQ_MNESIA_BASE"] = location
        os.environ["RABBITMQ_LOG_BASE"] = location
        rabbit_env["rabbitmq_server"]="/usr/sbin/rabbitmq-server"
        rabbit_env["rabbitmqctl"]="/usr/sbin/rabbitmqctl"        
    else:
        print "WARNING: cloudmesh rabbitmq user install not supported, " \
          "using system install"

set_rabbitmq_env()        
                
input = raw_input

__all__ = ['user',
           'install',
           'host',
           'allow',
           'check',
           "dns",
           "status",
           "start",
           "stop",
           "menu",
           "memory",
           "conumers",
           "msg",
           "info"]

PRODUCTION=cm_config_server().get('cloudmesh.server.production')



def installed(name):
    """check if the command with the name is installed and return true if it is"""
    result = local("which {0} | wc -l".format(name), capture=True)
    return result > 0

@task
def install():
    if PRODUCTION:
        print "Installation not enabled in production mode."
        sys.exit()
    """install the rabbitmq"""
    if sys.platform == "darwin":
        local("brew install rabbitmq")
        if not installed("rabbitmqctl"):
            print("ERROR: make sure /usr/local/sbin/ is added to your PATH")
    elif sys.platform == "linux":
        # TODO: untested
        local("sudo apt-get install rabbitmq-server")
        # when completed we see:
        # Starting rabbitmq-server: SUCCESS.
    else:
        print "ERROR: error no other install yet provided "
        sys.exit()

@task
def user(name=None):
    ''' create a user in rabbit mq
    
    :param name: if the name is ommited it will be queried for it.
    '''
    if name is None:
        rabbit_env["user"] = get_user()
    rabbit_env["password"] = get_password()
    local("{rabbitmqctl} {user} {password}".format(**rabbit_env))

@task
def host():
    """adding a host to rabbitmq"""
    rabbit_env["host"] = get_host()        
    local("{rabbitmqctl} add_vhost {host}".format(**rabbit_env))

@task
def allow():
    """allow a user to access the host in rabbitmq"""
    # print('{rabbitmqctl} set_permissions -p {host} {user} ".*" ".*" ".*"'.format(**rabbit_env))
    rabbit_env["host"] = get_host()
    rabbit_env["user"] = get_user()    
    local('{rabbitmqctl} set_permissions -p {host} {user} ".*" ".*" ".*"'.format(**rabbit_env))

@task
def check():
    """check if the /etc/hosts file is properly configures"""
    values = {
        'host': platform.node(),
        'hostname': platform.node().replace(".local", ""),
        'file': '/etc/hosts'
        }
    result = int(local("fgrep {host} {file} | wc -l".format(**values), capture=True))
    if result == 0:
        print ('ERROR: the etc file "{file}" does not contain the hostname "{host}"'.format(**values))
        print
        print ("make sure to add a line such as")
        print
        print ("127.0.0.1       localhost {hostname} {host}".format(**values))
        print
        print ("make sure to restart the dns server after you changed the etc host file")
        print ("do this with fab mq.dns")

@task
def dns():
    """restart the dns server"""
    local("dscacheutil -flushcache")

@task
def info():
    """print some essential information about the messaging system"""
    status()
    l = ["name", "memory", "consumers", "messages", "messages_ready", "messages_unacknowledged"]
    r = list_queues(" ".join(l)).split("\n")[1].split("\t")
    print r

    d = zip(l, r)
    pprint (d)

@task
def status():
    """print the status of rabbitmq"""
    if PRODUCTION:
        print "Run '/etc/init.d/rabbitmq-server status' to check status"
    else:
        local("sudo {rabbitmqctl} status".format(**rabbitmq_env))

def list_queues(parameters):
    """list all queues available in rabbitmq"""
    if PRODUCTION:
        print "Use 'rabbitmqctl list_queues' to list queues"
    else:
        rabbit_env['parameters'] = parameters
        r = local("{rabbitmqctl} list_queues {parameters}".format(**rabbit_env),
                                                     capture=True)
    return r

@task
def start(detached=None):
    """start the rabbit mq server"""
    if PRODUCTION:
        print "Run '/etc/init.d/rabbitmq-server start' to start server"
        while not yn_choice("Is rabbitmq running?", 'n'):
            print "Please start rabbitmq-server."
    else:
        PROGRESS.next()
        print
        if detached is None:
            rabbit_env['detached'] = "-detached"
        # log.info (rabbit_env)
        local("{rabbitmq_server} {detached}".format(**rabbit_env))

@task
def stop():
    """stop the rabbit mq server"""
    if PRODUCTION:
        print "Run '/etc/init.d/rabbitmq-server stop' to stop server"
        while not yn_choice("Is rabbitmq stopped?", 'n'):
            print "Please stop rabbitmq-server."
    else:
        local("{rabbitmqctl} stop".format(**rabbit_env))


menu_list = [
    ('install', install),
    ('dns', dns),
    ('host', host),
    ('user', user),
    ('allow', allow),
    ('check', check),
    ('status', status),
    ('start', start),
    ('stop', stop)
    ]

@task
def menu():
    """open a menu to start some commands with an ascii menu"""
    ascii_menu("RabbitMQ", menu_list)


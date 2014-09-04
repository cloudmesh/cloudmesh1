from fabric.api import task, local, settings, hide
from pprint import pprint
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh.user.cm_userLDAP import cm_userLDAP
from cloudmesh.pbs.pbs_mongo import pbs_mongo
from cloudmesh_common.util import path_expand
from cloudmesh_common.util import banner
from cloudmesh_common.util import yn_choice
from cloudmesh.inventory import Inventory
from sh import ls
import sys
import os
import time


def get_pid(command):
    with hide('output', 'running', 'warnings'):
        lines = local(
            "ps -ax |fgrep {0}".format(command), capture=True).split("\n")
    pid = None
    line = None
    for line in lines:
        if "fgrep" not in line:
            pid = line.split(" ")[0]
            break
    if pid is None:
        print "No mongod running"
    else:
        print "SUCCESS: mongod PID", pid
    return (pid, line)


@task
def reset():
    local("fab mongo.boot")
    local("fab user.mongo")
    local("fab mongo.simple")


@task
def install():
    """installs mongo in ~/ENV/bin. Make sure your path is set correctly"""
    if sys.platform == "darwin":
        os_version = "osx"
    elif sys.platform in ["linux", "linux2"]:
        os_version = "linux"
    else:
        print "ERROR: Wrong opertaing system: Found", sys.platform
        sys.exit()

    ENV = os.environ['VIRTUAL_ENV'] + "/bin"

    if not ENV.endswith("ENV/bin"):
        print "WARNING: You are using a non standrad development "\
            "virtualenv location"
        print "         The standard location is", path_expand("~/ENV/bin")
        print "         You use", ENV
        if not yn_choice("Would you like to proceed", default="n"):
            sys.exit()
    else:
        print "SUCCESS: You use the standard virtualenv setup"
        print "         The standard location is", path_expand("~/ENV/bin")

    mongo_version = "mongodb-{0}-x86_64-2.4.6".format(os_version)
    mongo_tar = "{0}.tgz".format(mongo_version)
    # for some reason with does not work
    # with cd('/tmp'):

    if os.path.isfile("/tmp/{0}".format(mongo_tar)):
        print "WRANING: mongo tar file already downloaded"
        print "         using", "/tmp/{0}".format(mongo_tar)
    else:
        if sys.platform == "darwin":
            local(
                "cd /tmp; curl -O http://fastdl.mongodb.org/{1}/{0}.tgz"
                .format(mongo_version, os_version))
        else:
            local(
                "cd /tmp; wget http://fastdl.mongodb.org/{1}/{0}.tgz"
                .format(mongo_version, os_version))

    local("cd /tmp; tar -xvf {0}.tgz".format(mongo_version))
    local("cd /tmp; cp {0}/bin/* {1}".format(mongo_version, ENV))
    where = local("which mongo", capture=True)

    if where.startswith(ENV):
        print "SUCCESS. mongo commands are now installed in", ENV
    else:
        print "ERROR: mongo is not in the path"
        print "       it should be in", ENV
        print "       we found it in", where

    if is_ubuntu():
        install_packages(["mongodb"])
    elif is_centos():
        install_packages(["mongodb",
                          "mongodb-server"])
    elif sys.platform == "darwin":
        local(
            'ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"')
        local('brew update')
        local('brew install mongodb')


@task
def admin():
    """creates a password protected user for mongo"""

    banner("create auth user")
    config = cm_config_server().get("cloudmesh.server.mongo")

    user = config["username"]
    password = config["password"]

    #
    # setting up the list of dbs
    #
    dbs = set()
    # print config["collections"]
    for collection in config["collections"]:
        dbs.add(config['collections'][collection]['db'])

    # setting the admin user
    script = []
    script.append('db.addUser("{0}", "{1}");'.format(user, password))
    script.append('db.auth("{0}", "{1}");'.format(user, password))

    # setting a password for each db

    for db in dbs:
        script.append('db = db.getSiblingDB("{0}");'.format(db))
        script.append('db.addUser("{0}", "{1}");'.format(user, password))
    script.append("use admin;")
    script.append('db.addUser("{0}", "{1}");'.format(user, password))
    script.append('db.auth("{0}", "{1}");'.format(user, password))
    script.append('db.shutdownServer();')

    mongo_script = '\n'.join(script)

    # print mongo_script

    command = "echo -e '{0}' | mongo".format(mongo_script)
    print command
    banner("Executing js")
    os.system(command)

    banner("Debugging reminder, remove in final version")
    print "USER", user
    print "PASSWORD", password


@task
def wipe():
    """wipes out all traces from mongo"""
    kill()
    config = cm_config_server().get("cloudmesh.server.mongo")

    path = path_expand(config["path"])

    banner("{0}".format(path))
    local("mkdir -p {0}".format(path))
    result = str(ls(path))
    banner(path, "-")
    print result
    print 70 * "-"
    if result != "":
        if yn_choice("deleting the directory", default="n"):
            local("rm -rf {0}".format(path))
            local("mkdir -p {0}".format(path))
            banner("{0}".format(path))
            local("ls {0}".format(path))


def isyes(value):
    check = str(value).lower()
    if check in ['true', 'false', 'y', 'n', 'yes', 'no']:
        return check in ['true', 'y', 'yes']
    else:
        print "parameter not in", ['true', 'false', 'y', 'n', 'yes', 'no']
        print "found", value, check
        sys.exit()


@task
def boot(auth=True):

    # wipe mongo
    wipe()

    time.sleep(1)

    # start mongo without auth
    start(auth=False)

    time.sleep(2)

    if isyes(auth):

        # create users
        admin()

        time.sleep(2)

        # restart with auth
        kill()

        time.sleep(10)

        start(auth=auth)

        time.sleep(1)

    config = cm_config_server().get("cloudmesh.server.mongo")
    path = path_expand(config["path"])
    banner(path)
    print ls(path)
    banner("PROCESS")
    with settings(warn_only=True):
        local("ps -ax | fgrep mongo")


@task
def start(auth=True):
    '''
    start the mongod service in the location as specified in
    cloudmesh_server.yaml
    '''
    banner("Starting mongod")
    config = cm_config_server().get("cloudmesh.server.mongo")

    path = path_expand(config["path"])
    port = config["port"]

    if not os.path.exists(path):
        print "Creating mongodb directory in", path
        local("mkdir -p {0}".format(path))

    with settings(warn_only=True):
        with hide('output', 'running', 'warnings'):
            lines = local(
                "ps -ax |grep '[m]ongod.*port {0}'".format(port), capture=True)\
                .split("\n")

    if lines != ['']:
        pid = lines[0].split(" ")[0]
        print "NO ACTION: mongo already running in pid {0} for port {1}"\
            .format(pid, port)
    else:
        print "ACTION: Starting mongod"
        with_auth = ""
        if isyes(auth):
            with_auth = "--auth"

        local(
            'mongod {2} --bind_ip 127.0.0.1 '
            '--fork --dbpath {0} '
            '--logpath {0}/mongodb.log '
            '--port {1}'
            .format(path, port, with_auth))


@task
def clean():
    port = cm_config_server().get("cloudmesh.server.mongo.port")
    result = local(
        'echo "show dbs" | mongo --quiet --port {0}'
        .format(port), capture=True).splitlines()
    for line in result:
        name = line.split()[0]
        local('mongo {0} --port {1} --eval "db.dropDatabase();"'
              .format(name, port))


@task
def inventory():
    mesh_inventory = Inventory()
    mesh_inventory.clear()
    mesh_inventory.generate()
    mesh_inventory.info()


@task
def info():
    (pid, line) = get_pid("mongod")
    print line


@task
def kill():
    stop()


@task
def stop():
    '''
    stops the currently running mongod
    '''
    # for some reason shutdown does not work
    # local("mongod --shutdown")
    with settings(warn_only=True):
        with hide('output', 'running', 'warnings'):
            local("killall -15 mongod")

    # (pid, line) = get_pid("mongod")
    # if pid is None:
    #     print "No mongod running"
    # else:
    #     print "Kill mongod"
    #     local ("killall -15 mongod")


@task
def vms_find():
    user = cm_config().get("cloudmesh.hpc.username")
    c = cm_mongo()
    c.activate(user)
    pprint(c.servers())


def refresh(types):

    user = cm_config().get("cloudmesh.hpc.username")

    c = cm_mongo()
    c.activate(user)
    c.refresh(user, types=types)


@task
def cloud():
    '''
    puts a snapshot of users, servers, images, and flavors into mongo
    '''
    refresh(types=['users', 'servers', 'images', 'flavors'])
    ldap()
    inventory()


@task
def simple():
    '''
    puts a snapshot of servers, images, and flavors into mongo (no users)
    '''
    refresh(types=['servers', 'images', 'flavors'])
    inventory()


@task
def users():
    '''
    puts a snapshot of the users into mongo
    '''
    refresh(types=['users'])


@task
def errormetric():
    """puts an example of a log file into the mongodb logfile"""
    # create the mongo object
    # parse the log file
    # put each error form the sql databse in toit


@task
def ldap(username=None):
    '''
    fetches a user list from ldap and displays it
    '''

    idp = cm_userLDAP()
    idp.connect("fg-ldap", "ldap")
    if username:
        idp.refresh_one(username)
    else:
        idp.refresh()
    _users = idp.list()

    print _users
    print ("Fetching {0} Users from LDAP".format(len(_users)))


# @task
# def fg():
#     """create a simple testbed"""
#     start()
#     local("python cloudmesh_web/fg.py")


@task
def projects():
    print "NOT IMPLEMENTED YET"
    print "this class will when finished be able to import project titles" \
        " and description from the fg portal"


@task
def pbs(host, kind):

    _pbs = pbs_mongo()

    # get hpc user

    config = cm_config()
    user = config.get("cloudmesh.hpc.username")

    _pbs.activate(host, user)

    print "ACTIVE PBS HOSTS", _pbs.hosts

    if host is None:
        hosts = _pbs.hosts
    else:
        hosts = [host]

    if kind is None:
        types = ['qstat', 'nodes']
    else:
        types = [kind]

    d = []

    for host in hosts:
        for kind in types:
            if kind in ["qstat", "queue", "q"]:
                d = _pbs.get_pbsnodes(host)
            elif kind in ["nodes"]:
                d = _pbs.refresh_pbsnodes(host)

    for e in d:
        print "PBS -->"
        pprint(e)

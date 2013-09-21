from fabric.api import task, local, settings
from pprint import pprint
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh.user.cm_userLDAP import cm_userLDAP
from cloudmesh.pbs.pbs_mongo import pbs_mongo
from cloudmesh.util.util import path_expand as cm_path_expand
from cloudmesh.util.util import banner
from cloudmesh.inventory import Inventory
from cloudmesh.user.cm_template import cm_template
from cloudmesh.config.ConfigDict import ConfigDict

import yaml
import sys
import os.path

def get_pid(command):
    lines = local("ps -ax |fgrep {0}".format(command), capture=True).split("\n")
    pid = None
    for line in lines:
        if not "fgrep" in line:
            pid = line.split(" ")[0]
            break
    return (pid, line)

@task
def user():
    """
    creates a user from tempalte and a simplified version of the yaml file and
    puts it into mongo as a profile
    """
    print "NOT YET IMPLEMENTED"

    user_config = ConfigDict(filename="~/.futuregrid/me.yaml")

    banner("CONFIG DICT")
    print user_config


    t = cm_template("~/.futuregrid/etc/cloudmesh.yaml")

    banner("VARIBALES")
    print '\n'.join(t.variables())

    banner("REPLACE")
    result = t.replace(kind="dict", values=user_config)

    banner("TEMPLATE")
    print t

    banner("CONFIG")
    # print result
    print yaml.dump(result, default_flow_style=False)

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
def start():
    '''
    start the mongod service in the location as specified in
    ~/.futuregrid/cloudmesh_server.yaml
    '''
    path = cm_path_expand(cm_config_server().get("mongo.path"))
    port = cm_config_server().get("mongo.port")

    if not os.path.exists(path):
        print "Creating mongodb directory in", path
        local("mkdir -p {0}".format(path))

    lines = local("ps -ax |fgrep mongod ", capture=True).split("\n")
    (pid, line) = get_pid("mongod")

    if not pid is None:
        print "mongo already running in pid", pid
    else:
        print "Starting mongod"
        local("mongod --fork --dbpath {0} --logpath {0}/mongodb.log --port {1}".format(path, port))



@task
def stop():
    '''
    stops the currently running mongod
    '''
    # for some reason shutdown does not work
    # local("mongod --shutdown")
    (pid, line) = get_pid("mongod")
    if pid is None:
        print "No mongod running"
    else:
        print "Kill mongod"
        local ("kill -9 {0}".format(pid))

@task
def clean():
    '''
    deletes _ALL_ databases from mongo. Even thos not related to cloudmesh.
    '''
    local("make clean")
    result = local('echo "show dbs" | mongo --quiet ', capture=True).splitlines()
    for line in result:
        name = line.split()[0]
        local('mongo {0} --eval "db.dropDatabase();"'.format(name))

@task
def vms_find():
    c = cm_mongo()
    c.activate()
    pprint (c.servers())

@task
def cloud():
    '''
    puts a snapshot of users, servers, images, and flavors into mongo
    '''
    clean()
    c = cm_mongo()
    c.activate()
    c.refresh(types=['users', 'servers', 'images', 'flavors'])
    ldap()
    inventory()

@task
def simple():
    '''
    puts a snapshot of servers, images, and flavors into mongo (no users)
    '''
    clean()
    c = cm_mongo()
    c.activate()
    c.refresh(types=['servers', 'images', 'flavors'])
    inventory()

@task
def metric():
    """puts an example of a log file into the mongodb logfile"""
    log_file = path_expand("~/.futuregrid/metric/sierra-sample.log")
    # create the mongo object
    # parse the log file
    # put each log information into the mongodb (or an obkject an than to mongodb)
    # maybe you do not need to parese log files for openstack but just read it from sql???

@task
def errormetric():
    """puts an example of a log file into the mongodb logfile"""
    # create the mongo object
    # parse the log file
    # put each error form the sql databse in toit


@task
def users():
    '''
    puts a snapshot of the users into mongo
    '''
    c = cm_mongo()
    c.activate()
    c.refresh(types=['users'])


@task
def ldap():
    '''
    fetches a user list from ldap and displays it
    '''

    idp = cm_userLDAP ()
    idp.connect("fg-ldap", "ldap")
    idp.refresh()

    users = idp.list()

    print ("Fetching {0} Users from LDAP".format(len(users)))

'''
@task
def fg():
    """create a simple testbed"""
    start()
    local("python webui/fg.py")    
'''

@task
def pbs(host, type):
    pbs = pbs_mongo()

    # get hpc user

    config = cm_config()
    user = config.config["cloudmesh"]["hpc"]["username"]


    pbs.activate(host, user)

    print "ACTIVE PBS HOSTS", pbs.hosts

    if host is None:
        hosts = pbs.hosts
    else:
        hosts = [host]

    if type is None:
        types = ['qstat', 'nodes']
    else:
        types = [type]

    d = []

    for host in hosts:
        for type in types:
            if type in  ["qstat", "queue", "q"]:
                d = pbs.get_pbsnodes(host)
            elif type in ["nodes"]:
                d = pbs.refresh_pbsnodes(host)

    for e in d:
        print "PBS -->"
        pprint(e)


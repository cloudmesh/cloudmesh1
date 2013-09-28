from fabric.api import task, local, settings, hide, run
from pprint import pprint
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh.user.cm_userLDAP import cm_userLDAP
from cloudmesh.pbs.pbs_mongo import pbs_mongo
from cloudmesh.util.util import path_expand as path_expand
from cloudmesh.util.util import banner
from cloudmesh.inventory import Inventory
from cloudmesh.user.cm_template import cm_template
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.user.cm_user import cm_user
from cloudmesh.util.util import yn_choice
from sh import keystone
from sh import less
from  yaml import dump as yaml_dump
import sys
import os.path
import os

@task
def yaml():
    """
    creates a user from tempalte and a simplified version of the yaml file and
    puts it into mongo as a profile
    
    """
    new_yaml = path_expand('~/.futuregrid/cloudmesh-new.yaml')
    old_yaml = path_expand('~/.futuregrid/cloudmesh.yaml')

    t = cm_template("~/.futuregrid/etc/cloudmesh.yaml")

    t.generate("~/.futuregrid/me.yaml",
               new_yaml)
    if yn_choice("Review the new yaml file", default='n'):
        os.system ("less -E {0}".format(new_yaml))
    if yn_choice("Move the new yaml file to {0}".format(old_yaml), default='y'):
        os.rename (new_yaml, old_yaml)

@task
def list():
     user = cm_user()
     list_of_users = user.list_users()
     pprint (list_of_users)
     print
     print "========================="
     num = len(list_of_users)
     print str(num) + " users listed"

@task
def info(id):
    user = cm_user()
    res = user.info(id)
    pprint (res)

@task
def password():
    user_config = cm_config(filename="~/.futuregrid/cloudmesh.yaml")
    user = user_config.cloud('sierra_openstack_grizzly')['credentials']

    server_config = ConfigDict(filename="~/.futuregrid/cloudmesh_server.yaml")
    server = server_config['keystone']['sierra_openstack_grizzly']

    print(" ".join(["keystone", "--os-username", server['OS_USERNAME'],
             "--os-password", server['OS_PASSWORD'],
             "--os-tenant-name", server['OS_TENANT_NAME'],
             "--os-auth-url", server['OS_AUTH_URL'],
             "user-password-update",
             "--pass", user['OS_PASSWORD'], user['OS_USERNAME']]))


    keystone("--os-username", server['OS_USERNAME'],
             "--os-password", server['OS_PASSWORD'],
             "--os-tenant-name", server['OS_TENANT_NAME'],
             "--os-auth-url", server['OS_AUTH_URL'],
             "user-password-update",
             "--pass", user['OS_PASSWORD'], user['OS_USERNAME'])


@task
def mongo():
    config = cm_config(filename="~/.futuregrid/cloudmesh.yaml")
    profile = config.profile()

    element = {
               "firstname" : profile["firstname"],
               "lastname" : profile["lastname"],
               "uidNumber" : profile["uid"],
               "phone" : profile["phone"],
               "gidNumber" : profile["gid"],
               "address" : profile["address"][0],
               "cm_user_id" : config.get("cloudmesh.hpc.username"),
               "email" : profile["e_mail"]
    }

    projects = {}

    active = config.get("cloudmesh.projects.active")

    if active != ['None']:
        projects["active"] = active

    completed = config.get("cloudmesh.projects.completed")
    if completed != ['None']:
        projects["completed"] = completed

    if projects != {}:
        element["projects"] = projects

    # get keys and clean the key titles (replace '.' with '_' due to mongo restriction)
    keys = config.get("cloudmesh.keys.keylist")
    for keytitle in keys.keys():
        if "." in keytitle:
            keycontent = keys[keytitle]
            newkeytitle = keytitle.replace(".", "_")
            del keys[keytitle]
            keys[newkeytitle] = keycontent
    element['keys'] = keys

    pprint (element)

    # hpc username as key
    username = element["cm_user_id"]
    # populate the local userinfo into the same mongo as though it were from LDAP.
    userstore = cm_userLDAP()
    userstore.updates(username, element)

from fabric.api import task, local, settings, hide, run
from pprint import pprint
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh.user.cm_userLDAP import cm_userLDAP
from cloudmesh.pbs.pbs_mongo import pbs_mongo
from cloudmesh_common.util import path_expand as path_expand
from cloudmesh_common.util import banner
from cloudmesh.inventory import Inventory
from cloudmesh.user.cm_template import cm_template
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.user.cm_user import cm_user
from cloudmesh_common.util import yn_choice
from sh import keystone
from sh import less
from  yaml import dump as yaml_dump
import sys
import os.path
import os
from cloudmesh_install import config_file

@task
def password():
    user_config = cm_config(filename=config_file("/cloudmesh.yaml"))
    user = user_config.cloud('sierra_openstack_grizzly')['credentials']

    server_config = ConfigDict(filename=config_file("/cloudmesh_server.yaml"))
    server = server_config.get('cloudmesh.server.keystone.sierra_openstack_grizzly')

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
def delete_defaults():
    filename = config_file("/cloudmesh.yaml")
    banner("reading data from {0}".format(filename))
    config = cm_config(filename=filename)
    username = config.get("cloudmesh.hpc.username")

    print username

    user = cm_user()

    user.set_defaults(username, {})
    # user.set_default_attribute(username, 'images', {})
    info(username)

@task
def register():

    config = cm_config()
    cm_user_id = config.get("cloudmesh.hpc.username")
    clouds = config.get("cloudmesh.clouds")

    user_obj = cm_user()

    for cloudname in config.cloudnames():
        user_obj.set_credential(cm_user_id,
                                cloudname,
                                clouds[cloudname]['credentials'])


@task
def mongo():
    register()

    filename = config_file("/cloudmesh.yaml")
    banner("reading data from {0}".format(filename))
    config = cm_config(filename=filename)

    profile = config.profile()

    element = {
               "firstname" : profile["firstname"],
               "lastname" : profile["lastname"],
               "uidNumber" : profile["uid"],
               "phone" : profile["phone"],
               "gidNumber" : profile["gid"],
               "address" : profile["address"][0],
               "cm_user_id" : config.get("cloudmesh.hpc.username"),
               "email" : profile["email"],
               "activeclouds" : config.get("cloudmesh.active")
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

    user_obj = cm_user()
    user_obj.init_defaults(username)

    # info disabled due to
    # NameError: global name 'info' is not defined
    #info(username)

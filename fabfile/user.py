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
    user = user_config.cloud('sierra')['credentials']

    server_config = ConfigDict(filename=config_file("/cloudmesh_server.yaml"))
    server = server_config.get('cloudmesh.server.keystone.sierra')

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
    database = Database()
    database.set_credentials()


@task
def mongo():
    from cloudmesh.server.database import Database

    database = Database()
    database.set_credentials()
    database.initialize_user()
    

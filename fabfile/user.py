from fabric.api import task, local, settings, hide
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
from cloudmesh.user.cm_user import cm_user

from  yaml import dump as yaml_dump
import sys
import os.path

@task
def yaml():
    """
    creates a user from tempalte and a simplified version of the yaml file and
    puts it into mongo as a profile
    
    """

    with hide('status'):
        user_config = ConfigDict(filename="~/.futuregrid/me.yaml")
        t = cm_template("~/.futuregrid/etc/cloudmesh.yaml")
        result = t.replace(kind="dict", values=user_config)
        print yaml_dump(result, default_flow_style=False)

@task
def list_users():
     user = cm_user()
     list_of_users = user.list_users()
     pprint (list_of_users)

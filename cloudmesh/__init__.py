"""
A package to manage virtual machines on various clouds infrastructures and bare metal images.
"""

#import pkg_resources
#__version_full__  = pkg_resources.get_distribution("cloudmesh").version

__version__ = '1.0'


def version():
    return __version__

import logging


def logger(on):
    logger = logging.getLogger()
    logger.disabeld = not on
    print logger.__dict__

    if on:
        logging.disable(logging.NOTSET)
    else:
        logging.disable(logging.CRITICAL)


from cloudmesh.util.helper import vm_name

try:
    from cloudmesh.sh.cm import shell
except:
    print "WARNING: cm not yet installed, skipping import"

from cloudmesh.config.cm_config import load as load

from cloudmesh.pbs.pbs import PBS

from cloudmesh.cm_mongo import cm_mongo
# from cloudmesh.cm_mongo2 import cm_mongo2

from cloudmesh.cm_mesh import cm_mesh
from cloudmesh_install.util import banner
from cloudmesh_install.util import path_expand
from cloudmesh_install.util import yn_choice

#from cloudmesh_install.util import grep


from cloudmesh.user.cm_user import cm_user as cm_user

# -----------------------------------------------------
# testing with m.py
from cloudmesh.iaas.cm_cloud import CloudManage
from cloudmesh.shell.cm_label import update_label, print_label
from cloudmesh.config.cm_keys import cm_keys_mongo
from cloudmesh.util.ssh import ssh_execute

# -----------------------------------------------------


def mesh(provider="yaml"):
    if provider in ["yaml"]:
        return cm_mesh()
    elif provider in ["mongo"]:
        return cm_mongo()


"""
# import sys
# __all__= ['cloudmesh', 'profile', 'accounting', 'config', 'iaas', 'inventory', 'util', 'iaas']

with_login = True


"""

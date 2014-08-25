"""
A package to manage virtual machines on various clouds infrastructures and bare metal images.
"""

"""
from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.config.cm_config import cm_config as load
from cloudmesh.config.cm_config import cm_config
from cloudmesh.pbs.pbs import PBS
from cloudmesh.cm_mesh import cloudmesh as mesh
from pbr import version

from cloudmesh.util.helper import vm_name 

__version__ = version.VersionInfo('cloudmesh')

# import pkg_resources
# __version_full__  = pkg_resources.get_distribution("cloudmesh").version

# import sys
# __all__= ['cloudmesh', 'profile', 'accounting', 'config', 'iaas', 'inventory', 'util', 'iaas']

with_login = True

def version():
    return __version__


"""

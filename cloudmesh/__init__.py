"""
A package to manage virtual machines on various clouds infrastructures and bare metal images.
"""

#import pkg_resources
#__version_full__  = pkg_resources.get_distribution("cloudmesh").version

__version__ = '1.0'

def version():
    return __version__

from cloudmesh.util.helper import vm_name 
from cloudmesh.sh.cm import shell

from cloudmesh.config.cm_config import cm_config as load


"""
from cloudmesh.config.cm_config import cm_config_server



from cloudmesh.config.cm_config import cm_config


from cloudmesh.pbs.pbs import PBS

    from cloudmesh.cm_mesh import cloudmesh as mesh
"""




"""
# import sys
# __all__= ['cloudmesh', 'profile', 'accounting', 'config', 'iaas', 'inventory', 'util', 'iaas']

with_login = True


"""

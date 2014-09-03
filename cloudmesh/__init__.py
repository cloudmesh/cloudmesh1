"""
A package to manage virtual machines on various clouds infrastructures and bare metal images.
"""

#import pkg_resources
#__version_full__  = pkg_resources.get_distribution("cloudmesh").version

__version__ = '1.0'

def version():
    return __version__

from cloudmesh.util.helper import vm_name

try:
    from cloudmesh.sh.cm import shell
except:
    print "WARNING: cm not yet installed, skipping import"
    
from cloudmesh.config.cm_config import load as load

from cloudmesh.pbs.pbs import PBS 
#from cloudmesh.cm_mongo import cm_mongo as mesh

#from cloudmesh.cm_mongo import cm_mongo

from cloudmesh.cm_mesh import cm_mesh

"""
def mesh(provider="yaml"):
    if provider in ["yaml"]:
        return cm_mesh()
    elif provider in ["mongo"]:
        return cm_mongo()
"""

"""
# import sys
# __all__= ['cloudmesh', 'profile', 'accounting', 'config', 'iaas', 'inventory', 'util', 'iaas']

with_login = True


"""

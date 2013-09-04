from pbr import version
__version__ = version.VersionInfo('cloudmesh')

#import pkg_resources
#__version_full__  = pkg_resources.get_distribution("cloudmesh").version

#import sys
#sys.path.append("..")
#__all__= ['cloudmesh', 'profile', 'accounting', 'config', 'iaas', 'inventory', 'util', 'iaas']

with_login = True


try:
     with_login = cm_config_server().get("ldap.with_ldap")
except:
    with_login = False
    print "WARGING: not using user login"




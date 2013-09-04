import sys
#print sys.path

from cloudmesh.cm_profile import cm_profile
from pprint import pprint
from cloudmesh.iaas.openstack.cm_compute import openstack

p = cm_profile()

print p.config
print p.server


pprint (p.data)

print 70 * "-"
pprint (p.get("abc"))

print 70 * "-"
p.write ("abc", {"hallo": "world"})
p.update ("abc", {"moon": "sun"})
pprint (p.get("abc"))

print 70 * "-"
p.write ("abc", {"saturn": "jupiter"})
pprint (p.get("abc"))


name = "sierra-openstack-grizzly"
#name = "india-openstack-essex"

credential = p.server.config["keystone"][name]

cloud = openstack(name, credential=credential)



#cloud.refresh("flavors")

#print cloud.flavors

#pprint (cloud.get_token(credential=credential))

#pprint (cloud.get_tenants(credential))
#pprint (cloud.get_users(credential))
#pprint (cloud.get_users())


c = openstack(name)

c.refresh("users")

pprint (c.get("users"))

#c.refresh("tenants")     
#print c.get("tenants")     

"""
from cloudmesh.cm_mesh import cloudmesh



c = cloudmesh()

print c.clouds
"""



#os = openstack()


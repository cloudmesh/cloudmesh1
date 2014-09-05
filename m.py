import cloudmesh
from pprint import pprint

cloudmesh.logger(False)
username = cloudmesh.load().username()

cloudmesh.banner("INIT MONGO")
mesh = cloudmesh.mesh("mongo")

cloudmesh.banner("ACTIVATE")
mesh.activate(username)

cloudmesh.banner("GET FLAVOR")
data = mesh.flavors(cm_user_id=username, clouds=["india"])

pprint (data)

cloudmesh.banner("GET FLAVOR")
mesh.refresh(username,types=['flavors'],names=["india"])

#
# PROPOSAL FOR NEW MESH API
#

userinfo = cloudmesh.cm_user().info(username)

cloud = "india"
prefix = userinfo['defaults']['prefix']
index = userinfo['defaults']['index']
flavor = userinfo['defaults']['flavors'][cloud] 
# or flavor = "2" small
image = userinfo['defaults']['images'][cloud] 
# or image = '02cf1545-dd83-493a-986e-583d53ee3728' 
# ubuntu-14.04 
key = "%s_%s" % (username, userinfo['defaults']['key'])
meta = { 'cm_owner': username }

# vm_create
result = mesh.vm_create(cloud, prefix, index, flavor, image, key, meta, username)

# increase index after the completion of vm_create()
cloudmesh.cm_user().set_default_attribute(username, "index", int(index) + 1)



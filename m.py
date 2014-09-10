import cloudmesh
from pprint import pprint

cloudmesh.logger(False)
username = cloudmesh.load().username()

cloudmesh.banner("INIT MONGO")
mesh = cloudmesh.mesh("mongo")

#
# authentication as a user - username is requried
# On webgui side, this is achieved by the framework,
# and the username is obtined from g.user.id
#
# On CLI side, a global user object or username variable
# should be maintained upon the start of the shell
# The username could be obtained from yaml file.

cloudmesh.banner("ACTIVATE")
mesh.activate(username)

cloudmesh.banner("GET FLAVOR")
mesh.refresh(username,types=['flavors'],names=["india"])
data = mesh.flavors(cm_user_id=username, clouds=["india"])

pprint (data)

cloudmesh.banner("GET IMAGE")
mesh.refresh(username,types=['images'],names=["india"])
data = mesh.images(cm_user_id=username, clouds=["india"])

pprint (data)

cloudmesh.banner("LIST KEYS")
#keyobj = cloudmesh.cm_keys_mongo(username)
#print keyobj.names()

#
# PROPOSAL FOR NEW MESH API
#

cloud = "india"

cloudmesh.banner("LAUNCH VM INSTANCE")
result = mesh.start(cloud, username)

cloudmesh.banner("TERMINATE VM INSTANCE")
server = result['server']['id']
mesh.delete(cloud, server, username)

cloudmesh.banner("LAUNCH 3 VM INSTANCES")
vm = {}
for i in range(1,3):
    vm[i] = mesh.start(cloud, username)


cloudmesh.banner("TERMINATE 3 VM INSTANCES")
for i in vm: 
    server = vm[i]['server']['id']
    mesh.delete(cloud, server, username)


cloudmesh.banner("GET A FLAVOR")
flavor=mesh.flavor(cloudname="india", flavorname="m1.small") 
flavor=mesh.flavor("india", "m1.small") 


cloudmesh.banner("GET AN IMAGE")
image=mesh.image(cloudname="india", imagename="futuregrid/ubuntu-14.04") 
image=mesh.image("india", "futuregrid/ubuntu-14.04") 


cloudmesh.banner("GET A VM NAME")
vmname = mesh.vmname()
print vmname


cloudmesh.banner("SET A VM NAME")
vmname = mesh.vmname(prefix="albert", idx=10)
print vmname
vmname = mesh.vmname("James", 20)
print vmname


cloudmesh.banner("GET A NEXT VM NAME")
vmname = mesh.vmname_next()
print vmname
vmname = mesh.vmname("Brian", "+2")
print vmname


cloudmesh.banner("SET A DEFAULT IMAGE OR A DEFAULT FLAVOR")
mesh.default("india", "image", image)
mesh.default("india", "flavor", flavor)


cloudmesh.banner("START A VM WITH OPTIONS")
cloud = "india"
prefix = "gregor"
index = "10000"
flavor = mesh.flavor("india", "m1.small") 
image = mesh.image("india", "futuregrid/ubuntu-14.04") 
vm = mesh.start(cloud, username, prefix=prefix, index=index, flavor=flavor,
                image=image)
vm = mesh.start("india", username, image=image, flavor=flavor)
server = vm['server']['id']


cloudmesh.banner("ASSIGN PUBLIC IP ADDRESS TO THE VM")
ip = mesh.assign_public_ip(cloud, server, username)

import time

# WAIT 10 SECONDS UNTIL THE VM IS READY
time.sleep(10)

cloudmesh.banner("RUN A COMMAND VIA SSH TO THE VM")
result = mesh.ssh_vm_with_command(ip, command="ls -al")

mesh.delete(cloud, server, username)

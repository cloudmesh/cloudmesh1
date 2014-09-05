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
data = mesh.flavors(cm_user_id=username, clouds=["india"])

pprint (data)

cloudmesh.banner("GET FLAVOR")
mesh.refresh(username,types=['flavors'],names=["india"])

#
# PROPOSAL FOR NEW MESH API
#

cloudmesh.banner("LAUNCH VM INSTANCE")
result = mesh.start(cloud, username)

cloudmesh.banner("TERMINATE VM INSTANCE")
server = result['server']['id']
mesh.delete(cloud, server, username)


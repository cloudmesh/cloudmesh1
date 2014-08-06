




# ---------------------------------------------------------------------------
# !!!unclear design!!!: import cloud info from ~/.futuregrid/cloudmesh.yaml 
# to mongo everytime cm startup:: wipe out all clouds then import
# ---------------------------------------------------------------------------

from cloudmesh.iaas.cm_cloud import CloudManage
from cloudmesh.config.cm_config import cm_config
from cloudmesh_common.bootstrap_util import path_expand
from cloudmesh.config.ConfigDict import ConfigDict


config = cm_config()
username = config['cloudmesh']['profile']['username']

cloudmanage = CloudManage()
cloud_names = []
clouds = cloudmanage.get_clouds(username)
for cloud in clouds:
    cloud_names.append(cloud['cm_cloud'].encode("ascii"))
    
for name in cloud_names:
    cloudmanage.remove_cloud(username, name)
    

file = path_expand("~/.futuregrid/cloudmesh.yaml")
fileconfig = ConfigDict(filename=file)
cloudsdict = fileconfig.get("cloudmesh", "clouds")

for key in cloudsdict:
    cloudmanage.import_cloud_to_mongo(cloudsdict[key], key, username)

# ---------------------------------------------------------------------------



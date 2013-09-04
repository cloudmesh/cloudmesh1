from flask import Blueprint
from flask import render_template, request, redirect
#from cloudmesh.provisioner.cm_launcher import cm_launcher

launch_module = Blueprint('launch  _module', __name__)

#
# ROUTE: launch  
#

# fake list of recipies which we need to get from cm_launcher

launch_recipies = {"india-openstack-essex":
                   [
                    {"name": "Slurm Cluster",
                     "types": ["VM", "baremetal"],
                     "description": "Deploys a Slurm cluster. One of the Vms is the Master, "
                                    "while the others register with the master as worker nodes"
                                    " The master will be the first node in the list"},
                    {"name": "Hadoop",
                     "types": ["VM", "baremetal"],                     
                     "description": "Deploys a haddop cluster on the VMs specified"},
                    {"name": "Ganglia",
                     "types": ["VM", "baremetal"],                     
                     "description": "Deploys a Ganglia service for the vms specified. "
                                    "The ganglia server will be the first node in the list"},
                    {"name": "Nagios",
                     "types": ["VM", "baremetal"],                     
                     "description": "Deploys a Nagios service for the vms specified. "
                                    "The ganglia server will be the first node in the list"},
                    ],
                   "sierra-openstack-grizzly": 
                   [
                    {"name": "Slurm Cluster",
                     "types": ["VM", "baremetal"],                     
                     "description": "Deploys a Slurm cluster. One of the Vms is the Master, "
                                    "while the others register with the master as worker nodes"
                                    " The master will be the first node in the list"},
                    {"name": "Hadoop",
                     "types": ["VM", "baremetal"],                     
                     "description": "Deploys a haddop cluster on the VMs specified"},
                    {"name": "Ganglia",
                     "types": ["VM", "baremetal"],                     
                     "description": "Deploys a Ganglia service for the vms specified. "
                                    "The ganglia server will be the first node in the list"},
                    {"name": "Nagios",
                     "types": ["VM", "baremetal"],                     
                     "description": "Deploys a Nagios service for the vms specified. "
                                    "The ganglia server will be the first node in the list"},
                    ],
                   }


@launch_module.route('/cm/launch/<host>/<recipie>')
def launch_run ():
    print "implement"
    pass

@launch_module.route('/cm/launch/launch_servers', methods = ["POST"])
def launch_servers():
    
    columns = {"india-openstack-essex" :
               ["name", "description"] ,
               "sierra-openstack-grizzly":
                ["name", "description"] 
    }
    server = request.form.get("server")
    resources = request.form.getlist("resource")
    return_string = "in server " + server + "<br>"
    for r in launch_recipies[server]:
        if r["name"] in resources:
            return_string += " start " + str(r["name"]) + "<br>"
    return return_string


@launch_module.route('/cm/launch')
def display_launch_table():
    
    # fake list of recipies which we need to get from cm_launcher
    columns = {"india-openstack-essex" :
               ["name", "description"] ,
               "sierra-openstack-grizzly":
                ["name", "description"] 
    }
        
    return render_template('mesh_launch.html',
                           recipies=launch_recipies,
                           columns=columns,
                           )


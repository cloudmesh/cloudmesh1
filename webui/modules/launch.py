from flask import Blueprint
from flask import render_template, request, redirect
#from cloudmesh.provisioner.cm_launcher import cm_launcher
from cloudmesh.util.util import cond_decorator
from flask.ext.login import login_required

import cloudmesh

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
                    {"name": "R",
                     "types": ["VM", "baremetal"],                     
                     "description": "Deploys R. Demonstrating different recipies for different clusters."},
                    ],
                   }
columns = {"india-openstack-essex" :
           ["name","description"] ,
           "sierra-openstack-grizzly":
            ["name", "description"] 
}

@launch_module.route('/cm/launch/<host>/<recipie>')
@cond_decorator(cloudmesh.with_login, login_required)
def launch_run ():
    print "implement"
    pass

@launch_module.route('/cm/launch/launch_servers', methods = ["POST"])
@cond_decorator(cloudmesh.with_login, login_required)
def launch_servers():
    name = request.form.get("name")
    resources = request.form.getlist("resource")
    return_dict = {}
    return_dict["name"] = name
    return_dict["host_list"] = request.form.get("hostlist")
    recipies_list = []
    for r in resources:
        recipies_list.append((r,request.form.get(r+"-select")))
    return_dict["recipies"] = recipies_list
    return str(return_dict)
   
#     return_string = "in server " + server + "<br>" #+ str(resources)
#     for r in resources:
#         return_string += " start " + str(r) +" - " + str(request.form.get(r+"-select")) +"</br>"
#     return return_string


@launch_module.route('/cm/launch')
@cond_decorator(cloudmesh.with_login, login_required)
def display_launch_table():
    
    # fake list of recipies which we need to get from cm_launcher

        
    return render_template('mesh_launch.html',
                           recipies=launch_recipies,
                           columns=columns,
                           )


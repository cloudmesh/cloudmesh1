from flask import Blueprint
from flask import render_template, request, redirect
#from cloudmesh.provisioner.cm_launcher import cm_launcher

launch_module = Blueprint('launch  _module', __name__)

#
# ROUTE: launch  
#


@launch_module.route('/cm/launch/<host>/<recipie>')
def launch_run ():
    print "implement"
    pass

@launch_module.route('/cm/launch/launch_servers', methods = ["POST"])
def launch_servers():
    # fake list of recipies which we need to get from cm_launcher
    columns = {"india-openstack-essex" :
               ["name", "description"] ,
               "sierra-openstack-grizzly":
                ["name", "description"] 
    }
    recipies = {"india-openstack-essex":
                                [
                                 {"name": "cluster",
                                  "description": "blabla"},
                                 {"name": "hadoop",
                                  "description": "blabla"},
                                 {"name": "whatever",
                                  "description": "blabla"},
                                 ],
                "sierra-openstack-grizzly": 
                                [
                                 {"name": "cluster",
                                  "description": "blabla"},
                                 {"name": "hadoop",
                                  "description": "blabla"},
                                 {"name": "whatever",
                                  "description": "blabla"},
                                 ],
                 }
    server = request.form.get("server")
    resources = request.form.getlist("resource")
    return_string = "in server " + server + "<br>"
    for r in recipies[server]:
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
    recipies = {"india-openstack-essex":
                                [
                                 {"name": "cluster",
                                  "description": "blabla"},
                                 {"name": "hadoop",
                                  "description": "blabla"},
                                 {"name": "whatever",
                                  "description": "blabla"},
                                 ],
                "sierra-openstack-grizzly": 
                                [
                                 {"name": "cluster",
                                  "description": "blabla"},
                                 {"name": "hadoop",
                                  "description": "blabla"},
                                 {"name": "whatever",
                                  "description": "blabla"},
                                 ],
                 }
               
    
    return render_template('mesh_launch.html',
                           recipies=recipies,
                           columns=columns,
                           )


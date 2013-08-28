from flask import Blueprint
from flask import render_template, request, redirect
from cloudmesh.provisioner.cm_launch import cm_launcher

launch_module = Blueprint('launch  _module', __name__)

#
# ROUTE: launch  
#


@launch_module.route('/cm/launch/<host>/<recipie>')
def launch_run ():
    print "implement"
    pass


@launch_module.route('/cm/launch')
def display_launch_table():
    
    # fake list of recipies which we need to get from cm_launcher
    recipies = {"india-openstack-essex": 
                                [
                                 {"name": "cluster",
                                  "description": "blabla"},
                                 {"name": "hadoop",
                                  "description": "blabla"},
                                 {"name": "whatever",
                                  "description": "blabla"},
                                 ],
                {"india-openstack-essex": 
                                [
                                 {"name": "cluster",
                                  "description": "blabla"},
                                 {"name": "hadoop",
                                  "description": "blabla"},
                                 {"name": "whatever",
                                  "description": "blabla"},
                                 ],
                 }
               }
    
    return render_template('mesh_launch.html')


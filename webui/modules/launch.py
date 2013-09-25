from flask import Blueprint
from flask import render_template, request, redirect
# from cloudmesh.provisioner.cm_launcher import cm_launcher
from cloudmesh.util.util import cond_decorator
from flask.ext.login import login_required
from cloudmesh.config.ConfigDict import ConfigDict as cm_config_launcher
from cloudmesh.launcher.queue.tasks import task_launch
from cloudmesh.launcher.cm_launcher_db import cm_launcher_db
import cloudmesh

launch_module = Blueprint('launch  _module', __name__)

#
# ROUTE: launch
#

# list of recipies which we need to get from cm_launcher.yaml
launcher_config = cm_config_launcher(filename = "~/.futuregrid/cloudmesh_launcher.yaml")
launch_recipies = launcher_config.get("launcher.recipies")
columns = launcher_config.get("launcher.columns")

@launch_module.route('/cm/launch/<host>/<recipie>')
@cond_decorator(cloudmesh.with_login, login_required)
def launch_run ():
    print "implement"
    pass



@launch_module.route('/cm/launch/launch_servers', methods=["POST"])
@cond_decorator(cloudmesh.with_login, login_required)
def launch_servers():

    name = request.form.get("name")
    resources = request.form.getlist("resource")
    return_dict = {}
    return_dict["user"] = "sridhar"  # default user.... change to read from session
    return_dict["name"] = name
    return_dict["host_list"] = request.form.get("hostlist")
    recipies_list = []
    for r in resources:
        recipies_list.append((r, request.form.get(r + "-select")))
    return_dict["recipies"] = recipies_list
    task_launch.apply_async(queue="launcher", args=[return_dict])
    return "tasks have been submitted to the queue."

#     return_string = "in server " + server + "<br>" #+ str(resources)
#     for r in resources:
#         return_string += " start " + str(r) +" - " + str(request.form.get(r+"-select")) +"</br>"
#     return return_string


@launch_module.route('/cm/launch')
@cond_decorator(cloudmesh.with_login, login_required)
def display_launch_table():
    return render_template('mesh_launch.html',
                           recipies=launch_recipies,
                           columns=columns,
                           )

@launch_module.route('/cm/launch/db_stats')
def launch_status():
    db = cm_launcher_db()
    res = db.find()
    print"000000000000000000000000000000000000000000000000000000000000"
    l = []
    for r in res:
        l.append(r)
    return str(l)

@launch_module.route('/cm/db_reset')
def launch_clear():
    print "clearing db ----------------------------- "
    db = cm_launcher_db()
    print db
    print db.clear()
    print "++++++++++++++++++++++++++++++++++++++++++"
    return "jsdnklnkls"

from cloudmesh_install import config_file
from flask import Blueprint
from flask import render_template, request, redirect
# from cloudmesh.provisioner.cm_launcher import cm_launcher
from cloudmesh_common.util import cond_decorator
from flask.ext.login import login_required
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.launcher.queue.tasks import task_launch
from cloudmesh.launcher.cm_launcher_db import cm_launcher_db
import cloudmesh
from flask.ext.principal import Principal, Identity, AnonymousIdentity, \
    identity_changed, Permission, identity_loaded, RoleNeed, UserNeed


from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)

launch_module = Blueprint('launch  _module', __name__)

rain_permission = Permission(RoleNeed('rain'))

#
# ROUTE: launch
#

# list of recipies which we need to get from cm_launcher.yaml




# @rain_permission.require(http_exception=403)
# @login_required

@launch_module.route('/cm/launch/launch_servers/', methods=["POST"])
def launch_servers():
    """

    launcher_config = ConfigDict(filename=config_file("/cloudmesh_launcher.yaml"))
    celery_config = ConfigDict(filename=config_file("/cloudmesh_celery.yaml"))
    launch_recipies = launcher_config.get("cloudmesh.launcher.recipies")

    server = request.form.get("server")
    name_index = request.form.get("name_index")
    return_dict = dict(launch_recipies[server][int(name_index)])
    return_dict["user"] = "sridhar"  # default user.... change to read from session
    return_dict["server"] = server

    parameters = launch_recipies[server][int(name_index)]["parameters"]  # load the needed set of parameters
    for parameter in parameters:
        parameters[parameter] = request.form.get("parameter_{0}".format(parameter))
    return_dict["parameters"] = parameters

    return_dict["name"] = launch_recipies[server][int(name_index)]["name"]
    queue = celery_config = celery_config.get("cloudmesh.workers.launcher.queue")
    task_launch.apply_async(queue=queue, args=[return_dict])
    return "Task has been submitted to the queue.... <br/><br/>Data sent was:<br/>" + str(return_dict)
    # return "tasks have been submitted to the queue."
    """
    log.error ("not yet implemented")    
    print "HALLO"
    
#     return_string = "in server " + server + "<br>" #+ str(resources)
#     for r in resources:
#         return_string += " start " + str(r) +" - " + str(request.form.get(r+"-select")) +"</br>"
#     return return_string


@launch_module.route('/cm/launch/', methods=['POST', 'GET'])
@login_required
@rain_permission.require(http_exception=403)
def display_launch_table():

    if request.method == 'POST':
        print "HHHHHHHHHHHHH"
        print "HHHHHH", request.form.keys()
        for key in request.form.keys():
            print key, ":", request.form[key]

    else:

        print "HEY JUDE"
        
    launcher_config = ConfigDict(filename=config_file("/cloudmesh_launcher.yaml"))
    launch_recipies = launcher_config.get("cloudmesh.launcher.recipies")
        
    return render_template('mesh/mesh_launch.html',
                           recipies=launch_recipies)


@launch_module.route('/cm/launch/db_stats')
@login_required
@rain_permission.require(http_exception=403)
def launch_status():
    db = cm_launcher_db()
    res = db.find()
    l = []
    for r in res:
        l.append(r)
    return str(l)

@launch_module.route('/cm/launch/db_reset')
@login_required
@rain_permission.require(http_exception=403)
def launch_clear():
    db = cm_launcher_db()
    log.info("DB: {0}".format(db))
    db.clear()
    log.info("DB after clear {0}".format(db))
    #
    # BUG: this return value does not look right
    #
    return "jsdnklnkls"


@launch_module.route('/cm/launch/run/<host>/<recipie>')
@login_required
@rain_permission.require(http_exception=403)
def launch_run ():
    log.error ("not yet implemented")
    pass

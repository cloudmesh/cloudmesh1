from cloudmesh_install import config_file
from flask import Blueprint
from flask import render_template, request, redirect
# from cloudmesh.provisioner.cm_launcher import cm_launcher
from cloudmesh_common.util import cond_decorator
from flask.ext.login import login_required
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.config.cm_config import cm_config
from cloudmesh.launcher.queue.tasks import task_launch
from cloudmesh.launcher.cm_launcher_db import cm_launcher_db
import cloudmesh
from flask.ext.principal import Principal, Identity, AnonymousIdentity, \
    identity_changed, Permission, identity_loaded, RoleNeed, UserNeed
import subprocess

from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)

launch_module = Blueprint('launch  _module', __name__)

rain_permission = Permission(RoleNeed('rain'))

#
# ROUTE: launch
#

# list of recipies which we need to get from cm_launcher.yaml




# @rain_permission.require(http_exception=403)
@login_required
@rain_permission.require(http_exception=403)
@launch_module.route('/cm/launch/launch_servers/', methods=["POST","GET"])
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
    config = cm_config()
    cloudname = request.form['cloud']
    user = config["cloudmesh"]["clouds"][cloudname]["credentials"]["OS_USERNAME"]
    hostname = config["cloudmesh"]["clouds"][cloudname]["cm_host"]

    data = dict((key, request.form.getlist(key.encode("utf-8"))) for key in request.form.keys())
    
    formatted_string = str("{name}{script}{selector}{other}{types}{nodes}{cloud}".format(**data))
    
    ssh_cmd = "ssh " + user + "@" + hostname + " \"" + request.form['script'] + "\" >> /home/cloudnaut/results.txt"

    shell_cmd = request.form['script'] + " " + " >> /home/cloudnaut/results.txt"
    
    subprocess.Popen(ssh_cmd,shell="True")
    return ssh_cmd


@launch_module.route('/cm/launch/', methods=['POST', 'GET'])
@login_required
@rain_permission.require(http_exception=403)
def display_launch_table():

    if request.method == 'POST':
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

from cloudmesh_install import config_file
from flask import Blueprint
from flask import render_template, request
from flask.ext.login import login_required
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.launcher.cm_launcher_db import cm_launcher_db
from flask.ext.principal import Permission, RoleNeed
from cloudmesh.config.cm_config import cm_config
import subprocess

from cloudmesh_common.logger import LOGGER

LOG_MSG = LOGGER(__file__)
launch_module = Blueprint('launch  _module', __name__)
RAIN_PERMISSION = Permission(RoleNeed('rain'))

#
# ROUTE: launch
#

# list of recipies which we need to get from cm_launcher.yaml

# @RAIN_PERMISSION.require(http_exception=403)


@login_required
@RAIN_PERMISSION.require(http_exception=403)
@launch_module.route('/cm/launch/launch_servers/', methods=["POST", "GET"])
def launch_servers():
    """ To satisfy Pylint. Will update with proper comments """
    config = cm_config()
    cloudname = request.form['cloud']
    #
    # this seems wrong as the script is formulated in the yaml file, so you need to get the type
    # from the form and read the script from the yaml file
    #
    data = {
        'usr': config["cloudmesh"]["clouds"][cloudname]["credentials"]["OS_USERNAME"],
        'hostname': config["cloudmesh"]["clouds"][cloudname]["cm_host"],
        'script': request.form['script']
    }
    ssh_cmd = "ssh {usr}@{hostname}\"{script}\" >> /home/cloudnaut/results.txt".format(**data)
    #
    # use sh instead or use the "Sequential" API
    #
    subprocess.Popen(ssh_cmd, shell="True")
    return ssh_cmd


@launch_module.route('/cm/launch/', methods=['POST', 'GET'])
@login_required
@RAIN_PERMISSION.require(http_exception=403)
def display_launch_table():
    """ To satisfy Pylint. Will update with proper comments """
    if request.method == 'POST':
        print "HHHHHH", request.form.keys()
        for key in request.form.keys():
            print key, ":", request.form[key]
    else:
        print "HEY JUDE"

    launcher_config = ConfigDict(
        filename=config_file("/cloudmesh_launcher.yaml"))
    launch_recipies = launcher_config.get("cloudmesh.launcher.recipies")
    return render_template('mesh/mesh_launch.html',
                           recipies=launch_recipies)


@launch_module.route('/cm/launch/db_stats')
@login_required
@RAIN_PERMISSION.require(http_exception=403)
def launch_status():
    """ To satisfy Pylint. Will update with proper comments """
    database = cm_launcher_db()
    results = database.find()
    output_list = []
    for item in results:
        output_list.append(item)
    return str(output_list)


@launch_module.route('/cm/launch/db_reset')
@login_required
@RAIN_PERMISSION.require(http_exception=403)
def launch_clear():
    """ To satisfy Pylint. Will update with proper comments """
    database = cm_launcher_db()
    LOG_MSG.info("DB: {0}".format(database))
    database.clear()
    LOG_MSG.info("DB after clear {0}".format(database))
    #
    # BUG: this return value does not look right
    #
    return "jsdnklnkls"


@launch_module.route('/cm/launch/run/<host>/<recipie>')
@login_required
@RAIN_PERMISSION.require(http_exception=403)
def launch_run():
    """ To satisfy Pylint. Will update with proper comments """
    LOG_MSG.error("not yet implemented")
    # pass

from flask import Blueprint
from flask import render_template, request, redirect

import cloudmesh
from flask.ext.login import login_required

status_module = Blueprint('status_module', __name__)

#
# ROUTE: status
#


@status_module.route('/status')
def display_status():

    msg = ""
    status = ""

    categories = ['India', 'Bravo', 'Echo', 'Hotel', 'Sierra', 'Alamo']
    jobs = [43000, 19000, 60000, 35000, 50000, 70000]
    users = [50000, 39000, 42000, 31000, 50000, 70000]


    return render_template('status.html',
                           categories=categories,
                           jobs=jobs,
                           users=users,
                           status=status,
                           show=msg)

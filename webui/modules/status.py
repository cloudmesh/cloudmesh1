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

    values = {
              'india' : { 'jobs' : 3, 'users' : 50},
              'bravo' : { 'jobs' : 13, 'users' : 40},
              'echo' : { 'jobs' : 23, 'users' : 30},
              'hotel' : { 'jobs' : 33, 'users' : 20},
              'sierra' : { 'jobs' : 43, 'users' : 10},
              'alamo' : { 'jobs' : 53, 'users' : 1},
              }

    categories = ['India', 'Bravo', 'Echo', 'Hotel', 'Sierra', 'Alamo']
    jobs = [43000, 19000, 60000, 35000, 50000, 70000]
    users = [50000, 39000, 42000, 31000, 50000, 70000]


    return render_template('status.html',
                           values=values,
                           categories=categories,
                           jobs=jobs,
                           users=users,
                           status=status,
                           show=msg)

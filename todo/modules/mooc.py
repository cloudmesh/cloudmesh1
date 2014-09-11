from flask import Blueprint
from flask import render_template, request, redirect
from cloudmesh.config.cm_keys import cm_keys
from cloudmesh.util.util import cond_decorator

import cloudmesh

from flask.ext.login import login_required


from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

mooc_module = Blueprint('mooc_module', __name__)

#
# ROUTE: mooc
#


@mooc_module.route('/mooc')
def display_mooc():

    return render_template('mooc.html')

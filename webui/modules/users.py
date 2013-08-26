from flask import Blueprint
from flask import render_template, request, redirect
from cloudmesh.config.cm_config import cm_config
from cloudmesh.config.cm_config import cm_config_server

from datetime import datetime
from cloudmesh.util.util import path_expand
import yaml
from cloudmesh.config.cm_config import get_mongo_db

users_module = Blueprint('users_module', __name__)

#
# ROUTE: KEYS
#


@users_module.route('/users/ldap/')
def display_usres_ldap():

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    collection = "user"
    db_clouds = get_mongo_db(collection)        

        

    config = cm_config()

    result = db_clouds.find({})
    data = {}
    for entry in result:
        id = entry['cm_user_id']
        data[id] = entry
        
        
    #print data


    return render_template('users_ldap.html', updated=time_now, users=data)



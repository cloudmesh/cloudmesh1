from flask import Blueprint
from flask import render_template, request, redirect
from cloudmesh.config.cm_config import cm_config
from cloudmesh.config.cm_config import cm_config_server
from pymongo import MongoClient
from datetime import datetime

users_module = Blueprint('users_module', __name__)

#
# ROUTE: KEYS
#


@users_module.route('/users/ldap/')
def display_usres_ldap():

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    collection = "user"
    db_name = cm_config_server().config["mongo"]["db"]
        
    client = MongoClient()    
    db = client[db_name]          
    db_clouds = db[collection]    
    config = cm_config()

    result = db_clouds.find({})
    data = {}
    for entry in result:
        id = entry['cm_user_id']
        data[id] = entry
        
        
    #print data


    return render_template('users_ldap.html', updated=time_now, users=data)



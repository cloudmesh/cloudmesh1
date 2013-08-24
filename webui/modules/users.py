from flask import Blueprint
from flask import render_template, request, redirect
from cloudmesh.config.cm_config import cm_config
from cloudmesh.config.cm_config import cm_config_server
<<<<<<< HEAD
from datetime import datetime
from cloudmesh.util.util import path_expand
import yaml
from cloudmesh.config.cm_config import get_mongo_db
=======
from pymongo import MongoClient
from datetime import datetime
from cloudmesh.util.util import path_expand
import yaml
>>>>>>> 218abdd0e3364bb70666402f9554d3f0e0ad4f4b

users_module = Blueprint('users_module', __name__)

#
# ROUTE: KEYS
#


@users_module.route('/users/ldap/')
def display_usres_ldap():

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
<<<<<<< HEAD

    collection = "user"
    db_clouds = get_mongo_db(collection)        

        
=======
    
    mongo_config = cm_config_server().config["mongo"]
    mongo_collection = "user"
        
    mongo_host = mongo_config["host"]
    mongo_port = mongo_config["port"]
    mongo_db_name = mongo_config["collections"][mongo_collection]['db']

    client = MongoClient(host=mongo_host,
                              port=mongo_port)  
    db = client[mongo_db_name]          
    db_clouds = db[mongo_collection]    
    
    
>>>>>>> 218abdd0e3364bb70666402f9554d3f0e0ad4f4b
    config = cm_config()

    result = db_clouds.find({})
    data = {}
    for entry in result:
        id = entry['cm_user_id']
        data[id] = entry
        
        
    #print data


    return render_template('users_ldap.html', updated=time_now, users=data)



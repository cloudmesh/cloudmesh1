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
    
    self.mongo_config = cm_config_server().config["mongo"]
    self.mongo_collection = "user"
        
    self.mongo_host = self.mongo_config["host"]
    self.mongo_port = self.mongo_config["port"]
    self.mongo_db_name = self.mongo_config["collections"][self.mongo_collection]['db']

    self.client = MongoClient(host=self.mongo_host,
                              port=self.mongo_port)  
    db = client[self.mongo_db_name]          
    self.db_clouds = db[self.mongo_collection]    
    
    
    config = cm_config()

    result = db_clouds.find({})
    data = {}
    for entry in result:
        id = entry['cm_user_id']
        data[id] = entry
        
        
    #print data


    return render_template('users_ldap.html', updated=time_now, users=data)



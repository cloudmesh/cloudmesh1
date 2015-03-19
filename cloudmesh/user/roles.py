from __future__ import print_function
from cloudmesh.config.cm_config import cm_config, \
    cm_config_server, \
    get_mongo_db
from cloudmesh_base.logger import LOGGER
from cloudmesh_base.util import path_expand
import yaml


log = LOGGER(__file__)


class Roles:

    def get_config(self, **kwargs):

        if 'roles' not in kwargs:  
            self.roles = cm_config_server().get("cloudmesh.server.roles")

    mongo_host = 'localhost'
    mongo_port = 27017
    mongo_db_name = "cloudmesh"
    mongo_collection = "cloudmesh"

    def __init__(self):

        collection = "user"
        self.db_clouds = get_mongo_db(collection)

        self.get_config()

    def _get_mongo(self):

        result = self.db_clouds.find({})
        data = {}
        for entry in result:
            id = entry['cm_user_id']
            data[id] = entry

        print(data)

    def clear(self):
        self.roles = None

    def get_roles(self, user):
        pass

    def authorized(self, user, role):
        return False

    def users(self, role):
        single_users = self.roles[role]['users']
        projects = self.roles[role]['projects']
        result = self.db_clouds.find({'projects.active': {"$in": projects}})
        project_users = []
        for entry in result:
            project_users.append(entry['cm_user_id'])
        s = list(set(single_users + project_users))
        return s

    def get(self, user):
        user_roles = []
        for r in self.roles:
            us = self.users(r)
            if user in us:
                user_roles.append(r)
        return user_roles

    def __str__(self):
        return str(self.roles)

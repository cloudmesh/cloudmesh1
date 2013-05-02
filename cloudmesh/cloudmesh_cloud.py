import os
import yaml

class cloudmesh_cloud:
    """Provides credentials for various cloud platforms""" 
    CLOUD_DEFNS = 'cloudmesh_clouds.yaml'

    def __init__(self, username, cloudname):
        self._username = username
        self._cloudname = cloudname
        self._data = yaml.safe_load(open(self.CLOUD_DEFNS, "r"))[cloudname]

    @property
    def username(self):
        return self._username

    @property
    def cloudname(self):
        return self._cloudname

    @property
    def data(self):
        return self._data

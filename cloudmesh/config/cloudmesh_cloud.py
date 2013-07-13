import os
import yaml
import string
from random import choice

class cloudmesh_cloud:
    """Abstract class, provides credentials for various cloud platforms""" 

    def __init__(self, profiledata, defaultproj, projectlist, cloudname, clouddata):
        self._profile = profiledata
        self._projectlist = projectlist
        self._defaultproj = defaultproj
        self._cloudname = cloudname
        self._data = clouddata

    @property
    def username(self):
        return self._profile['username']

    @property
    def email(self):
        return self._profile['e-mail']

    @property
    def cloudname(self):
        return self._cloudname

    @property
    def projects(self):
        return self._projectlist

    @property
    def defaultproject(self):
        return self._defaultproj

    @property
    def clouddefaults(self):
        return self._data['default']

    @property
    def credentials(self):
        return self._data['credentials']

    @property
    def data(self):
        d = dict(self._data)
        del d['cm_admin']
        return d

    @property
    def admin_data(self):
        return self._data

    def newpass(self):
        """Credit: http://stackoverflow.com/questions/3854692/generate-password-in-python"""
        chars = string.letters + string.digits
        length = 12
        return ''.join([choice(chars) for _ in range(length)])

    def initialize_cloud_user(self):
        raise Exception("Not implemented")

    def change_password(self, oldpass, newpass):
        raise Exception("Not implemented")

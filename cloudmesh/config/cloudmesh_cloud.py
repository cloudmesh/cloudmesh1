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
        return self._profile['e_mail']

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
    def credentials(self):
        return self._data['credentials']
    @credentials.setter
    def credentials(self, v):
        self._data['credentials'] = v

    @property
    def data(self):
        return self._data

    def newpass(self):
        """Credit: http://stackoverflow.com/questions/3854692/generate-password-in-python"""
        chars = string.letters + string.digits
        length = 12
        return ''.join([choice(chars) for _ in range(length)])

    def initialize_cloud_user(self):
        raise Exception("Not implemented")

    def change_own_password(self, oldpass, newpass):
        if self.data['credentials']['OS_PASSWORD'] != oldpass:
            print "Current password is incorrect; password not changed"
            return False
        else:
            return True

    def get_own_password(self):
        raise Exception("Not implemented")

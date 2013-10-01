import os
import yaml
import string
from random import choice


class cloudmesh_cloud:
    """Abstract class, provides credentials for various cloud platforms"""

    def __init__(self, username, email, defaultproj, projectlist, cloudname, cloudcreds, cloudadmincreds=None):
        self._username = username
        self._email = email
        self._defaultproj = defaultproj
        self._projectlist = projectlist
        self._cloudname = cloudname
        self._cloudcreds = cloudcreds
        self._cloudadmincreds = cloudadmincreds

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

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
        return self._cloudcreds
    @credentials.setter
    def credentials(self, v):
        self._cloudcreds = v

    @property
    def admin_credentials(self):
        return self._cloudadmincreds

    def newpass(self):
        """Credit: http://stackoverflow.com/questions/3854692/generate-password-in-python"""
        chars = string.letters + string.digits
        length = 12
        return ''.join([choice(chars) for _ in range(length)])

    def initialize_cloud_user(self):
        raise Exception("Not implemented")

    def change_own_password(self, oldpass, newpass):
        raise Exception("Not implemented")

    def get_own_password(self):
        raise Exception("Not implemented")

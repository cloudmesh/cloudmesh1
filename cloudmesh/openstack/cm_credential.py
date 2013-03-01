#! /usr/bin/env pythos
from pprint import pprint
import json
import os
import sys
from sh import fgrep
import novaclient

from novaclient.v1_1 import client


class credentials:

    location =  '.futuregrid/openstack/novarc'
    
    username = None
    password = None
    project = None
    label = None
    url = None
    home = os.environ['HOME']

    filename = "%s/%s" % (home, location)

    variables = {
        "project": "OS_TENANT_NAME", 
        "username": "OS_USERNAME", 
        "password":"OS_PASSWORD",
        "url": "OS_AUTH_URL"
        }

    def type (self, name):
        if name == 'openstack':
            self.variables = {
                "project": "OS_TENANT_NAME", 
                "username": "OS_USERNAME", 
                "password":"OS_PASSWORD",
                "url": "OS_AUTH_URL"
                }
        if name == 'eucalyptus':
            self.variables = { 
                "accesskey"  : "EC2_ACCESS_KEY", 
                "secretkey" : "EC2_SECRET_KEY"
            }


    def __init__(self, label, filename=None): 
        if filename != None:
            self.filename = filename
        self._load()
        self.label = label
        return

    def _get_rc_variable (self, variable):
        (attribute, value) = fgrep("export " + self.variables[variable], self.filename).replace("\n","").split("=")
        return value

    def _load(self):
        
        self.project = self._get_rc_variable('project')
        self.username = self._get_rc_variable('username')
        self.password = self._get_rc_variable('password')
        self.url = self._get_rc_variable('url')

        return credentials

    def __str__(self):
        return json.dumps(
            { 'username' : self.username,
              'password' : self.password,
              'url' : self.url,
              'project' : self.project},
            indent=4)

    def set(name, value):
        self.credentials.name = value
 
if __name__=="__main__":

    credential = credentials('india')

    print credential

    """
    flavors = nova.flavors.list()
    for flavor in flavors:
        details = flavor.__dict__
        pprint(details)
    """

